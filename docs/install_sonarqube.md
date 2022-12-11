# Install Jenkins on Mac OS M1 (aarch64)

SonarQube server needs a data store such as Elastic Search.  For development envionment, use brew instead of docker to install SonarQube:
```
brew install sonarqube
brew services start sonarqube
brew info sonarqube
brew services info sonarqube
# Default username/password = admin/admin
# Create a SonarQube project call devops and note down the token
# A project analysis token also can be created from User > My Account > Security
brew install sonar-scanner
coverage run -m unittest unit_test.py
coverage xml
sonar-scanner   -Dsonar.projectKey=devops   -Dsonar.sources=.   -Dsonar.host.url=http://localhost:9000   -Dsonar.login=sqp_26fc51fd1384a43db7303c8c9f433d08e1050b72 -X -Dsonar.python.version=3.10 -Dsonar.python.coverage.reportPaths=coverage.xml
open http://localhost:9000 > Projects > devops > Overall Code
```
Brew will also install Java in order to run SonarQube.

Note:
  [Community Edition does not scan C/C++](https://www.almtoolbox.com/blog/sonarqube-editions-differences/)