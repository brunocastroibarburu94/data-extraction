{{ config(materialized='view') }}

SELECT 

-- Original fields
Overall           as overall,
unixTimestamp     as unix_timestamp,
Timestamp         as timestamp,
dnoRegion         as dno_region,
dnoRegionName     as dno_region_name,
voltageLevel      as voltage_level,
voltageLevelName  as voltage_level_name,

-- Parsed original fields
overall as pennies_per_kwh,
datetime(unixTimestamp, 'unixepoch', 'utc') as date,

cast(unixTimestamp as text)  || '__' ||
cast(dnoRegion as text)  || '__' ||
cast(voltageLevel as text)  as id --Unique Identifier for record

FROM {{ get_source(this.name) }}