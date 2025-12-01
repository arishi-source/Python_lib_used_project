# Python_lib_used_project
import requests

# Simple Currency Converter using a free API
# API used: https://open.er-api.com/v6/latest/USD
# (This API does NOT require an API key)

print("=== SIMPLE CURRENCY CONVERTER ===")
print("Example currency codes: USD, INR, EUR, GBP, JPY\n")

# 1. Take input from the user
from_currency = input("Convert from (e.g. USD): ").upper()
to_currency = input("Convert to (e.g. INR): ").upper()
amount = float(input("Amount: "))

# 2. Build the API URL based on the 'from' currency
url = f"https://open.er-api.com/v6/latest/{from_currency}"

# 3. Fetch data from API
response = requests.get(url)
data = response.json()

# 4. Check if API returned valid data
if data["result"] != "success":
    print("Error: Invalid currency code!")
else:
    rates = data["rates"]  # All exchange rates based on 'from_currency'

if to_currency in rates:
        # 5. Convert using the rate
        rate = rates[to_currency]
        converted_amount = amount * rate
        print("\n=== RESULT ===")
        print(f"{amount} {from_currency} = {converted_amount} {to_currency}")
        print(f"Conversion Rate: 1 {from_currency} = {rate} {to_currency}")
else:
        print("Error: Target currency code not found!")
