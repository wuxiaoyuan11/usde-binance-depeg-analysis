# USDe Binance Depeg: On-chain Price Stability and Liquidity Response

This project studies the Oct 10-11, 2025 USDe Binance depeg event from an on-chain market risk perspective. Using Dune SQL and Python, it compares Binance's reported USDe dislocation with Ethereum DEX price behavior, trading volume, net sell pressure, and large-wallet activity.

**Dashboard:** https://dune.com/jessicahuan/usde-binance-depeg-on-chain-price-stability-and-liquidity-response

## Related Links

- Dune dashboard: https://dune.com/jessicahuan/usde-binance-depeg-on-chain-price-stability-and-liquidity-response
- Research memo: [reports/research_memo.md](reports/research_memo.md)
- Dune SQL queries: [dune_queries.md](dune_queries.md)

## Key Takeaway

The Binance USDe depeg appears more consistent with venue-specific liquidity and pricing dislocation than a broad on-chain stablecoin run. Ethereum DEX prices stayed close to peg, trading activity spiked, and large-wallet flows were concentrated but two-sided.

## Research Question

Did the USDe Binance depeg reflect a broad on-chain stablecoin run, or was it mainly a venue-specific dislocation?

## Methodology

The analysis uses an event-study framework around Oct 10-11, 2025:

- Price stability: USDe DEX price measured against USDT, USDC, and DAI
- Trading activity: daily USDe DEX volume and volume versus trailing 7-day average
- Flow direction: USDe buy/sell volume and daily net sell pressure
- Large-wallet behavior: top net buyers/sellers and wallet concentration during the core event window

## Initial Findings

- USDe remained close to peg on Ethereum DEX venues: the minimum median DEX price observed was `0.997641` at `2025-10-10 23:00 UTC`, only about `0.236%` below 1 USD.
- Daily USDe DEX trading volume reached `$571.89m` on Oct 11, around `3.0x` the trailing 7-day average, showing elevated market activity even though on-chain prices stayed near peg.
- USDe net sell pressure was positive on Oct 10 (`$34.67m`) but turned negative on Oct 11 (`-$19.16m`), suggesting that DEX markets did not show persistent one-way panic selling.
- During the core event window, USDe saw `$514.18m` bought and `$528.62m` sold, with only `-$14.44m` net flow. Top 10 buyers represented `50.0%` of buying volume, while top 10 sellers represented `37.7%` of selling volume.

## Interpretation

The data suggests that the USDe stress episode was not a broad on-chain stablecoin collapse. Instead, the event showed:

- Limited DEX price deviation despite the Binance dislocation
- A sharp but temporary trading activity spike
- Two-sided flow rather than persistent USDe selling
- Concentrated large-wallet participation, consistent with arbitrage or market-maker rebalancing

This framing is relevant for exchanges, market makers, DeFi protocols, and digital asset risk teams monitoring venue-specific liquidity and oracle risk.

## Data Sources

- Dune `dex.trades`: Ethereum DEX trades involving USDe, USDT, USDC, and DAI
- CoinGecko: off-chain stablecoin market data for cross-checking price behavior
- DeFiLlama-style market risk framing: TVL, protocol exposure, and stablecoin risk context
- Public event coverage and Ethena/Binance-related market commentary

## Dune Queries

- USDe hourly DEX price: https://dune.com/queries/7468714/
- USDe buy vs sell volume: https://dune.com/queries/7476256/
- USDe net sell pressure: https://dune.com/queries/7476285/
- USDe daily DEX volume: https://dune.com/queries/7476326/
- Top USDe buyers and sellers: https://dune.com/queries/7476429/
- Large wallet flow summary: https://dune.com/queries/7476531/

## Skills Demonstrated

- On-chain data analysis with Dune SQL
- Stablecoin and DeFi market risk analysis
- Event-window research design
- Wallet-level flow interpretation
- Dashboard storytelling for digital asset research
- Translating raw blockchain data into exchange / market-maker risk insights

## Project Structure

```text
usde-depeg-analysis/
  README.md
  dune_queries.md
  reports/
    research_memo.md
  scripts/
    fetch_coingecko.py
    analyze_event.py
  data/
    processed/
```
