
# Ubuntu 20.04 Autoinstall

## Install Debian utility packages
```
sudo apt install wget git p7zip xorriso isolinux
```

## Generate a salted password for user-data file
mkpasswd -m sha-512

Note the $.$..........$ in password string is a salt value and different salt will generate different hash for the same password in user-data file

## Note down your Target_System type instrument's primary network interface name
```
ip link
```

## Note down the name and storage capacity of the target drive
```
lsblk
```

## Clone my_repo
```
git clone https://github.com/stliang/devops.git
cd devops/linux/autoinstall/ubuntu_20.04
```

## Update user-data file with the noted network interface name, storage drive name, and set desired storage partition size
```
vi user-data
```

## Download ISO Installer
```
wget https://ubuntu.volia.net/ubuntu-releases/20.04.6/ubuntu-20.04.6-live-server-amd64.iso
```

## Extract ISO using xorriso and fix permissions
```
xorriso -osirrox on -indev "ubuntu-20.04.6-live-server-amd64.iso" -extract / iso && chmod -R +w iso
```

## Create ISO distribution dirrectory
```
mkdir -p iso/nocloud/
```

## Create empty meta-data file
```
touch iso/nocloud/meta-data
```

## Copy my_site director to ./iso/
```
cp -r ./my_site iso/
```

## Copy user-data file
```
cp user-data iso/nocloud/user-data
```

## Copy grub.cfg and txt.cfg into iso locations
```
cp grub.cfg iso/boot/grub/grub.cfg
cp txt.cfg iso/isolinux/txt.cfg
```

## Regenerate md5
### The find will warn 'File system loop detected' and return non-zero exit status on the 'ubuntu' symlink to '.'
### To avoid that, temporarily move it out of the way
```
mv iso/ubuntu .
(cd iso; find '!' -name "md5sum.txt" '!' -path "./isolinux/*" -follow -type f -exec "$(which md5sum)" {} \; > ../md5sum.txt)
mv md5sum.txt iso/
mv ubuntu iso
```

## Validate user-data file (no error means YAML file is well formed)
```
python3 -c 'import yaml, sys; print(yaml.safe_load(sys.stdin))' < iso/nocloud/user-data
```

## Create Install ISO from extracted dir
```
xorriso -as mkisofs -r \
  -V Ubuntu\ custom\ amd64 \
  -o ubuntu-20.04.6-live-server-amd64-autoinstall.iso \
  -J -l -b isolinux/isolinux.bin -c isolinux/boot.cat -no-emul-boot \
  -boot-load-size 4 -boot-info-table \
  -eltorito-alt-boot -e boot/grub/efi.img -no-emul-boot \
  -isohybrid-gpt-basdat -isohybrid-apm-hfsplus \
  -isohybrid-mbr /usr/lib/ISOLINUX/isohdpfx.bin  \
  iso/boot iso
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
sudo dd bs=4M if=./ubuntu-20.04.6-live-server-amd64-autoinstall.iso of=/dev/<USB drive name> conv=fdatasync status=progress
```

## Start autoinstall
Plug the USB 2.0 drive just created into Target_System. Power up the instrument and press the "Delete" key to get into UEFI/BIOS.  This entry key may differ depend on motherboard manufacture.  Go to the boot section and select UEFI USB drive that matches the plugged in USB drive as the top boot priority.  This could be "UEFI USB CD/DVD".  Save and reboot.  The first GRUB menu item is "Install Ubuntu 20.04", the autoinstall process will select the first menu item automatically and begin installing.  The instrument will reboot itself when autoinstall is done.  Before the instrument boot passes UEFI/BIOS entry key prompt, uplug the USB drive.  Get into the UEFI/BIOS boot section again and set the top boot priority to the installed drive.  Save and reboot.

## After install
At the GUI login screen, press Ctrl + Alt + F3 to switch to none GUI mode.  Login with username "root" and password "root" and then change root user's password.  Exit out of root account and press Ctrl + Alt + F1 to get back into GUI mode.  You can select any of the default super user account and login with its credential.

## Testing
After you login as a super user, inspect the drive partitions, the $HOME directory, network interfaces, and "sudo su" command.  Bring up a terminal and perform the following commands:
```
ip add
lsblk
ls -la $HOME
sudo su

## Troubleshooting
If autoinstall crash during Debian package install, this may be due to network interface failed to get an IP address from DHCP server.  In this case, try a different network interface name as your primary way of getting out to the Internet.  Other crash may be due to bad user-data settings.

## Clean up (Optional)
Once autoinstall is successful, move or delete the iso directory, ubuntu-20.04.6-live-server-amd64-autoinstall.iso and ubuntu-20.04.6-live-server-amd64.iso files from working directory where ISO image is made.  This is to prevent accidental git push of ISO files into github project.

## References
- [How To](https://gist.github.com/s3rj1k/55b10cd20f31542046018fcce32f103e)
- [About USB](https://www.storagereview.com/news/what-is-usb-c-background-and-overview)
- [isolinux](https://github.com/tadas-s/custom-ubuntu-install/issues/5)
