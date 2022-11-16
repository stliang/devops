# Common reasons that can lead to Linux Boot issues due to fstab misconfiguration:
# Traditional filesystem name is used instead of the Universally Unique Identifier (UUID) of the filesystem.
# An incorrect UUID is used.
# An entry exists for an unattached device without nofail option within fstab configuration.
# Incorrect entry within fstab configuration.
# reference: https://learn.microsoft.com/en-us/troubleshoot/azure/virtual-machines/linux-virtual-machine-cannot-start-fstab-errors


# verify fstab using findmnt --verify --verbose
# The command verify /etc/fstab parsability and usability.  It checks if source dev exists!
# https://linuxhandbook.com/findmnt-command-guide/