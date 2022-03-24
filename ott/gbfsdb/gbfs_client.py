import datetime
from ott.utils import json_utils
import logging
log = logging.getLogger(__file__)


class GbfsClient(object):
    """
    simple wget client for streaming each GBFS file from a vendor gbfs service
    @see https://github.com/NABSA/gbfs
    @see https://github.com/NABSA/gbfs/blob/master/systems.csv
    """
    GBFS_JSON = 'gbfs.json'
    SYSTEM_INFORMATION_JSON = 'system_information.json'
    STATION_STATUS_JSON = 'station_status.json'
    STATION_INFO_JSON = 'station_information.json'
    FREE_BIKE_STATUS_JSON = 'free_bike_status.json'
    SYSTEM_HOURS_JSON = 'system_hours.json'
    SYSTEM_CALENDAR_JSON = 'system_calendar.json'
    SYSTEM_REGIONS_JSON = 'system_regions.json'
    SYSTEM_PRICING_PLANS_JSON = 'system_pricing_plans.json'
    SYSTEM_ALERTS_JSON = 'system_alerts.json'


    def __init__(self, base_url):
        self.base_url = base_url

    def gbfs(self):
        return self.stream_json(self.GBFS_JSON)

    def system_information(self):
        return self.stream_json(self.SYSTEM_INFORMATION_JSON)

    def station_status(self):
        return self.stream_json(self.STATION_STATUS_JSON)

    def station_information(self):
        return self.stream_json(self.STATION_INFO_JSON)

    def free_bike_status(self, check_free=True, check_coords=True, check_date=False):
        ret_val = []
        json = self.stream_json(self.FREE_BIKE_STATUS_JSON)
        recs = json['data']['bikes']

        #import pdb; pdb.set_trace()
        for r in recs:
            add = False
            if r:
                add = True
                if check_coords and ('lat' not in r or 'lon' not in r):
                    add = False
                if check_free and 'is_reserved' in r and r['is_reserved'] is not False:
                    add = False
                if check_free and 'is_disabled' in r and r['is_disabled'] is not False:
                    add = False
            if add:    
                ret_val.append(r)
        return ret_val

    def system_hours(self):
        return self.stream_json(self.SYSTEM_HOURS_JSON)

    def system_calendar(self):
        return self.stream_json(self.SYSTEM_CALENDAR_JSON)

    def system_regions(self):
        return self.stream_json(self.SYSTEM_REGIONS_JSON)

    def system_pricing_plans(self):
        return self.stream_json(self.SYSTEM_PRICING_PLANS_JSON)

    def system_alerts(self):
        return self.stream_json(self.SYSTEM_ALERTS_JSON)

    def stream_json(self, api_file, def_val=[]):
        ret_val = def_val
        url = "{}/{}".format(self.base_url, api_file)
        try:
            ret_val = json_utils.stream_json(url)
        except Exception as e:
            log.error(url)
            log.error(e)
        return ret_val


def main():
    log.info("\nRunning {}\n".format(datetime.datetime.now()))
    a = GbfsClient('http://biketownpdx.socialbicycles.com/opendata')
    print(a.station_status())


if __name__ == '__main__':
    main()
