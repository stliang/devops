## Run Prometheus in Raspberry Pi
It is a bad idea to mount USB drive to serve as Prometheus data storage becaue editing the fstab is not reliable

```
docker run \
    -p 9090:9090 \
    -v /path/to/prometheus.yml:/etc/prometheus/prometheus.yml \
    prom/prometheus
```
