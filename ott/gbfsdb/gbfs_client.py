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
    def __init__(self, base_url, lang="en"):
        # import pdb; pdb.set_trace()
        self.base_url = base_url
        gbfs = json_utils.stream_json(base_url)
        if json_utils.exists_in(gbfs, 'data', lang, 'feeds'):
            json = gbfs['data'][lang]['feeds']
            self.gbfs_links = json_utils.rec_array_to_dict(json, 'name', 'url')

    def _curl_data(self, data_name, def_val=[]):
        ret_val = None
        if data_name in self.gbfs_links:
            #url = "{}/{}".format(self.base_url, api_file)
            url = self.gbfs_links[data_name]
            ret_val = json_utils.stream_json(url, def_val=def_val)
        return ret_val

    def gbfs_versions(self):
        return self._curl_data("gbfs_versions")

    def system_information(self):
        return self._curl_data("system_information")

    def vehicle_types(self):
        return self._curl_data("vehicle_types")

    def station_status(self):
        return self._curl_data("station_status")
        
    def station_information(self):
        return self._curl_data("station_information")

    def station_status(self):
        return self._curl_data("station_status")

    def free_bike_status(self, check_free=True, check_coords=True, check_date=False):
        ret_val = []
        json = self._curl_data("free_bike_status")
        recs = json['data']['bikes'] if json_utils.exists_in(json, 'data', 'bikes') else []

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
        return self._curl_data("system_hours")

    def system_alerts(self):
        return self._curl_data("system_alerts")

    def system_calendar(self):
        return self._curl_data("system_calendar")

    def system_regions(self):
        return self._curl_data("system_regions")

    def system_pricing_plans(self):
        return self._curl_data("system_pricing_plans")

    def geofencing_zones(self):
        return self._curl_data("geofencing_zones")


def main():
    log.info("\nRunning {}\n".format(datetime.datetime.now()))
    a = GbfsClient('http://biketownpdx.socialbicycles.com/opendata')
    print(a.station_status())


if __name__ == '__main__':
    main()
