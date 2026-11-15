#!/bin/bash
# runs once, as root, on the server's first boot
set -euo pipefail
dnf install -y python3-pip
pip3 install flask gunicorn
mkdir -p /opt/photo-notes
cat > /opt/photo-notes/app.py <<'PY'
__APP__
PY
chown -R ec2-user: /opt/photo-notes
cat > /etc/systemd/system/photo-notes.service <<'UNIT'
[Unit]
Description=Photo Notes web app
After=network-online.target

[Service]
User=ec2-user
WorkingDirectory=/opt/photo-notes
ExecStart=/usr/local/bin/gunicorn --bind 0.0.0.0:80 --workers 2 app:app
AmbientCapabilities=CAP_NET_BIND_SERVICE
Restart=always

[Install]
WantedBy=multi-user.target
UNIT
systemctl daemon-reload
systemctl enable --now photo-notes
