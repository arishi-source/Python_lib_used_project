import requests
from locations import get_country_from_location

REST = "https://restcountries.com/v3.1"
EXCHANGE = "https://open.er-api.com/v6/latest/"

print("=== SMART CURRENCY CONVERTER ===")
print("Enter COUNTRY or CURRENCY CODE (e.g., 'Germany' or 'EUR')")
print("You can also enter a CITY/PLACE (e.g., 'Paris' or 'Mumbai')")
print("Type 'q' to quit\n")


def resolve_currency(text):
    text = text.strip()
    if not text:
        return None
    try:
        # Currency code case (USD, INR, EUR)
        if len(text) == 3 and text.isalpha():
            code = text.upper()
            r = requests.get(f"{REST}/currency/{code}", timeout=10)
            if r.status_code != 200:
                return None
            for c in r.json():
                cur = c.get("currencies", {})
                if code in cur:
                    return code, cur[code].get("name", code)
            return code, code
        # Country name case
        r = requests.get(f"{REST}/name/{text}",
                         params={"fullText": "true"},
                         timeout=10)
        if r.status_code != 200:
            r = requests.get(f"{REST}/name/{text}", timeout=10)
        if r.status_code != 200:
            return None
        data = r.json()
        cur = data[0].get("currencies", {})
        if not cur:
            return None
        code, info = next(iter(cur.items()))
        return code.upper(), info.get("name", code.upper())
    except:
        return None

def resolve_place_to_country(input_text, var_name):
    """Checks if the input is a place and resolves it to a country name."""
    is_currency_code = (len(input_text) == 3 and input_text.isalpha())
    if not is_currency_code and input_text.lower() not in ('q',):
        country_name_result = get_country_from_location(input_text)
        if isinstance(country_name_result, str) and (
            country_name_result.startswith("ERROR")
            or country_name_result in (
                "Location not found.",
                "Country not found in location details.",
                "Country code not found and address parsing failed."
            )
        ):
            if var_name == "from":
                print(f"⚠️ Could not resolve '{input_text}' as a place name. Trying as country/currency...")
            return input_text
        else:
            print(f"🌍 Resolved '{input_text}' to country: {country_name_result}")
            return country_name_result
    return input_text


while True:
    print("\n------------------------------")
    frm = input("Convert from (Country/Currency/Place): ").strip()
    if frm.lower() in ("q", "quit", "exit"):
        break
    # Resolve source place → country
    frm = resolve_place_to_country(frm, "from")
    to = input("Convert to (Country/Currency/Place): ").strip()
    if to.lower() in ("q", "quit", "exit"):
        break
    # Resolve target place → country
    to = resolve_place_to_country(to, "to")
    amt_str = input("Amount: ").strip()
    if amt_str.lower() in ("q", "quit", "exit"):
        break
    try:
        amount = float(amt_str)
    except:
        print("❌ Invalid amount.")
        continue
    src = resolve_currency(frm)
    dst = resolve_currency(to)
    if not src or not dst:
        if not src:
            print(f"❌ Could not find currency for source: '{frm}'.")
        if not dst:
            print(f"❌ Could not find currency for target: '{to}'.")
        print("❌ Invalid source or target country/currency name.")
        continue
    from_code, from_name = src
    to_code, to_name = dst
    try:
        r = requests.get(EXCHANGE + from_code, timeout=10)
        data = r.json()
    except:
        print("❌ Exchange-rate API error.")
        continue
    if data.get("result") != "success":
        print(f"❌ Could not use {from_code} as a base currency.")
        continue
    rate = data.get("rates", {}).get(to_code)
    if rate is None:
        print(f"❌ Target currency {to_code} not supported.")
        continue
    converted = amount * rate
    print("\n=== ✅ RESULT ===")
    print(f"{amount} {from_code} ({from_name})")
    print(f"= {converted:.2f} {to_code} ({to_name})")
    print(f"Rate: 1 {from_code} = {rate} {to_code}")
    if input("\nConvert again? (y/n): ").strip().lower() not in ("y", "yes"):
        break
print("\n👋 Bye!")

