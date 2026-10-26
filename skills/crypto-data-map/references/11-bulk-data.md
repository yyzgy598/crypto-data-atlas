# 11 · 历史全量数据下载与采集模式

目录
1. 交易所官方历史数据门户（Binance Vision、Bybit、OKX、Bitget、Gate、Deribit、BitMEX S3、Coinbase、Kraken、Bitfinex、Bitstamp、KuCoin、Hyperliquid S3、dYdX、Drift S3）
2. 第三方历史数据：Tardis、Kaiko、CoinAPI Flat Files、CCData、Crypto Lake、CryptoDataDownload、Kaggle、Databento（CME）、Amberdata、Coin Metrics、Dune/BigQuery/AWS（见 04）、Binance Research、Bitcoinity、Cryptowatch（退）、Nomics（退）
3. 采集模式：REST 翻页策略、WS 断线与序列号校验、盘口快照同步、限频与多 IP、时间对齐、幂等落库、数据质量校验
4. 开源采集框架与库：CCXT、cryptofeed、cryptostore、tardis-machine、Hummingbot、Nautilus Trader、Freqtrade、Jesse、Barter（Rust）、ccapi（C++）、binance-connector、okx-sdk、bybit-sdk、hyperliquid-python-sdk、websockets/aiohttp 模板
5. 存储与格式建议
6. 变更记录

---

## 1. 交易所官方历史数据门户
| 交易所 | 入口 | 内容 | 格式/粒度 | 备注 |
|---|---|---|---|---|
| Binance | `https://data.binance.vision/`（浏览 `https://data.binance.vision/?prefix=data/spot/daily/klines/BTCUSDT/1m/`）；路径规则 `data/{spot|futures/um|futures/cm|option}/{daily|monthly}/{klines|trades|aggTrades|bookDepth|bookTicker|indexPriceKlines|markPriceKlines|premiumIndexKlines|metrics|liquidationSnapshot|BVOLIndex|EOHSummary}/{SYMBOL}/[{interval}/]{SYMBOL}-{type}-{yyyy-mm[-dd]}.zip`，每个 zip 配 `.CHECKSUM` | 现货：klines（所有周期）、trades、aggTrades；U 本位：klines、trades、aggTrades、indexPriceKlines、markPriceKlines、premiumIndexKlines、**bookDepth**（每 1000ms 快照，±1%~±5% 档位，2023 起）、**bookTicker**（逐 tick 最优买卖）、**metrics**（5 分钟 OI、多空比、主动买卖比，2021.12 起）、**liquidationSnapshot**（清算快照，抽样）；币本位同；期权：BVOLIndex、EOHSummary | CSV in ZIP；日/月 | **免费、无需登录、最常用**；`bookDepth` 不是全量深度；aggTrades 回溯到 2017.8；用 `https://github.com/binance/binance-public-data` 脚本批量下载 |
| Bybit | `https://public.bybit.com/`（`trading/{SYMBOL}/{SYMBOL}{yyyy-mm-dd}.csv.gz`（永续/交割逐笔）、`spot/{SYMBOL}/...`、`kline_for_metatrader4/`、`premium_index/`、`spot_index/`、`trading_option/`、`option_index/`） | 逐笔成交（2019.10 起）、MT4 K 线、溢价指数、期权成交 | CSV.gz；日 | 免费；无盘口/OI/资金费归档（用 REST） |
| OKX | `https://www.okx.com/data-download`（登录后下载：aggtrades、trades、swaprate、allswaprate、options tickers、allfuturesinstruments 等按日 zip；也有 CDN `https://static.okx.com/cdn/okex/traderecords/{aggtrades|trades|swaprate|allswaprate}/daily/{yyyymmdd}/{INST}-{type}-{yyyy-mm-dd}.zip`） | 现货/合约/期权逐笔、资金费率 | CSV in ZIP；日 | 需登录（部分 CDN 直链可用）；历史约 2 年 |
| Bitget | `https://www.bitget.com/data-download`（登录；现货/合约逐笔、K 线） | 逐笔、K 线 | CSV | — |
| Gate.io | `https://www.gate.io/developers/data-download`、`https://download.gatedata.org/{spot|futures_usdt|futures_btc}/{candlesticks_1m|orderbooks|trades}/{yyyymm}/{PAIR}-{yyyymm}.csv.gz` | 现货/合约 K 线、逐笔、**订单簿快照**（2019 起） | CSV.gz；月 | 免费直链；盘口为 1 秒快照 |
| Deribit | 无官方归档；历史通过 REST `get_last_trades_by_currency_and_time`、`get_tradingview_chart_data`、`get_funding_rate_history`、`get_volatility_index_data`、`get_settlement_history_*` 翻页（无深度限制）；Tardis 有 Deribit 全量 WS 录制（2019.3 起，含期权盘口） | 成交、K 线、资金费、DVOL、结算 | JSON | 期权 IV 曲面历史只能 Tardis/Laevitas/Amberdata |
| BitMEX | `https://public.bitmex.com/?prefix=data/trade/`（`data/trade/{yyyymmdd}.csv.gz`）、`data/quote/{yyyymmdd}.csv.gz`（**最优买卖报价逐 tick**） | 全部合约逐笔成交与报价，2014.11 起至今 | CSV.gz；日 | **免费、最长历史的永续数据**；REST `trade/bucketed`、`funding` 可补 |
| Coinbase Exchange | 无官方归档；REST `products/{id}/trades`（`after`/`before` 翻页，**全历史 2015 起**）、`candles`（300/次）；Coinbase 数据产品 `https://www.coinbase.com/data`（机构） | 成交、K 线 | JSON | 用 Tardis/Kaiko 取盘口 |
| Kraken | `https://support.kraken.com/hc/en-us/articles/360047124832-Downloadable-historical-OHLCVT-data`（**季度 zip：全部交易对 1/5/15/30/60/240/720/1440 分钟 OHLCVT，2013 起，Google Drive**）、`https://support.kraken.com/hc/en-us/articles/360047543791`（逐笔 CSV）；REST `Trades?since=` 全历史 | OHLCVT、逐笔 | CSV | 免费；季度更新 |
| Bitfinex | REST `candles/trade:1m:tBTCUSD/hist?limit=10000&start=&end=`（**全历史分钟 K 线，2013 起**）、`trades/tBTCUSD/hist?limit=10000`（全历史逐笔）、`stats1/...`（多空持仓历史）；无归档 | — | JSON | 免费、限频 90/min |
| Bitstamp | REST `ohlc/{pair}/?step=60&limit=1000&start=`（**全历史 2011 起**）、`transactions`（近 24h）；Bitstamp 数据 `https://www.bitstamp.net/market-data/`（机构）；Bitcoincharts `https://api.bitcoincharts.com/v1/csv/bitstampUSD.csv.gz`（**2011 起全量逐笔 CSV，免费**；也有 coinbaseUSD、krakenUSD、bitfinexUSD、localbtcUSD 等老所） | K 线、逐笔 | CSV | Bitcoincharts 是最老的免费逐笔归档 |
| KuCoin | 无归档；REST `market/candles`（1500/次）、合约 `kline/query`；Tardis 含 | — | — | — |
| HTX / MEXC / BingX / Phemex / CoinEx / WhiteBIT / LBank / Poloniex | 无归档（Poloniex 旧 `returnChartData` 全历史 2014 起已退）；REST 翻页；Tardis（Huobi、Phemex、Woo、Poloniex）；CoinAPI/Kaiko | — | — | — |
| Hyperliquid | S3 `s3://hl-mainnet-node-data/`（`explorer_blocks/`、`node_fills_by_block/hourly/{yyyymmdd}/{h}.lz4`（2024+）、`node_trades/`、`node_order_statuses/`、`replica_cmds/{ts}/{yyyymmdd}/{height}.lz4`、`periodic_abci_states/`、`market_data/{yyyymmdd}/{h}/l2Book/{coin}.lz4`（**L2 盘口快照每 1s? 2023.4 起部分**）、`market_data/.../l4Book/`（2025）；`aws s3 ls s3://hl-mainnet-node-data/ --request-payer requester`，**requester pays**）；`https://stats-data.hyperliquid.xyz/Mainnet/...`（社区 JSON 日级：`daily_usd_volume`、`daily_usd_volume_by_coin`、`daily_usd_volume_by_user`、`daily_notional_liquidated_total`、`daily_notional_liquidated_by_coin`、`daily_notional_liquidated_by_leverage_type`、`daily_unique_users`、`cumulative_*`、`open_interest`、`funding_rate`、`hlp_liquidator_pnl`、`hlp_positions`、`asset_ctxs`、`liquidity_by_coin`、`largest_users_by_usd_volume`、`largest_user_depositors`、`largest_liquidated_notional_by_user`、`largest_user_trade_count`、`total_accrued_fees`、`cumulative_new_users`、`daily_trades_by_coin`、`daily_trades_by_user`、`cumulative_inflow`、`daily_inflow`、`cumulative_hlp_liquidator_pnl`）；REST `candleSnapshot`（5000/次，1m 回溯有限）、`fundingHistory`（500/次，全历史）、`userFillsByTime`（2000/次，全历史） | 全量订单/成交/盘口（S3）；日级统计（社区） | lz4 + JSON | S3 是唯一全量；Tardis 2024 起录制 Hyperliquid WS；Allium/Dune 有解析后的表 |
| dYdX v4 | Indexer REST（`candles` 1000/次、`trades`、`historicalFunding`，全历史）；全节点快照 `https://docs.dydx.xyz/nodes/snapshots`（Polkachu/KingNodes）；Numia 数据集；Tardis（dYdX v3/v4） | — | JSON | — |
| Drift | S3 `https://drift-historical-data-v2.s3.eu-west-1.amazonaws.com/program/dRiftyHA39MWEi3m9aunc5MzRF1JYuBsbn6VPcn33UH/{market|user}/{marketName|authority}/{tradeRecords|fundingRateRecords|fundingPaymentRecords|liquidationRecords|settlePnlRecords|depositRecords|lpRecords|insuranceFundRecords|insuranceFundStakeRecords|swapRecords|candles/{resolution}}/{year}/{yyyymmdd}` | 全量永续事件 CSV | CSV；日 | **免费公开，Solana 永续最完整** |
| GMX / Jupiter / Aevo / Vertex / Orderly / Paradex / Lighter / Aster | 子图/Indexer 翻页；Dune/Allium/Goldsky；Tardis（Aevo、Vertex?）；无官方归档 | — | — | — |
| CME | DataMine（付费）、Databento（按量，`GLBX.MDP3`）、CME 结算/成交 CmeWS 非正式 JSON（当日）、CFTC COT（见 07） | — | — | — |

---

## 2. 第三方历史数据
| 服务 | 覆盖 | 格式/访问 | 价格 | 备注 |
|---|---|---|---|---|
| Tardis.dev | 40+ CEX/DEX 原始 WS 消息（trades、L2 增量、L3（Coinbase/Bitfinex/Kraken/Hyperliquid 2025）、quotes、derivative_ticker、liquidations、options_chain），2019.3 起 | Datasets CSV.gz（`https://datasets.tardis.dev/v1/{exchange}/{dataType}/{yyyy}/{mm}/{dd}/{SYMBOL}.csv.gz`）、原始 API、tardis-machine 回放 | 按交易所月费（$100–$1000+/所），每月第 1 日免费 | 回测/盘口重建标配 |
| Kaiko | 100+ CEX 逐笔自 2010/2014、L2 快照、DEX 事件、衍生品、参考价 | REST/Stream/CSV 交付/Snowflake | 机构 | 合规基准 |
| CoinAPI Flat Files | 380+ 所 trades/quotes/orderbooks（L2 快照+更新）/OHLCV，2010 起 | S3 式 `https://s3.coinapi.io/`（parquet/csv.gz 按日）、`GET /v1/flatfiles` 列表 | 按 GB 或订阅 | 覆盖最广 |
| CCData（CryptoCompare）| 逐所分钟 OHLCV 多年、逐笔（部分）、CADLI 指数、OI/资金费 | REST（免费层可拉）、Enterprise CSV | 免费～企业 | 免费拉分钟级历史的最佳选择 |
| Crypto Lake（`https://crypto-lake.com/`） | Binance/Bybit/OKX/Coinbase/Kraken/Gate/KuCoin/Bitget/Hyperliquid 等 L2 盘口（book、book_delta_v2）、trades、candles、funding、OI，2022 起 | Python `lakeapi`（`lakeapi.load_data(table='book', start=, end=, symbols=, exchanges=)`，parquet on S3） | 免费样本 + 订阅（比 Tardis 便宜） | 盘口数据性价比 |
| CryptoDataDownload（`https://www.cryptodatadownload.com/data/`） | Binance/Coinbase/Bitstamp/Gemini/Kraken/Bitfinex/Poloniex/Bittrex/HitBTC/KuCoin/OKX/Bybit/Gate 日/小时/分钟 OHLCV（部分逐笔、盘口样本） | CSV 直链（`https://www.cryptodatadownload.com/cdd/Binance_BTCUSDT_1h.csv`） | 免费 | 快速原型 |
| Kaggle 数据集 | "Bitcoin Historical Data"（Bitstamp 1m 2012 起，持续更新）、"Binance Full History"、"Cryptocurrency Historical Prices"、"G-Research Crypto Forecasting"、Ethereum 链上数据集、Solana、NFT、Reddit/Twitter 情绪集 | CSV/Parquet | 免费 | 质量参差，核对来源 |
| Databento | CME（BTC/ETH/MBT/MET 期货与期权，MBO/MBP-10/TBBO/OHLCV/statistics/definitions）、CBOE、Nasdaq/NYSE（COIN/MSTR/IBIT）、OPRA（IBIT/MSTR 期权） | Python/REST/Live；按量付费（$125 起充值） | 低价全量 | 传统所最便宜 |
| Amberdata | CEX/DEX/期权/链上 2010 起 | REST/WS/S3 交付 | 机构 | — |
| Coin Metrics | 市场数据（逐笔/盘口/资金费/OI/清算/期权）+ 网络数据 | REST/WS/Flat files（Pro） | Community 免费日级；Pro 付费 | — |
| Bitcoinity（`https://data.bitcoinity.org/`）、Bitcoincharts（`https://api.bitcoincharts.com/v1/csv/`，**老所全量逐笔 CSV 免费**）、Cryptowatch（Kraken，2023 关）、Nomics（2023 关）、Messari Historical（付费）、CoinGecko/CMC 历史（付费层）、Investing.com 历史 CSV（抓取）、Yahoo `BTC-USD` 日线（CMC 源）、Quandl BCHAIN（Blockchain.com 镜像，免费）、Glassnode CSV 导出（付费）、Binance Research 报告数据、Coinglass CSV（付费层导出） | — | — | — | — |
| 链上全量 | 见 04：BigQuery、AWS Public Blockchain、Blockchair dumps（`https://gz.blockchair.com/{bitcoin|ethereum|...}/{blocks|transactions|outputs|inputs|erc-20/transactions|...}/`，**TSV.gz 每日，免费**）、Hyperliquid S3、Near Lake、Solana Bigtable（Google 公共 `solana-mainnet` 归档需凭据；Old Faithful `https://old-faithful.net/`，**Solana 历史账本 CAR 文件，免费**）、Ethereum era files（`https://era.ithaca.xyz/`、`https://mainnet.era1.nimbus.team/`，**历史区块归档**）、Bitcoin 区块文件（自建节点 `blocks/*.dat`，或 `https://bitcoin-blocks.s3.amazonaws.com`? 用 torrent/IBD）、Erigon 快照（`https://github.com/erigontech/erigon-snapshot`，torrent）、Reth/Geth 快照（各 RPC 商）、Cosmos 快照（Polkachu）、Allium/Dune/Flipside 导出 | — | — | — | — |

---

## 3. 采集模式（通用做法）
### REST 翻页
- **按时间窗**：Binance `klines`/`aggTrades` 用 `startTime/endTime` + `limit=1000`，取返回最后一条时间 +1ms 作为下一窗起点；注意 `endTime` 与 `startTime` 跨度限制（aggTrades 1 小时、合约 klines 无、`fundingRate` 无）。
- **按游标/ID**：Binance `aggTrades?fromId=`、OKX `after=`（tradeId/ts）、Bybit `cursor`、Coinbase `after/before`、Kraken `since`（纳秒）、BitMEX `start`、Bitfinex `start/end` + `sort=1`、Hyperliquid `startTime`（`userFillsByTime`、`fundingHistory`）、Gate `last_id`、KuCoin `startAt/endAt`、Deribit `start_timestamp/end_timestamp` + `count`。
- **历史深度上限**：Binance `/futures/data/*` 30 天；OKX `history-trades` 3 个月；Bitget `fills-history` 7 天；Kraken `OHLC` 720 根；HTX `history/kline` 2000 根无时间参数；Hyperliquid `historicalOrders` 2000 条、`candleSnapshot` 5000 根；Upbit `trades/ticks` 7 天；Dexscreener 无历史。超出上限的必须持续落库或改用第三方。
- **去重键**：成交用 `(exchange, symbol, trade_id)`；K 线用 `(exchange, symbol, interval, open_time)`；资金费用 `(exchange, symbol, funding_time)`；OI 快照用 `(exchange, symbol, ts)`；Hyperliquid 订单用 `(wallet, oid, status, statusTimestamp)`（事件日志语义）。
- **时间对齐**：统一 UTC ms；K 线用开盘时间；Kraken/Coinbase 秒级要 ×1000；OKX 字符串 ms；Deribit ms；Hyperliquid `t`（开）/`T`（收）；日线边界各所 UTC 00:00（Upbit KST 09:00 对应 UTC 00:00；部分所"日线"是本地时间）。
- **限频**：读响应头（Binance `X-MBX-USED-WEIGHT-1M`、Bybit `X-Bapi-Limit-Status`、OKX 无、CoinGecko 无、Coinglass 无、Etherscan 无）；429 退避（指数 + 抖动）；418/403 停止一段时间；多 IP/代理池按所分流（Binance 按 IP 计权重，Hyperliquid 按 IP + 地址）；对 Hyperliquid 用 `ExecutorCompletionService` 滑动窗口并发（本仓库做法）。

### WebSocket
- **心跳**：Binance 服务端 ping 每 3 分钟需 pong，24h 强制断；Bybit 客户端每 20s 发 `{"op":"ping"}`；OKX 30s 内无数据需发 `ping`；Hyperliquid 60s 无消息断开，发 `{"method":"ping"}`；Deribit JSON-RPC `public/set_heartbeat`；Coinbase `heartbeats` 频道；Kraken v2 `ping`；Gate `spot.ping`。
- **序列号校验**：Binance 深度增量 `U/u/pu`（合约有 `pu` 前一更新 id）必须与 REST 快照 `lastUpdateId` 衔接，缺口则重拉快照；Bybit `u` + `seq`；OKX `seqId/prevSeqId` + `checksum`（CRC32）；Coinbase `sequence`；Kraken `checksum`；Hyperliquid `l2Book` 为全量快照（无增量，`time` 字段）；Deribit `change_id/prev_change_id`。
- **断线重连**：指数退避 + 重新订阅 + 以 REST 快照回补断线期间（成交用 `aggTrades` 按时间补；盘口重拉快照；Hyperliquid 用 `userFillsByTime` 补用户成交）。
- **多路复用**：Binance 单连接 ≤1024 流、每秒 ≤5 条订阅消息；Bybit 每连接 ≤10 args/次（spot）、linear 无限但建议 ≤500；OKX 每连接 ≤240 订阅、每小时 480 次连接；Hyperliquid 每 IP ≤100 连接、≤1000 订阅、每分钟 ≤2000 消息。
- **消息时间**：用交易所事件时间（Binance `E`、Bybit `ts`、OKX `ts`、Hyperliquid `time`），同时记录本地接收时间，监控延迟。

### 落库与质量
- 幂等 upsert（MySQL `INSERT ... ON DUPLICATE KEY UPDATE`，本仓库 `upsertBatch`）；大表按日/月分区；K 线用 `DECIMAL` 或字符串保留精度。
- 完整性校验：K 线连续性（相邻 open_time 差 = interval）、成交 id 连续（Binance aggTrades id 连续）、每日条数与官方归档对比（`data.binance.vision` 月文件抽样）。
- 口径字段：保留 `source`、`fetched_at`、原始 JSON（或关键原始字段）以便追溯；聚合商数据与交易所原生分表。
- 多源冗余：主源交易所原生 + 备源 CCData/Coinalyze/Coinglass，差异报警。

---

## 4. 开源采集框架与库
| 工具 | 语言 | 用途 | 备注 |
|---|---|---|---|
| CCXT | Python/JS/PHP/C#/Go | 100+ 所统一 REST + WS（`ccxt.pro` 已并入） | 见 01；快速原型；高频用原生 |
| cryptofeed | Python | 多所 WS 采集框架（trades、l2/l3 book、ticker、funding、OI、liquidations、candles），后端 Kafka/Redis/Postgres/InfluxDB/Arctic/Parquet/ZMQ/RabbitMQ/GCP PubSub | Binance/Bybit/OKX/Deribit/Kraken/Coinbase/Bitfinex/Bitstamp/Gemini/HTX/Gate/KuCoin/BitMEX/Phemex/dYdX/Hyperliquid(社区 PR)；配 `cryptostore` 持久化 |
| tardis-machine / tardis-dev（Node）/ tardis-client（Python） | Node/Python | 历史回放 + 实时标准化多所 WS | 付费数据 |
| Hummingbot | Python | 做市/套利机器人，含 60+ 所连接器（含 Hyperliquid、dYdX、Vertex、Derive）与数据采集 | 连接器可复用 |
| Nautilus Trader | Python/Rust | 事件驱动回测+实盘，适配器 Binance/Bybit/OKX/dYdX/Deribit/Coinbase Intl/Kraken/Hyperliquid(2025)/Databento/Tardis/Polymarket | 高性能 |
| Freqtrade / Jesse / Backtrader / vectorbt / Zipline-crypto / QuantConnect LEAN（含 Binance/Coinbase/Kraken/Bybit/Bitfinex 数据） | Python/C# | 回测与策略 | Freqtrade 基于 CCXT 下载历史（`freqtrade download-data`） |
| Barter-rs、ccapi（C++ 多所 WS）、go-binance、binance-connector-python/js/java、okx-sdk、pybit、bybit-api（Node）、python-kucoin、gate-api、huobi-sdk、deribit-api、hyperliquid-python-sdk / hyperliquid-rust-sdk / hyperliquid-ts（nktkas）、dydx-v4-client、drift-sdk/driftpy、jupiter-ts、solana-py/solders、web3.py/ethers/viem、cryo（链上抽数）、polymarket py-clob-client、kalshi-python | 各语言 | 原生 SDK | 高频/低延迟选原生 |
| 数据管道：Airflow/Dagster/Prefect 调度、Kafka/Redpanda 流、ClickHouse/TimescaleDB/QuestDB/InfluxDB/DuckDB/Parquet+Iceberg 存储、Arctic/ArcticDB（Man Group，tick 数据）、kdb+（机构）、Pandas/Polars 处理、Great Expectations 质量校验 | — | 存储与质量 | 见下 |

---

## 5. 存储与格式建议
- **逐笔/盘口**：Parquet（按 exchange/symbol/date 分区）+ DuckDB/ClickHouse 查询；ArcticDB 适合 tick 级 Python 工作流。
- **K 线/资金费/OI**：MySQL/Postgres/TimescaleDB 关系表即可；本仓库用 MySQL + 幂等 upsert。
- **链上事件**：ClickHouse 或 Postgres（Goldsky Mirror/Subsquid 输出）；大规模用 BigQuery/Athena。
- **精度**：价格/数量用 `DECIMAL(38,18)` 或字符串；Hyperliquid 价格 5 位有效数字、数量按 `szDecimals`。
- **时间**：全部 UTC，存 `BIGINT` ms 或 `TIMESTAMP(3)`；K 线存 open_time，另存 close_time 便于查询。
- **元数据表**：`exchange_symbol_map`（统一 symbol ↔ 各所原生 symbol、合约乘数、结算周期、上/下架时间），是跨所对比的前提。

## 6. 变更记录
- 2026-10 初版。
