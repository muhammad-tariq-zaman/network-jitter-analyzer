# network-jitter-analyzer

Analyse network jitter from a CSV of latency samples per host: jitter is the mean of the absolute differences between consecutive samples — STABLE under 10 ms, MODERATE under 30 ms, UNSTABLE at 30 ms or more, worst jitter first.

## How to run

```sh
python3 main.py latency.csv
```

## Example output

```
router-2: UNSTABLE (jitter 90.00 ms, avg latency 55.00 ms, max 100 ms, 2 sample(s))
router-1: STABLE (jitter 3.00 ms, avg latency 50.00 ms, max 52 ms, 3 sample(s))
1 host(s) unstable.
```

Standard library only. Run the tests with `python3 -m unittest discover`.
