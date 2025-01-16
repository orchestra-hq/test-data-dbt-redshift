{{ config(
  materialized='table',
  file_format='delta'
) }}

select


C_CUSTKEY as CUSTKEY,
C_NAME as NAME,
C_ADDRESS as ADDRESS,
C_NATIONKEY as NATIONKEY,
C_PHONE as PHONE,
C_ACCTBAL as ACCTBAL,
C_MKTSEGMENT as MKTSEGMENT,
C_COMMENT as COMMENT

from {{ref('customers')}} a 