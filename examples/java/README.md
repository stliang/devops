# Use maven with jacoco

Run on docker
```
nerdctl run -v $(pwd):/home/Workspace/devops -it local/ubuntu:20.04 bash
```

Maven build, test, and package with sonar scan
```
 mvn sonar:sonar -Pcoverage package -Dsonar.host.url=<sonarqube server address> -Dsonar.login=<user token>
```

# Reference
- [sonarqube doc](https://docs.sonarqube.org/latest/analyzing-source-code/test-coverage/java-test-coverage/)
- [jacoco example 1](https://www.lambdatest.com/blog/reporting-code-coverage-using-maven-and-jacoco-plugin/)
- [jacoco example 2](https://mkyong.com/maven/maven-jacoco-code-coverage-example/)
- [sonar-project.propertys](https://github.com/marekchowaniok/jacoco-maven-example/blob/master/sonar-project.properties)