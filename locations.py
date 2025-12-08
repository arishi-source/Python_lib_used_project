from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import requests

REST = "https://restcountries.com/v3.1"

def get_country_from_location(location_name: str) -> str:
    """
    Finds the English common name for a location with native-name fixes.
    """

    NATIVE_NAME_MAP = {
        'پاکستان': 'Pakistan',
        '中国': 'China',
        '대한민국': 'South Korea',
        '日本': 'Japan',
        'الإمارات العربية المتحدة': 'United Arab Emirates',
        'مصر': 'Egypt',
        'Türkiye': 'Turkey',
        'Ελλάδα': 'Greece',
        'Deutschland': 'Germany',
        'España': 'Spain',
        'Italia': 'Italy',
        'Србија': 'Serbia',
        'Россия': 'Russia',
        'Éire': 'Ireland',
        'Suomi': 'Finland',
        'ኢትዮጵያ إثيوبια': 'Ethiopia',
    }

    try:
        geolocator = Nominatim(user_agent="city_to_country_module")
        location_data = geolocator.geocode(location_name, timeout=15)

        if not location_data:
            return "Location not found."

        raw_address = location_data.raw.get('address', {})
        country_code = raw_address.get('country_code')

        if country_code:
            r = requests.get(f"{REST}/alpha/{country_code}", timeout=10)
            if r.status_code == 200:
                return r.json()[0]['name']['common']

        else:
            full_address_str = location_data.address
            address_parts = [part.strip() for part in full_address_str.split(',')]

            if address_parts and address_parts[-1]:
                final_country_guess = address_parts[-1]

                if final_country_guess in NATIVE_NAME_MAP:
                    return NATIVE_NAME_MAP[final_country_guess]

                r = requests.get(
                    f"{REST}/name/{final_country_guess}",
                    params={"fullText": "true"},
                    timeout=10
                )

                if r.status_code == 200:
                    return r.json()[0]['name']['common']

                return final_country_guess

    except GeocoderTimedOut:
        return "ERROR: Geocoding service timed out."
    except GeocoderServiceError as e:
        return f"ERROR: Geocoding service error - {e}"
    except Exception as e:
        return f"ERROR: An unexpected error occurred - {e}"

    return "Country code not found and address parsing failed."
  
