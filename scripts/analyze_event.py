"""Analyze stablecoin price behavior around the USDe depeg event.

This script expects CoinGecko CSV files created by fetch_coingecko.py.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path


def read_prices(data_dir: Path) -> dict[str, list[tuple[datetime, float]]]:
    prices: dict[str, list[tuple[datetime, float]]] = defaultdict(list)
    for path in data_dir.glob("*_market_chart.csv"):
        with path.open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["metric"] != "prices":
                    continue
                prices[row["symbol"]].append((
                    datetime.fromisoformat(row["timestamp"]),
                    float(row["value"]),
                ))
    return prices


def summarize_price_deviation(prices: dict[str, list[tuple[datetime, float]]]) -> list[dict[str, str]]:
    summary = []
    for symbol, observations in prices.items():
        if not observations:
            continue
        values = [value for _, value in observations]
        min_price = min(values)
        max_price = max(values)
        avg_price = sum(values) / len(values)
        max_abs_deviation = max(abs(value - 1.0) for value in values)
        summary.append({
            "symbol": symbol,
            "observations": str(len(values)),
            "min_price": f"{min_price:.6f}",
            "max_price": f"{max_price:.6f}",
            "avg_price": f"{avg_price:.6f}",
            "max_abs_deviation_from_1": f"{max_abs_deviation:.6f}",
        })
    return sorted(summary, key=lambda row: row["symbol"])


def write_summary(rows: list[dict[str, str]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "symbol",
        "observations",
        "min_price",
        "max_price",
        "avg_price",
        "max_abs_deviation_from_1",
    ]
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", default="data/raw")
    parser.add_argument("--output", default="data/processed/price_deviation_summary.csv")
    args = parser.parse_args()

    prices = read_prices(Path(args.data_dir))
    rows = summarize_price_deviation(prices)
    write_summary(rows, Path(args.output))

    for row in rows:
        print(row)


if __name__ == "__main__":
    main()

