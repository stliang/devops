# Nginx Hosted Kotlin Consumer and Producer of RabbitMQ

## 1. Setup RabbitMQ Ubuntu 20.04

### 1.a Install RabbitMQ
```
#!/bin/sh

sudo apt-get install curl gnupg apt-transport-https -y

## Team RabbitMQ's main signing key
curl -1sLf "https://keys.openpgp.org/vks/v1/by-fingerprint/0A9AF2115F4687BD29803A206B73A36E6026DFCA" | sudo gpg --dearmor | sudo tee /usr/share/keyrings/com.rabbitmq.team.gpg > /dev/null
## Community mirror of Cloudsmith: modern Erlang repository
curl -1sLf https://github.com/rabbitmq/signing-keys/releases/download/3.0/cloudsmith.rabbitmq-erlang.E495BB49CC4BBE5B.key | sudo gpg --dearmor | sudo tee /usr/share/keyrings/rabbitmq.E495BB49CC4BBE5B.gpg > /dev/null
## Community mirror of Cloudsmith: RabbitMQ repository
curl -1sLf https://github.com/rabbitmq/signing-keys/releases/download/3.0/cloudsmith.rabbitmq-server.9F4587F226208342.key | sudo gpg --dearmor | sudo tee /usr/share/keyrings/rabbitmq.9F4587F226208342.gpg > /dev/null

## Add apt repositories maintained by Team RabbitMQ
sudo tee /etc/apt/sources.list.d/rabbitmq.list <<EOF
## Provides modern Erlang/OTP releases
##
deb [signed-by=/usr/share/keyrings/rabbitmq.E495BB49CC4BBE5B.gpg] https://ppa1.novemberain.com/rabbitmq/rabbitmq-erlang/deb/ubuntu focal main
deb-src [signed-by=/usr/share/keyrings/rabbitmq.E495BB49CC4BBE5B.gpg] https://ppa1.novemberain.com/rabbitmq/rabbitmq-erlang/deb/ubuntu focal main

# another mirror for redundancy
deb [signed-by=/usr/share/keyrings/rabbitmq.E495BB49CC4BBE5B.gpg] https://ppa2.novemberain.com/rabbitmq/rabbitmq-erlang/deb/ubuntu focal main
deb-src [signed-by=/usr/share/keyrings/rabbitmq.E495BB49CC4BBE5B.gpg] https://ppa2.novemberain.com/rabbitmq/rabbitmq-erlang/deb/ubuntu focal main

## Provides RabbitMQ
##
deb [signed-by=/usr/share/keyrings/rabbitmq.9F4587F226208342.gpg] https://ppa1.novemberain.com/rabbitmq/rabbitmq-server/deb/ubuntu focal main
deb-src [signed-by=/usr/share/keyrings/rabbitmq.9F4587F226208342.gpg] https://ppa1.novemberain.com/rabbitmq/rabbitmq-server/deb/ubuntu focal main

# another mirror for redundancy
deb [signed-by=/usr/share/keyrings/rabbitmq.9F4587F226208342.gpg] https://ppa2.novemberain.com/rabbitmq/rabbitmq-server/deb/ubuntu focal main
deb-src [signed-by=/usr/share/keyrings/rabbitmq.9F4587F226208342.gpg] https://ppa2.novemberain.com/rabbitmq/rabbitmq-server/deb/ubuntu focal main
EOF

## Update package indices
sudo apt-get update -y

## Install Erlang packages
sudo apt-get install -y erlang-base \
                        erlang-asn1 erlang-crypto erlang-eldap erlang-ftp erlang-inets \
                        erlang-mnesia erlang-os-mon erlang-parsetools erlang-public-key \
                        erlang-runtime-tools erlang-snmp erlang-ssl \
                        erlang-syntax-tools erlang-tftp erlang-tools erlang-xmerl

## Install rabbitmq-server and its dependencies
sudo apt-get install rabbitmq-server -y --fix-missing
```

### 1.b Configure RabbitMQ
```
sudo systemctl enable rabbitmq-server.service
sudo systemctl start rabbitmq-server.service
sudo systemctl status rabbitmq-server.service
sudo systemctl edit rabbitmq-server.service

# Add the following to change number of file descriptors
[Service]
LimitNOFILE=4000

# Confirm file descriptor setting change
sudo systemctl restart rabbitmq-server.service
sudo systemctl status rabbitmq-server.service

# Another way to confirm file descriptor setting
sudo rabbitmq-diagnostics status
cat /proc/$RABBITMQ_BEAM_PROCESS_PID/limits

# The RABBITMQ_BEAM_PROCESS_PID is the "OS PID", 36335 for example:
cat /proc/36335/limits 
Limit                     Soft Limit           Hard Limit           Units     
Max cpu time              unlimited            unlimited            seconds   
Max file size             unlimited            unlimited            bytes     
Max data size             unlimited            unlimited            bytes     
Max stack size            8388608              unlimited            bytes     
Max core file size        0                    unlimited            bytes     
Max resident set          unlimited            unlimited            bytes     
Max processes             380457               380457               processes 
Max open files            4000                 4000                 files     
Max locked memory         65536                65536                bytes     
Max address space         unlimited            unlimited            bytes     
Max file locks            unlimited            unlimited            locks     
Max pending signals       380457               380457               signals   
Max msgqueue size         819200               819200               bytes     
Max nice priority         0                    0                    
Max realtime priority     0                    0                    
Max realtime timeout      unlimited            unlimited            us 

# User level max file descriptor
ulimit -n
1024

# Kernel level max file descriptor
sysctl fs.file-max
fs.file-max = 9223372036854775807
```

### 1.c Debug SystemD unit start up order
```
cd
sudo systemd-analyze plot > plot.html

# From a machine that can display html file
scp user_name@<rabbitmq_host>:~/plot.html .
```

## 2. Setup Nginx on Ubuntu 20.04
### 2.a Install Nginx
```
sudo apt update
sudo apt install nginx
```
### 2.b Create static page
```
cd /var/www
sudo mkdir plot
sudo chown $(whoami):$(whoami) plot
sudo systemd-analyze plot > /var/www/plot/index.html

cd /etc/nginx/sites-enabled/

sudo "${EDITOR:-vi}" plot
# input the follow
server {
       listen 81;
       listen [::]:81;

       server_name example.ubuntu.com;

       root /var/www/plot;
       index index.html;

       location / {
               try_files $uri $uri/ =404;
       }
}

sudo service nginx restart

# Go to http://<your_site>:81
```


## Reference
[cloudsmith](https://www.rabbitmq.com/install-debian.html#apt-quick-start-cloudsmith)
