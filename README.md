# devops
devops tools and sample infrastructure code

## Assumptions
1. pip install pipreqs
2. pipreqs /home/project/location
3. pip install -r requirements.txt
4. Nodes files exist ~/.nodes/*.yaml

# Local development environment
[Setup virtualenv for mac](https://opensource.com/article/19/6/python-virtual-environments-mac)
[Setup virtualenv](https://www.bogotobogo.com/python/python_virtualenv_virtualenvwrapper.php)

## Nodes Files
The nodes files contains short_name, host_address, port, username, and password information in yaml form:
```
nodes:
- capabilities:
    time_service: timesyncd
    container_service: docker
    docker_client_version: 19.03.14
    docker_server_version: 19.03.14
    java_version: 1.8.0_352
  host_address: 1.1.1.1
  password: ********
  port: 22
  short_name: node1
  operational_limits:
    cpu: 80
    jvm_heap: 60
    jvm_stack: 60
    mem: 60
    mount_points:
	    /: 70
  username: ********
- capabilities:
    time_service: timesyncd
    java_version: 11.0.17
  host_address: 1.1.1.2
  password: ********
  port: 22
  short_name: node2
  operational_limits:
    cpu: 80
    jvm_heap: 60
    jvm_stack: 60
    mem: 60
    mount_points:
	    /: 70
  username: ********
```

## Investigating the boot process
These devops tools should inspect bootstrap config files for the system startup scripts, inspect the arguments passed from boot loader to kernel, check filesystems mount and system daemons start up status, inspect init script or unit files running sequence by init or systemd, review what devices firmware sees, 

## Config Recommendations
Save journal across reboot
```
cat /etc/systemd/journald.conf.d/storage.conf 
[Journal]
Storage=persistent
systemctl restart systemd-journal
```


## Check for idle ssh connect
```
use "w"
Use "pstree -p"
use "sudo kill <PID>"
```
[reference](https://www.maketecheasier.com/show-active-ssh-connections-linux/)


## System Recovery
"journalctl -xb" to viewsystem logs, "systemctl set-default <target>" to set boot target mode, "systemctl reboot" to reboot, "systemctl default" to try again to boot into default mode.
[reference](https://learn.microsoft.com/en-us/troubleshoot/azure/virtual-machines/linux-virtual-machine-cannot-start-fstab-errors)


## Install ArgoCD using Helm
Installing ArgoCD using Helm chart runs into certification error like this:
```
"https://prometheus-community.github.io/helm-charts/index.yaml": x509: certificate signed by unknown authority
```
[reference](https://www.arthurkoziel.com/setting-up-argocd-with-helm/)


To get the initial password, use k9s to view the argocd-initial-admin-secret file then 
```
echo <base64 encoded password> | base64 -d > ~/Desktop/argo.pass
```

I found the following command does not always work:
```
kubectl -n <default | argocd namespace> get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

Delete argocd-server pod might help as it did me
[reference](https://stackoverflow.com/questions/68297354/what-is-the-default-password-of-argocd)
[bug](https://github.com/argoproj/argo-cd/issues/6048)
