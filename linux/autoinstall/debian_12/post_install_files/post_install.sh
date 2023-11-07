#!/bin/bash

# ### Global variables ###

# File_Server="10.21.240.115"

# msg() {
#     echo -e "\e[1;37;44m==> ${1}\e[0m"
# }

# rabbitmq_pkg_installation() {
#    msg 'Install rabbitmq 3.6.15'
#    Rabbitmq_file='rabbitmq-server_3.6.15-1_all.deb'
#    mkdir -p /opt/rabbitmq
#    cd /opt/rabbitmq/
#    wget http://rssregistry.roche.com:8081/artifactory/list/RSC/Files/$Rabbitmq_file
#    dpkg -i $Rabbitmq_file
# }

# create_raid5_array() {
#    msg 'Create RAID5 Array'
#    echo "checking current raid5 configuration"
#    raid5_array_name=`lsblk |grep raid5|awk '{print $1}' | sort -u`
#    echo $raid5_array_name

#    if [ -z "$raid5_array_name" ]
#    then
#       dd if=/dev/zero of=/dev/sda bs=512 count=2048
#       dd if=/dev/zero of=/dev/sdb bs=512 count=2048
#       dd if=/dev/zero of=/dev/sdc bs=512 count=2048
#       dd if=/dev/zero of=/dev/sdd bs=512 count=2048
#       raid5_device_name="/dev/md127"
#       mdadm --create --force --verbose "$raid5_device_name" --level=5 --raid-devices=4 /dev/sda /dev/sdb /dev/sdc /dev/sdd <<EOF
# yes
# EOF
#    else
#       raid5_dev_name=`echo $raid5_array_name |sed "s/[^a-zA-Z0-9]//g" `
#       raid5_device_name="/dev/$raid5_dev_name"
#       echo $raid5_device_name
#    fi

#    mkfs.ext4 -F $raid5_device_name
#    raid5_mount_point="/var/roche/htp"
#    mkdir -p $raid5_mount_point
#    chown -R genia:genia "$raid5_mount_point"

#    echo "$raid5_device_name $raid5_mount_point    ext4  rw,auto,nofail,x-systemd.device-timeout=1  0 0" | tee -a /etc/fstab 
 
#    msg 'mount disk and create dirctories for labcode'
#    mount -a
#    chown -R genia:genia /var/roche/htp/
#    if [ ! -d /var/roche/htp/run ]
#    then 
#       mkdir /var/roche/htp/run
#       chown -R genia:genia /var/roche/htp/run
#    fi

#    if [ ! -d /var/roche/htp/raw ]
#    then
#       mkdir /var/roche/htp/raw
#       chown -R genia:genia /var/roche/htp/raw
#    fi 
#    ls -al /var/roche/htp
#    if [ ! -d /var/log/roche/htp/runs ]
#    then 
#       mkdir /var/log/roche/htp/runs
#       chown -R genia:genia /var/log/roche/htp/runs
#    fi  
# }

# xilinx_installation() {
#    msg 'Installing Xilinx software'
#    file_prefix='Xilinx_Vivado_Lab_Lin_2016.4_1215_1'
#    file_url="http://${File_Server}/${file_prefix}.tar.gz"
#    cd /opt
#    curl --silent --output /opt/${file_prefix}.tar.gz $file_url
#    tar xzf $file_prefix.tar.gz
# }

# HTP_repo_info() {
#    msg 'Add HTP Repo Information'
#    wget http://rssregistry.roche.com:8081/artifactory/api/gpg/key/public -O- | apt-key add -
#    echo "deb [arch=amd64] http://rssregistry.roche.com:8081/artifactory/RSC-HTP/ testing main" | tee /etc/apt/sources.list.d/genia.list
# }

# ##### Main Script #####
# # How to use the script:
# #
# # preseed-late or preseed-late dev/prod 
# # with no args,it will run as preseed-lat dev
# #
# #######################

# # Run as root
# if [[ $EUID -ne 0 ]]; then
#     echo "This script must be run as root" 2>&1
#     exit 1
# fi

echo "POST INSTALL ACTIONS"
# rabbitmq_pkg_installation
# create_raid5_array
# xilinx_installation
# HTP_repo_info

# Disable sleep
gsettings set org.gnome.desktop.session idle-delay 0
systemctl mask suspend.target

# # Clean up
# rm -f /usr/sbin/post_install.sh || true

# ##########
# # End of install
# ##########
