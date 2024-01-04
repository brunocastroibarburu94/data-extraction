import requests
import pandas as pd
from datetime import datetime 

dno_map = {
    '10' : "Eastern England",
    '11' : "East Midlands",
    '12' : "London",
    '13' : "North Wales & Mersey",
    '14' : "Midlands",
    '15' : "North East",
    '16' : "North West",
    '17' : "Northern Scotland",
    '18' : "Southern Scotland",
    '19' : "South East",
    '20' : "Southern",
    '21' : "South Wales",
    '22' : "South Western",
    '23' : "Yorkshire",
    }

voltage_level_map = {
    'LV' : 'Low voltage',
    'LV-Sub' : 'Low voltage substation',
    'HV' : 'High voltage',
}

def cost_extract(config: dict):
    """Retrieves information from Electricity Costs API. For up to date information visit: https://electricitycosts.org.uk/api/

    API references:
    - DNO: Used to select the DNO region, the parameter should be added as a string in the format “dno=XX”, 
    where XX is an integer from 10 to 23.

    - Voltage: Used to select the voltage level, the parameter should be added as a string in the format “voltage=XX”,
    where XX can be “HV”, “LV” or “LV-Sub”. It is important to add these letter exactly as presented for the API request
    to work correctly.

    - Start: Used to define the start date, the parameter should be added as a string in the format “start=DD-MM-YYYY”.
    It is important to add the “-” in-between the numbers.

    - End: Used to define the end date, the parameter should be added as a string in the format “end=DD-MM-YYYY”. 
    It is important to add the “-” in-between the numbers.

    - Voltage Levels
        - Low voltage (LV) - voltage level below 1 kV. SMEs usually are connected to LV levels.
        - Low voltage substation (LV-Sub) - connected to a substation with a supply point voltage level below 1 kV.
        - High voltage (HV) - voltage level of at least 1kV and less than 22kV. (London Power Networks, 2011)

    - DNO Regions Numbers
        - 10 - Eastern England
        - 11 - East Midlands
        - 12 - London
        - 13 - North Wales & Mersey
        - 14 - Midlands
        - 15 - North East
        - 16 - North West
        - 17 - Northern Scotland
        - 18 - Southern Scotland
        - 19 - South East
        - 20 - Southern
        - 21 - South Wales
        - 22 - South Western
        - 23 - Yorkshire

    Rate limit or maximum length period are not specified. However the call may fail if time period is too long. 
    Therefore an arbitrary maximum shall be specified (i.e., 14 days) to facilitate healthy responses from the server.
     
    
    Args:
        config (dict): _description_

    Raises:
        Exception: _description_

    Returns:
        _type_: _description_
    """
    headers = {"Accept": "application/json"}
    base = "https://odegdcpnma.execute-api.eu-west-2.amazonaws.com/development/prices"
    default_job = {'dno':21,'voltage':'HV', 'start':'01-06-2021', 'end':datetime.now().strftime("%d-%m-%Y"),}
    job = {k : config.get(k) or default_job.get(k)  for k in default_job.keys()}
    r = requests.get(base, params=job, headers = headers)
    if r.status_code == 200:
        return r.json()
    else:
        raise Exception(f"Extraction failed with code: ${r.status_code}")

def costs_transform(raw_data):
    dnoRegion = raw_data['data']['dnoRegion']
    dnoRegionName = dno_map[dnoRegion]
    voltageLevel = raw_data['data']['voltageLevel']
    voltageLevelName = voltage_level_map[voltageLevel]
    df = pd.DataFrame(raw_data['data']['data'])
    df['dnoRegion'] = dnoRegion
    df['dnoRegionName'] = dnoRegionName
    df['voltageLevel'] = voltageLevel
    df['voltageLevelName'] = voltageLevelName
    return df
