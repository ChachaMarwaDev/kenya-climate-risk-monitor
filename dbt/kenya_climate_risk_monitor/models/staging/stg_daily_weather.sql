-- models/staging/stg_daily_weather.sql
with source as (

    select * from {{ source('raw_weather', 'daily_weather') }}

),

renamed as (

    select
        cast(date as date)                      as weather_date,
        county,
        cast(latitude as float64)               as latitude,
        cast(longitude as float64)              as longitude,
        cast(rainfall_mm as float64)            as rainfall_mm,
        cast(temp_max_c as float64)             as temp_max_c,
        cast(temp_min_c as float64)             as temp_min_c,
        cast(temp_avg_c as float64)             as temp_avg_c,
        cast(evapotranspiration_mm as float64)  as evapotranspiration_mm,
        cast(wind_speed_kmh as float64)         as wind_speed_kmh,
        data_source

    from source

)

select * from renamed