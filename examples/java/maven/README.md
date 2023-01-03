# Use maven with jacoco

Run on docker
```
nerdctl run -v $(pwd):/home/Workspace/devops -it local/ubuntu:20.04 bash
```

Maven build, test, and package with sonar scan
```
 mvn sonar:sonar -Pcoverage package -Dsonar.host.url=<sonarqube server address> -Dsonar.login=<user token> -Dsonar.coverage.jacoco.xmlReportPaths=${base_dir}/target/site/jacoco/jacoco.xml
```

Maven settings
```
mvn -X clean | grep "settings"
mvn help:effective-settings
mvn clean --settings user-settings.xml --global-settings global-settings.xml
```

# Reference
- [SonarQube doc](https://docs.sonarqube.org/latest/analyzing-source-code/test-coverage/java-test-coverage/)
- [SonarScanner Maven plugin](https://docs.sonarqube.org/latest/analyzing-source-code/scanners/sonarscanner-for-maven/)
- [SonarQube Jenkins extension](https://docs.sonarqube.org/latest/analyzing-source-code/scanners/jenkins-extension-sonarqube/)
- [Maven basic example](https://github.com/SonarSource/sonar-scanning-examples/tree/master/sonarqube-scanner-maven/maven-basic)
- [Maven settings](https://www.baeldung.com/maven-settings-xml)
- [Jacoco example 1](https://www.lambdatest.com/blog/reporting-code-coverage-using-maven-and-jacoco-plugin/)
- [Jacoco example 2](https://mkyong.com/maven/maven-jacoco-code-coverage-example/)
- [sonar-project.propertys](https://github.com/marekchowaniok/jacoco-maven-example/blob/master/sonar-project.properties)