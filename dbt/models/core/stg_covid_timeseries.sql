{{ config(
  materialized='table',
  cluster_by=['province'],
  partition_by = {
  "field": "date",
  "data_type": "date",
  }
) }}


with covid_data as
(
  select 
    *,
    -- setting string 'NULL' to null
    nullif(avaccine, 'NULL') as avaccine_null,
    nullif(cumulative_avaccine, 'NULL') as cumulative_avaccine_null,
    nullif(cumulative_cvaccine, 'NULL') as cumulative_cvaccine_null,
    nullif(cumulative_dvaccine, 'NULL') as cumulative_dvaccine_null,
    nullif(cumulative_deaths, 'NULL') as cumulative_deaths_null,
    nullif(cumulative_testing, 'NULL') as cumulative_testing_null,
    nullif(cumulative_recovered, 'NULL') as cumulative_recovered_null,
    nullif(dvaccine, 'NULL') as dvaccine_null,
    nullif(deaths, 'NULL') as deaths_null,
    nullif(cvaccine, 'NULL') as cvaccine_null,
    nullif(recovered, 'NULL') as recovered_null,
    nullif(testing, 'NULL') as testing_null,
    nullif(testing_info, 'NULL') as testing_info_null,
    -- setting province acronyms to full names
    {{ full_province_names('province') }} as province_full,
    -- convert date field from string to date type
    PARSE_DATE('%d-%m-%Y', date) as formatted_date
  from {{ source('core','covid_CA_raw') }}
  where date is not null 
)
select
    cast(active_cases as integer) as active_cases,
    cast(active_cases_change as integer) as active_cases_change,
    cast(avaccine_null as float64) as avaccine,
    cast(cases as integer) as cases,
    cast(cumulative_avaccine_null as float64) as cumulative_avaccine,
    cast(cumulative_cases as integer) as cumulative_cases,
    cast(cumulative_cvaccine_null as float64) as cumulative_cvaccine,
    cast(cumulative_deaths_null as float64) as cumulative_deaths,
    cast(cumulative_dvaccine_null as float64) as cumulative_dvaccine,
    cast(cumulative_recovered_null as float64) as cumulative_recovered,
    cast(cumulative_testing_null as float64) as cumulative_testing,
    cast(cvaccine_null as float64) as cvaccine,
    cast(formatted_date as date) as date,
    cast(deaths_null as float64) as deaths,
    cast(dvaccine_null as float64) as dvaccine,
    cast(province_full as string) as province,
    cast(recovered_null as float64) as recovered,
    cast(testing_null as float64) as testing,
    cast(testing_info_null as string) as testing_info
from covid_data

