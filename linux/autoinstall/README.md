# Install Debian utility packages
sudo apt install p7zip wget xorriso isolinux

# Download ISO Installer:
wget https://ubuntu.volia.net/ubuntu-releases/20.04.6/ubuntu-20.04.6-live-server-amd64.iso

# Create ISO distribution dirrectory:
mkdir -p iso/nocloud/

# Extract ISO using 7z:
7z x ubuntu-20.04.6-live-server-amd64.iso -x'![BOOT]' -oiso
# Or extract ISO using xorriso and fix permissions:
xorriso -osirrox on -indev "ubuntu-20.04.6-live-server-amd64.iso" -extract / iso && chmod -R +w iso

# Create empty meta-data file:
touch iso/nocloud/meta-data

# Generate a salted password for user-data file
mkpasswd -m sha-512

Note the $.$..........$ in password string is a salt value and different salt will generate different hash for the same password in user-data file


# Copy user-data file:
cp user-data iso/nocloud/user-data

# Update boot flags with cloud-init autoinstall:
# Should look similar to this: initrd=/casper/initrd quiet autoinstall ds=nocloud;s=/cdrom/nocloud/ ---
sed -i 's|---|autoinstall ds=nocloud\\\;s=/cdrom/nocloud/ ---|g' iso/boot/grub/grub.cfg
sed -i 's|---|autoinstall ds=nocloud;s=/cdrom/nocloud/ ---|g' iso/isolinux/txt.cfg

# Disable mandatory md5 checksum on boot:
md5sum iso/.disk/info > iso/md5sum.txt
sed -i 's|iso/|./|g' iso/md5sum.txt

# (Optionally) Regenerate md5:
# The find will warn 'File system loop detected' and return non-zero exit status on the 'ubuntu' symlink to '.'
# To avoid that, temporarily move it out of the way
mv iso/ubuntu .
(cd iso; find '!' -name "md5sum.txt" '!' -path "./isolinux/*" -follow -type f -exec "$(which md5sum)" {} \; > ../md5sum.txt)
mv md5sum.txt iso/
mv ubuntu iso

# Validate user-data file
cloud-init schema --config-file iso/nocloud/user-data

# Create Install ISO from extracted dir (Ubuntu):
xorriso -as mkisofs -r \
  -V Ubuntu\ custom\ amd64 \
  -o ubuntu-20.04.6-live-server-amd64-autoinstall.iso \
  -J -l -b isolinux/isolinux.bin -c isolinux/boot.cat -no-emul-boot \
  -boot-load-size 4 -boot-info-table \
  -eltorito-alt-boot -e boot/grub/efi.img -no-emul-boot \
  -isohybrid-gpt-basdat -isohybrid-apm-hfsplus \
  -isohybrid-mbr /usr/lib/ISOLINUX/isohdpfx.bin  \
  iso/boot iso
  
# Burn ISO to USB
lsblk
sudo fdisk /dev/<USB drive path>
p - for print existing partitions
d - for delete all partitions one at a time
w - save changes

sudo dd bs=4M if=./<ISO file name> of=/dev/<USB drive path> conv=fdatasync status=progress

# After install:
 - login with 'root:root' and change root user password
