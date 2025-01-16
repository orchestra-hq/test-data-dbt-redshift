{{ config(
  materialized='table',
  file_format='delta'
) }}

select

    a.*,
    b.NAME as customer_NAME,
    b.ADDRESS as customer_ADDRESS,
    b.NATIONKEY as customer_NATIONKEY,
    b.PHONE as customer_PHONE,
    b.ACCTBAL as customer_ACCTBAL,
    b.MKTSEGMENT as customer_MKTSEGMENT,
    b.COMMENT as customer_COMMENT

from
{{ref('stg_orderlines')}} a 
left join {{ref('stg_customers')}} b 
on a.custkey = b.custkey