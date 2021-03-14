#!/usr/bin/env python
# Bulk script for adding new records for domain via Cloudflare API
# Reads domainlist.txt one domain per line
# then creates desired A, CNAME, and TXT records for each domain

import os
import sys

sys.path.insert(0, os.path.abspath('..'))
import CloudFlare

def main():

    cf = CloudFlare.CloudFlare(email='yourname@example.com', token='yourapitoken')

    with open('domainlist.txt') as f:
        domain_list = f.read().splitlines()
    
    for zone_name in domain_list:

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

        # DNS records to create
        dns_records = [
            {'name':'@', 'type':'A', 'content':'192.0.2.0', 'proxied': True},
            {'name':'www', 'type':'CNAME', 'content':'{}'.format(zone_name), 'proxied': True}, # CNAME requires FQDN at content
            {'name':'@', 'type':'TXT', 'content':"text record content"}
        ]

        print('Create DNS records ...')
        for dns_record in dns_records:
            # Create DNS record
            r = cf.zones.dns_records.post(zone_id, data=dns_record)
            
            # Print respose info - they should be the same
            dns_record = r
            print('\t%s %30s %6d %-5s %s ; proxied=%s proxiable=%s' % (
                dns_record['id'],
                dns_record['name'],
                dns_record['ttl'],
                dns_record['type'],
                dns_record['content'],
                dns_record['proxied'],
                dns_record['proxiable']
            ))

        print('')


if __name__ == '__main__':
    main()