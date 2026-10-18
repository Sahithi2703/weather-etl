import sys
sys.path.insert(0, "src")

from extract import flatten


def test_flatten_returns_one_row_per_hour():
    payload = {
        "hourly": {
            "time": ["2026-10-17T00:00", "2026-10-17T01:00"],
            "temperature_2m": [22.4, 21.9],
            "relative_humidity_2m": [88, 90],
            "precipitation": [0.0, 0.2],
        }
    }
    rows = flatten("Hyderabad", payload)

    assert len(rows) == 2
    assert rows[0] == {
        "city": "Hyderabad",
        "ts": "2026-10-17T00:00",
        "temp_c": 22.4,
        "humidity": 88,
        "precip_mm": 0.0,
    }