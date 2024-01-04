{{
    config(
        materialized='incremental'
    )
}}

SELECT DISTINCT
    id,
    overall,
    unix_timestamp,
    dno_region,
    dno_region_name,
    voltage_level,
    voltage_level_name,
    pennies_per_kwh,
    date

FROM {{ ref('python_extractor__sources.costs') }}


{% if is_incremental() %}
-- this filter will only be applied on an incremental run
where unix_timestamp > (select max(unix_timestamp) from {{ this }})
{% endif %}