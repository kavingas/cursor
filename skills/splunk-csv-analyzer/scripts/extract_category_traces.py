#!/usr/bin/env python3
"""Extract trace_ids from ES queries with categoryPath and get productCount from related log entries.
Usage: extract_category_traces.py [path/to/splunk.logs.csv]
       Default CSV path: splunk.logs.csv in current directory.
"""
import re
import sys

def main():
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "splunk.logs.csv"

    # trace_id in CSV _raw: ""trace_id"":""xxxxxxxx"" (doubled quotes when in CSV)
    trace_id_re = re.compile(r'trace_id[^\w]{0,20}([a-f0-9]{32})')
    product_count_re = re.compile(r'productCount[=:](\d+)')

    # First pass: get trace_ids from ElasticsearchQueryDao + categoryPath lines
    category_trace_ids = set()
    with open(csv_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            if "ElasticsearchQueryDao" in line and "categoryPath" in line:
                m = trace_id_re.search(line)
                if m:
                    category_trace_ids.add(m.group(1))

    print(f"Found {len(category_trace_ids)} unique trace_ids from ElasticsearchQueryDao + categoryPath", file=sys.stderr)

    # Second pass: for each trace_id, find productCount in any line with that trace_id
    trace_to_product_count = {}
    trace_log_messages = {tid: [] for tid in category_trace_ids}

    with open(csv_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            for tid in category_trace_ids:
                if tid in line:
                    mc = product_count_re.search(line)
                    if mc and tid not in trace_to_product_count:
                        trace_to_product_count[tid] = int(mc.group(1))
                    # Capture logger and message snippet for first occurrence
                    if len(trace_log_messages[tid]) < 5:
                        if "logger_name" in line:
                            logger = "logger_name"
                        else:
                            logger = "raw"
                        msg = line[:200] if len(line) > 200 else line
                        trace_log_messages[tid].append((logger, msg[:150]))
                    break

    # Output: trace_id -> productCount (and sample messages)
    print("\n=== Trace IDs with categoryPath (ES query) and their productCount ===\n")
    for tid in sorted(category_trace_ids):
        count = trace_to_product_count.get(tid, "N/A")
        print(f"trace_id: {tid}  ->  productCount: {count}")

    # Summary stats for categoryPath queries
    counts = [trace_to_product_count[tid] for tid in category_trace_ids if tid in trace_to_product_count]
    if counts:
        print(f"\n=== Summary (categoryPath ES queries) ===")
        print(f"Traces with productCount: {len(counts)}")
        print(f"productCount=0: {sum(1 for c in counts if c == 0)}")
        print(f"productCount>0: {sum(1 for c in counts if c > 0)}")
        print(f"Min: {min(counts)}, Max: {max(counts)}, Avg: {sum(counts)/len(counts):.1f}")

if __name__ == "__main__":
    main()
