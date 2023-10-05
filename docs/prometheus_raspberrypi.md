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

## Install Prometheus without container
```
cd ~/
wget https://github.com/prometheus/prometheus/releases/download/v2.47.1/prometheus-2.47.1.linux-armv7.tar.gz
tar xfz prometheus-2.47.1.linux-armv7.tar.gz 
mv prometheus-2.47.1.linux-armv7 prometheus
rm prometheus-2.47.1.linux-armv7.tar.gz 
cd /var/lib/
sudo mv ~/prometheus .
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

# Start the service
sudo systemctl enable prometheus
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
wget https://github.com/prometheus/node_exporter/releases/download/v1.6.1/node_exporter-1.6.1.linux-armv7.tar.gz
tar -xvzf node_exporter-1.6.1.linux-armv7.tar.gz 
sudo cp node_exporter-1.6.1.linux-armv7/node_exporter /usr/local/bin
sudo chmod +x /usr/local/bin/node_exporter
sudo useradd -m -s /bin/bash node_exporter
sudo mkdir /var/lib/node_exporter
sudo chown -R node_exporter:node_exporter /var/lib/node_exporter
sudo vi /etc/systemd/system/node_exporter.service
sudo systemctl daemon-reload 
sudo systemctl enable node_exporter.service
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
    - targets: ['192.168.1.70:9100']

```
3.) Calculate disk usage
Go to http://localhost:9090/ and enter query:
```
100 - ((node_filesystem_avail_bytes{mountpoint="/",fstype!="rootfs"} * 100) /            node_filesystem_size_bytes{mountpoint="/",fstype!="rootfs"})
```

Refrence:

[How To](https://linuxhit.com/prometheus-node-exporter-on-raspberry-pi-how-to-install/)
