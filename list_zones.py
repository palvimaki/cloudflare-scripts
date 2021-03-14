import CloudFlare

# List all zones in account -> zone id, domain


def main():
    cf = CloudFlare.CloudFlare(email='yourname@example.com', token='yourapitoken')
    zones = cf.zones.get(params = {'per_page':200})
    for zone in zones:
        zone_id = zone['id']
        zone_name = zone['name']
        print(zone_id, zone_name)

if __name__ == '__main__':
    main()