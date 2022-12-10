Docker containers created:
```
docker container ls -a
CONTAINER ID   IMAGE                                                   COMMAND                  CREATED       STATUS                     PORTS                                                                      NAMES
8c147ecda194   releases-docker.jfrog.io/jfrog/jfrog-cli-v2-jf          "jf -v"                  12 days ago   Exited (0) 12 days ago                                                                                confident_yalow
16b0a206a090   jenkins/jenkins:lts-jdk11                               "/usr/bin/tini -- /u…"   12 days ago   Exited (255) 2 hours ago   0.0.0.0:2376->2376/tcp, 0.0.0.0:8080->8080/tcp, 0.0.0.0:50000->50000/tcp   jenkins_docker
ea9a61fd897d   releases-docker.jfrog.io/jfrog/artifactory-pro:latest   "/entrypoint-artifac…"   12 days ago   Exited (137) 12 days ago                                                                              artifactory_pro
416182802ff6   releases-docker.jfrog.io/jfrog/artifactory-oss:latest   "/entrypoint-artifac…"   2 weeks ago   Exited (255) 2 hours ago   0.0.0.0:8082->8082/tcp, 0.0.0.0:8084->8081/tcp          
```

Brew service started:
```
brew services info  sonarqube
sonarqube (homebrew.mxcl.sonarqube)
Running: ✔
Loaded: ✔
Schedulable: ✘
```