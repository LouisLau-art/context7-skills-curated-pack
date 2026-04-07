from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import fetch_skills_sh_rankings as rankings


class _FakeResponse:
    def __init__(self, body: str) -> None:
        self._body = body.encode("utf-8")

    def __enter__(self) -> "_FakeResponse":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        return None

    def read(self) -> bytes:
        return self._body


class FetchApiPageRetryTests(unittest.TestCase):
    def test_fetch_api_page_retries_after_timeout(self) -> None:
        payload = {"skills": [{"name": "demo"}], "hasMore": False}
        calls = {"count": 0}

        def flaky_urlopen(_req, timeout=30):
            calls["count"] += 1
            if calls["count"] < 3:
                raise TimeoutError("timed out")
            return _FakeResponse(json.dumps(payload))

        with patch.object(rankings, "urlopen", side_effect=flaky_urlopen):
            result = rankings.fetch_api_page("https://skills.sh", "all-time", 1)

        self.assertEqual(result, payload)
        self.assertEqual(calls["count"], 3)


class KeepStaleSnapshotTests(unittest.TestCase):
    def test_main_keeps_existing_snapshot_when_fetch_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            out_json = root / "skills.json"
            out_csv = root / "skills.csv"
            old_json = {"generatedAtUtc": "2026-04-01T00:00:00+00:00", "items": []}
            old_csv = "rank,name\n1,existing\n"
            out_json.write_text(json.dumps(old_json), encoding="utf-8")
            out_csv.write_text(old_csv, encoding="utf-8")

            argv = [
                "fetch_skills_sh_rankings.py",
                "--output-json",
                str(out_json),
                "--output-csv",
                str(out_csv),
                "--keep-stale-on-error",
            ]
            with patch.object(sys, "argv", argv):
                with patch.object(rankings, "fetch_html", side_effect=TimeoutError("timed out")):
                    rc = rankings.main()

            self.assertEqual(rc, 0)
            self.assertEqual(json.loads(out_json.read_text(encoding="utf-8")), old_json)
            self.assertEqual(out_csv.read_text(encoding="utf-8"), old_csv)


if __name__ == "__main__":
    unittest.main()
