## Install Prometheus on Raspberry Pi
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
