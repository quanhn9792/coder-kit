# SQL & Spark patterns

## Dedupe latest record per key
```sql
select * from (
  select *, row_number() over (partition by id order by updated_at desc, _ingested_at desc) as rn
  from staging.events
) where rn = 1
```

## Idempotent incremental load (MERGE)
```sql
merge into mart.orders t
using (select * from staging.orders where _date = @run_date) s
on t.order_id = s.order_id
when matched then update set *
when not matched then insert *
```

## Fan-out check
```sql
select count(*) as before_join from a;
select count(*) as after_join, count(distinct a.id) as distinct_ids from a left join b on a.k = b.k;
-- after_join must equal before_join when b is supposed to be 1:1
```

## SCD Type 2 columns
`valid_from`, `valid_to` (null = current), `is_current`, plus a hash of tracked columns to detect change.

## PySpark: broadcast + controlled write
```python
from pyspark.sql import functions as F
df = facts.join(F.broadcast(dim), "dim_id", "left")
(df.repartition("event_date")
   .write.mode("overwrite")
   .option("partitionOverwriteMode", "dynamic")
   .partitionBy("event_date")
   .parquet(path))
```

## NULL traps
- `x NOT IN (subquery)` returns no rows if the subquery contains NULL → use `NOT EXISTS`.
- `NULL = NULL` is not true → use `IS NOT DISTINCT FROM` / null-safe `<=>`.
