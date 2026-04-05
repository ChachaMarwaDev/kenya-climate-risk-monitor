with source as (

    select * from {{ source('kenya_weather', 'dim_counties') }}

),

renamed as (

    select
        county,
        county_id,
        cast(latitude as float64)               as latitude,
        cast(longitude as float64)              as longitude,

    from source

)

select * from renamed