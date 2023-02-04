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
  -
    short_name: vm01
    host_address: 172.0.0.1
    port: 22
    username: joe
    password: morning_joe
    jenkins_auth: "joe:************************"
    jenkins_url: "http://localhost:8080/"
    capabilities:
      docker: "20.10.21"
      java: "11"
  -
    short_name: vm02
    host_address: 172.0.0.2
    port: 22
    username: jane
    password: morning_jane
    jenkins_auth: "jane:************************"
    jenkins_url: "http://localhost:8080/"
    capabilities:
      docker: "20.10.21"
      java: "11"
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
