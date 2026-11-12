"""Analyse network jitter from latency samples per host.

Usage: python3 main.py latency.csv
CSV columns: host,timestamp,latency_ms.
Jitter = the mean of the absolute differences between consecutive
latency samples for a host (in timestamp order).
- STABLE: jitter under 10 ms.
- MODERATE: jitter under 30 ms.
- UNSTABLE: jitter 30 ms or more.
A host with one sample has jitter 0.0. Worst jitter first.
"""
import argparse, csv, sys
from collections import defaultdict

def analyse(rows):
    per_host = defaultdict(list)
    for row in rows:
        per_host[row["host"].strip()].append(
            (row["timestamp"].strip(), int(row["latency_ms"])))
    out = []
    for host in sorted(per_host):
        samples = sorted(per_host[host])
        latencies = [latency for _, latency in samples]
        diffs = [abs(b - a) for a, b in zip(latencies, latencies[1:])]
        jitter = round(sum(diffs) / len(diffs), 2) if diffs else 0.0
        avg = round(sum(latencies) / len(latencies), 2)
        worst = max(latencies)
        if jitter < 10:
            verdict = "STABLE"
        elif jitter < 30:
            verdict = "MODERATE"
        else:
            verdict = "UNSTABLE"
        out.append((host, len(latencies), avg, worst, jitter, verdict))
    return sorted(out, key=lambda r: (-r[4], r[0]))

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    args = parser.parse_args(argv)
    with open(args.path, newline="", encoding="utf-8") as f:
        results = analyse(list(csv.DictReader(f)))
    for host, count, avg, worst, jitter, verdict in results:
        print(f"{host}: {verdict} (jitter {jitter:.2f} ms, avg latency {avg:.2f} ms, "
              f"max {worst} ms, {count} sample(s))")
    print(f"{sum(1 for *_, v in results if v == 'UNSTABLE')} host(s) unstable.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
