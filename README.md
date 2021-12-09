# ddns

This project trys to read your public IP address from ipify.org and update your cloudflare DNS record with it.
Before running this project you need to create a .env file with the following variables:
DDNS_ZONE=<your-zone>
DDNS_ANAME=<your-name>
CF_API_KEY=<your-api-key>