# devops
devops tools and sample infrastructure code

## Assumptions
1.) pip install paramiko
2.) pip install pyyaml
3.) Nodes files exist ~/.nodes/*.yaml

## Nodes Files
The nodes files contains short_name, host_address, port, username, and password information in yaml form:
nodes:
 - {short_name: fm040, host_address: 172.0.0.1, port: 22, username: joe, password: morning_joe}
 - {short_name: fm050, host_address: 172.0.0.2, port: 22, username: jane, password: morning_jane}

## Investigating the boot process
These devops tools should inspect bootstrap config files for the system startup scripts, inspect the arguments passed from boot loader to kernel, check filesystems mount and system daemons start up status, inspect init script or unit files running sequence by init or systemd, review what devices firmware sees, 

## Config Recommendations
Save journal across reboot
cat /etc/systemd/journald.conf.d/storage.conf 
[Journal]
Storage=persistent
systemctl restart systemd-journal

Check for idle ssh connect
use "w"
Use "pstree -p"
use "sudo kill <PID>"

https://www.maketecheasier.com/show-active-ssh-connections-linux/

