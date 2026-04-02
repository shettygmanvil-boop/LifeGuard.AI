import requests

OVERPASS_URL = "https://overpass-api.de/api/interpreter"


def get_nearby_hospitals(lat: float, lng: float, radius: int = 5000):
    """
    Finds hospitals near the given coordinates using OpenStreetMap Overpass API.
    Completely free — no API key or billing required.
    """
    # Overpass QL query: find nodes/ways tagged as hospitals within radius
    query = f"""
    [out:json][timeout:25];
    (
      node["amenity"="hospital"](around:{radius},{lat},{lng});
      way["amenity"="hospital"](around:{radius},{lat},{lng});
      node["amenity"="clinic"](around:{radius},{lat},{lng});
      way["amenity"="clinic"](around:{radius},{lat},{lng});
    );
    out center 10;
    """

    try:
        response = requests.post(
            OVERPASS_URL,
            data={"data": query},
            timeout=30,
            headers={"User-Agent": "LifeGuard.AI/1.0"},
        )
        response.raise_for_status()
        elements = response.json().get("elements", [])

        hospitals = []
        for el in elements:
            tags = el.get("tags", {})
            name = tags.get("name") or tags.get("name:en")
            if not name:
                continue  # skip unnamed entries

            # Nodes have lat/lon directly; ways have a "center"
            if el["type"] == "node":
                elat, elng = el.get("lat"), el.get("lon")
            else:
                center = el.get("center", {})
                elat, elng = center.get("lat"), center.get("lon")

            if not elat or not elng:
                continue

            hospitals.append({
                "name": name,
                "address": tags.get("addr:full")
                    or ", ".join(filter(None, [
                        tags.get("addr:housenumber"),
                        tags.get("addr:street"),
                        tags.get("addr:city"),
                    ]))
                    or tags.get("addr:street")
                    or "Address not available",
                "phone": tags.get("phone") or tags.get("contact:phone"),
                "website": tags.get("website") or tags.get("contact:website"),
                "emergency": tags.get("emergency"),
                "type": tags.get("amenity", "hospital"),
                "lat": elat,
                "lng": elng,
            })

            if len(hospitals) >= 10:
                break

        return hospitals

    except requests.RequestException as e:
        raise ValueError(f"Overpass API network error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Hospital search failed: {str(e)}")
