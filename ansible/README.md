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
@chromium-browser --noerrdialogs --kiosk http://localhost:8000 --incognito --disable-translate
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
