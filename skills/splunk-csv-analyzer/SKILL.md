---
name: splunk-csv-analyzer
description: Analyzes Splunk logs exported as CSV from internal Adobe Commerce SaaS services. Use proactively when the user has splunk CSV exports, needs category/productCount or trace_id analysis, or asks to analyze Splunk logs. Incorporates and runs scripts in the skill's scripts/ directory.
---

# Splunk CSV analyzer

Analyze Splunk log exports (CSV) from **internal Adobe Commerce SaaS** (search-service, product recommendations, Live Search). Logs are internal only; do not suggest sharing raw logs or PII with customers.

## Log format

- **Columns**: `_serial`, `_time`, `source`, `sourcetype`, `host`, `index`, `splunk_server`, `_raw`.
- **`_raw`**: JSON with `message` (timestamp, logger_name, message, trace_id 32-char hex, level) and context (namespace, pod_name, service_name, etc.). In CSV, quotes are escaped as `""`.

**Key fields**: `trace_id` (correlate across lines), `logger_name` (e.g. ProductQueryResolver, QueryGrpcService, ElasticsearchQueryDao, MetaIndexClient), `categoryPath` in filter `""eq"":""<path>""`, `productCount`, and errors (`level":"ERROR"`, UNAVAILABLE, no healthy upstream).

## Scripts (skill folder)

Run from the **project directory** that contains the Splunk CSV (or pass CSV path as first argument).

**list_category_paths_and_product_counts.py** — Joins category path (ProductQueryResolver + categoryPath) with product count (QueryGrpcService) by trace_id.

```bash
python3 ~/.cursor/skills/splunk-csv-analyzer/scripts/list_category_paths_and_product_counts.py [path/to/splunk.logs.csv]
```

Output: CSV table `category_path,product_count,trace_id` and stderr summary (totals, product_count=0 vs >0). Omit path to use `splunk.logs.csv` in current directory.

**extract_category_traces.py** — Finds trace_ids from ElasticsearchQueryDao + categoryPath, then productCount per trace.

```bash
python3 ~/.cursor/skills/splunk-csv-analyzer/scripts/extract_category_traces.py [path/to/splunk.logs.csv]
```

Output: trace_id → productCount list and summary (min/max/avg, counts with 0 vs >0). Omit path to use `splunk.logs.csv` in current directory.

## Workflow

1. **Clarify goal**: category empty results, productCount=0, errors (MetaIndexClient, UNAVAILABLE), trace correlation, or exploration.
2. **Choose approach**:
   - Category path + product count by request → run `list_category_paths_and_product_counts.py`.
   - ES categoryPath traces and productCount → run `extract_category_traces.py`.
   - Errors or ad-hoc patterns → use `grep`/`rg` or line-by-line Python (stream; avoid loading full file). Remember `""` in _raw.
3. **Run and interpret**: Execute script/commands; summarize (e.g. “X of Y category queries had product_count=0”).
4. **Report**: Short summary, key numbers, next steps (e.g. DSRS escalation if backend/unhealthy upstream).

## Ad-hoc patterns

- **trace_id**: `trace_id[^\w]{0,20}([a-f0-9]{32})`
- **categoryPath**: `categoryPath.*?""eq"":""([^"]+)""`
- **productCount**: `productCount[=:](\d+)`
- **Errors**: Search _raw for `"level":"ERROR"`, `UNAVAILABLE`, `no healthy upstream`, `MetaIndexClient`.

Prefer running the skill scripts when they match the question; use grep/Python only when needed.
