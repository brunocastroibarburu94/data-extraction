{% macro get_source(filename=none) -%}{%
    set split_name = filename.split('__') %}{%
    set src_name = split_name[0] %}{% 
    set table_name = split_name[1] %}{{
    source(src_name, table_name) }}{%- 
    endmacro %}

