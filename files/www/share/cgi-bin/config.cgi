#!/bin/bash

# Cyborg Unplug CGI script for the RT5350f. Takes an 'event' from the PHP
# interface, parses it and writes configuration files used by the detection
# routine. 
# 
# Copyright (C) 2015 Julian Oliver 
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

readonly EVENT=$(echo $QUERY_STRING | sed 's/\+/\ /g')
readonly OLDIFS=$IFS
readonly IFS="&"

set $EVENT
#EVENT=${EVENT/=*/} 
env > environment

echo $EVENT > /tmp/event.log
# Remove each time script is invoked to disarm in case the user goes back

html() {
    echo Content-type: text/html
    echo
    echo '<html>'
    echo '<meta http-equiv="Refresh" content="1; url=/'"$1"'">'
    echo '</html>'
}

case "$EVENT" in
    *sharerefresh*)
        block umount
        block mount
        sleep 3
        # Give random visitors to Little Snipper's main page a button to access the share
        cp /www/index.html.share /www/index.html 
        # Test if we really truly do have access to the USB mass storage file
        # system by looking for a unique file we put in the mountpoint folder
        if [ ! -f /www/share/usb/$(cat /www/config/rev) ]; then 
            # Give random visitors to the share resource a page without reboot, Wi-Fi, config buttons
            cp /www/share/index.php.share /www/share/index.php
        else 
            cp /www/share/index.php.conf /www/share/index.php
        fi
        html share/index.php
    ;; 
    *umount*)
        block umount
        sleep 1
        cp /www/index.html.conf /www/index.html
        cp /www/share/index.php.conf /www/share/index.php
        html index.html 
    ;; 
	*)
esac
IFS=$OLDIFS
