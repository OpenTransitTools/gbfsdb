
def to_location(id, name, lat, lng, num_vehicles, street="", city="", state="", zip="", country="US"):
    location = {
        "location_id": id,
        "display_name": name,
        "coordinates": {
            "lat": lat,
            "lng": lng
        },
        "address": {
            "street": street,
            "city": city,
            "region_name": state,
            "postal_code": zip,
            "country_code": country
        },
        "num_vehicles": num_vehicles,
        "products": [
            {
                "type": "standard",
                "label": "Zipcars"
            }
        ]
    }
    return location


def counts(pod_list):
    num_vehicles = 0
    for p in pod_list:
        len += p.get('num_vehicles')
    return num_vehicles
