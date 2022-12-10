# Install Jenkins on Mac OS M1 (aarch64)

SonarQube server needs a data store such as Elastic Search.  For development envionment, use brew instead of docker to install SonarQube:
```
brew install sonarqube
brew services start sonarqube
brew info sonarqube
brew services info sonarqube
http://localhost:9000
Default username/password = admin/admin
brew install sonar-scanner
```
Brew will also install Java in order to run SonarQube.