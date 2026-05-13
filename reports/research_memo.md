# USDe Binance Depeg: On-chain Price Stability and Liquidity Response

## Executive Summary

This memo analyzes the Oct 10-11, 2025 USDe Binance depeg event from an on-chain market risk perspective. The core question is whether the reported Binance dislocation reflected a broad on-chain stablecoin run or a venue-specific liquidity and pricing event.

Ethereum DEX data suggests that the event was not a broad on-chain USDe collapse. USDe remained close to peg on DEX venues, with a minimum observed median DEX price of `0.997641`. However, trading activity increased sharply: daily USDe DEX volume reached `$571.89m` on Oct 11, around `3.0x` the trailing 7-day average. Flow data also shows that initial sell pressure was followed by net buying demand, and large-wallet activity was concentrated but two-sided.

The evidence is more consistent with a venue-specific dislocation than a generalized stablecoin run. This has implications for exchange risk monitoring, market-maker rebalancing, stablecoin due diligence, and venue-level liquidity stress analysis.

## 1. Event Background

USDe is a synthetic dollar product issued by Ethena. During the Oct 10-11, 2025 market stress window, USDe reportedly experienced an extreme price dislocation on Binance. This created an important research question: did the Binance price move represent a system-wide USDe failure, or was the stress concentrated in a specific trading venue?

To answer this, I analyzed Ethereum DEX trading data involving USDe against major stablecoins, including USDT, USDC, and DAI. The analysis focuses on whether DEX prices, trading volume, net sell pressure, and large-wallet flows showed evidence of broad panic selling.

## 2. Methodology

The analysis uses an event-study framework around Oct 10-11, 2025.

Data sources:

- Dune `dex.trades` for Ethereum DEX trades involving USDe, USDT, USDC, and DAI
- CoinGecko market data for off-chain price cross-checking
- Public market commentary around the Binance USDe dislocation

Core metrics:

- USDe DEX price measured against USDT, USDC, and DAI
- Daily USDe DEX trading volume
- Volume versus trailing 7-day average
- Daily USDe buy volume, sell volume, and net sell pressure
- Top USDe net buyers and sellers during the core event window
- Top 10 buyer and seller concentration

Dashboard:

- https://dune.com/jessicahuan/usde-binance-depeg-on-chain-price-stability-and-liquidity-response

## 3. Price Stability

USDe remained close to peg on Ethereum DEX venues during the event window.

Key evidence:

- Minimum median DEX price: `0.997641`
- Timestamp: `2025-10-10 23:00 UTC`
- Approximate maximum deviation from peg: `0.236%`

This contrasts with the reported extreme Binance dislocation. The DEX data therefore does not support the interpretation that USDe experienced a broad on-chain stablecoin collapse. Instead, price stress appears to have been much more severe on Binance than across Ethereum DEX venues.

Dune query:

- https://dune.com/queries/7468714/

## 4. Trading Activity Spike

Although USDe prices stayed close to peg on DEX venues, trading activity rose sharply during the event.

Key evidence:

- Highest daily USDe DEX volume: `$571.89m`
- Date: Oct 11, 2025
- Volume versus trailing 7-day average: `3.0x`

This indicates that market participants actively responded to the Binance dislocation. The event was therefore meaningful for on-chain markets, even though the price impact was limited on Ethereum DEXs.

Dune query:

- https://dune.com/queries/7476326/

## 5. Net Sell Pressure

Flow direction does not show persistent one-way panic selling.

Key evidence:

- Oct 10 net sell pressure: `+$34.67m`
- Oct 11 net sell pressure: `-$19.16m`

A positive value means USDe selling volume exceeded buying volume. A negative value means USDe buying volume exceeded selling volume. The shift from positive sell pressure on Oct 10 to net buying demand on Oct 11 suggests that initial selling pressure was absorbed by buyers, potentially including arbitrageurs or market makers.

Dune queries:

- https://dune.com/queries/7476256/
- https://dune.com/queries/7476285/

## 6. Large-Wallet Behavior

Large-wallet flow was concentrated but two-sided.

Key evidence from the core event window:

- Total USDe bought: `$514.18m`
- Total USDe sold: `$528.62m`
- Net USDe flow: `-$14.44m`
- Top 10 buyers' share of buy volume: `50.0%`
- Top 10 sellers' share of sell volume: `37.7%`

The aggregate net sell flow was small relative to more than `$1.0bn` in two-sided USDe trading activity. This suggests that the event window was not dominated by broad one-way on-chain panic. Instead, large buyers and sellers both played major roles, consistent with arbitrage, market-maker rebalancing, or liquidity rotation around a venue-specific price dislocation.

Dune queries:

- https://dune.com/queries/7476429/
- https://dune.com/queries/7476531/

## 7. Risk Interpretation

The main risk highlighted by this event is not simply "stablecoin depeg risk" in the abstract. The data points to a more specific risk category: venue-level liquidity and pricing dislocation.

For exchanges, this kind of event raises questions about:

- Internal price references and oracle design
- Liquidity depth during stress windows
- Liquidation engines and collateral valuation
- Stablecoin listing and monitoring standards

For market makers, the event highlights:

- The need to monitor price divergence across venues
- Arbitrage and inventory rebalancing opportunities
- Concentrated wallet behavior during stress
- Liquidity provision risks when CeFi and DeFi prices diverge

For digital asset research teams, the event shows why on-chain data can help distinguish between broad protocol-level stress and venue-specific market structure failures.

## 8. Limitations

This analysis focuses on Ethereum DEX data and does not reconstruct Binance's internal order book, liquidation engine, account-level positions, or exact internal pricing mechanism. Wallet-level DEX activity may include aggregators, routers, arbitrage bots, market makers, and institutional wallets, so wallet labels should be interpreted cautiously unless enriched with additional address attribution.

The conclusion should therefore be framed carefully: the on-chain evidence does not show a broad Ethereum DEX-based USDe run, but it does not fully explain the internal mechanics of the Binance dislocation.

## 9. Conclusion

The USDe Binance depeg appears more consistent with venue-specific liquidity and pricing dislocation than a broad on-chain stablecoin run. USDe stayed near peg on Ethereum DEXs, trading activity spiked, net sell pressure reversed into net buying demand, and large-wallet flows were concentrated but two-sided.

This project demonstrates how Dune SQL and on-chain event analysis can be used to evaluate stablecoin stress, capital flow behavior, and market structure risk in digital asset markets.

