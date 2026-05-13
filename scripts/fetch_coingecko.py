"""Fetch CoinGecko market data for USDe, USDT, and USDC.

Run after confirming the exact event window:
    python scripts/fetch_coingecko.py --from-date 2025-10-01 --to-date 2025-10-20
"""

from __future__ import annotations

import argparse
import csv
import json
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


COINS = {
    "usde": "ethena-usde",
    "usdt": "tether",
    "usdc": "usd-coin",
}


def to_unix(date_str: str) -> int:
    dt = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    return int(dt.timestamp())


def fetch_market_chart(coin_id: str, start_ts: int, end_ts: int) -> dict:
    params = urllib.parse.urlencode({
        "vs_currency": "usd",
        "from": start_ts,
        "to": end_ts,
    })
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart/range?{params}"
    with urllib.request.urlopen(url, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def write_coin_csv(symbol: str, data: dict, output_dir: Path) -> None:
    output_path = output_dir / f"{symbol}_market_chart.csv"
    rows = []
    for metric, values in data.items():
        if metric not in {"prices", "market_caps", "total_volumes"}:
            continue
        for ts_ms, value in values:
            rows.append({
                "symbol": symbol,
                "metric": metric,
                "timestamp": datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc).isoformat(),
                "value": value,
            })

    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["symbol", "metric", "timestamp", "value"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--from-date", required=True, help="UTC start date, YYYY-MM-DD")
    parser.add_argument("--to-date", required=True, help="UTC end date, YYYY-MM-DD")
    parser.add_argument("--output-dir", default="data/raw")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    start_ts = to_unix(args.from_date)
    end_ts = to_unix(args.to_date)

    for symbol, coin_id in COINS.items():
        data = fetch_market_chart(coin_id, start_ts, end_ts)
        write_coin_csv(symbol, data, output_dir)
        time.sleep(3)


if __name__ == "__main__":
    main()

