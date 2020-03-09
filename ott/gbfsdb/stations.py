from ott.gbfsdb.gbfs_client import GbfsClient
import logging
log = logging.getLogger(__file__)


class Stations(object):
    """
    combine stations
    @see https://github.com/NABSA/gbfs
    @see https://github.com/NABSA/gbfs/blob/master/systems.csv
    """
    _station_cache = None

    def __init__(self, base_url):
        self.client = GbfsClient(base_url)

    def active_stations(self):
        ret_val = []
        status = self.station_status
        for k in self.station_cache:
            if status[k].get('is_renting') or status[k].get('is_returning'):
                info = {'station': self.station_cache[k], 'status': status[k]}
                ret_val.append(info)
        return ret_val

    def all_stations(self):
        ret_val = []
        status = self.station_status
        for k in self.station_cache:
            info = {'station': self.station_cache[k], 'status': status[k]}
            ret_val.append(info)
        return ret_val

    @property
    def station_cache(self, force_update=False):
        """
        put station info in a hashtable, with station_id as the hash
        """
        if self._station_cache is None or force_update:
            log.info("grab station info")
            station_info = self.client.station_information()
            h = self._service_response_to_hashtable(station_info)
            if h and len(h.keys()) > 0:
                self._station_cache = h
        return self._station_cache

    @property
    def station_status(self):
        log.info("grab station status")
        station_info = self.client.station_status()
        ret_val = self._service_response_to_hashtable(station_info)
        return ret_val

    @classmethod
    def _service_response_to_hashtable(cls, resp):
        """
        put station info in a hashtable, with station_id as the hash
        """
        ret_val = {}
        data = resp.get('data', {})
        for s in data.get('stations', []):
            i = s.get('station_id')
            ret_val[i] = s
        return ret_val


def main():
    a = Stations('http://biketownpdx.socialbicycles.com/opendata')
    print(a.active_stations())


if __name__ == '__main__':
    main()
