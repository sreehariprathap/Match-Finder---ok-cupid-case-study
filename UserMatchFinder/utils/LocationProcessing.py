import requests
from math import radians, sin, cos, sqrt, atan2

def get_user_location(api_url, api_key, ip_address):
    """
    Fetches the user's geolocation based on their IP address.
    
    Parameters:
        api_url (str): The URL of the geolocation API.
        api_key (str): The API key for authentication.
        ip_address (str): The user's IP address.

    Returns:
        dict: A dictionary containing latitude and longitude.
    """
    response = requests.get(f"{api_url}/{ip_address}?apikey={api_key}")
    if response.status_code == 200:
        data = response.json()
        return {
            "latitude": data["latitude"],
            "longitude": data["longitude"]
        }
    else:
        raise Exception("Failed to fetch geolocation data")

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculates the Haversine distance between two geographical points.
    
    Parameters:
        lat1, lon1 (float): Latitude and longitude of the first user.
        lat2, lon2 (float): Latitude and longitude of the second user.

    Returns:
        float: The distance in kilometers.
    """
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    radius_earth_km = 6371  # Earth's radius in kilometers
    return radius_earth_km * c

def assign_proximity_score(distance):
    """
    Assigns a proximity score based on distance.
    
    Parameters:
        distance (float): Distance in kilometers between users.

    Returns:
        int: A proximity score (1-10).
    """
    if distance < 10:
        return 10
    elif distance < 50:
        return 8
    elif distance < 100:
        return 6
    elif distance < 500:
        return 4
    elif distance < 1000:
        return 2
    else:
        return 1

def calculate_proximity_score(api_url, api_key, user1_ip, user2_ip):
    """
    Calculates the proximity score between two users based on their geolocation.
    
    Parameters:
        api_url (str): The URL of the geolocation API.
        api_key (str): The API key for authentication.
        user1_ip (str): IP address of the first user.
        user2_ip (str): IP address of the second user.

    Returns:
        int: The proximity score (1-10).
    """
    # Get geolocation for both users
    user1_location = get_user_location(api_url, api_key, user1_ip)
    user2_location = get_user_location(api_url, api_key, user2_ip)

    # Calculate the distance between the two users
    distance = calculate_distance(
        user1_location["latitude"], user1_location["longitude"],
        user2_location["latitude"], user2_location["longitude"]
    )

    # Assign and return a proximity score
    return assign_proximity_score(distance)

# Example usage:
# Replace `api_url`, `api_key`, and `ip_address` with actual values
# proximity_score = calculate_proximity_score("https://api.ipgeolocation.io/ipgeo", "your_api_key", "192.168.1.1", "192.168.1.2")
