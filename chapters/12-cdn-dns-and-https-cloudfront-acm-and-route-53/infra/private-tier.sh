#!/bin/bash
mkdir -p /srv/status
cat > /usr/local/bin/egress-check <<'SH'
#!/bin/bash
while true; do
  ip=$(curl -s -m 5 https://checkip.amazonaws.com || echo none)
  s3=$(curl -s -m 5 -o /dev/null -w '%{http_code}' https://s3.us-east-2.amazonaws.com)
  echo "$(date -u +%H:%M:%S) internet: ${ip:-none} s3: $s3" > /srv/status/egress.txt
  sleep 15
done
SH
chmod +x /usr/local/bin/egress-check
systemd-run --unit egress-check /usr/local/bin/egress-check
systemd-run --unit status-web python3 -m http.server 8080 --directory /srv/status
