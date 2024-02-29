import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/dcnios/markdown-page',
    component: ComponentCreator('/dcnios/markdown-page', 'dd1'),
    exact: true
  },
  {
    path: '/dcnios/docs',
    component: ComponentCreator('/dcnios/docs', 'ea7'),
    routes: [
      {
        path: '/dcnios/docs',
        component: ComponentCreator('/dcnios/docs', 'a69'),
        routes: [
          {
            path: '/dcnios/docs',
            component: ComponentCreator('/dcnios/docs', 'bc2'),
            routes: [
              {
                path: '/dcnios/docs/intro',
                component: ComponentCreator('/dcnios/docs/intro', '614'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/dcnios/docs/ProcessGroup/dcache',
                component: ComponentCreator('/dcnios/docs/ProcessGroup/dcache', '24f'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/dcnios/docs/ProcessGroup/generic',
                component: ComponentCreator('/dcnios/docs/ProcessGroup/generic', 'ac9'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/dcnios/docs/ProcessGroup/OSCAR',
                component: ComponentCreator('/dcnios/docs/ProcessGroup/OSCAR', '568'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/dcnios/docs/Users',
                component: ComponentCreator('/dcnios/docs/Users', '3c9'),
                exact: true,
                sidebar: "tutorialSidebar"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/dcnios/',
    component: ComponentCreator('/dcnios/', 'e02'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
