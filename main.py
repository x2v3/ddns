import CloudFlare
import requests
import logging
import os

aname = os.getenv('DDNS_ANAME')
target_zone = os.getenv('DDNS_ZONE')
logger = logging.getLogger()


def main():
    cf = CloudFlare.CloudFlare()
    zones = cf.zones.get(params={'name': target_zone})
    if len(zones) == 1:
        zone_id = zones[0]['id']
        zone_name = zones[0]['name']

        my_ip = get_my_ip()
        logger.info('my real ip is %s', my_ip)
        update_record(cf, zone_id, my_ip)
    else:
        logger.error('zone not available.')


def update_record(cf, zone_id, content):
    record = {
        'name': aname,
        'type': 'A',
        'content': content,
        'proxied': False
    }
    current = cf.zones.dns_records.get(zone_id, params={'name': aname + '.' + target_zone})
    logger.info('my current setting is %s' % current)
    if len(current) == 0 or current[0]['content'] != content:
        logger.info('updating dns record')
        cf.zones.dns_records.post(zone_id, data=record)
        logger.info('dns record updated')
    else:
        logger.info('no need to update current dns')


def get_my_ip():
    url = 'https://api.ipify.org/?format=json'
    r = requests.get(url)
    ip = r.json()
    return ip['ip']


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)-15s %(levelname)s %(message)s',level=logging.DEBUG)
    main()
