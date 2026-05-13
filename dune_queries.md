# Dune Query Plan

Use this file to track the SQL queries that power the dashboard. Add Dune query links after creating them.

## Dashboard Sections

### 1. USDe Price Deviation

Goal: measure how far USDe traded from the 1 USD peg during the event window.

Metrics:

- Hourly average USDe price
- Minimum hourly price
- Maximum deviation from 1 USD
- Time to recovery

Potential data:

- DEX trade prices from `dex.trades`
- Stablecoin pool swaps involving USDe
- CoinGecko price as an off-chain reference

First query to create in Dune:

```sql
-- USDe hourly DEX price against major stablecoins
-- Event window uses UTC. 2025-10-11 early morning Singapore time is 2025-10-10 UTC evening.

WITH usde_trades AS (
    SELECT
        date_trunc('hour', block_time) AS hour,
        blockchain,
        project,
        CASE
            WHEN token_bought_address = 0x4c9edd5852cd905f086c759e8383e09bff1e68b3
                THEN token_sold_symbol
            WHEN token_sold_address = 0x4c9edd5852cd905f086c759e8383e09bff1e68b3
                THEN token_bought_symbol
        END AS quote_symbol,
        CASE
            WHEN token_bought_address = 0x4c9edd5852cd905f086c759e8383e09bff1e68b3
                THEN token_sold_amount / NULLIF(token_bought_amount, 0)
            WHEN token_sold_address = 0x4c9edd5852cd905f086c759e8383e09bff1e68b3
                THEN token_bought_amount / NULLIF(token_sold_amount, 0)
        END AS usde_price,
        amount_usd
    FROM dex.trades
    WHERE blockchain = 'ethereum'
      AND block_time >= TIMESTAMP '2025-10-03 00:00:00'
      AND block_time <  TIMESTAMP '2025-10-18 00:00:00'
      AND block_date >= DATE '2025-10-03'
      AND block_date <  DATE '2025-10-18'
      AND amount_usd >= 1000
      AND (
          (
              token_bought_address = 0x4c9edd5852cd905f086c759e8383e09bff1e68b3
              AND token_sold_address IN (
                  0xdac17f958d2ee523a2206206994597c13d831ec7, -- USDT
                  0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48, -- USDC
                  0x6b175474e89094c44da98b954eedeac495271d0f  -- DAI
              )
          )
          OR
          (
              token_sold_address = 0x4c9edd5852cd905f086c759e8383e09bff1e68b3
              AND token_bought_address IN (
                  0xdac17f958d2ee523a2206206994597c13d831ec7, -- USDT
                  0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48, -- USDC
                  0x6b175474e89094c44da98b954eedeac495271d0f  -- DAI
              )
          )
      )
)

SELECT
    hour,
    quote_symbol,
    approx_percentile(usde_price, 0.5) AS median_usde_price,
    avg(usde_price) AS avg_usde_price,
    min(usde_price) AS min_usde_price,
    max(usde_price) AS max_usde_price,
    abs(approx_percentile(usde_price, 0.5) - 1) AS abs_deviation_from_peg,
    sum(amount_usd) AS volume_usd,
    count(*) AS trade_count
FROM usde_trades
WHERE usde_price BETWEEN 0.90 AND 1.10
GROUP BY 1, 2
ORDER BY 1, 2;
```

### 2. Stablecoin Substitution Flow

Goal: identify whether users moved from USDe into USDT, USDC, or other assets.

Metrics:

- USDe swap volume by counterparty token
- USDe-to-USDT volume
- USDe-to-USDC volume
- Net stablecoin inflow / outflow around major DEX pools

Potential data:

- `dex.trades`
- ERC-20 transfer tables
- Token addresses for USDe, USDT, USDC

### 3. Liquidity Stress

Goal: observe whether liquidity providers withdrew liquidity during the event.

Metrics:

- Pool TVL before, during, and after the depeg
- Liquidity changes in USDe pools
- Volume-to-liquidity ratio

Potential data:

- DEX pool event tables
- DeFiLlama pool / protocol TVL

### 4. Large Wallet Behavior

Goal: identify whether large wallets accelerated the depeg or absorbed the dislocation.

Metrics:

- Top 20 USDe senders and receivers
- Net USDe balance change by wallet
- Large swaps involving USDe

Potential data:

- ERC-20 transfer tables
- `dex.trades`

## Query Log

| Query | Purpose | Link | Status |
| --- | --- | --- | --- |
| USDe hourly price | Price deviation | https://dune.com/queries/7468714/ | Done |
| USDe buy vs sell volume | Stablecoin substitution | https://dune.com/queries/7476256/ | Done |
| USDe net sell pressure | Net stablecoin flow | https://dune.com/queries/7476285/ | Done |
| USDe daily DEX volume | Trading activity spike | https://dune.com/queries/7476326/ | Done |
| USDe pool liquidity | Liquidity stress | TBD | Optional |
| Top USDe buyers and sellers | Large wallet behavior | https://dune.com/queries/7476429/ | Done |
| Large wallet flow summary | Large wallet concentration | https://dune.com/queries/7476531/ | Done |

## Query 4: Top USDe Buyers and Sellers During Event Window

Purpose: identify large wallets that bought or sold USDe during the core Binance depeg event window. This helps determine whether on-chain activity looked like panic selling, arbitrage buying, or two-sided liquidity rebalancing.

Core event window:

- UTC: `2025-10-10 00:00:00` to `2025-10-12 00:00:00`
- Singapore / Beijing time: roughly Oct 10 to Oct 12, covering the Oct 11 early-morning event.

Visualization:

- Type: table
- Sort by: `abs_net_usde_flow_usd` descending
- Title: `Top USDe Buyers and Sellers During Event Window`

```sql
-- Top USDe buyers and sellers during the core event window
-- Positive net_usde_flow_usd = net USDe buyer
-- Negative net_usde_flow_usd = net USDe seller

WITH wallet_flows AS (
    SELECT
        tx_from AS wallet,
        sum(
            CASE
                WHEN token_bought_address = 0x4c9edd5852cd905f086c759e8383e09bff1e68b3
                    THEN amount_usd
                ELSE 0
            END
        ) AS bought_usde_usd,
        sum(
            CASE
                WHEN token_sold_address = 0x4c9edd5852cd905f086c759e8383e09bff1e68b3
                    THEN amount_usd
                ELSE 0
            END
        ) AS sold_usde_usd,
        count(*) AS trade_count,
        min(block_time) AS first_trade_time,
        max(block_time) AS last_trade_time
    FROM dex.trades
    WHERE blockchain = 'ethereum'
      AND block_time >= TIMESTAMP '2025-10-10 00:00:00'
      AND block_time <  TIMESTAMP '2025-10-12 00:00:00'
      AND block_date >= DATE '2025-10-10'
      AND block_date <  DATE '2025-10-12'
      AND amount_usd >= 1000
      AND (
          token_bought_address = 0x4c9edd5852cd905f086c759e8383e09bff1e68b3
          OR token_sold_address = 0x4c9edd5852cd905f086c759e8383e09bff1e68b3
      )
    GROUP BY 1
)

SELECT
    wallet,
    bought_usde_usd,
    sold_usde_usd,
    bought_usde_usd - sold_usde_usd AS net_usde_flow_usd,
    abs(bought_usde_usd - sold_usde_usd) AS abs_net_usde_flow_usd,
    CASE
        WHEN bought_usde_usd - sold_usde_usd > 0 THEN 'Net buyer'
        WHEN bought_usde_usd - sold_usde_usd < 0 THEN 'Net seller'
        ELSE 'Balanced'
    END AS wallet_role,
    trade_count,
    first_trade_time,
    last_trade_time
FROM wallet_flows
WHERE bought_usde_usd + sold_usde_usd >= 100000
ORDER BY abs_net_usde_flow_usd DESC
LIMIT 50;
```

Optional summary query:

```sql
-- Summary of large wallet buyer / seller concentration

WITH wallet_flows AS (
    SELECT
        tx_from AS wallet,
        sum(
            CASE
                WHEN token_bought_address = 0x4c9edd5852cd905f086c759e8383e09bff1e68b3
                    THEN amount_usd
                ELSE 0
            END
        ) AS bought_usde_usd,
        sum(
            CASE
                WHEN token_sold_address = 0x4c9edd5852cd905f086c759e8383e09bff1e68b3
                    THEN amount_usd
                ELSE 0
            END
        ) AS sold_usde_usd
    FROM dex.trades
    WHERE blockchain = 'ethereum'
      AND block_time >= TIMESTAMP '2025-10-10 00:00:00'
      AND block_time <  TIMESTAMP '2025-10-12 00:00:00'
      AND block_date >= DATE '2025-10-10'
      AND block_date <  DATE '2025-10-12'
      AND amount_usd >= 1000
      AND (
          token_bought_address = 0x4c9edd5852cd905f086c759e8383e09bff1e68b3
          OR token_sold_address = 0x4c9edd5852cd905f086c759e8383e09bff1e68b3
      )
    GROUP BY 1
),
ranked AS (
    SELECT
        wallet,
        bought_usde_usd,
        sold_usde_usd,
        bought_usde_usd - sold_usde_usd AS net_usde_flow_usd,
        row_number() OVER (ORDER BY bought_usde_usd DESC) AS buyer_rank,
        row_number() OVER (ORDER BY sold_usde_usd DESC) AS seller_rank
    FROM wallet_flows
)

SELECT
    sum(bought_usde_usd) AS total_bought_usde_usd,
    sum(sold_usde_usd) AS total_sold_usde_usd,
    sum(bought_usde_usd) - sum(sold_usde_usd) AS total_net_usde_flow_usd,
    sum(CASE WHEN buyer_rank <= 10 THEN bought_usde_usd ELSE 0 END) AS top_10_buyer_volume_usd,
    sum(CASE WHEN seller_rank <= 10 THEN sold_usde_usd ELSE 0 END) AS top_10_seller_volume_usd,
    sum(CASE WHEN buyer_rank <= 10 THEN bought_usde_usd ELSE 0 END) / NULLIF(sum(bought_usde_usd), 0) AS top_10_buyer_share,
    sum(CASE WHEN seller_rank <= 10 THEN sold_usde_usd ELSE 0 END) / NULLIF(sum(sold_usde_usd), 0) AS top_10_seller_share
FROM ranked;
```

## Query 3: Daily USDe DEX Trading Volume Spike

Purpose: show whether USDe trading activity increased around the Binance depeg event, even if on-chain prices remained close to peg.

Visualization:

- Type: bar chart
- X axis: `day`
- Y axis: `daily_volume_usd`
- Title: `Daily USDe DEX Trading Volume`

```sql
-- Daily USDe DEX trading volume across USDT, USDC, and DAI pairs

WITH daily_volume AS (
    SELECT
        date_trunc('day', block_time) AS day,
        sum(amount_usd) AS daily_volume_usd,
        count(*) AS trade_count
    FROM dex.trades
    WHERE blockchain = 'ethereum'
      AND block_time >= TIMESTAMP '2025-10-03 00:00:00'
      AND block_time <  TIMESTAMP '2025-10-18 00:00:00'
      AND block_date >= DATE '2025-10-03'
      AND block_date <  DATE '2025-10-18'
      AND amount_usd >= 1000
      AND (
          (
              token_sold_address = 0x4c9edd5852cd905f086c759e8383e09bff1e68b3
              AND token_bought_address IN (
                  0xdac17f958d2ee523a2206206994597c13d831ec7, -- USDT
                  0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48, -- USDC
                  0x6b175474e89094c44da98b954eedeac495271d0f  -- DAI
              )
          )
          OR
          (
              token_bought_address = 0x4c9edd5852cd905f086c759e8383e09bff1e68b3
              AND token_sold_address IN (
                  0xdac17f958d2ee523a2206206994597c13d831ec7, -- USDT
                  0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48, -- USDC
                  0x6b175474e89094c44da98b954eedeac495271d0f  -- DAI
              )
          )
      )
    GROUP BY 1
)

SELECT
    day,
    daily_volume_usd,
    trade_count,
    avg(daily_volume_usd) OVER (
        ORDER BY day
        ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING
    ) AS trailing_7d_avg_volume_usd,
    daily_volume_usd / NULLIF(
        avg(daily_volume_usd) OVER (
            ORDER BY day
            ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING
        ),
        0
    ) AS volume_vs_trailing_7d_avg
FROM daily_volume
ORDER BY day;
```

Optional second visualization from the same query:

- Type: line chart
- X axis: `day`
- Y axis: `volume_vs_trailing_7d_avg`
- Title: `USDe Volume vs Trailing 7D Average`

## Query 2: USDe Swap Volume by Quote Stablecoin

Purpose: measure whether users swapped USDe into USDT, USDC, or DAI during the Binance depeg event window.

Visualization:

- Type: stacked bar chart or area chart
- X axis: `hour`
- Y axis: `volume_usd`
- Series: `flow_direction`

```sql
-- USDe swap volume by direction and counterparty stablecoin
-- Positive research use: identify whether users moved out of USDe during the event.

WITH usde_swaps AS (
    SELECT
        date_trunc('hour', block_time) AS hour,
        blockchain,
        project,
        CASE
            WHEN token_sold_address = 0x4c9edd5852cd905f086c759e8383e09bff1e68b3
                THEN 'USDe sold for ' || token_bought_symbol
            WHEN token_bought_address = 0x4c9edd5852cd905f086c759e8383e09bff1e68b3
                THEN token_sold_symbol || ' sold for USDe'
        END AS flow_direction,
        CASE
            WHEN token_sold_address = 0x4c9edd5852cd905f086c759e8383e09bff1e68b3
                THEN token_bought_symbol
            WHEN token_bought_address = 0x4c9edd5852cd905f086c759e8383e09bff1e68b3
                THEN token_sold_symbol
        END AS counterparty_stablecoin,
        amount_usd
    FROM dex.trades
    WHERE blockchain = 'ethereum'
      AND block_time >= TIMESTAMP '2025-10-03 00:00:00'
      AND block_time <  TIMESTAMP '2025-10-18 00:00:00'
      AND block_date >= DATE '2025-10-03'
      AND block_date <  DATE '2025-10-18'
      AND amount_usd >= 1000
      AND (
          (
              token_sold_address = 0x4c9edd5852cd905f086c759e8383e09bff1e68b3
              AND token_bought_address IN (
                  0xdac17f958d2ee523a2206206994597c13d831ec7, -- USDT
                  0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48, -- USDC
                  0x6b175474e89094c44da98b954eedeac495271d0f  -- DAI
              )
          )
          OR
          (
              token_bought_address = 0x4c9edd5852cd905f086c759e8383e09bff1e68b3
              AND token_sold_address IN (
                  0xdac17f958d2ee523a2206206994597c13d831ec7, -- USDT
                  0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48, -- USDC
                  0x6b175474e89094c44da98b954eedeac495271d0f  -- DAI
              )
          )
      )
)

SELECT
    hour,
    flow_direction,
    counterparty_stablecoin,
    sum(amount_usd) AS volume_usd,
    count(*) AS trade_count
FROM usde_swaps
GROUP BY 1, 2, 3
ORDER BY 1, 2;
```

### Cleaner Visualization Version

If the hourly chart is too noisy, use this daily net-flow version. It is better for a resume project and research memo because it directly compares USDe selling pressure versus buying demand.

Visualization:

- Type: grouped bar chart or line chart
- X axis: `day`
- Y axis: `volume_usd`
- Series: `flow_side`

```sql
-- Cleaner daily chart: USDe sell pressure vs buy demand

WITH usde_swaps AS (
    SELECT
        date_trunc('day', block_time) AS day,
        CASE
            WHEN token_sold_address = 0x4c9edd5852cd905f086c759e8383e09bff1e68b3
                THEN 'Sell USDe for other stablecoins'
            WHEN token_bought_address = 0x4c9edd5852cd905f086c759e8383e09bff1e68b3
                THEN 'Buy USDe with other stablecoins'
        END AS flow_side,
        amount_usd
    FROM dex.trades
    WHERE blockchain = 'ethereum'
      AND block_time >= TIMESTAMP '2025-10-03 00:00:00'
      AND block_time <  TIMESTAMP '2025-10-18 00:00:00'
      AND block_date >= DATE '2025-10-03'
      AND block_date <  DATE '2025-10-18'
      AND amount_usd >= 1000
      AND (
          (
              token_sold_address = 0x4c9edd5852cd905f086c759e8383e09bff1e68b3
              AND token_bought_address IN (
                  0xdac17f958d2ee523a2206206994597c13d831ec7, -- USDT
                  0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48, -- USDC
                  0x6b175474e89094c44da98b954eedeac495271d0f  -- DAI
              )
          )
          OR
          (
              token_bought_address = 0x4c9edd5852cd905f086c759e8383e09bff1e68b3
              AND token_sold_address IN (
                  0xdac17f958d2ee523a2206206994597c13d831ec7, -- USDT
                  0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48, -- USDC
                  0x6b175474e89094c44da98b954eedeac495271d0f  -- DAI
              )
          )
      )
)

SELECT
    day,
    flow_side,
    sum(amount_usd) AS volume_usd,
    count(*) AS trade_count
FROM usde_swaps
GROUP BY 1, 2
ORDER BY 1, 2;
```

### Net Flow Table Version

Use this if you want one clean table showing net sell pressure. A positive `net_sell_pressure_usd` means more USDe was sold than bought that day.

```sql
-- Daily USDe net sell pressure

WITH usde_swaps AS (
    SELECT
        date_trunc('day', block_time) AS day,
        CASE
            WHEN token_sold_address = 0x4c9edd5852cd905f086c759e8383e09bff1e68b3
                THEN amount_usd
            ELSE 0
        END AS sell_usde_volume_usd,
        CASE
            WHEN token_bought_address = 0x4c9edd5852cd905f086c759e8383e09bff1e68b3
                THEN amount_usd
            ELSE 0
        END AS buy_usde_volume_usd
    FROM dex.trades
    WHERE blockchain = 'ethereum'
      AND block_time >= TIMESTAMP '2025-10-03 00:00:00'
      AND block_time <  TIMESTAMP '2025-10-18 00:00:00'
      AND block_date >= DATE '2025-10-03'
      AND block_date <  DATE '2025-10-18'
      AND amount_usd >= 1000
      AND (
          (
              token_sold_address = 0x4c9edd5852cd905f086c759e8383e09bff1e68b3
              AND token_bought_address IN (
                  0xdac17f958d2ee523a2206206994597c13d831ec7,
                  0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48,
                  0x6b175474e89094c44da98b954eedeac495271d0f
              )
          )
          OR
          (
              token_bought_address = 0x4c9edd5852cd905f086c759e8383e09bff1e68b3
              AND token_sold_address IN (
                  0xdac17f958d2ee523a2206206994597c13d831ec7,
                  0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48,
                  0x6b175474e89094c44da98b954eedeac495271d0f
              )
          )
      )
)

SELECT
    day,
    sum(sell_usde_volume_usd) AS sell_usde_volume_usd,
    sum(buy_usde_volume_usd) AS buy_usde_volume_usd,
    sum(sell_usde_volume_usd) - sum(buy_usde_volume_usd) AS net_sell_pressure_usd
FROM usde_swaps
GROUP BY 1
ORDER BY 1;
```

Recommended visualization:

- Type: bar chart
- X axis: `day`
- Y axis: `net_sell_pressure_usd`
- Title: `Daily USDe Net Sell Pressure Around Binance Depeg Event`

Interpretation:

- Above zero: net selling pressure, users sold more USDe than they bought.
- Below zero: net buying demand, users bought more USDe than they sold.
- If Oct 10-11 is below zero or close to zero, this supports the thesis that the Binance depeg was not accompanied by broad on-chain panic selling.
