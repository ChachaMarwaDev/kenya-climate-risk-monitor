with dlt_counties as (
    select * from {{ source('kenya_weather', 'dim_counties') }}
),

seed_counties as (
    select * from {{ ref('kenya_counties') }}
),

joined as (
    select
        d.county_id,
        d.county,
        d.latitude,
        d.longitude,
        s.agro_zone,       -- ← from seed
        s.lat_min,         -- ← bounding box from seed
        s.lat_max,
        s.lon_min,
        s.lon_max

    from dlt_counties d
    left join seed_counties s on lower(trim(d.county)) = lower(trim(s.county))
)

select * from joined

