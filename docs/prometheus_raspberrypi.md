## Run Prometheus in Raspberry Pi
First, add an external storage using a USB drive.  Use gparted as needed to install the USB drive.
Fix fstab so that the USB drive will be properly configured on boot.  Ues /var/lib/prometheus for data storage we have:
```
blkid  -sUUID  
/dev/sda1: UUID="bc9bc40d-0875-472f-a4ed-862d146d6196"

sudo vi /etc/fstab
PARTUUID=bc9bc40d-0875-472f-a4ed-862d146d6196  /var/lib/prometheus    ext4    defaults   0   0
```

[fstab options](https://linuxopsys.com/topics/linux-fstab-options)

```
docker run \
    -p 9090:9090 \
    -v /path/to/prometheus.yml:/etc/prometheus/prometheus.yml \
    prom/prometheus
```
