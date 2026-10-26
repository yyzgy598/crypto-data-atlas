# 07 · 衍生品专项：资金费率、持仓量、清算、多空比、期权、基差、CME/CFTC

目录
1. 需求 → 数据源速查
2. Coinglass API v4 全接口
3. Coinalyze、Laevitas、Velo、Amberdata、Glassnode derivatives、Coin Metrics、Kaiko、CCData futures、CoinAPI metrics、Tardis derivative_ticker
4. 期权专项：Deribit、Laevitas、Amberdata、Greeks.live、Block Scholes、Volmex、Derive(Lyra)、Aevo、Paradex、Bybit/OKX/Binance options、链上期权（Hegic、Premia、Dopex/Stryke、Rysk、Ribbon/Aevo、Thetanuts、Panoptic、Opyn）
5. CME / Cboe / CFTC COT / Bitnomial / Coinbase Derivatives / MIAX / Nodal / Eurex / 港交所
6. 清算数据专题（各所可得性）
7. 口径与换算
8. 变更记录

---

## 1. 需求 → 数据源速查
| 需求 | 免费 | 付费/机构 | 原始源 |
|---|---|---|---|
| 当前资金费率全所对比 | Coinglass `futures/funding-rate/exchange-list`、DefiLlama `yields/perps`、CoinGecko `derivatives`、Hyperliquid `predictedFundings`、Paradex WS `funding_rate_comparison` | Laevitas、Velo、Amberdata | 各所 `premiumIndex`/`funding-rate` |
| 历史资金费率（分所） | 交易所原生（Binance/OKX/Bybit/Gate/Bitget/HTX/BitMEX/Deribit/Kraken Futures/dYdX/Hyperliquid 全可回溯）、Coinalyze、Coinglass（免费层短） | Coinglass Standard+、CCData futures、Coin Metrics、Kaiko、Amberdata、Tardis | 交易所 |
| OI 聚合历史 | Coinglass `futures/open-interest/aggregated-history`、Coinalyze `open-interest-history`（最深免费） | Glassnode、Coin Metrics、CCData、Laevitas、Velo | Binance 30 天、Bybit 深、OKX rubik、Gate contract_stats、Bitfinex、Deribit、Hyperliquid 节点 |
| 清算（聚合） | Coinglass `futures/liquidation/*`（免费层有限）、Coinalyze `liquidation-history`、Hyperliquid 社区 stats | Coinglass 付费、Amberdata、Kaiko、Coin Metrics `market-liquidations`、Tardis `liquidations` | WS：Binance `!forceOrder@arr`（抽样）、Bybit `allLiquidation`、OKX `liquidation-orders`（REST 有历史）、Gate `liq_orders`、CoinEx `liquidation-history`、Backpack WS `liquidation`、Orderly `public/liquidation`、Paradex `/liquidations`、extended、dYdX fills `LIQUIDATED` |
| 多空比 | Binance `/futures/data/*`、OKX `rubik/stat/contracts/long-short-*`、Bybit `account-ratio`、Gate `contract_stats`、HTX `elite_*_ratio`、EdgeX、Coinglass `futures/global-long-short-account-ratio` 等 | Coinglass、Laevitas | 交易所 |
| 主动买卖量 / CVD | 交易所 aggTrades 自算、Binance `takerlongshortRatio`、OKX `rubik/stat/taker-volume`、Coinglass `futures/taker-buy-sell-volume/*`、Glassnode `futures_cvd_*`/`spot_cvd_*` | Velo、Laevitas、Amberdata、Kaiko | 交易所逐笔 |
| 基差/期限结构 | Binance `/futures/data/basis`、`deliveryPrice`；Deribit/OKX/Bybit 交割合约价；Coinglass `futures/basis`；Glassnode `futures_term_structure`、`futures_annualized_basis_3m` | Laevitas、Velo、Amberdata、Coin Metrics | 交易所 |
| 期权 IV/Skew/OI/Max Pain | Deribit `public/*`（当前）、Coinglass `option/*`、Laevitas 免费层 | Laevitas、Amberdata、Block Scholes、Greeks.live、Glassnode options_* | Deribit、OKX、Bybit、Binance eapi |
| CME 持仓/COT | CFTC COT（免费）、CME 官网日报表、Coinglass CME 页、Velo CME | CME DataMine、Refinitiv/Bloomberg | CME |
| 清算热力图 / 预估清算档位 | Coinglass `futures/liquidation/aggregated-heatmap/*`（付费层）；Hyperliquid 可从持仓直接算（HyperDash/Hypurrscan） | Coinglass、Velo | 自算（OI 分布 + 杠杆估计） |

---

## 2. Coinglass API v4
- 文档：https://docs.coinglass.com/reference/ ；Base `https://open-api-v4.coinglass.com/api/`；Header `CG-API-KEY`；返回 `{"code":"0","msg":"success","data":...}`。套餐：Hobbyist（免费，30 req/min，部分接口、历史约 1 个月、interval 最小 4h 等）、Startup（80 req/min）、Standard（300 req/min，全部接口，分钟级）、Professional（1200 req/min）、Enterprise。以下为接口族（路径以文档为准，v4 2025 版）：
- **通用**：`futures/supported-coins`、`futures/supported-exchange-pairs`、`spot/supported-coins`、`spot/supported-exchange-pairs`、`option/supported-coins`（v4 路径多为 `/api/futures/...`）
- **合约行情**：`futures/price/history?exchange=Binance&symbol=BTCUSDT&interval=1h&limit=1000&start_time=&end_time=`（OHLC）、`futures/pairs-markets?symbol=BTC`（**各所各交易对快照：价格、OI、24h 量、资金费、多空比、清算 24h、OI 变化**）、`futures/coins-markets`（按币聚合）、`futures/coins-price-change`、`futures/exchange-rank`、`futures/delisted-pairs`、`futures/orderbook/ask-bids-history?exchange=&symbol=&interval=&range=0.25|0.5|1|2|5|10`（**±X% 盘口深度历史**）、`futures/orderbook/aggregated-ask-bids-history`、`futures/orderbook/history`（大单挂单热力）、`futures/orderbook/large-limit-order`（**大额限价单实时**）、`futures/orderbook/large-limit-order-history`、`futures/taker-buy-sell-volume/history`、`futures/aggregated-taker-buy-sell-volume/history`、`futures/taker-buy-sell-volume/exchange-list`、`futures/whale-index`、`futures/basis/history?exchange=&symbol=&interval=`、`futures/rsi/list`（**全币种多周期 RSI**）、`futures/v2/...`
- **持仓量 OI**：`futures/open-interest/history?exchange=&symbol=&interval=&limit=`（OHLC 形式）、`futures/open-interest/aggregated-history?symbol=BTC&interval=1h`（全所聚合）、`futures/open-interest/aggregated-stablecoin-margin-history`、`futures/open-interest/aggregated-coin-margin-history`、`futures/open-interest/exchange-list?symbol=BTC`（**各所 OI 与份额、1h/4h/24h 变化**）、`futures/open-interest/exchange-history-chart?symbol=&range=12h|24h|...`（各所堆叠时序）
- **资金费率**：`futures/funding-rate/history?exchange=&symbol=&interval=`（OHLC）、`futures/funding-rate/oi-weight-history?symbol=&interval=`（**OI 加权**）、`futures/funding-rate/vol-weight-history`（成交量加权）、`futures/funding-rate/exchange-list?symbol=`（**各所当前费率、下次时间、周期**；含 stablecoin/coin 保证金两列）、`futures/funding-rate/accumulated-exchange-list?range=1d|7d|30d|365d`（**累计资金费**）、`futures/funding-rate/arbitrage?usd=10000`（**套利机会：所间费率差与年化**）
- **多空比**：`futures/global-long-short-account-ratio/history?exchange=&symbol=&interval=`、`futures/top-long-short-account-ratio/history`、`futures/top-long-short-position-ratio/history`、`futures/taker-buy-sell-volume/exchange-list`、`futures/long-short-ratio/...`（Hyperliquid/Bitfinex 等）
- **清算**：`futures/liquidation/history?exchange=&symbol=&interval=`（多/空清算量时序）、`futures/liquidation/aggregated-history?symbol=&interval=`、`futures/liquidation/coin-list?exchange=`（**各币 1h/4h/12h/24h 多空清算**）、`futures/liquidation/exchange-list?symbol=&range=`（**各所清算**）、`futures/liquidation/order?exchange=&symbol=&min_liquidation_amount=`（**清算订单流，大额**）、`futures/liquidation/heatmap/model1|model2|model3?exchange=&symbol=&range=`（**清算热力图：价格档位 × 时间的预估清算杠杆分布**）、`futures/liquidation/aggregated-heatmap/model1|2|3?symbol=&range=`、`futures/liquidation/map?exchange=&symbol=&range=`（**清算地图：各价位累计清算量**）、`futures/liquidation/aggregated-map`
- **现货**：`spot/price/history`、`spot/pairs-markets`、`spot/coins-markets`、`spot/orderbook/ask-bids-history`、`spot/orderbook/aggregated-ask-bids-history`、`spot/orderbook/history`、`spot/orderbook/large-limit-order`、`spot/orderbook/large-limit-order-history`、`spot/taker-buy-sell-volume/history`、`spot/aggregated-taker-buy-sell-volume/history`、`spot/supported-coins`、`spot/supported-exchange-pairs`
- **期权**：`option/max-pain?symbol=BTC&exchange=Deribit`（**各到期日 Max Pain、OI、名义**）、`option/info?symbol=`（各所期权 OI/量/份额）、`option/exchange-oi-history?symbol=&unit=USD&range=`、`option/exchange-vol-history`、`option/oi-by-strike`（v4 新）、`option/oi-by-expiry`、`option/volume-by-strike`、`option/iv/...`、`option/put-call-ratio/...`、`option/block-trades`、`option/gex`（部分套餐）
- **交易所 / 链上**：`exchange/assets?exchange=Binance`（**交易所钱包资产明细**）、`exchange/balance/list?symbol=BTC`（**各所 BTC/ETH/USDT/USDC… 余额与 1d/7d/30d 变化**）、`exchange/balance/chart?symbol=&exchange=`（历史）、`exchange/chain/tx/list?symbol=&exchange=&min_usd=`（**大额链上充提交易**）、`exchange/hyperliquid/...`（见下）、`hyperliquid/whale-alert`（**Hyperliquid 巨鲸开平仓动态**）、`hyperliquid/whale-position`（**巨鲸当前持仓**）、`hyperliquid/...`（HLP、清算、资金费）
- **ETF**：`etf/bitcoin/list`（**全部现货 BTC ETF：AUM、持仓 BTC、份额、价格、溢价、费率、发行方、托管方**）、`etf/bitcoin/net-assets/history`（总 AUM 时序）、`etf/bitcoin/flow-history`（**日度净流入按基金**）、`etf/bitcoin/premium-discount/history?ticker=`、`etf/bitcoin/history?ticker=`（单基金 AUM/持仓/份额历史）、`etf/bitcoin/price/history?ticker=`、`etf/bitcoin/detail?ticker=`、`etf/bitcoin/aum`、`etf/bitcoin/hk/flow-history`（**香港 BTC ETF**）、`etf/ethereum/list`、`etf/ethereum/net-assets/history`、`etf/ethereum/flow-history`、`etf/ethereum/hk/...`、`etf/solana/...`、`etf/xrp/...`（2025 新）、`grayscale/holdings-list`（**灰度各信托持仓/溢价**）、`grayscale/premium-history?symbol=`
- **指标**：`index/fear-greed-history`、`index/option-vs-futures-oi-ratio`、`index/bitcoin/bubble-index`、`index/ahr999`、`index/two-year-ma-multiplier`、`index/two-hundred-week-moving-average-heatmap`、`index/altcoin-season`（**山寨季指数**）、`index/bitcoin/short-term-holder-sopr`、`index/bitcoin/long-term-holder-sopr`、`index/bitcoin/short-term-holder-realized-price`、`index/bitcoin/long-term-holder-realized-price`、`index/bitcoin/short-term-holder-supply`、`index/bitcoin/long-term-holder-supply`、`index/bitcoin/rhodl-ratio`、`index/bitcoin/reserve-risk`、`index/bitcoin/active-addresses`、`index/bitcoin/new-addresses`、`index/bitcoin/net-unrealized-pnl`、`index/bitcoin/correlations`、`index/bitcoin/macro-oscillator`、`index/bitcoin/profitable-days`、`index/bitcoin/rainbow-chart`、`index/bitcoin/stock-flow`、`index/pi-cycle-indicator`、`index/golden-ratio-multiplier`、`index/puell-multiple`、`index/stableCoin-marketCap-history`（**稳定币市值**）、`index/bitcoin/vs-global-m2`、`index/bitcoin/vs-us-m2`、`index/bitcoin/dominance`、`index/coinbase-premium-index`、`index/bitfinex-margin-long-short`、`index/borrow-interest-rate/history?exchange=Binance&symbol=BTC`（**借贷利率**）、`index/bull-market-peak-indicator`（**牛市顶部信号 30 项汇总**）、`index/crypto-market-cap/history`、`index/btc-etf-netflow`
- **宏观 / 日历**：`calendar/economic-data`（**经济日历**）、`macro/...`（美元指数、黄金、纳指对比，部分）
- **Hyperliquid 专区**（v4）：`hyperliquid/whale-alert`、`hyperliquid/whale-position`、`hyperliquid/liquidation/...`、`hyperliquid/open-interest/...`、`hyperliquid/funding-rate/...`、`hyperliquid/hlp/...`、`hyperliquid/top-trader/...`
- 参数惯例：`exchange`（Binance、OKX、Bybit、Bitget、Gate、HTX、Kraken、Deribit、BitMEX、Bitfinex、CoinEx、MEXC、Hyperliquid、dYdX、Coinbase、Crypto.com、WhiteBIT、BingX、KuCoin、Bitunix、Phemex…）、`symbol`（币 `BTC` 或对 `BTCUSDT`）、`interval`（1m/3m/5m/15m/30m/1h/4h/6h/8h/12h/1d/1w，低套餐限制）、`limit<=4500`、`start_time`/`end_time` 毫秒。
- 坑：接口路径在 v3→v4 大改（2025），以文档实时为准；免费层 interval 最低 4h、历史 ~30 天、无 WS；`exchange_list` 类接口包含 `All` 聚合行。

---

## 3. 其他衍生品数据商
| 数据商 | 文档 | Base | 认证/价格 | 覆盖 | 关键接口 | 备注 |
|---|---|---|---|---|---|---|
| Coinalyze | https://api.coinalyze.net/v1/doc/ | `https://api.coinalyze.net/v1/` | `api_key` 查询参数，**免费**（40 req/min） | Binance、Bybit、OKX、Bitget、Gate、Deribit、BitMEX、Kraken、Bitfinex、HTX、Phemex、dYdX、Hyperliquid(2024+)、Coinbase Intl、Vertex、Woo、Crypto.com、Bitstamp(spot) 等 | `exchanges`、`future-markets`（symbol 形如 `BTCUSDT_PERP.A`，后缀=交易所代码）、`spot-markets`、`open-interest?symbols=&convert_to_usd=true`、`open-interest-history?symbols=&interval=1min|5min|15min|30min|1hour|2hour|4hour|6hour|12hour|daily&from=&to=&convert_to_usd=`（**OI 历史回溯多年**）、`funding-rate`、`funding-rate-history?symbols=&interval=&from=&to=`、`predicted-funding-rate`、`predicted-funding-rate-history`、`liquidation-history?symbols=&interval=&from=&to=&convert_to_usd=`（**多空清算历史**）、`long-short-ratio-history`（**多空账户比**）、`ohlcv-history?symbols=&interval=&from=&to=`（K 线含 `bv`/`tx`/`btx` 买量/笔数）；聚合符号 `BTCUSDT_PERP.A` 等，支持 `.6`（聚合全所）类 | 免费层最慷慨的衍生品历史 |
| Laevitas | https://docs.laevitas.ch/ | `https://api.laevitas.ch/`（`apiKey` 头） | 免费层有限（Basic），Pro/Enterprise | Deribit、OKX、Bybit、Binance、Bit.com、Delta、Aevo、Lyra、Hyperliquid、dYdX、GMX 等；期权为核心 | Analytics：`analytics/options/instruments/{market}/{currency}`、`analytics/options/oi_expiry/{market}/{currency}`、`analytics/options/oi_strike_all/{market}/{currency}/{maturity}`、`analytics/options/oi_type/...`、`analytics/options/top_traded_option/...`、`analytics/options/v_strike/...`（**按行权价成交**）、`analytics/options/volume_buy_sell/...`、`analytics/options/iv_rv/...`、`analytics/options/gex_date/{market}/{currency}/{maturity}`（**GEX**）、`analytics/options/gex_date_all/...`、`analytics/options/max_pain/...`、`analytics/options/greeks/...`、`analytics/options/skew/{market}/{currency}/{maturity}`、`analytics/options/atm_iv_ts/...`（**期限结构**）、`analytics/options/model_charts/...`、`analytics/options/oi_gainers_and_losers`、`analytics/options/snapshot/...`、`analytics/options/oi_net_change_all/...`、`analytics/options/butterfly/...`、`analytics/options/iv_smile/...`、`analytics/options/vol_surface/...`；Futures：`analytics/futures/instruments/{market}/{currency}`、`analytics/futures/oi_breakdown/{market}/{currency}`、`analytics/futures/oi_breakdown_by_exchange`、`analytics/futures/snapshot/...`、`analytics/futures/liquidations/...`、`analytics/futures/funding/...`、`analytics/futures/basis/...`、`analytics/futures/term_structure/...`、`analytics/futures/perpetual_funding/{currency}`（**全所资金费对比**）、`analytics/futures/alt_currency/{currency}`、`analytics/futures/markets_oi_gainers_and_losers`、`analytics/futures/aggregated_oi_volume`；Derivs：`analytics/derivs/summary/...`、`analytics/derivs/oi_gainers/...`、`analytics/derivs/price_change/...`、`analytics/derivs/futures/...`、`analytics/derivs/perpetuals/...`；Historical：`historical/options/...`、`historical/futures/...`、`historical/derivs/...`（`?start=&end=&limit=&page=`）；DeFi：`analytics/defi/...`（dYdX、GMX、Lyra、Dopex、Ribbon） | 期权分析最细；图表 `https://app.laevitas.ch/` |
| Velo Data | https://velodata.app/api ；文档 `https://velodata.app/docs` | `https://api.velo.xyz/api/v1/`（Basic auth，`api:KEY`）；Python `velodata` | 付费（Pro/Enterprise），有试用 | Binance、Bybit、OKX、Deribit、Coinbase、BitMEX、Hyperliquid、dYdX、Kraken、Bitfinex、CME 等 | `status`、`futures`（产品列表）、`options`、`spot`、`rows?type=futures|spot|options&exchanges=&products=&coins=&columns=&begin=&end=&resolution=1m|5m|1h|1d`（**统一列：open_price、close_price、high、low、coin_volume、dollar_volume、buy_trades、sell_trades、total_trades、buy_coin_volume、sell_coin_volume、buy_dollar_volume、sell_dollar_volume、coin_open_interest_high/low/close、dollar_open_interest_*、funding_rate、premium、buy_liquidations、sell_liquidations、buy_liquidations_coin_volume、sell_liquidations_coin_volume、buy_liquidations_dollar_volume、sell_liquidations_dollar_volume、iv_1w/1m/3m/6m、skew_1w/…、vega、gamma、delta、theta、index_price、mark_price、basis_annualized、term_structure**）、`caps`（市值）、`news`（**Velo 新闻流，含 effectivePrice**，WS `wss://api.velo.xyz/api/w/connect`） | 列式统一数据，做跨所对比最省；CME 数据含 |
| Amberdata Derivatives | 见 03 | `markets/futures/*`、`markets/options/*`、`markets/derivatives/analytics/*` | 付费 | 全所期权期货 | 见 03 列表；Derivatives Analytics（原 Genesis Volatility 收购）：`volatility-surfaces`、`term-structure`、`realized-volatility`、`iv-rank`、`skew`、`butterfly`、`gex`、`dealer-positioning`、`flows`、`block-trades`、`pain`、`strike-breakdown`、`level-1-quotes`、`options/volatility/cones`、`constant-maturity`（CM IV）、`trades/flow/alerts` | 机构期权标准 |
| Glassnode derivatives | 见 05 | `derivatives/futures_*`、`options_*` | 付费（Advanced+ 分钟级） | Binance、Bybit、OKX、Deribit、BitMEX、Bitfinex、Huobi、Kraken、CME、Coinbase、Bitget、Gate、dYdX… | OI/量/资金费/清算/CVD/期限结构/期权 IV/Skew/GEX | 聚合口径一致性好 |
| Coin Metrics | 见 03 | `timeseries/market-funding-rates`、`market-openinterest`、`market-liquidations`、`market-greeks`、`market-implied-volatility`、`market-contract-prices`、`market-metrics`（`liquidations_reported_future_*`、`open_interest_reported_future_*`、`funding_rate_*`）、`asset-metrics`（`open_interest_reported_future_usd`、`volume_reported_future_*`、`liquidations_reported_future_*_usd_1d`、`futures_aggregate_funding_rate_*`、`basis_annualized_*`） | Community 有部分日级 | Binance、Bybit、OKX、Deribit、BitMEX、Huobi、FTX(历史)、Kraken、Bitfinex、CME、Coinbase Intl、Hyperliquid(2024+) | — | 市场数据 Pro |
| Kaiko | 见 03 | `derivatives.v2/exchanges/{exchange}/{class}/{instrument}/risk|price|reference|oi|funding|liquidations` | 机构 | Binance、Bybit、OKX、Deribit、BitMEX、Bitfinex、Kraken、CME、Coinbase Intl、Bitget、Gate、Huobi… | — | — |
| CCData futures/options | 见 03 | `futures/v1/historical/{minutes|hours|days}`、`historical/funding-rate/*`、`historical/open-interest/*`、`options/v1/*` | 免费层可用 | 多所 | — | 分钟级历史 |
| CoinAPI metrics | 见 03 | `metrics/symbol/history?metric_id=DERIVATIVES_FUNDING_RATE_CURRENT|DERIVATIVES_FUNDING_RATE_NEXT|DERIVATIVES_OPEN_INTEREST|DERIVATIVES_MARK_PRICE|DERIVATIVES_INDEX_PRICE|LIQUIDATION_*`、`metrics/exchange/*` | 付费 | 全所 | — | 统一 metric_id |
| Tardis `derivative_ticker` / `liquidations` | 见 11 | 每日 CSV：`derivative_ticker`（funding_rate、predicted_funding_rate、open_interest、last_price、index_price、mark_price，逐 tick）、`liquidations`（Binance/Bybit/OKX/Deribit/BitMEX/Huobi/FTX/dYdX/Hyperliquid） | 付费（每月 1 日免费） | — | 回测级原始数据 | — |
| The Block Data、Kaiko Research、Blockworks Research、K33、Arcane、Bitwise 周报、CoinShares、Deribit Insights、Greeks.live Daily、GSR、Wintermute、QCP Capital 周评、Galaxy Derivatives | 报告 | 解读 | — | — | — | — |

---

## 4. 期权专项
| 来源 | 内容 | 访问 |
|---|---|---|
| Deribit（市场份额 ~70–80%） | 全部合约 ticker（IV、Greeks、OI、mark）、DVOL（BTC/ETH 波动率指数，`get_volatility_index_data`）、历史成交、结算/交割、大宗（`get_last_trades_by_currency` 中 `block_trade_id`）、RFQ、组合保证金 | 见 01；历史 IV 曲面需 Tardis/Laevitas/Amberdata |
| OKX 期权 | `public/opt-summary`（IV、Greeks、OI）、`market/tickers?instType=OPTION`、`rubik/stat/option/*`（OI/量按到期/行权价、PCR、大宗量）、`public/instruments?instType=OPTION`、`rfq/public-trades` | 01 |
| Bybit 期权 | `market/tickers?category=option`（markIv、bid/ask IV、delta/gamma/vega/theta、OI）、`market/instruments-info?category=option`、`market/historical-volatility`、`market/recent-trade?category=option`、`market/delivery-price` | 01 |
| Binance 期权（eapi） | `eapi/v1/mark`（markIV、Greeks）、`/ticker`、`/openInterest`、`/exerciseHistory`、`/historicalTrades`、`/blockTrades`、`/index` | 01 |
| Bit.com（Matrixport，退）、Delta Exchange（印度，`https://api.india.delta.exchange/v2/tickers?contract_types=call_options,put_options`、`/v2/products`、`/v2/history/candles?symbol=MARK:C-BTC-100000-310125&resolution=1h`，有免费 API，期权流动性第二梯队）、Coincall（`https://api.coincall.com/open/option/...`）、Bitget 期权、Gate 期权、KuCoin（无）、Kraken（无）、Coinbase（无；CDE 期权 2025 筹备）、CME 期权（见 5）、Cboe（2025 恢复 BTC/ETH 期权筹备）、IBIT 期权（Nasdaq，2024.11 起，**美股期权数据源：CBOE/OPRA、Yahoo `IBIT` options、Polygon.io options、Tradier、ORATS、CBOE DataShop**） | — | — |
| 链上期权：Derive（原 Lyra，`https://api.lyra.finance/`：`public/get_instruments`、`public/get_ticker`、`public/get_trade_history`、`public/get_option_settlement_prices`、`public/get_funding_rate_history`、`public/statistics`、`public/get_all_currencies`、`public/get_spot_feed_history`、`public/get_latest_signed_feeds`、`public/get_vaults`；WS `wss://api.lyra.finance/ws`）、Aevo（见 02）、Paradex（见 02）、Hegic（子图）、Premia（`https://api.premia.finance/`）、Stryke（Dopex v2，`https://api.stryke.xyz/...`）、Rysk、Thetanuts、Panoptic（子图）、Opyn（Squeeth 退）、Ribbon（→Aevo）、Friktion（退）、Zeta（退）、PsyOptions（退）、Moby（Arbitrum）、Ithaca、Valorem（退）、Buffer、Siren（退）、Dopex、Jones DAO、Cega、Hyperliquid（无期权）、Bitcoin 期权链上（无） | DefiLlama `overview/options` 聚合 | — |
| 分析商：Laevitas、Amberdata、Block Scholes（`https://www.blockscholes.com/`，机构，有 API）、Greeks.live（`https://greeks.live/`，中文社区；Daily 报告、API 需联系）、Volmex（BVIV/EVIV 波动率指数，链上 + `https://charts.volmex.finance/`，有 API `https://rest-v1.volmex.finance/public/iv/history?symbol=BVIV&resolution=1h`）、Deribit DVOL、Glassnode options、Coinglass options、Velo、Genesis Volatility（→Amberdata）、Skew（→Coinbase，退）、Deribit Metrics `https://metrics.deribit.com/`、Bitcoin Volatility Index (BitVol/EthVol by T3 Index `https://t3index.com/`，有数据下载)、CME CVOL（`https://www.cmegroup.com/market-data/cme-group-benchmark-administration/cme-group-volatility-indexes.html`，BTC CVOL） | IV、Skew、GEX、Dealer 持仓、流 | — |

---

## 5. CME / Cboe / CFTC / 传统交易所
| 来源 | 内容 | 访问 |
|---|---|---|
| CME Group | BTC（5 BTC）、Micro BTC（0.1）、ETH（50 ETH）、Micro ETH、SOL/XRP 期货（2025）、BTC/ETH 期权、Micro 期权、BTC Friday Futures（BFF）、Spot-Quoted；日报：成交量、OI、大户持仓；结算价；CVOL | 免费：`https://www.cmegroup.com/markets/cryptocurrencies/bitcoin/bitcoin.volume.html`（页面）、`https://www.cmegroup.com/CmeWS/mvc/Volume/Details/F/8478/{yyyyMMdd}/P`（**非正式 JSON，成交/OI 按到期**）、`https://www.cmegroup.com/CmeWS/mvc/Settlements/Futures/Settlements/8478/FUT?tradeDate=`（结算）、`https://www.cmegroup.com/CmeWS/mvc/Quotes/Future/8478/G`（报价）、Daily Bulletin PDF；付费：CME DataMine（历史逐笔/盘口）、CME Market Data Platform、Refinitiv/Bloomberg、Databento（`https://databento.com/`，**CME 全量 MBO/MBP/OHLCV，按量付费，Python API**，`GLBX.MDP3` 数据集，symbols `BTC.FUT`、`MBT.FUT`、`ETH.FUT`、`MET.FUT`）、Barchart、Quandl/Nasdaq Data Link（CHRIS/CME_BTC1 已停）、TradingView（CME:BTC1!）、Coinglass CME 页、Velo、Glassnode `futures_*`（含 CME）、Coin Metrics `cme-*` markets、Kaiko |
| CFTC Commitments of Traders (COT) | 每周二持仓（周五发布）：Legacy/Disaggregated/TFF（Traders in Financial Futures）报告，BTC/Micro BTC/ETH/Micro ETH；Dealer/Asset Manager/Leveraged Funds/Other Reportables 多空持仓 | 免费：`https://www.cftc.gov/dea/newcot/FinFutWk.txt`（TFF 本周）、`https://www.cftc.gov/files/dea/history/fut_fin_txt_{year}.zip`（历史）、Socrata API `https://publicreporting.cftc.gov/resource/gpe5-46if.json?$where=market_and_exchange_names like '%BITCOIN%'`（**TFF Futures Only，JSON，可筛 `cftc_contract_market_code` 133741（BTC）、1330E1（Micro BTC）、146021（ETH）、1460E1（Micro ETH）**）、`https://publicreporting.cftc.gov/resource/6dca-aqww.json`（Legacy）、`https://publicreporting.cftc.gov/resource/72hh-3qpy.json`（Disaggregated）、`https://publicreporting.cftc.gov/resource/yw9f-hn96.json`（TFF Combined）；Python `cot_reports`；Tradingster、Barchart、Coinglass CME COT 页、Velo |
| Cboe | Cboe Digital（原 ErisX）2025 关闭现货/期货；Cboe BZX 上市 BTC/ETH ETF；Cboe 计划 2025 Q4 推出 FTX-style 连续期货（Cboe Futures Exchange BTC/ETH Continuous Futures）、Cboe Bitcoin US ETF Index 期权（CBTX、MBTX） | `https://www.cboe.com/us/futures/market_statistics/`、Cboe DataShop（付费）、CBOE Index `https://www.cboe.com/us/indices/dashboard/CBTX/` |
| Coinbase Derivatives（CDE，原 FairX） | nano BTC/ETH、BTC/ETH 期货（美国 CFTC），2025 加 SOL/XRP/DOGE/ADA 等 | Advanced Trade API `products?product_type=FUTURE`、`GET /market/products/{id}/candles`；CDE 日报页面 |
| Bitnomial | BTC/ETH/XRP 实物交割期货/期权（美国） | `https://bitnomial.com/`，API `https://bitnomial.com/api/...`（需账户）；Tardis 含 Bitnomial |
| Kraken Futures（CFTC 注册 2025）、Robinhood（Bitstamp Derivatives 欧洲永续）、Bitstamp Derivatives、Gemini Derivatives（欧洲永续）、Crypto.com US 衍生品、FalconX、Hidden Road（Ripple）、Nodal Exchange（美国 BTC/ETH 实物期货 2025）、MIAX（Bitnomial 合作）、Eurex（Bitcoin ETN 期货 `https://www.eurex.com/`）、ICE Futures（Bakkt BTC 月度期货，2024 退市）、港交所（HKEX 虚拟资产 ETF 期货）、新加坡 SGX（2025 筹备 BTC 永续）、日本 OSE（无）、B3 巴西（BTC 期货 `https://www.b3.com.br/`）、CME 的 BRR/BRRNY 结算基准、CF Benchmarks（见 03） | 传统监管衍生品 | 各自 |
| 美股/ETF 相关衍生：IBIT/FBTC/GBTC 期权（OPRA）、MSTR 期权、COIN 期权、MARA/RIOT 期权、BITX（2x）、BITI（反向）、YieldMax（MSTY）、Defiance、ProShares BITO（CME 期货 ETF，持仓 `https://www.proshares.com/our-etfs/strategic/bito`） | 美股期权数据：Polygon.io options、Tradier、CBOE DataShop、ORATS、OptionMetrics、Yahoo Finance options（`yfinance Ticker.option_chain`）、Unusual Whales、Market Chameleon、OptionCharts | 见 09 |

---

## 6. 清算数据专题（各所可得性）
| 交易所 | REST 历史 | WS 实时 | 完整性 | 备注 |
|---|---|---|---|---|
| Binance | 无（2021.4 下线 `allForceOrders`） | `<symbol>@forceOrder`、`!forceOrder@arr` | **抽样**：每个合约每 1 秒最多推 1 条 | 聚合商（Coinglass 等）的 Binance 清算都是基于此抽样再估算 |
| Bybit | 无 | `allLiquidation.{symbol}`（2024.10 起，全量）；旧 `liquidation.{symbol}`（抽样，将下线） | 全量（新频道） | — |
| OKX | `public/liquidation-orders?instType=SWAP&uly=&state=filled&before=&after=&limit=100`（**有历史**） | `liquidation-orders`（instType 级，公共） | 较全 | 聚合所有 uly 需遍历 |
| Bitget | 无公开 | 无公开 | — | 用 Coinglass |
| Gate | `futures/{settle}/liq_orders?contract=&from=&to=&limit=1000`（**有历史**） | `futures.public_liquidates` | 较全 | — |
| HTX | `linear-swap-api/v3/swap_liquidation_orders?contract=&trade_type=0&start_time=&end_time=`（需 key，历史） | 无（公共） | 较全 | — |
| KuCoin Futures | 无 | 无 | — | — |
| MEXC | 无 | 无 | — | — |
| BingX | 无 | 无 | — | — |
| CoinEx | `futures/liquidation-history?market=&start_time=&end_time=`（**公开历史**） | 无 | 全 | — |
| BitMEX | `liquidation`（当前挂着的清算单）；历史需 `trade` 中无法区分 | `liquidation` | 实时可见 | 历史不可回溯 |
| Deribit | `get_settlement_history_by_currency?type=bankruptcy`（破产结算）；`get_last_trades_by_currency` 中 `liquidation` 字段（M/T/MT） | `trades.*` 的 `liquidation` 字段 | 全（成交级别标注） | 期权清算也有 |
| Kraken Futures | 无 | `trade` 的 `type=liquidation` | 实时 | — |
| Bitfinex | `pos.size` 统计；`liquidations` 旧 `https://api-pub.bitfinex.com/v2/liquidations/hist?start=&end=&limit=500`（**公开历史**，保证金清算） | WS `status` 频道 `liq` | 全（保证金） | — |
| Hyperliquid | 无单独接口；`userFills` 的 `liquidation` 字段（按用户）；全市场需节点 `node_fills`/S3 `node_fills_by_block` 或第三方（Hypurrscan `/liquidations`、HyperDash、Coinglass Hyperliquid、`stats-data.hyperliquid.xyz` 日级 `liquidations_by_coin`） | `trades`（含 `liquidation`?）、`userEvents.liquidation` | 节点全量 | 清算有两种：市价清算（流动性强）与 backstop 清算（由 HLP/Liquidator vault 接管） |
| dYdX v4 | `fills?...` 中 `type=LIQUIDATED`（按账户）；Indexer 无全市场清算接口 | `v4_subaccounts` 的 fills | 需遍历或用 Indexer DB | — |
| Paradex | `GET /liquidations?market=`（**公开**） | — | 全 | — |
| Orderly | `public/liquidation?symbol=&start_t=&end_t=`、`public/liquidated_positions`（**公开**） | `liquidation` | 全 | — |
| Backpack | 无 REST | WS `liquidation`（**公开全量**） | 全 | — |
| extended | `info/{market}/liquidations` | — | 全 | — |
| GMX / Drift / Jupiter Perps | 链上事件（`PositionDecrease` isLiquidation / Drift `LiquidationRecord` / Jupiter `LiquidateFullPositionEvent`）；Drift 历史 S3 `liquidations` CSV | Geyser/日志订阅 | 全（链上） | — |
| 聚合 | Coinglass（估算+多所）、Coinalyze、Amberdata、Kaiko、Coin Metrics、Tardis（原始 WS 录制）、Glassnode `futures_liquidated_volume_*`、Velo（列式） | — | 聚合口径差异大 | **Binance 清算在所有聚合商中都是低估的** |

---

## 7. 口径与换算
- **资金费率年化**：`年化 = 单期费率 × (24/结算小时数) × 365`。Binance/OKX/Bybit 多数 8h（×1095），Hyperliquid 1h（×8760），部分 Bybit/Bitget/Gate 小币 4h 或 1h（看 `fundingInterval`/`fundingInfo`）。Coinglass 的 "OI 加权" 把不同周期折算到 8h 显示。
- **OI 单位**：Binance USDⓈ-M `openInterest` 为合约张数 = 币数量（1 张 = 1 币，除 1000SHIB 等倍数合约）；COIN-M 张数（1 张 = 100 USD 或 10 USD）；Bybit 币数量；OKX `oi`（张，合约面值见 `ctVal`）/`oiCcy`（币）/`oiUsd`；Bitget 币；Gate 张（`quanto_multiplier`）；Deribit USD（反向）/币（线性 USDC）；BitMEX 合约数（XBTUSD 1 合约 = 1 USD）；Hyperliquid 币；dYdX 币；Kraken Futures 合约（1 = 1 USD 反向，线性为币）。统一到 USD 用标记价。
- **多空比三种**：账户数比（散户情绪）、大户持仓比（top trader position，按持仓 USD）、大户账户比（top trader account）；Binance 三种都给（仅 30 天），OKX 给账户比与合约持仓比，Bybit 只给账户比，Gate `contract_stats` 给 `lsr_taker`/`lsr_account`/`top_lsr_account`/`top_lsr_size`。
- **主动买卖 / CVD**：`isBuyerMaker=false` 为主动买；CVD = Σ(主动买量 − 主动卖量)；现货 CVD 与合约 CVD 分开看（Glassnode spot_cvd / futures_cvd）。
- **清算量**：聚合商的 Binance 数据是抽样估算；"24h 清算 $X 亿" 在不同网站差 2–3 倍属正常。做研究用 Bybit 全量 + OKX 历史 + Hyperliquid 节点较可靠。
- **期权 OI 名义价值**：OI（张） × 标的价；Deribit 1 张 = 1 BTC / 1 ETH；OKX 1 张 = 0.01 BTC / 0.1 ETH（看 `ctVal`）；Binance 1 张 = 1 币；Bybit 1 张 = 1 币；对比时按币折算。
- **基差年化**：`(期货价/现货价 − 1) × 365/剩余天数`；Glassnode `futures_annualized_basis_3m` 用滚动 3 个月合约。
- **CME 与加密所的时间**：CME 交易时段 CT 17:00–16:00（次日），周末休市；CME 周末缺口（gap）分析需对齐 UTC。

## 8. 变更记录
- 2026-10 初版。
