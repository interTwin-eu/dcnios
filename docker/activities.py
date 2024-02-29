from threading import Thread
from urllib.parse import urljoin
import tempfile
import os
import requests
import time
import zipfile
import shutil
import subprocess

class BaseActivity:
    """The base class that does nothing when presented with events."""

    def onNewFile(self, path):
        pass

    def onDeletedFile(self, path):
        pass

    def onFileMetadataChanged(self, path):
        pass

    def onMovedFile(self, fromPath, toPath):
        pass

    def onNewDirectory(self, path):
        pass

    def onDeletedDirectory(self, path):
        pass

    def onDirMetadataChanged(self, path):
        pass

    def onMovedDirectory(self, fromPath, toPath):
        pass

    def onEventLoss(self):
        pass

    def close(self):
        pass


class HttpBasedActivity(BaseActivity):
    """Any activity that makes use of python's Requests library."""
    def __init__(self, *args, **kwargs):
        if kwargs is None:
            raise Exception('Missing kwargs in HttpBasedActivity')

        self.__session_factory = kwargs.get('session_factory')
        if self.__session_factory is None:
            raise Exception('Missing session_factory in HttpBasedActivity')

        self.__args = kwargs.get('args')
        if self.__args is None:
            raise Exception('Missing args in HttpBasedActivity')

        self.__session = None

    def session(self):
        if self.__session is None:
            self.__session = self.__session_factory(self.__args)
        return self.__session

    def close(self):
        if self.__session is not None:
            self.__session.close()
            self.__session = None


class FrontendBasedActivity(HttpBasedActivity):
    """Any activity that makes use of dCache's REST API."""
    def __init__(self, *args, **kwargs):
        super(FrontendBasedActivity, self).__init__(*args, **kwargs)

        if kwargs is None:
            raise Exception('Missing kwargs in FrontendBasedActivity')

        self.__api_uri = kwargs.get('api_url')

        if self.__api_uri is None:
            raise Exception('Missing api_uri argument')

    def rest_url(self, path):
        return self.__api_uri + '/' + path ## REVISIT: use URL combining to resolve

    def close(self):
        super(FrontendBasedActivity, self).close()


class TransferringActivity(FrontendBasedActivity):
    """
    Any activity that transfers data between the client and dCache.  This
    is based on FrontendBasedActivity as the client must discover which
    doors are available.
    """
    def __init__(self, *args, **kwargs):
        super(TransferringActivity, self).__init__(*args, **kwargs)
        self.__doors = None

    def __discoverDoors(self):
        r = self.session().get(self.rest_url("doors"))
        r.raise_for_status()
        return r.json()

    def __load(self, door_info):
        return door_info['load']

    def doors(self, protocol, tags):
        """Return the URL of a door with this protocol"""
        ## REVISIT: should cached value expires after some time?
        if not self.__doors:
            self.__doors = self.__discoverDoors()

        selected_doors = []
        for door in self.__doors:
            if door['protocol'] != protocol:
                continue
            if not tags or all(elem in door['tags'] for elem in tags):
                selected_doors.append(door)

        if not selected_doors:
            raise Exception('No doors match protocol=' + protocol + ', tags=' + str(tags))

        selected_doors.sort(key = self.__load)
        best_door = selected_doors[0]

        addresses = set(best_door['addresses'])
        address = addresses.pop() # What if there are multiple interfaces?
        return "%s://%s:%d/" % (protocol, address, best_door['port'])


    def close(self):
        super(TransferringActivity, self).close()


class PrintActivity(BaseActivity):
    "Simple activity that prints information about events."
    def onNewFile(self, path):
        print("NEW FILE %s" % path)

    def onDeletedFile(self, path):
        print("DELETED FILE %s" % path)

    def onFileMetadataChanged(self, path):
        print("FILE METADATA CHANGED %s" % path)

    def onMovedFile(self, fromPath, toPath):
        print("FILE MOVED FROM %s TO %s" % (fromPath, toPath))

    def onNewDirectory(self, path):
        print("NEW DIRECTORY %s/" % path)

    def onDeletedDirectory(self, path):
        print("DELETED DIRECTORY %s/" % path)

    def onDirMetadataChanged(self, path):
        print("DIRECTORY METADATA CHANGED %s" % path)

    def onMovedDirectory(self, fromPath, toPath):
        print("DIRECTORY MOVED FROM %s/ TO %s/" % (fromPath, toPath))

    def onEventLoss(self):
        print("EVENT LOSS")


class UnarchiveActivity(TransferringActivity):
    """Extract newly uploaded archive files to a target directory"""

    def __init__(self, *args, **kwargs):
        super(UnarchiveActivity, self).__init__(*args, **kwargs)
        targetPath = args[0]
        print("Extracting archives into %s" % targetPath)
        self.__threads = []
        webdav_url = self.doors('https', ['dcache-view'])
        self.__download_url = webdav_url
        self.__target_url = urljoin(webdav_url, targetPath + '/')
        self.__extensions = [e for f in shutil.get_unpack_formats() for e in f[1]]


    def onNewFile(self, path):
        for extension in self.__extensions:
            if path.endswith(extension):
                print("Extracting files from archive: %s (%s)" % (path,extension))
                thread = Thread(target = self.extract, args = (path,extension))
                thread.start()
                self.__threads.append(thread)
                break


    def extract(self, path, extension):
        name = os.path.basename(path)[:-len(extension)] # REVISIT: shouldn't this be OS independent?
        localname = 'archive' + extension
        upload_base_url = urljoin(self.__target_url, name + '/');

        with tempfile.TemporaryDirectory() as tmpdirname:
            local_archive = os.path.join(tmpdirname, localname)

            url = urljoin(self.__download_url, path)
            print("Downloading %s into %s" % (url, local_archive))
            r = self.session().get(url, allow_redirects=True)
            open(local_archive, 'wb').write(r.content)

            target_dir = os.path.join(tmpdirname, 'contents')
            shutil.unpack_archive(local_archive, target_dir)

            for r, d, f in os.walk(target_dir):
                for file in f:
                    abs_path = os.path.join(r, file)
                    rel_path = os.path.relpath(abs_path, target_dir)
                    upload_url = urljoin(upload_base_url, rel_path)

                    print("    UPLOADING %s to %s" % (abs_path, upload_url))
                    with open(abs_path, 'rb') as data:
                        self.session().put(upload_url, data=data)

    def close(self):
        isFirst = True
        for thread in self.__threads:
            if thread.isAlive():
                if isFirst:
                    print("Waiting for background tasks to finish")
                    isFirst = False
                thread.join()
        super(UnarchiveActivity, self).close()


class ExecuteActivity(BaseActivity):
    """Run arbitrary command on events"""

    def __init__(self, *args, **kwargs):
        self.command = args[0]
        self.__invocations = []

    def onNewFile(self, path):
        self._runCommand("NEW_FILE", path)

    def onDeletedFile(self, path):
        self._runCommand("DELETED_FILE", path)

    def onFileMetadataChanged(self, path):
        self._runCommand("FILE_METADATA_CHANGED", path)

    def onMovedFile(self, fromPath, toPath):
        self._runCommand("MOVED_FILE", fromPath, toPath)

    def onNewDirectory(self, path):
        self._runCommand("NEW_DIR", path)

    def onDeletedDirectory(self, path):
        self._runCommand("DELETED_DIR", path)

    def onDirMetadataChanged(self, path):
        self._runCommand("DIR_METADATA_CHANGED", path)

    def onMovedDirectory(self, fromPath, toPath):
        self._runCommand("MOVED_DIR", fromPath, toPath)

    def _runCommand(self, operation, path, targetPath=None):
        if targetPath:
            invocation = subprocess.Popen([self.command, operation, path, targetPath])
        else:
            invocation = subprocess.Popen([self.command, operation, path])
        self.__invocations.append(invocation)

    def close(self):
        isFirst = True
        for invocation in self.__invocations:
            if invocation.poll() == None:
                if isFirst:
                    print("Waiting for command to finish")
                    isFirst = False
                thread.wait() # REVISIT add timeout?
