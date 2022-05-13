import datetime
from ott.utils import json_utils
from .pod import to_location


def status(num, date=None, status_code="success"):
    if date is None:
        date = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    status_val = {
        "code": status_code,
        "request_time": date,
        "num_results": num,
        "num_returned": num
    }
    return status_val


def scrape_pods(url="https://www.zipcar.com/api/drupal/1.0/locations?lat=45.505&lon=-122.67&lat_delta=1.11&lon_delta=2.22"):
    """
    locations: [
        {'vehicleCount': 3, 'latitude': 45.522, 'longitude': -122.6749, 'description': None, 'marketId': '209', 'locationId': '7712', 'directions': '<p>Zipcars are located on the Second-level parking garage of US Bancorp Tower Garage.</p><p><strong>By Vehicle</strong></p><p>Enter the garage from SW 4th Avenue at Pine Street.  Zipcar spaces are located on the Second floor.</p><p><strong>Pedestrian Access</strong></p><p>Take the elevator behind the courtyard on SW 5th Avenue at Pine Street to the second floor.</p><p><strong>Parking Pass Type</strong></p><p>Parking pass keycard located in the visor on the driver side. Do not remove from vehicle.The gate should open automatically when you drive up. If a ticket pops out, please leave it on the dashboard.</p>'}
    """
    ret_val = []
    zips = json_utils.stream_json(url)
    for z in zips.get('locations'):
        if z.get('vehicleCount') > 0:
            pod = to_location(z.get('locationId'), z.get('directions'), z.get('latitude'), z.get('longitude'), z.get('vehicleCount'))
            ret_val.append(pod)
    return ret_val


def zipcar_json_ws_response():
    pods = scrape_pods()
    stat = status(len(pods))
    ret_val = {
        'status': stat,
        'locations': pods
    }
    return ret_val


def main():
    url = "https://www.zipcar.com/api/drupal/1.0/locations?lat=45.505&lon=-122.67&lat_delta=1.11&lon_delta=2.22"
    zips = json_utils.stream_json(url, raw_data=True)
    print(zips)


if __name__ == '__main__':
    main()
