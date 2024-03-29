## Install Prometheus on Raspberry Pi in Container
Note: It is a bad idea to mount USB drive to serve as Prometheus data storage.

1.) Create prometheus.yml

```
sudo mkdir /etc/prometheus/
sudo vi /etc/prometheus/prometheus.yml

global:
  scrape_interval:     15s # By default, scrape targets every 15 seconds.

  # Attach these labels to any time series or alerts when communicating with
  # external systems (federation, remote storage, Alertmanager).
  external_labels:
    monitor: 'prometheus'

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: 'prometheus'

    # Override the global default and scrape targets from this job every 5 seconds.
    scrape_interval: 5s

    static_configs:
      - targets: ['localhost:9090']
```

2.) Create prometheus service
```
sudo vi /etc/systemd/system prometheus.service

[Unit]
Description=Prometheus container
After=docker.service
Wants=network-online.target docker.socket
Requires=docker.socket

[Service]
Restart=always
ExecStartPre=/bin/bash -c "/usr/bin/docker container inspect prometheus 2> /dev/null || /usr/bin/docker run -d --name prometheus --privileged -p 9090:9090 -v /etc/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml -v /var/lib/prometheus:/var/lib/prometheus prom/prometheus"
ExecStart=/usr/bin/docker start -a prometheus
ExecStop=/usr/bin/docker stop -t 10 prometheus

[Install]
WantedBy=multi-user.target
```

3.) Enable service
```
sudo systemctl enable prometheus.service
sudo reboot
```

4.) Troubleshoot
```
systemctl status prometheus.service
sudo systemctl start prometheus.service
sudo systemctl stop prometheus.service
sudo systemctl restart prometheus.service

journalctl -r -u prometheus.service
```

## Install Prometheus Without Container
```
cd ~/
wget https://github.com/prometheus/prometheus/releases/download/v2.47.1/prometheus-2.47.1.linux-armv7.tar.gz
tar xfz prometheus-2.47.1.linux-armv7.tar.gz 
mv prometheus-2.47.1.linux-armv7 prometheus
rm prometheus-2.47.1.linux-armv7.tar.gz 
cd /var/lib/
sudo mv ~/prometheus .

sudo mkdir /etc/prometheus/
sudo vi /etc/prometheus/prometheus.yml

# prometheus.yml content:
global:
  scrape_interval:     15s # By default, scrape targets every 15 seconds.

  # Attach these labels to any time series or alerts when communicating with
  # external systems (federation, remote storage, Alertmanager).
  external_labels:
    monitor: 'prometheus'

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: 'prometheus'

    # Override the global default and scrape targets from this job every 5 seconds.
    scrape_interval: 5s

    static_configs:
      - targets: ['localhost:9090']

sudo vi /etc/systemd/system/prometheus.service

# prometheus.service content:
[Unit]
Description=Prometheus Server
Documentation=https://prometheus.io/docs/introduction/overview/
After=network-online.target

[Service]
Restart=on-failure

ExecStart=/var/lib/prometheus/prometheus \
  --config.file=/etc/prometheus/prometheus.yml \
  --storage.tsdb.path=/var/lib/prometheus/data

[Install]
WantedBy=multi-user.target

# Enable service
sudo systemctl enable prometheus

# Reboot to start and test service
sudo reboot

# Start the service
sudo systemctl start prometheus
sudo systemctl status prometheus
```

## Install Grafana on Raspberry Pi

Note: As of this writting, there is no compatible grafana container image that would run on Raspberry Pi.  The following grafana.service definition will not work:
```
sudo vi /etc/systemd/system grafana.service

[Unit]
Description=Grafana container
After=docker.service
Wants=network-online.target docker.socket
Requires=docker.socket

[Service]
Restart=always
ExecStartPre=/bin/bash -c "/usr/bin/docker container inspect grafana 2> /dev/null || /usr/bin/docker run -d --name grafana --privileged -p 3000:3000 -v /var/lib/grafana:/var/lib/grafana grafana/grafana"
ExecStart=/usr/bin/docker start -a grafana
ExecStop=/usr/bin/docker stop -t 10 grafana

[Install]
WantedBy=multi-user.target
```

1.) Install Grafana with apt
```
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
sudo apt-get update
sudo apt-get install -y grafana
sudo /bin/systemctl enable grafana-server
sudo /bin/systemctl start grafana-server
sudo /bin/systemctl status grafana-server
```

Reference:
[Official doc](https://grafana.com/tutorials/install-grafana-on-raspberry-pi/)

## Install Node Exporter in Raspberry Pi
1.) Install Node Exporter
```
sudo mkdir /opt/node_exporter
cd /opt/node_exporter
sudo wget https://github.com/prometheus/node_exporter/releases/download/v1.6.1/node_exporter-1.6.1.linux-armv7.tar.gz
sudo tar -xvf node_exporter-1.6.1.linux-armv7.tar.gz --strip-components=1
sudo rm node_exporter-1.6.1.linux-armv7.tar.gz 
sudo vi /etc/systemd/system/node_exporter.service

# node_exporter.service content:
[Unit]
Description=Prometheus Node Exporter
Documentation=https://prometheus.io/docs/guides/node-exporter/
After=network-online.target

[Service]
Restart=on-failure

ExecStart=/opt/node_exporter/node_exporter

[Install]
WantedBy=multi-user.target

# Enable service and reboot
sudo systemctl enable node_exporter
sudo reboot

sudo systemctl start node_exporter.service
sudo systemctl status node_exporter.service
```

2.) Configure Prometheus to scrap Node Exporter
```
sudo vi /etc/prometheus/prometheus.yml

global:
  scrape_interval:     15s # By default, scrape targets every 15 seconds.

  # Attach these labels to any time series or alerts when communicating with
  # external systems (federation, remote storage, Alertmanager).
  external_labels:
    monitor: 'prometheus'

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: 'prometheus'

    # Override the global default and scrape targets from this job every 5 seconds.
    scrape_interval: 5s

    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'raspberry_pi_01'
    scrape_interval: 15s
    static_configs:
    - targets: ['localhost:9100']

```
3.) Calculate disk usage
Go to http://localhost:9090/ and enter query:
```
100 - ((node_filesystem_avail_bytes{mountpoint="/",fstype!="rootfs"} * 100) /            node_filesystem_size_bytes{mountpoint="/",fstype!="rootfs"})
```
### Install Alert Manager
```
wget https://golang.org/dl/go1.21.3.linux-armv6l.tar.gz
sudo rm -rf /usr/local/go; sudo tar -C /usr/local -xzf go1.21.3.linux-armv6l.tar.gz 
sudo ln -s /usr/local/go/bin/go /usr/local/bin
go install github.com/prometheus/alertmanager/cmd/alertmanager@latest

sudo useradd -M -r -s /bin/false alertmanager
cd go/bin
sudo cp alertmanager /usr/local/bin/
sudo chown alertmanager:alertmanager /usr/local/bin/alertmanager
sudo mkdir -p /etc/alertmanager
sudo vi /etc/alertmanager/alertmanager.yml

# /etc/alertmanager/alertmanager.yml  content
route:
  group_by: ['alertname']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 1h
  receiver: 'slack_monitor'
receivers:
  - name: 'slack_monitor'
    slack_configs:
      - api_url: 'https://hooks.slack.com/services/############/###########/##################'
        channel: '#monitor'
        send_resolved: true
inhibit_rules:
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname', 'dev', 'instance']


sudo chown -R alertmanager:alertmanager /etc/alertmanager
sudo mkdir -p /var/lib/alertmanager
sudo chown alertmanager:alertmanager /var/lib/alertmanager
sudo vi /etc/systemd/system/alertmanager.service
[Unit]
Description=Prometheus Alertmanager
Wants=network-online.target
After=network-online.target

[Service]
User=alertmanager
Group=alertmanager
Type=simple
ExecStart=/usr/local/bin/alertmanager \
--config.file /etc/alertmanager/alertmanager.yml \
--cluster.listen-address= \
--storage.path /var/lib/alertmanager/

[Install]
WantedBy=multi-user.target

Note:
This --cluster.advertise-address=0.0.0.0:9093 setting is not needed if HA is disabled by settting --cluster.listen-address= with empty string.


# Enable alertmanager service
sudo systemctl enable alertmanager
sudo systemctl start alertmanager
sudo systemctl status alertmanager
```
# Configure Prometheus to use Alertmanager
```
global:
  scrape_interval:     15s # By default, scrape targets every 15 seconds.

  # Attach these labels to any time series or alerts when communicating with
  # external systems (federation, remote storage, Alertmanager).
  external_labels:
    monitor: 'prometheus'

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: 'prometheus'

    # Override the global default and scrape targets from this job every 5 seconds.
    scrape_interval: 5s

    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'raspberry_pi_01'
    scrape_interval: 15s
    static_configs:
    - targets: ['localhost:9100']

# Alerting specifies settings related to the Alertmanager
alerting:
  alertmanagers:
    - static_configs:
      - targets:
        # Alertmanager's default port is 9093
        - localhost:9093
```
# Test Alertmanager
Go to http://localhost:9093/#/alerts to see the alertmanager is up.
Go to Prometheus page and query prometheus_notifications_alertmanagers_discovered to confirm Alertmanager is up

# Update prometheus config
```
/etc/prometheus/prometheus.yml 
global:
  scrape_interval:     15s # By default, scrape targets every 15 seconds.

  # Attach these labels to any time series or alerts when communicating with
  # external systems (federation, remote storage, Alertmanager).
  external_labels:
    monitor: 'prometheus'

# Rules and alerts are read from the specified file(s)
rule_files:
  - rules.yml

# Alerting specifies settings related to the Alertmanager
alerting:
  alertmanagers:
    - static_configs:
      - targets:
        # Alertmanager's default port is 9093
        - localhost:9093

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: 'prometheus'

    # Override the global default and scrape targets from this job every 5 seconds.
    scrape_interval: 5s

    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'alertmanager'
    scrape_interval: 5s
    static_configs:
      - targets: ['localhost:9093']

  - job_name: 'raspberry_pi_01'
    scrape_interval: 15s
    static_configs:
    - targets: ['localhost:9100']

```

# Add rules.yml
```
groups:
- name: AllInstances
  rules:
  - alert: InstanceDown
    # Condition for alerting
    expr: up == 0
    for: 1m
    # Annotation - additional informational labels to store more information
    annotations:
      title: 'Instance {{ $labels.instance }} down'
      description: '{{ $labels.instance }} of job {{ $labels.job }} has been down for more than 1 minute.'
    # Labels - additional labels to be attached to the alert
    labels:
      severity: 'critical'
```


Refrence:

[How To](https://linuxhit.com/prometheus-node-exporter-on-raspberry-pi-how-to-install/)

[slack integration video](https://www.youtube.com/watch?v=2E6GH9rAUwU)
