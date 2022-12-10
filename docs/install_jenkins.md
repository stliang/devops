# Install Jenkins on Mac OS M1 (aarch64)

Dockerfile
```
FROM jenkins/jenkins:2.361.2-jdk11
USER root
RUN apt-get update && apt-get install -y lsb-release
RUN curl -fsSLo /usr/share/keyrings/docker-archive-keyring.asc \
  https://download.docker.com/linux/debian/gpg
RUN echo "deb [arch=$(dpkg --print-architecture) \
  signed-by=/usr/share/keyrings/docker-archive-keyring.asc] \
  https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list
RUN apt-get update && apt-get install -y docker-ce-cli
USER jenkins
RUN jenkins-plugin-cli --plugins "blueocean:1.25.8 docker-workflow:521.v1a_a_dd2073b_2e"
```

Build
```
docker build -t myjenkins-blueocean:2.361.2-1 .
```

Run
```
docker run --name jenkins-blueocean --restart=on-failure --detach \
  --network jenkins --env DOCKER_HOST=tcp://docker:2376 \
  --env DOCKER_CERT_PATH=/certs/client --env DOCKER_TLS_VERIFY=1 \
  --publish 8080:8080 --publish 50000:50000 \
  --volume jenkins-data:/var/jenkins_home \
  --volume jenkins-docker-certs:/certs/client:ro \
  myjenkins-blueocean:2.361.2-1
  ```

  console:
  ```
  docker run --dns=192.168.86.1 -p 8080:8080 -p 50000:50000 --name jenkins_docker -d --privileged --env DOCKER_TLS_CERTDIR=/certs -v jenkins-docker-certs:/certs/client -v jenkins-data:/var/jenkins_home --publish 2376:2376 jenkins/jenkins:lts-jdk11
  ```
  
Reference
  https://www.jenkins.io/doc/book/installing/docker/
