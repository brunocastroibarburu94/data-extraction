WITH 
{{ import('sources_costs') }}

SELECT
    id,
    overall,
    unix_timestamp,
    dno_region,
    dno_region_name,
    voltage_level,
    voltage_level_name,
    pennies_per_kwh,
    date
from sources_costs