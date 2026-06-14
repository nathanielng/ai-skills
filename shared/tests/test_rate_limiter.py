import json
import tempfile
import time
from pathlib import Path
from unittest.mock import patch
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from gws_common import RateLimiter


def test_rate_limiter_increments():
    """Test that rate limiter increments counter."""
    with tempfile.TemporaryDirectory() as tmpdir:
        rate_file = Path(tmpdir) / "rate.json"

        with patch('gws_common.RATE_FILE', rate_file):
            limiter = RateLimiter(calls_per_min=5)

            for i in range(1, 6):
                limiter.check()
                state = json.loads(rate_file.read_text())
                assert state["calls"] == i


def test_rate_limiter_exceeds():
    """Test that rate limiter raises SystemExit when limit exceeded."""
    with tempfile.TemporaryDirectory() as tmpdir:
        rate_file = Path(tmpdir) / "rate.json"

        with patch('gws_common.RATE_FILE', rate_file):
            limiter = RateLimiter(calls_per_min=3)

            # Make 3 calls
            for _ in range(3):
                limiter.check()

            # 4th call should raise SystemExit
            try:
                limiter.check()
                assert False, "Expected SystemExit"
            except SystemExit as e:
                assert "Rate limit exceeded" in str(e)


def test_rate_limiter_resets_after_window():
    """Test that rate limiter resets after time window."""
    with tempfile.TemporaryDirectory() as tmpdir:
        rate_file = Path(tmpdir) / "rate.json"

        with patch('gws_common.RATE_FILE', rate_file):
            limiter = RateLimiter(calls_per_min=2)

            # First window
            limiter.check()
            limiter.check()

            # Mock the window_start to be > 60 seconds ago
            state = json.loads(rate_file.read_text())
            state["window_start"] = time.time() - 61
            rate_file.write_text(json.dumps(state))

            # Should not raise - window reset
            limiter.check()
            state = json.loads(rate_file.read_text())
            assert state["calls"] == 1
