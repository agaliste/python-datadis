"""
Basic example of using the Datadis API client.
"""

import os
from datetime import datetime, timedelta
from datadis_client import create_client


# Get credentials from environment variables
username = os.environ.get("DATADIS_USERNAME")
password = os.environ.get("DATADIS_PASSWORD")

if not username or not password:
    print("Please set DATADIS_USERNAME and DATADIS_PASSWORD environment variables.")
    exit(1)

# Create and authenticate the client
client = create_client(username, password)

# Get supplies
supplies = client.get_supplies()
print(f"Found {len(supplies.get('supplies', []))} supplies")

# If we have supplies, get details for the first one
if supplies.get('supplies') and len(supplies['supplies']) > 0:
    supply = supplies['supplies'][0]
    cups = supply['cups']
    distributor_code = supply['distributorCode']
    point_type = supply['pointType']
    
    print(f"\nSupply Details:")
    print(f"CUPS: {cups}")
    print(f"Distributor Code: {distributor_code}")
    print(f"Point Type: {point_type}")
    
    # Get contract details
    contract = client.get_contract_detail(cups, distributor_code)
    if contract.get('contract') and len(contract['contract']) > 0:
        print(f"\nContract Details:")
        contract_data = contract['contract'][0]
        print(f"Marketer: {contract_data.get('marketer', 'N/A')}")
        print(f"Access Fare: {contract_data.get('accessFare', 'N/A')}")
        print(f"Postal Code: {contract_data.get('postalCode', 'N/A')}")
        
        # Get powers if available
        powers = contract_data.get('contractedPowerkW', [])
        if powers:
            print(f"Contracted Powers (kW): {', '.join(str(p) for p in powers)}")
    
    # Get consumption data for the last month
    now = datetime.now()
    last_month = now - timedelta(days=30)
    
    start_date = last_month.strftime("%Y/%m")
    end_date = now.strftime("%Y/%m")
    
    print(f"\nGetting consumption data from {start_date} to {end_date}")
    
    consumption = client.get_consumption_data(
        cups=cups,
        distributor_code=distributor_code,
        start_date=start_date,
        end_date=end_date,
        measurement_type="0",  # Hourly data
        point_type=str(point_type)
    )
    
    time_curve = consumption.get('timeCurve', [])
    if time_curve:
        print(f"\nFound {len(time_curve)} consumption readings")
        print("Sample of consumption data:")
        for i, reading in enumerate(time_curve[:5]):
            print(f"  {reading.get('date')} {reading.get('time')}: {reading.get('consumptionKWh')} kWh")
        
        # Calculate total consumption
        total_consumption = sum(float(reading.get('consumptionKWh', 0)) for reading in time_curve)
        print(f"\nTotal consumption: {total_consumption:.2f} kWh")
else:
    print("No supplies found for this user.") 