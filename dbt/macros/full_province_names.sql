 {#
    This macro returns the the full name of the provinces and territories 
#}

{% macro full_province_names(province) -%}

    case {{ province }}
        when 'NWT' then 'Northwest Territories'
        when 'NL' then 'Newfoundland and Labrador'
        when 'PEI' then 'Prince Edward Island'
        when 'BC' then 'British Columbia'
        else {{ province }}
    end

{%- endmacro %}