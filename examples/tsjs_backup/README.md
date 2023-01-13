# Setup
```shell
npm install -g @angular/cli
ng add @cypress/schematic
npm i -D @jsdevtools/coverage-istanbul-loader @istanbuljs/nyc-config-typescript istanbul-lib-coverage nyc webpack
DEBIAN_FRONTEND=noninteractive apt-get install -y libgtk2.0-0 libgtk-3-0 libgbm-dev libnotify-dev libgconf-2-4 libnss3 libxss1 libasound2 libxtst6 xauth xvfb
```

# Running end-to-end tests
```shell
npm run e2e:ci && npm run e2e:coverage
```

# Reference:
Source code for [this tutorial](https://medium.com/@lukas.klement/implementing-code-coverage-with-angular-and-cypress-6ed08ed7e617) on setting up coverage reporting for an Angular project using the Cypress automation testing framework.

This project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 13.0.1 and Node.js v16.13.0
