---
name: data-engineering
description: Data engineering guidance - design, build and review data pipelines, ETL/ELT, SQL, data models, orchestration and data quality. Use when the user works on SQL queries, dbt models, Spark/PySpark jobs, Airflow/Dagster/Prefect DAGs, Kafka/streaming, data warehouses (BigQuery, Snowflake, Redshift, Databricks), schema design, backfills or data quality checks.
---

# Data engineering

Reply in the user's language. Act as a senior data engineer: correctness and idempotency first, then cost and performance.

## Design principles
- **Idempotent & re-runnable** – every job can be re-run for a partition/date and produce the same result (use `MERGE`/upsert or partition overwrite, never blind `INSERT` append for batch).
- **Incremental by default** – process by partition or watermark; support backfill of an arbitrary date range.
- **Layered model** – raw/bronze (immutable, as received) → staging/silver (cleaned, typed, deduped) → marts/gold (business entities, aggregates).
- **Explicit contracts** – schema, grain (one row per …), primary key, freshness SLA documented for each table.
- **Late & duplicate data** – define how late-arriving and duplicate events are handled (dedupe key + latest by event/ingest time).
- **Time** – store UTC; distinguish event time vs processing time.

## SQL standards
- State the grain at the top of each model; assert uniqueness of the key.
- CTEs with clear names over nested subqueries; no `SELECT *` in final models.
- Watch for: join fan-out (check row counts before/after), `NULL` in join keys and `NOT IN`, integer division, implicit casts, timezone conversions, window function frames.
- Filter on partition/cluster columns to limit scanned bytes; avoid functions on partition columns in `WHERE`.
See `references/sql-and-spark.md` for patterns.

## Spark / PySpark
- Prefer DataFrame API / Spark SQL over UDFs; use built-ins.
- Watch shuffles: broadcast small dimension tables, handle skew (salting, AQE), avoid `collect()` and `toPandas()` on large data.
- Control output file count and size (`repartition`/`coalesce` before write); partition by low-cardinality columns used in filters.

## Orchestration
- Tasks small and atomic; retries with backoff; `catchup`/backfill configured deliberately; no business logic in DAG files; parameterize by logical date, not `now()`.

## Data quality (always propose)
Not-null and unique on keys, accepted values, referential integrity, row-count / volume anomaly, freshness. Implement with dbt tests, Great Expectations, Soda or SQL assertions, and fail or alert before bad data reaches marts.

## When reviewing pipelines
Use the `code-review` format, plus check: idempotency, grain/key uniqueness, join fan-out, late data, backfill safety, partition pruning, schema evolution, PII handling, cost.
