# Install Jenkins on Mac OS M1 (aarch64)

SonarQube server needs a data store such as Elastic Search.  For development envionment, use brew instead of docker to install SonarQube:
```
brew install sonarqube
brew services start sonarqube
brew info sonarqube
brew services info sonarqube
http://localhost:9000
Default username/password = admin/admin
# Create a project and note down the token
# A project analysis token also can be created from User > My Account > Security
brew install sonar-scanner
sonar-scanner   -Dsonar.projectKey=devops   -Dsonar.sources=.   -Dsonar.host.url=http://localhost:9000   -Dsonar.login=sqp_26fc51fd1384a43db7303c8c9f433d08e1050b72 -X -Dsonar.python.version=3.10
```
Brew will also install Java in order to run SonarQube.