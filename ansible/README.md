# Manual and ansible insttructions for setting up Raspberry pi
# Initialize the Raspberry PI with local keyboard and monitor

## Ansible updates to station-server

ansible-playbook pi-config.yml -i hosts

## Manual instructions for initial setup

On machine with SD writer:
- Create pi desktop image

- write to SD (/Volumes/boot) /wpa_supplicant.conf

```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=US

network={
 ssid="slvfdg"
 psk="blevins1"
}
```

- "touch ssh" on SD (/Volumes/boot)



On Mac (on pi via ssh)
```
ssh-copy-id pi@<ip-address>
ssh pi@<ip-address>
# this may fail to remove things that don't exist, that's fine
sudo apt-get remove --purge wolfram-engine scratch nuscratch sonic-pi idle3 smartsim java-common minecraft-pi python-minecraftpi python3-minecraftpi libreoffice python3-thonny geany claws-mail bluej greenfoot
sudo apt-get autoremove
sudo apt-get update
sudo apt-get upgrade
sudo apt-get dist-upgrade
sudo apt-get install unclutter chromium-browser
```

sudo vi /home/pi/.config/lxsession/LXDE-pi/autostart
```
@xset s off
@xset -dpms
@xset s noblank
@sed -i 's/"exited_cleanly": false/"exited_cleanly": true/' ~/.config/chromium/Default/Preferences
@sleep 10
@chromium-browser --noerrdialogs --kiosk http://localhost:8000/stationData --incognito --disable-translate
```

sudo vi /etc/systemd/system/station-server.service
```
[Unit]
Description=Unicorn Daemon for station-server
After=network.target

[Service]
User=pi
Environment="PYTEMP_CONFIG=config/pytemp-prod.cfg"
WorkingDirectory=/home/pi/station-server
ExecStart=/home/pi/venv/station-server/bin/gunicorn --workers 4 station-server:app
ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s TERM $MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
```

sudo systemctl daemon-reload && sudo systemctl enable station-server

Change hostname via 'sudo raspi-config'; system options

put hostname in ansible/hosts

Make /boot/config.txt look like the following:
```
# uncomment if you get no picture on HDMI for a default "safe" mode
#hdmi_safe=1

# uncomment this if your display has a black border of unused pixels visible
# and your display can output without overscan
#disable_overscan=1

# uncomment the following to adjust overscan. Use positive numbers if console
# goes off screen, and negative if there is too much border
#overscan_left=16
#overscan_right=16
#overscan_top=16
#overscan_bottom=16

# uncomment to force a console size. By default it will be display's size minus
# overscan.
#framebuffer_width=1280
#framebuffer_height=720

# uncomment if hdmi display is not detected and composite is being output
hdmi_force_hotplug=1

# uncomment to force a specific HDMI mode (here we are forcing 800x480!)
hdmi_group=2
hdmi_mode=87
hdmi_cvt=800 480 60 6 0 0 0
hdmi_drive=1

max_usb_current=1

# uncomment to force a HDMI mode rather than DVI. This can make audio work in
# DMT (computer monitor) modes
#hdmi_drive=2

# uncomment to increase signal to HDMI, if you have interference, blanking, or
# no display
#config_hdmi_boost=4

# uncomment for composite PAL
#sdtv_mode=2

#uncomment to overclock the arm. 700 MHz is the default.
#arm_freq=800

# for more options see http://elinux.org/RPi_config.txt
```
