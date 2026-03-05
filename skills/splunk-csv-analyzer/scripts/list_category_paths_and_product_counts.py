#!/usr/bin/env python3
"""
List all category paths and product counts for each query execution.
- Category path: from ProductQueryResolver "Entry: Received request" with filter attribute categoryPath, eq value.
- Product count: from QueryGrpcService line with same trace_id.
Usage: list_category_paths_and_product_counts.py [path/to/splunk.logs.csv]
       Default CSV path: splunk.logs.csv in current directory.
"""
import re
import sys

TRACE_ID_RE = re.compile(r'trace_id[^\w]{0,20}([a-f0-9]{32})')
# In CSV, "" is escaped quote. After categoryPath we have ""in"":null,""eq"":""<path>""
CATEGORY_PATH_RE = re.compile(r'categoryPath.*?""eq"":""([^"]+)""')
PRODUCT_COUNT_RE = re.compile(r'productCount[=:](\d+)')

def main():
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "splunk.logs.csv"

    # Pass 1: ProductQueryResolver + categoryPath -> trace_id -> category_path
    trace_to_path = {}
    with open(csv_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            if "ProductQueryResolver" not in line or "categoryPath" not in line:
                continue
            tm = TRACE_ID_RE.search(line)
            cm = CATEGORY_PATH_RE.search(line)
            if tm and cm:
                tid = tm.group(1)
                path = cm.group(1).strip()
                if path and (tid not in trace_to_path or not trace_to_path[tid]):
                    trace_to_path[tid] = path

    # Pass 2: QueryGrpcService -> trace_id -> product_count
    trace_to_count = {}
    with open(csv_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            if "QueryGrpcService" not in line or "productCount" not in line:
                continue
            tm = TRACE_ID_RE.search(line)
            pm = PRODUCT_COUNT_RE.search(line)
            if tm and pm:
                trace_to_count[tm.group(1)] = int(pm.group(1))

    # Build list: (category_path, product_count) for traces that have both
    results = []
    for tid, path in trace_to_path.items():
        count = trace_to_count.get(tid)
        if count is not None:
            results.append((path, count, tid))

    # Sort by category_path then product_count for readability
    results.sort(key=lambda x: (x[0], -x[1]))

    # Output as table
    print("category_path,product_count,trace_id")
    for path, count, tid in results:
        # Escape path for CSV if it contains comma
        path_escaped = f'"{path}"' if "," in path else path
        print(f"{path_escaped},{count},{tid}")

    print(f"\n# Total: {len(results)} query executions with category path and product count", file=sys.stderr)
    if results:
        zeros = sum(1 for _, c, _ in results if c == 0)
        print(f"# product_count=0: {zeros}, product_count>0: {len(results)-zeros}", file=sys.stderr)

if __name__ == "__main__":
    main()
