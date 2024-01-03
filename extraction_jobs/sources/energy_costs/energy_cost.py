
# Example
import requests

# Maximum is 14 days at a time
# This parameterized job takes data from https://electricitycosts.org.uk/api/ and drops into a Postgres database

def extract_energy_cost(start:str,end:str,dno:int=10,voltage:str='HV'): 
    headers ={'Accept': 'application/json'}
    r = requests.get(f'https://odegdcpnma.execute-api.eu-west-2.amazonaws.com/development/prices?dno={dno}&voltage=HV&start={start}&end={end}', params={}, headers = headers)
    return r.json()