#!/bin/bash
mkdir -p /srv/web
echo '<h1>Photo Notes web tier</h1>' > /srv/web/index.html
systemd-run --unit web python3 -m http.server 80 --directory /srv/web
