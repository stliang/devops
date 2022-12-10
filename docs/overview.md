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


Nodes:
```
# https://octopus.com/blog/jenkins-docker-install-guide
alias jenkins='docker run -d -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts-jdk11 --name jenkins'

# https://www.jenkins.io/doc/book/installing/docker/
alias make_jenkins_once='docker run --dns=192.168.86.1 -p 8080:8080 -p 50000:50000 --name jenkins_docker -d --privileged --env DOCKER_TLS_CERTDIR=/certs -v jenkins-docker-certs:/certs/client -v jenkins-data:/var/jenkins_home --publish 2376:2376 jenkins/jenkins:lts-jdk11'

#alias restart_jenkins='docker stop jenkins_docker; docker start jenkins_docker'

export JFROG_HOME=/opt/jfrog

# connect Jenkins to Artifactory
# https://www.arvinep.com/2016/04/jenkins-docker-container-problem.html
# https://stackoverflow.com/questions/40053718/jenkins-artifactory-plug-in-error-occurred-while-requesting-version-information/58704060#58704060
# use http://172.17.0.2:8081/artifactory


alias make_artifactory_oss='docker run --name artifactory_oss -v $JFROG_HOME/artifactory/var/:/var/opt/jfrog/artifactory -d -p 8084:8081 -p 8082:8082 releases-docker.jfrog.io/jfrog/artifactory-oss:latest'
alias make_artifactory_pro='docker run --name artifactory_pro -v $JFROG_HOME/artifactory/var/:/var/opt/jfrog/artifactory -d -p 8084:8081 -p 8082:8082 releases-docker.jfrog.io/jfrog/artifactory-pro:latest'

# edit the file sharing file vi ~/Library/Group\ Containers/group.com.docker/settings.json
# edit system.yaml
# cd /opt/jfrog/artifactory/var/etc
# vi cat system.yaml
#configVersion: 1
#shared:
#    node:
#        id: localhost
#        ip: localhost
```