## Prep
```
sudo apt update
```
```
sudo apt -y install curl git xorriso
```
```
git clone https://github.com/stliang/devops.git
cd linux/autoinstall/debian_12
```

## Update preseed.cfg and post_install_files/interfaces.cfg
Note down the primary network interface name, hostname, and storage drive partitions of the target system.
Then update preseed.cfg and post_install_files/interfaces.cfg accordingly

### Packages needed to generate hashed password, whois installs mkpasswd
```
sudo apt -y install pwgen whois
```
```
mkpasswd -m sha-512 -S $(pwgen -ns 16 1) <MY_PASSWORD>
```

## Download Debian ISO
```
curl -LO# https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/debian-12.9.0-amd64-netinst.iso
```

## Extract ISO files
```
xorriso -osirrox on -indev "debian-12.9.0-amd64-netinst.iso" -extract / iso
```

## Add preseed to initrd
```
chmod +w -R iso/install.amd/
gunzip iso/install.amd/initrd.gz
```
```
echo preseed.cfg | cpio -H newc -o -A -F iso/install.amd/initrd
```
```
gzip iso/install.amd/initrd
chmod -w -R iso/install.amd/
```

## Modify the boot loader
```
chmod +w iso/boot/grub
cp -f grub.cfg iso/boot/grub/grub.cfg
chmod -w iso/boot/grub
```
```
chmod +w iso/isolinux
cp isolinux.cfg iso/isolinux/isolinux.cfg
chmod -w iso/isolinux
```

## Post install stuff
```
chmod +w iso
(cd post_install_files; cp * ../iso/.)
```

## Fix iso file checksum
```
mv iso/debian .
(cd iso; find '!' -name "md5sum.txt" '!' -path "./isolinux/*" -follow -type f -exec "$(which md5sum)" {} \; > ../md5sum.txt)
mv -f md5sum.txt iso/
mv debian iso/
chmod -w iso
```

## Create the ISO
```
dd if=./debian-12.9.0-amd64-netinst.iso bs=1 count=432 of=isohdpfx.bin
xorriso -as mkisofs \
        -r -V 'Debian 12.9.0 amd64 n' \
        -J -J -joliet-long -cache-inodes \
        -isohybrid-mbr isohdpfx.bin \
        -b isolinux/isolinux.bin \
        -c isolinux/boot.cat \
        -boot-load-size 4 -boot-info-table -no-emul-boot \
        -eltorito-alt-boot \
        -e boot/grub/efi.img \
        -no-emul-boot -isohybrid-gpt-basdat -isohybrid-apm-hfsplus \
        -o ./debian-12.9.0-amd64-unattended.iso \
        iso
```

## Plugin a USB 2.0 drive to create Ubuntu installation drive
### Note down new USB drive path
```
lsblk
```

### Unmount all USB drive partitions before fdisk
```
umount /dev/<USB drive name><partition number>
```

### Clean out existing partions of USB drive
```
sudo fdisk /dev/<USB drive name>
p - for print existing partitions
d - for delete all partitions one at a time
w - save changes
```

### Burn ISO to USB drive
```
sudo dd bs=4M if=./debian-12.9.0-amd64-unattended.iso of=/dev/<USB drive name> conv=fdatasync status=progress
```

### Troubleshooting
To extract answers for preseed of a previouse installation

```
sudo su
apt-get install debconf-utils
debconf-get-selections --installer
```

View log
```
vi /var/log/installer/syslog
```

## Reference
- [How To](https://www.librebyte.net/en/systems-deployment/unattended-debian-installation/)
- [dead genisoimage](https://unix.stackexchange.com/questions/572751/how-to-make-a-reproducible-iso-file-with-mkisofs-genisoimage)
- [iso shell script](https://gist.github.com/palacaze/dec0624165fd4359114c2158da175420)
- [bookworm preseed](https://www.debian.org/releases/bookworm/example-preseed.txt)
- [Debian 12 make ISO](https://medium.com/@maros.kukan/automating-debian-linux-installation-24d10c85f797)
- [preseed.cfg location](https://www.reddit.com/r/debian/comments/s8t43y/preseed_config_being_ignored_by_installer/)
- [extract right answers for preseed](https://serverfault.com/questions/722021/preseeding-debian-install-efi)
- [preseed ignors netcfg](https://www.reddit.com/r/debian/comments/an03dj/preseed_netcfg_section_completely_ignored/)
- [no network after first install](https://lists.debian.org/debian-user/2018/02/msg00015.html)
- [GDM suspend system after 15 minutes](https://discussion.fedoraproject.org/t/talk-gnome-suspends-after-15-minutes-of-user-inactivity-even-on-ac-power/80257/59?page=2)
- [disable sleep 1](https://myelo.elotouch.com/support/s/article/How-to-Disable-Screen-Lock-and-System-Suspend-in-Ubuntu)
- [disable sleep 2](https://unix.stackexchange.com/questions/36477/how-do-i-prevent-gnome-suspending-while-i-finish-a-compilation-job)
