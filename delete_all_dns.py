#!/usr/bin/env python
# Delete all DNS records for all domains in file domainlist.txt one domain per line

import os
import sys

sys.path.insert(0, os.path.abspath('..'))
import CloudFlare

def main():
    
    with open('domainlist.txt') as f:
        domain_list = f.read().splitlines()

    for zone_name in domain_list:

        cf = CloudFlare.CloudFlare(email='yourname@example.com', token='yourapitoken')

        print(zone_name)

        # grab the zone identifier
        try:
            params = {'name':zone_name}
            zones = cf.zones.get(params=params)
        except CloudFlare.exceptions.CloudFlareAPIError as e:
            exit('/zones %d %s - api call failed' % (e, e))
        except Exception as e:
            exit('/zones.get - %s - api call failed' % (e))

        if len(zones) == 0:
            exit('/zones.get - %s - zone not found' % (zone_name))

        if len(zones) != 1:
            exit('/zones.get - %s - api call returned %d items' % (zone_name, len(zones)))

        zone = zones[0]

        zone_id = zone['id']
        zone_name = zone['name']

        print('ZONE:', zone_id, zone_name)

        try:
            dns_records = cf.zones.dns_records.get(zone_id)
        except CloudFlare.exceptions.CloudFlareAPIError as e:
            exit('/zones/dns_records %s - %d %s - api call failed' % (zone_name, e, e))

        found = False
        for dns_record in dns_records:
            dns_record_id = dns_record['id']
            dns_record_name = dns_record['name']
            dns_record_type = dns_record['type']
            dns_record_value = dns_record['content']
            print('DNS RECORD:', dns_record_id, dns_record_name, dns_record_type, dns_record_value)

            try:
                dns_record = cf.zones.dns_records.delete(zone_id, dns_record_id)
                print('DELETED')
            except CloudFlare.exceptions.CloudFlareAPIError as e:
                exit('/zones.dns_records.delete %s - %d %s - api call failed' % (zone_name, e, e))
            found = True

        if not found:
            print('RECORD NOT FOUND')


if __name__ == '__main__':
    main()