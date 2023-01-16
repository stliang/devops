# Run
```shell
npm install
if ! npx cypress verify >/dev/null 2>&1; then
    npx cypress install --force
fi
NO_COLOR=1 npm run e2e:ci && npm run e2e:coverage
```

# Base Project:
Source code for [this tutorial](https://medium.com/@lukas.klement/implementing-code-coverage-with-angular-and-cypress-6ed08ed7e617) on setting up coverage reporting for an Angular project using the Cypress automation testing framework.

This project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 13.0.1 and Node.js v16.13.0

# Missing Feature
Cypress test report is not generated for sonarqube by default.  See [issue](https://community.sonarsource.com/t/genric-report-from-cypress-testing-fails-upload/79559)

# Cypress reference
[cypress integration with CI](https://docs.cypress.io/guides/continuous-integration/introduction#Setting-up-CI)