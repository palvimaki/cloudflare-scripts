#!/usr/bin/env python
# Add a new domain to Cloudflare and set up DNS records
# usage for a single domain: python add_domain.py domain.tld
# usage for multiple domains: omit argument, put domains one per line in newdomains.txt

import os
import sys

sys.path.insert(0, os.path.abspath('..'))
import CloudFlare

def main():

    cf = CloudFlare.CloudFlare(email='yourname@example.com', token='apitoken')

    try:
        domain_list = [sys.argv[1]]
    except:

        with open('newdomains.txt') as f:
            domain_list = f.read().splitlines()
        
    for zone_name in domain_list:

        """Cloudflare API code """


        # Create zone - which will only work if ...
        # 1) The zone is not on Cloudflare.
        # 2) The zone passes a whois test
        print('Create zone %s ...' % (zone_name))
        try:
            zone_info = cf.zones.post(data={'jump_start':False, 'name': zone_name})
        except CloudFlare.exceptions.CloudFlareAPIError as e:
            exit('/zones.post %s - %d %s' % (zone_name, e, e))
        except Exception as e:
            exit('/zones.post %s - %s' % (zone_name, e))

        zone_id = zone_info['id']
        if 'email' in zone_info['owner']:
            zone_owner = zone_info['owner']['email']
        else:
            zone_owner = '"' + zone_info['owner']['name'] + '"'
        zone_plan = zone_info['plan']['name']
        zone_status = zone_info['status']
        print('\t%s name=%s owner=%s plan=%s status=%s\n' % (
            zone_id,
            zone_name,
            zone_owner,
            zone_plan,
            zone_status
        ))

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
            {'name':'@', 'type':'TXT', 'content':"your text record content"}
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