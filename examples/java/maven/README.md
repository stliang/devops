# Basic Maven Example

This simple Maven project is importing JaCoCo's coverage report. For multi-module project example 
see [multi-module Maven project](https://github.com/SonarSource/sonar-scanning-examples/blob/master/sonarqube-scanner-maven/maven-multimodule/README.md)

## Usage

* Run on docker
```shell
nerdctl run -v $(pwd):/home/Workspace/devops -it local/ubuntu:20.04 bash
```

* Build the project, execute all the tests and analyze the project with SonarQube Scanner for Maven(from root  of the project):
```shell
mvn clean verify sonar:sonar -Dsonar.host.url=<sonarqube server address> -Dsonar.login=<user token>
```

* Maven settings
```shell
mvn -X clean | grep "settings"
mvn help:effective-settings
mvn clean --settings user-settings.xml --global-settings global-settings.xml
```

## Reference
- [Sonar scanning examples](https://github.com/SonarSource/sonar-scanning-examples)
- [SonarScanner for Maven](https://docs.sonarqube.org/latest/analysis/scan/sonarscanner-for-maven/)
- [SonarQube doc](https://docs.sonarqube.org/latest/analyzing-source-code/test-coverage/java-test-coverage/)
- [SonarScanner Maven plugin](https://docs.sonarqube.org/latest/analyzing-source-code/scanners/sonarscanner-for-maven/)
- [SonarQube Jenkins extension](https://docs.sonarqube.org/latest/analyzing-source-code/scanners/jenkins-extension-sonarqube/)
- [Maven basic example](https://github.com/SonarSource/sonar-scanning-examples/tree/master/sonarqube-scanner-maven/maven-basic)
- [Maven settings](https://www.baeldung.com/maven-settings-xml)
- [Jacoco example 1](https://www.lambdatest.com/blog/reporting-code-coverage-using-maven-and-jacoco-plugin/)
- [Jacoco example 2](https://mkyong.com/maven/maven-jacoco-code-coverage-example/)
- [sonar-project.propertys](https://github.com/marekchowaniok/jacoco-maven-example/blob/master/sonar-project.properties)