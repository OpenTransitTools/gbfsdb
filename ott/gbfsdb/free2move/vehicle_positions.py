from ..gbfs_client import GbfsClient
import datetime
import logging
log = logging.getLogger(__file__)


portland = 'https://www.free2move.com/carsharing/api/trimet/gbfs/6076e74f102f56f35fdc9bb8'

def main():
    log.info("\nRunning {}\n".format(datetime.datetime.now()))
    a = GbfsClient(portland)
    a.FREE_BIKE_STATUS_JSON = 'free_bike_status'
    print(a.free_bike_status())


if __name__ == '__main__':
    main()
