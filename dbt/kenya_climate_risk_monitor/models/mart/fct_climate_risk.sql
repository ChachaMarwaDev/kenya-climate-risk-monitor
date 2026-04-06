with daily_weather as (
    select * from {{ ref('stg_daily_weather') }}
),

counties as (
    select * from {{ ref('stg_counties') }}
),

agro_zones as (
    select * from {{ ref('dim_agro_zones') }}
),

thresholds as (
    select * from {{ ref('dim_thresholds') }}
),

-- Selected distinct to avoid single date duplicates that match multiple seasons in the rainy_seasons table
rainy_seasons as (
    select distinct
        agro_zone,
        start_month,
        end_month,
        season_type,
        season_name
    from {{ ref('rainy_seasons') }}
)

select
    dw.weather_date,
    dw.county,
    dw.rainfall_mm,
    dw.temp_max_c,
    dw.temp_min_c,
    dw.evapotranspiration_mm,
    c.agro_zone,
    az.zone_description,       
    t.drought_threshold_mm,       
    t.flood_7day_mm,
    t.critical_soil_moisture,
    rs.season_name,
    rs.season_type,

-- Case failed test so coalesce replaces any null result with false
-- Drought flag: true if rainfall_mm < drought_threshold_mm, else false
coalesce(dw.rainfall_mm < t.drought_threshold_mm, false) as is_drought_risk,

-- Flood flag: true if rainfall_mm > flood_7day_mm, else false
coalesce(dw.rainfall_mm > t.flood_7day_mm, false)        as is_flood_risk,


-- Rainy season flag: true if season_type is 'wet', else false
    case
        when rs.season_type = 'wet' then true
        else false
    end as is_rainy_season

from daily_weather dw
left join counties          c  on dw.county   = c.county
left join agro_zones        az on c.agro_zone = az.agro_zone
left join thresholds        t  on c.agro_zone = t.agro_zone
left join rainy_seasons     rs on c.agro_zone = rs.agro_zone
    and extract(month from dw.weather_date) between rs.start_month and rs.end_month