# Dune Dashboard Copy and Layout

Dashboard title:

```text
USDe Binance Depeg: On-chain Price Stability and Liquidity Response
```

Dashboard description:

```text
This dashboard analyzes the USDe Binance depeg event from an on-chain market risk perspective, covering DEX price stability, trading volume spike, net sell pressure, and large-wallet behavior during the Oct 10-11, 2025 event window.
```

## Top Text Block

Use this as the first text / markdown block under the dashboard title:

```markdown
## Key Findings

USDe experienced an extreme dislocation on Binance during Oct 10-11, 2025, but Ethereum DEX data does not show a broad on-chain stablecoin run. USDe's minimum median DEX price stayed near peg at 0.997641, while DEX trading volume rose to $571.89m, around 3.0x the trailing 7-day average. Large-wallet flows were two-sided and concentrated, suggesting market-maker or arbitrage activity rather than persistent panic selling.
```

## Section 1: Price Stability

Text block:

```markdown
## USDe Stayed Close to Peg on Ethereum DEXs

USDe's minimum median DEX price was 0.997641 during the event window, suggesting that the extreme Binance dislocation was not mirrored across Ethereum DEX venues.
```

Chart to place below:

- Query: USDe hourly DEX price
- Link: https://dune.com/queries/7468714/
- Recommended visualization title: `USDe DEX Price Deviation from $1 Peg`
- Recommended Y axis: `abs_deviation_from_peg`

If keeping the price chart instead of deviation chart:

- Recommended visualization title: `USDe DEX Price Stayed Close to Peg`
- Recommended Y axis range: `0.995` to `1.005`
- Recommended decimal places: `3` or `4`

## Section 2: Trading Activity

Text block:

```markdown
## DEX Trading Activity Spiked During the Event

USDe DEX trading volume reached $571.89m on Oct 11, about 3.0x the trailing 7-day average, showing elevated on-chain activity despite limited DEX price deviation.
```

Charts to place below, preferably side by side:

- Query: USDe daily DEX volume
- Link: https://dune.com/queries/7476326/
- Visualization 1 title: `Daily USDe DEX Trading Volume`
- Visualization 2 title: `USDe Volume vs Trailing 7D Average`

## Section 3: Flow Direction

Text block:

```markdown
## Net Flow Did Not Show Persistent Panic Selling

Net sell pressure shifted from +$34.67m on Oct 10 to -$19.16m on Oct 11, suggesting that initial selling pressure was followed by net buying demand.
```

Charts to place below:

- Query: USDe net sell pressure
- Link: https://dune.com/queries/7476285/
- Recommended first chart title: `Daily USDe Net Sell Pressure`

- Query: USDe buy vs sell volume
- Link: https://dune.com/queries/7476256/
- Recommended second chart title: `Daily USDe Buy vs Sell Volume`

Place the net sell pressure chart before the buy vs sell volume chart because it communicates the conclusion more directly.

## Section 4: Large Wallet Behavior

Text block:

```markdown
## Large Wallets Drove Two-sided Flow

During the core event window, USDe saw $514.18m bought and $528.62m sold, with only -$14.44m net flow. Top 10 buyers represented 50.0% of buy volume, while top 10 sellers represented 37.7% of sell volume, indicating concentrated two-sided large-wallet activity.
```

Charts / tables to place below:

- Query: Large wallet flow summary
- Link: https://dune.com/queries/7476531/
- Recommended title: `Large Wallet Flow Summary`

- Query: Top USDe buyers and sellers
- Link: https://dune.com/queries/7476429/
- Recommended title: `Top USDe Buyers and Sellers During Event Window`

Place the summary before the detailed table.

## Bottom Text Block

Use this as the final text block at the bottom:

```markdown
## Key Takeaway

The Binance USDe depeg appears more consistent with venue-specific liquidity and pricing dislocation than a broad on-chain stablecoin run. Ethereum DEX prices stayed close to peg, trading activity spiked, and large-wallet flows were concentrated but two-sided.
```

## Final Layout Order

1. Dashboard title and description
2. Key Findings text block
3. Section 1 text block: USDe stayed close to peg
4. Price deviation / price stability chart
5. Section 2 text block: DEX trading activity spiked
6. Daily volume chart and volume vs 7D average chart
7. Section 3 text block: net flow did not show persistent panic selling
8. Net sell pressure chart
9. Buy vs sell volume chart
10. Section 4 text block: large wallets drove two-sided flow
11. Large wallet summary
12. Top buyers and sellers table
13. Key Takeaway text block

## Final Polish Notes

After the latest dashboard review, the structure is strong and can be used as a portfolio artifact. Optional polish items:

- Shorten duplicated visualization subtitles where Dune shows both the visualization title and query title.
- If possible, show the first chart as `abs_deviation_from_peg` rather than raw USDe price to make the small peg deviation visually clearer.
- Keep the large wallet summary above the detailed wallet table.
- Keep the final Key Takeaway at the bottom because it reinforces the research conclusion after the reader has seen the evidence.
