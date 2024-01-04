{% macro import(src_name) 
-%}{{ src_name }} AS (SELECT * FROM {{ ref(src_name) }}){%-
endmacro %}