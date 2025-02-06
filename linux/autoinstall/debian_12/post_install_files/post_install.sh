#!/bin/bash

# ### Global variables ###

echo "POST INSTALL ACTIONS"

# Disable sleep
gsettings set org.gnome.desktop.session idle-delay 0
systemctl mask suspend.target

# # Clean up
# rm -f /usr/sbin/post_install.sh || true

# ##########
# # End of install
# ##########
