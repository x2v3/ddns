from cloudflare import Cloudflare
import requests
import logging
import os
import time

aname = os. getenv('DDNS_ANAME')
target_zone = os.getenv('DDNS_ZONE')
logger = logging.getLogger()


def main():
    # Initialize the new Cloudflare client
    # It will automatically use CLOUDFLARE_API_TOKEN or CLOUDFLARE_API_KEY from environment
    cf = Cloudflare()
    
    # Get zones using the new API structure
    zones = cf.zones. list(name=target_zone)
    
    # Convert to list since the new SDK returns an iterator
    zones_list = list(zones)
    
    if len(zones_list) == 1:
        zone_id = zones_list[0]. id
        zone_name = zones_list[0].name

        my_ip = get_my_ip()
        logger.info('my real ip is %s', my_ip)
        update_record(cf, zone_id, my_ip)
    else:
        logger.error('zone not available.')


def update_record(cf, zone_id, content):
    record_data = {
        'name': aname,
        'type': 'A',
        'content': content,
        'proxied': False
    }
    
    # Get current DNS records using the new API
    full_record_name = f"{aname}.{target_zone}"
    current_records = cf. dns. records.list(zone_id=zone_id, name=full_record_name)
    
    # Convert to list
    current = list(current_records)
    
    logger.info('my current setting is %s' % current)
    
    if len(current) == 0:
        logger.info('adding dns record')
        cf.dns. records.create(
            zone_id=zone_id,
            name=aname,
            type='A',
            content=content,
            proxied=False
        )
        logger.info('dns record added')
    elif current[0]. content != content:
        logger. info('updating dns record')
        record_id = current[0]. id
        cf.dns.records.update(
            dns_record_id=record_id,
            zone_id=zone_id,
            name=aname,
            type='A',
            content=content,
            proxied=False
        )
        logger.info('dns record updated')
    else:
        logger.info('no need to update current dns')


def get_my_ip():
    url = 'https://api.ipify.org/?format=json'
    r = requests.get(url)
    ip = r.json()
    return ip['ip']


if __name__ == '__main__':
    logging. basicConfig(format='%(asctime)-15s %(levelname)s %(message)s', level=logging.DEBUG)
    while True:
        try:
            main()
        except Exception as e:
            logger.error(e)
        time.sleep(60 * 60)  # one hour
