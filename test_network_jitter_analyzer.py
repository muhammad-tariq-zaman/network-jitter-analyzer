import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import analyse

def row(host, ts, latency):
    return {"host": host, "timestamp": ts, "latency_ms": str(latency)}

class TestJitterAnalyzer(unittest.TestCase):
    def test_jitter_mean_absolute_diff(self):
        r = analyse([row("h1", "2026-11-09T09:00:00", 10),
                     row("h1", "2026-11-09T09:01:00", 20),
                     row("h1", "2026-11-09T09:02:00", 30)])
        self.assertEqual(r[0][4], 10.0)
    def test_stable(self):
        r = analyse([row("h1", "2026-11-09T09:00:00", 50),
                     row("h1", "2026-11-09T09:01:00", 52),
                     row("h1", "2026-11-09T09:02:00", 48)])
        self.assertEqual(r[0][5], "STABLE")
    def test_unstable(self):
        r = analyse([row("h1", "2026-11-09T09:00:00", 10),
                     row("h1", "2026-11-09T09:01:00", 100)])
        self.assertEqual(r[0][5], "UNSTABLE")
    def test_single_sample_jitter_zero(self):
        r = analyse([row("h1", "2026-11-09T09:00:00", 42)])
        self.assertEqual((r[0][4], r[0][5]), (0.0, "STABLE"))
    def test_samples_sorted_by_timestamp(self):
        r = analyse([row("h1", "2026-11-09T09:02:00", 30),
                     row("h1", "2026-11-09T09:00:00", 10),
                     row("h1", "2026-11-09T09:01:00", 20)])
        self.assertEqual(r[0][4], 10.0)
    def test_avg_and_max(self):
        r = analyse([row("h1", "2026-11-09T09:00:00", 10),
                     row("h1", "2026-11-09T09:01:00", 30)])
        self.assertEqual((r[0][2], r[0][3]), (20.0, 30))
    def test_worst_jitter_first(self):
        r = analyse([row("a", "2026-11-09T09:00:00", 10),
                     row("a", "2026-11-09T09:01:00", 12),
                     row("b", "2026-11-09T09:00:00", 10),
                     row("b", "2026-11-09T09:01:00", 100)])
        self.assertEqual(r[0][0], "b")
    def test_empty_input(self):
        self.assertEqual(analyse([]), [])
