# Install Jenkins on Mac OS M1 (aarch64)
```
export JFROG_HOME=/opt/jfrog
cd $JFROG_HOME
mkdir -p $JFROG_HOME/artifactory/var/etc/
cd $JFROG_HOME/artifactory/var/etc/
touch ./system.yaml
sudo chown -R 1030:1030 $JFROG_HOME/artifactory/var
sudo chmod -R 777 $JFROG_HOME/artifactory/var
docker run --name artifactory -v $JFROG_HOME/artifactory/var/:/var/opt/jfrog/artifactory -d -p 8081:8081 -p 8082:8082 releases-docker.jfrog.io/jfrog/artifactory-oss:latest
```

console log:
```
docker run --name artifactory -v $JFROG_HOME/artifactory/var/:/var/opt/jfrog/artifactory -d -p 8084:8081 -p 8082:8082 releases-docker.jfrog.io/jfrog/artifactory-oss:latest
docker ps
docker logs -f 416182802ff6
```