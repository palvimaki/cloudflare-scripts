# get zone identifier for domain

# Cloudflare API - create A, CNAME and TXT records for domains
# reads domains from text file domainlist.txt one domain per line

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
