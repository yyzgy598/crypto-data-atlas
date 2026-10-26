# 03 · 行情聚合与市场数据商

目录
1. 免费/准免费聚合：CoinGecko、CoinMarketCap、CryptoCompare(CCData)、Coinpaprika、CoinCap、LiveCoinWatch、Mobula、CoinStats、Cryptorank、CoinLore、Messari（基础）
2. 机构级市场数据：Kaiko、Coin Metrics、Amberdata、CoinAPI、Tardis、CryptoCompare 企业版、CoinDesk Indices、Lukka、Digital Asset Research、S&P/Bloomberg/Refinitiv 加密指数
3. Coinglass（概览，细节见 07）
4. 预言机价格：Pyth、Chainlink、RedStone、Band、API3、Switchboard、Chronicle、Stork、DIA
5. 指数与参考价：CME CF、Coinbase/Kraken 指数、Deribit 指数、Binance 指数成分、Bitwise、CoinDesk 指数、MarketVector(MVIS)、Galaxy/Bloomberg
6. 口径与选型建议
7. 变更记录

---

## 1. 免费/准免费聚合

### CoinGecko
- 文档：https://docs.coingecko.com/reference/introduction
- Base：免费 Demo `https://api.coingecko.com/api/v3/`（需 `x-cg-demo-api-key`，30 req/min，10k/月）；Pro `https://pro-api.coingecko.com/api/v3/`（`x-cg-pro-api-key`，Analyst 500 req/min 起）
- 核心接口
  - `ping`、`key`（用量）
  - `simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true&precision=full`
  - `simple/token_price/{platform_id}?contract_addresses=&vs_currencies=`
  - `simple/supported_vs_currencies`
  - `coins/list?include_platform=true`（全部币 id ↔ 合约地址映射，**代币元数据对齐的基础表**）
  - `coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page=1&sparkline=false&price_change_percentage=1h,24h,7d&category=`（排行榜，一次 250）
  - `coins/{id}?localization=false&tickers=true&market_data=true&community_data=true&developer_data=true&sparkline=false`（全量详情：各交易所 tickers、社区/开发者数据、ATH/ATL、供应、分类、链接）
  - `coins/{id}/tickers?exchange_ids=&include_exchange_logo=&page=&order=&depth=true`（**每个币在各交易所的交易对、价格、量、trust_score、spread、±2% 深度**）
  - `coins/{id}/history?date=30-12-2023&localization=false`（某日快照）
  - `coins/{id}/market_chart?vs_currency=usd&days=max&interval=daily&precision=`（价格/市值/成交量时序；免费 1 天内 5 分钟粒度、90 天内小时、以上日级；Pro 可 `interval=5m/hourly`，Enterprise 可全历史 5m）
  - `coins/{id}/market_chart/range?vs_currency=&from=&to=`
  - `coins/{id}/ohlc?vs_currency=usd&days=1|7|14|30|90|180|365|max`（免费粒度自动：1–2 天 30min，3–30 天 4h，31+ 天 4 天；Pro `interval=hourly|daily` + `ohlc/range`）
  - `coins/{id}/contract/{contract_address}`、`coins/{platform_id}/contract/{addr}/market_chart`、`/market_chart/range`
  - `coins/categories/list`、`coins/categories?order=market_cap_desc`（**赛道市值/涨跌**）
  - `coins/top_gainers_losers?vs_currency=usd&duration=24h`（Pro）、`coins/list/new`（Pro，最近 200 新币）
  - `asset_platforms?filter=nft`、`token_lists/{asset_platform_id}/all.json`
  - `exchanges?per_page=250`（交易所列表含 `trust_score`、`trade_volume_24h_btc`、`trade_volume_24h_btc_normalized`）、`exchanges/list`、`exchanges/{id}`、`exchanges/{id}/tickers`、`exchanges/{id}/volume_chart?days=`、`exchanges/{id}/volume_chart/range`（Pro）
  - `derivatives`（全部永续/交割 tickers：price、index、basis、spread、funding_rate、open_interest、volume_24h、expired_at）、`derivatives/exchanges?order=open_interest_btc_desc`、`derivatives/exchanges/{id}?include_tickers=all`、`derivatives/exchanges/list`
  - `nfts/list`、`nfts/{id}`、`nfts/{asset_platform}/contract/{addr}`、`nfts/markets`（Pro）、`nfts/{id}/market_chart`（Pro）、`nfts/{id}/tickers`
  - `exchange_rates`（BTC 对各法币/商品汇率）
  - `search?query=`、`search/trending`（**热搜币/NFT/分类**）
  - `global`（总市值、BTC/ETH 占比、活跃币数、市场数）、`global/decentralized_finance_defi`、`global/market_cap_chart?days=`（Pro）
  - `companies/public_treasury/{bitcoin|ethereum}`（**上市公司持币**）
  - Pro 专属：`coins/{id}/circulating_supply_chart`、`/total_supply_chart`、`exchanges/{id}/volume_chart/range`、`onchain/*`（GeckoTerminal 数据，见 02）
- 坑：免费层 `market_chart` 过去 365 天以上只给日级；id 不等于 symbol（`bitcoin` vs `btc`，重名币多，用 `coins/list` 对齐）；更新延迟 1–10 分钟；`coins/{id}` 权重大；`derivatives` 的 funding_rate 为百分比字符串。

### CoinMarketCap
- 文档：https://coinmarketcap.com/api/documentation/v1/
- Base：`https://pro-api.coinmarketcap.com/`（`X-CMC_PRO_API_KEY`）；沙盒 `https://sandbox-api.coinmarketcap.com/`；免费 Basic 10k credits/月、30 req/min，仅 latest 类接口；Hobbyist/Startup/Standard/Professional/Enterprise 解锁历史。
- 核心接口
  - `v1/cryptocurrency/map?listing_status=active,untracked&start=&limit=5000&sort=cmc_rank`（id、slug、symbol、platform/合约地址、first_historical_data）
  - `v2/cryptocurrency/info?id=&slug=&address=&aux=urls,logo,description,tags,platform,date_added,notice,status`（元数据：合约地址多链、标签、官网、白皮书、Twitter、`self_reported_*`）
  - `v1/cryptocurrency/listings/latest?start=1&limit=5000&convert=USD&sort=market_cap&cryptocurrency_type=all&tag=all&aux=num_market_pairs,cmc_rank,date_added,tags,platform,max_supply,circulating_supply,total_supply,market_cap_by_total_supply,volume_24h_reported,volume_7d,volume_30d,is_market_cap_included_in_calc`
  - `v1/cryptocurrency/listings/historical?date=`（付费，历史排行）、`v1/cryptocurrency/listings/new`（Startup+）
  - `v2/cryptocurrency/quotes/latest?id=&symbol=&slug=&convert=USD,BTC&aux=...`（批量最新报价，`volume_change_24h`、`percent_change_1h/24h/7d/30d/60d/90d`、`market_cap_dominance`、`fully_diluted_market_cap`、`tvl`）
  - `v2/cryptocurrency/quotes/historical?id=&time_start=&time_end=&count=&interval=5m|10m|15m|30m|45m|1h|2h|3h|4h|6h|12h|24h|1d|2d|3d|7d|14d|15d|30d|60d|90d|365d`（Hobbyist 1 个月历史，Startup 1 年，Standard 全部；5m 粒度仅 Enterprise 以下按套餐）
  - `v2/cryptocurrency/ohlcv/latest`、`v2/cryptocurrency/ohlcv/historical?id=&time_period=daily|hourly&time_start=&time_end=&count=&interval=`
  - `v2/cryptocurrency/market-pairs/latest?id=&limit=&category=spot|derivatives|otc|perpetual|futures&fee_type=&aux=num_market_pairs,category,fee_type,market_url,currency_name,currency_slug,price_quote,notice,cmc_rank,effective_liquidity,market_score,market_reputation`（**各交易所交易对、流动性分、交易所评分**）
  - `v2/cryptocurrency/price-performance-stats/latest?id=&time_period=all_time,yesterday,24h,7d,30d,90d,365d`（ATH/ATL、区间最高最低）
  - `v1/cryptocurrency/categories`、`v1/cryptocurrency/category?id=`（赛道）
  - `v1/cryptocurrency/airdrops`、`v1/cryptocurrency/airdrop?id=`
  - `v1/cryptocurrency/trending/latest`、`/trending/most-visited`、`/trending/gainers-losers?time_period=24h&sort_dir=desc`
  - `v1/exchange/map`、`v1/exchange/info?id=`（含 `spot_volume_usd`、`weekly_visits`、`fiats`、`maker_fee`/`taker_fee`、`urls`）、`v1/exchange/listings/latest?sort=exchange_score|volume_24h`（含 `exchange_score`、`liquidity_score`、`num_coins`、`num_market_pairs`、`traffic_score`）、`v1/exchange/quotes/latest`、`v1/exchange/quotes/historical`、`v1/exchange/market-pairs/latest?id=&category=spot&limit=5000`、`v1/exchange/assets?id=`（**交易所公开钱包资产 / 储备证明**）
  - `v1/global-metrics/quotes/latest`（总市值、24h 量、BTC/ETH 占比、DeFi/稳定币量、`derivatives_volume_24h`、`derivatives_24h_percentage_change`）、`v1/global-metrics/quotes/historical?time_start=&time_end=&interval=`
  - `v2/tools/price-conversion?amount=&id=&convert=`、`v1/tools/postman`
  - `v1/blockchain/statistics/latest?symbol=BTC,ETH`（块高、难度、哈希率、出块时间、矿工奖励、待处理交易）
  - `v3/fear-and-greed/latest`、`v3/fear-and-greed/historical?start=&limit=`（**CMC 恐惧贪婪指数**）
  - `v1/content/latest?id=&news_type=news|alexandria|all&content_type=all|news|video|audio`、`v1/content/posts/top`、`/posts/latest`、`/posts/comments`（CMC Community 帖子）
  - `v1/community/trending/topic`、`/trending/token`
  - `v3/index/cmc100-latest`、`v3/index/cmc100-historical`（CMC100 指数）
  - DEX（v4，2024 新增）：`v4/dex/listings/quotes`、`v4/dex/listings/info`、`v4/dex/networks/list`、`v4/dex/pairs/quotes/latest?contract_address=&network_slug=`、`v4/dex/pairs/ohlcv/latest|historical`、`v4/dex/pairs/trade/latest`、`v4/dex/spot-pairs/latest`
- 坑：免费层无历史；`convert` 多币种多扣 credit；symbol 重名多，始终用 `id`；市值口径（`circulating_supply` 由 CMC 核验，`self_reported` 另列）与 CoinGecko 不同。

### CryptoCompare → CCData
- 文档：https://developers.ccdata.io/documentation/data-api/introduction （新 Data API）；旧 Min-API https://min-api.cryptocompare.com/documentation
- Base：新 `https://data-api.ccdata.io/`（`Authorization: Apikey <key>`，免费 Developer 层 ~250k 调用/月）；旧 `https://min-api.cryptocompare.com/data/`（免费 100k/月，无 key 也能少量用）
- 新 Data API
  - Spot：`spot/v1/latest/tick?market=binance&instruments=BTC-USDT&apply_mapping=true`、`spot/v1/historical/{minutes|hours|days}?market=&instrument=&limit=2000&to_ts=&aggregate=1&fill=true&apply_mapping=true`（**逐交易所 OHLCV，分钟级可回溯多年**）、`spot/v1/historical/trades?market=&instrument=&after_ts=`、`spot/v1/historical/trades/hour`、`spot/v1/historical/orderbook/l2/metrics/minute`、`spot/v1/latest/instrument/metadata`、`spot/v1/markets`、`spot/v1/markets/instruments?market=&instrument_status=ACTIVE`
  - Futures：`futures/v1/latest/tick?market=binance&instruments=BTC-USDT-VANILLA-PERPETUAL`、`futures/v1/historical/{minutes|hours|days}`、`futures/v1/historical/funding-rate/{minutes|hours|days}`、`futures/v1/historical/open-interest/{minutes|hours|days}`、`futures/v1/latest/funding-rate/tick`、`futures/v1/latest/open-interest/tick`、`futures/v1/markets`、`futures/v1/markets/instruments`
  - Options：`options/v1/latest/tick`、`options/v1/historical/{days}`、`options/v1/markets`
  - Index：`index/cc/v1/latest/tick?market=cadli&instruments=BTC-USD`（CADLI = CCData 聚合指数，取代 CCCAGG）、`index/cc/v1/historical/{minutes|hours|days}?market=cadli&instrument=BTC-USD&limit=2000&to_ts=`（**跨所综合价格历史**）、`index/cc/v1/historical/messages`、`index/cc/v1/markets/instruments`
  - On-chain：`onchain/v1/data/by-address?chain_asset=ETH&address=`、`onchain/v1/blocks/{chain_asset}/...`、`onchain/v1/historical/supply/days?asset=`、`onchain/v2/historical/...`
  - Asset：`asset/v1/metadata?asset=BTC&asset_lookup_priority=SYMBOL`（含 `SUPPLY_*`、`LAUNCH_DATE`、`WEBSITE_URL`、`EXPLORER_ADDRESSES`、`SMART_CONTRACT_ADDRESSES`、社交指标、代码仓库指标）、`asset/v1/top/list?page_size=100&sort_by=CIRCULATING_MKT_CAP_USD`、`asset/v1/summary/list`、`asset/v1/events`（**代币事件：升级、解锁、硬分叉**）、`asset/v1/historical/code-repository/days`、`asset/v1/historical/discord/days`、`asset/v1/historical/reddit/days`、`asset/v1/historical/telegram/days`、`asset/v1/historical/twitter/days`
  - News：`news/v1/article/list?lang=EN&limit=100&categories=&exclude_categories=&source_ids=`、`news/v1/source/list`、`news/v1/category/list`
  - Overview：`overview/v1/latest/marketcap/all/tick`、`overview/v1/historical/marketcap/all/days`
  - Reference Rates、Exchange Benchmark（交易所评级，`exchange/v1/...`）
  - WS：`wss://data-streamer.cryptocompare.com/?api_key=`（旧）/ `wss://data-streamer.ccdata.io`（`SUBSCRIBE` 到 `0~Coinbase~BTC~USD`（trade）、`2~...`（current）、`5~CCCAGG~BTC~USD`、`8~...`（orderbook）、`30~...`（funding）等频道）
- 旧 Min-API 常用：`price?fsym=BTC&tsyms=USD,EUR`、`pricemulti`、`pricemultifull`、`v2/histoday|histohour|histominute?fsym=&tsym=&limit=2000&toTs=&e=CCCAGG|binance`、`top/totalvolfull`、`top/mktcapfull`、`top/exchanges`、`all/coinlist`、`all/exchanges`、`exchanges/general`、`blockchain/histo/day?fsym=`（链上日指标）、`social/coin/histo/day`、`v2/news/?lang=EN`、`v4/all/exchanges`、`exchange/histoday`。
- 坑：`histominute` 旧接口只保留 7 天分钟数据；新 Data API 分钟级有多年；免费层 WS 有限；指数 CADLI 替代 CCCAGG。

### 其他免费聚合速查
| 数据商 | 文档 | Base | 认证/限频 | 特色 | 备注 |
|---|---|---|---|---|---|
| Coinpaprika | https://api.coinpaprika.com/ | `https://api.coinpaprika.com/v1/` ；Pro `https://api-pro.coinpaprika.com/v1/` | 免费无 key 20k/月（约 10 req/s）；Pro 有历史 | `global`、`coins`、`coins/{id}`、`coins/{id}/twitter`、`coins/{id}/events`、`coins/{id}/exchanges`、`coins/{id}/markets`、`coins/{id}/ohlcv/latest`、`coins/{id}/ohlcv/historical?start=&end=&interval=1d`（免费仅 1 年日级）、`coins/{id}/ohlcv/today`、`people/{id}`、`tags`、`tickers?quotes=USD,BTC`、`tickers/{id}`、`tickers/{id}/historical?start=&interval=5m|1h|1d`（免费 24h）、`exchanges`、`exchanges/{id}`、`exchanges/{id}/markets`、`search?q=`、`price-converter`、`contracts/{platform}`、`contracts/{platform}/{address}`、`key/info` | 事件、人物、标签独有 |
| CoinCap | https://docs.coincap.io/ | `https://rest.coincap.io/v3/`（2025 v3 需 key；旧 v2 `api.coincap.io/v2/` 已退役） | 免费 key 2500 credits/天 | `assets?limit=2000`、`assets/{id}`、`assets/{id}/history?interval=m1|m5|m15|m30|h1|h2|h6|h12|d1&start=&end=`、`assets/{id}/markets`、`rates`、`exchanges`、`markets?exchangeId=&baseSymbol=`、`candles?exchange=&interval=&baseId=&quoteId=`；WS `wss://wss.coincap.io/prices?assets=bitcoin,ethereum`、`wss://wss.coincap.io/trades/{exchange}` | 实时价格 WS 免费 |
| LiveCoinWatch | https://livecoinwatch.github.io/lcw-api-docs/ | `https://api.livecoinwatch.com/` | `x-api-key` 免费 10k/天 | `status`、`credits`、`overview`、`overview/history`、`coins/single`、`coins/single/history?code=BTC&start=&end=`、`coins/map`、`coins/list?sort=rank&limit=100`、`coins/contract`、`fiats/all`、`exchanges/single`、`exchanges/list`、`platforms/all` | 全 POST |
| CoinStats | https://openapi.coinstats.app/ | `https://openapiv1.coinstats.app/` | `X-API-KEY` 免费层 | `coins`、`coins/{id}`、`coins/{id}/charts?period=24h|1w|1m|3m|6m|1y|all`、`coins/price/avg`、`coins/price/exchange`、`tickers/exchanges`、`tickers/markets`、`blockchains`、`wallet/balance`、`wallet/transactions`、`exchange/support`、`fiats`、`markets`、`currencies`、`news`、`news/type/{type}`、`news/{id}`、`portfolio/...`、`nft/...`、`insights/btc-dominance`、`insights/fear-and-greed`、`insights/rainbow-chart` | 钱包聚合 + 新闻 |
| CryptoRank | https://api.cryptorank.io/v2/docs | `https://api.cryptorank.io/v2/` | `X-Api-Key` 免费 100 credits/天 | `currencies`、`currencies/{id}`、`currencies/{id}/sparkline`、`currencies/map`、`currencies/categories`、`currencies/tags`、`currencies/fiat`、`exchanges`、`exchanges/{id}`、`exchanges/{id}/markets`、`global`、`hist-price/{id}?interval=1d&from=&to=`、`funding-rounds`（**融资**）、`token-unlocks`（**解锁**）、`ico`、`launchpads`、`vesting/...` | 融资/解锁/ICO 是特色，详见 06 |
| CoinLore | https://www.coinlore.com/cryptocurrency-data-api | `https://api.coinlore.net/api/` | 无 key，无硬限 | `global/`、`tickers/?start=&limit=100`、`ticker/?id=`、`coin/markets/?id=`、`exchanges/`、`exchange/?id=`、`coin/social_stats/?id=` | 极简免费 |
| Messari（免费层） | https://docs.messari.io/ | `https://api.messari.io/`（新）、旧 `https://data.messari.io/api/v1|v2/` | `x-messari-api-key`；免费层少量 | 新：`metrics/v2/assets?limit=`、`metrics/v2/assets/{id}/metrics/{metric}/time-series/{granularity}`、`metrics/v2/assets/details`、`metrics/v2/assets/ath`、`metrics/v2/assets/roi`、`metrics/v2/exchanges`、`metrics/v2/exchanges/{id}/metrics`、`metrics/v2/networks`、`metrics/v2/markets`、`metrics/v2/markets/{id}/metrics/price/time-series/{gran}`、`metrics/v1/...`；`ai/v1/chat/completions`（Messari AI）、`ai/v1/classification/extraction`；`intel/v1/events`、`intel/v1/assets`（**协议事件日历：升级、治理、解锁**）；`news/v1/news/feed`、`news/v1/news/assets`、`news/v1/news/sources`；`research/v1/reports`；`funding/v1/rounds`、`funding/v1/rounds/investors`、`funding/v1/mergers-and-acquisitions`、`funding/v1/organizations`、`funding/v1/projects`（**融资数据库**）；`token-unlocks/v1/assets`、`token-unlocks/v1/assets/{id}/vesting-schedule`、`token-unlocks/v1/assets/{id}/events`、`token-unlocks/v1/allocations`（**解锁**）；`diligence/v1/reports/...`；`signal/v1/...`（Signal 社交热度）；`asset-recommendations`；`networks/v1/...`（Protocol Metrics）；`marketdata/v1/assets/{id}/price/time-series?interval=1d&startTime=&endTime=`、`marketdata/v1/assets/{id}/price`、`marketdata/v1/exchanges/...`、`marketdata/v1/markets/...`（含逐交易所 OHLCV 与 **Real Volume 口径**）、`marketdata/v1/assets/{id}/ath`、`marketdata/v1/assets/{id}/roi` | 研究 + 数据，Pro/Enterprise 解锁大部分 |

---

## 2. 机构级市场数据

| 数据商 | 文档 | Base | 认证/价格 | 覆盖 | 关键接口 / 数据集 | 备注 |
|---|---|---|---|---|---|---|
| Kaiko | https://docs.kaiko.com/ | `https://us.market-api.kaiko.io/v2/data/`、`https://eu.market-api.kaiko.io/`；Reference Data `https://reference-data-api.kaiko.io/v1/` | `X-Api-Key`，机构合同（年费数万美元起） | 100+ CEX + 主要 DEX，逐笔自 2014，L2 盘口快照 | `trades.v1/exchanges/{exchange}/{instrument_class}/{instrument}/trades?start_time=&end_time=&page_size=`、`.../aggregations/count_ohlcv_vwap?interval=1m`、`.../aggregations/ohlcv`、`.../aggregations/vwap`、`.../aggregations/count_ohlcv_vwap`（跨所 `trades.v1/spot_exchange_rate/{base}/{quote}`、`spot_direct_exchange_rate`、`robust_pair_price`、Kaiko Reference Rates `analytics.v2/reference_rate/...`）、`order_book_snapshots.v1/exchanges/.../snapshots/full|raw|depth|slippage|aggregations`（**盘口深度/滑点**）、`order_book_averages.v1`、`derivatives.v2/exchanges/.../risk|price|reference|oi|funding|liquidations`（含 **清算**）、`analytics.v2/exchange_metrics?exchange=&metric=`、`analytics.v2/asset_metrics`、`analytics.v2/value_at_risk`、`analytics.v2/liquidity_score`、`analytics.v2/market_depth`、Cross Price、Lending Rates、`dex.v1/liquidity/events|snapshots`（Uniswap/Curve LP 事件）、`wallet.v1/...`；Reference Data：`exchanges`、`assets`、`instruments?exchange_code=&class=`、`pools`；Stream（gRPC）`gateway-v0-grpc.kaiko.ovh` | 监管级参考价（Kaiko Reference Rates 为 BMR 合规） |
| Coin Metrics | https://docs.coinmetrics.io/api/v4 | `https://api.coinmetrics.io/v4/`（社区免费层无 key 可用，有限指标）；Pro 需 `api_key` | 免费 Community：日级链上指标 + 参考价；Pro 付费 | 网络数据（BTC/ETH 等 100+ 资产链上指标）、市场数据（40+ 交易所逐笔/盘口/资金费/OI/清算）、参考价 CMBI 指数 | `catalog-v2/assets`、`catalog-v2/asset-metrics`、`catalog-v2/markets`、`catalog-v2/exchanges`、`catalog-v2/indexes`、`catalog-v2/pairs`、`catalog-v2/institutions`；`timeseries/asset-metrics?assets=btc&metrics=PriceUSD,CapMrktCurUSD,AdrActCnt,TxCnt,FeeTotUSD,HashRate,SplyCur,ReferenceRateUSD,CapMVRVCur,SplyAct1yr,...&frequency=1d&start_time=&end_time=&page_size=10000`、`timeseries/market-trades?markets=coinbase-btc-usd-spot`、`timeseries/market-candles?markets=binance-BTCUSDT-future&frequency=1m`、`timeseries/market-orderbooks`、`timeseries/market-quotes`、`timeseries/market-funding-rates`、`timeseries/market-funding-rates-predicted`、`timeseries/market-openinterest`、`timeseries/market-liquidations`、`timeseries/market-greeks`、`timeseries/market-implied-volatility`、`timeseries/market-contract-prices`、`timeseries/market-metrics`（含 `liquidity_depth_*`、`volume_reported_*`、**`volume_trusted_spot_usd_1d`（Trusted Volume）**）、`timeseries/exchange-metrics`、`timeseries/exchange-asset-metrics`、`timeseries/pair-metrics`、`timeseries/pair-candles`、`timeseries/institution-metrics`（**Grayscale 等信托持仓**）、`timeseries/index-levels?indexes=CMBIBTC`、`timeseries/index-candles`、`timeseries/index-constituents`、`timeseries/asset-alerts`、`timeseries/defi-balance-sheets`、`timeseries/asset-chains`（链重组）、`timeseries/mempool-feerates`、`timeseries/mining-pool-tips-summary`、`blockchain-v2/{asset}/blocks|accounts|transactions|balance-updates`（原子级链上）、`taxonomy/assets`、`taxonomy-metadata/assets`、`profile/assets`、`reference-data/*`；WS `wss://api.coinmetrics.io/v4/timeseries-stream/asset-metrics|market-trades|market-orderbooks|market-quotes|market-candles|market-openinterest|market-liquidations|index-levels|pair-quotes` | Community 层是免费链上日指标最权威来源；Trusted Volume/Trusted Exchange 框架 |
| Amberdata | https://docs.amberdata.io/ | `https://api.amberdata.com/`（`x-api-key`）；WS `wss://ws.web3api.io`（链上）、`wss://ws.amberdata.com`（市场） | 付费，有限试用 | 链上（BTC/ETH/L2/Solana 等）、CEX 现货/期货/期权（Deribit、OKX、Bybit 期权全量 Greeks/IV 曲面）、DeFi（借贷、DEX、稳定币） | 市场：`markets/spot/prices/pairs/{pair}/historical`、`markets/spot/ohlcv/{instrument}`、`markets/spot/trades/{instrument}`、`markets/spot/order-book-snapshots/{instrument}`、`markets/spot/order-book-events`、`markets/spot/tickers`、`markets/spot/twap|vwap`、`markets/spot/exchanges/reference`、`markets/spot/prices/assets/{asset}/latest`；期货：`markets/futures/ohlcv|trades|order-book-snapshots|funding-rates|open-interest|liquidations|insurance-fund|long-short-ratio|tickers`（**清算与多空比**）；期权：`markets/options/instruments|ohlcv|trades|order-book-snapshots|tickers|volatility-surfaces/{exchange}/{asset}`、`markets/options/term-structure`、`markets/options/level-1-quotes`、`markets/options/greeks`、`markets/options/put-call-ratios`、`markets/options/open-interest`、`markets/options/flows`（**期权流**）、`markets/options/gex`、`markets/options/pain`、`markets/options/strike-breakdown`、`markets/options/liquidations`、`markets/derivatives/analytics/...`（Amberdata Derivatives: DVOL 类指数、Realized Vol、IV Rank）；DeFi：`defi/dex/pairs|trades|liquidity|ohlcv`、`defi/lending/protocols|assets|rates|positions|liquidations`、`defi/stablecoins/...`、`defi/metrics/...`；链上：`blockchains/addresses/{address}/...`（余额、交易、代币、ERC标签、`metrics`）、`blockchains/blocks`、`blockchains/transactions`、`blockchains/tokens/{address}/holders|transfers|supplies|rankings`、`blockchains/metrics/{blockchain}/latest|historical`（网络指标）、`blockchains/mempool`、`blockchains/internal-messages`、`blockchains/logs`、`blockchains/uncles`、`market/metrics/...`（Signals：`exchange flows`、`whale`）；Reference：`markets/spot/exchanges/information`、`markets/futures/exchanges/reference`、`markets/options/exchanges/reference` | 期权数据与清算最全的商业源之一 |
| CoinAPI | https://docs.coinapi.io/ | `https://rest.coinapi.io/v1/`；WS `wss://ws.coinapi.io/v1/`；FIX；Flat Files `https://s3.coinapi.io/`（历史 CSV） | `X-CoinAPI-Key`，免费 Startup 100 req/天；按日请求/数据量付费 | 380+ 交易所 2010 至今逐笔、盘口 L2/L3、OHLCV、报价、指数 | `exchanges`、`exchanges/{id}`、`assets`、`assets/{id}`、`assets/icons/{size}`、`symbols?filter_exchange_id=&filter_symbol_id=&filter_asset_id=`、`symbols/map/{exchange}`、`exchangerate/{base}/{quote}?time=`、`exchangerate/{base}?invert=`、`exchangerate/{base}/{quote}/history?period_id=1MIN&time_start=&time_end=&limit=`（**跨所综合汇率历史**）、`exchangerate/{base}/{quote}/apikey-...`、`ohlcv/periods`、`ohlcv/{symbol_id}/latest?period_id=1MIN&limit=`、`ohlcv/{symbol_id}/history?period_id=&time_start=&time_end=&limit=100000`、`ohlcv/exchanges/{exchange_id}/history`、`trades/latest`、`trades/{symbol_id}/latest`、`trades/{symbol_id}/history?time_start=&time_end=&limit=`、`quotes/latest`、`quotes/{symbol}/history`、`orderbooks/current`、`orderbooks/{symbol}/current?limit_levels=`、`orderbooks/{symbol}/latest`、`orderbooks/{symbol}/history?time_start=&limit_levels=`、`orderbooks3/current`、`orderbooks3/{symbol}/current`（L3）、`metrics/listing`、`metrics/symbol/listing`、`metrics/symbol/current?metric_id=DERIVATIVES_FUNDING_RATE_CURRENT&symbol_id=`、`metrics/symbol/history?metric_id=DERIVATIVES_OPEN_INTEREST&symbol_id=&time_start=`、`metrics/exchange/listing|current|history`（**衍生品指标：OI、funding、mark/index price、liquidation 等统一字段**）、`metrics/asset/listing|current|history`、`indexes`、`indexes/{id}/current|history|timeseries`；Flat Files：`v1/flatfiles`（`trades`、`quotes`、`orderbooks`、`ohlcv` 按日 parquet/csv）；EMS（交易执行）、Market Data Shared Nodes | 覆盖最广，历史 Flat Files 可整批下载 |
| Tardis.dev | https://docs.tardis.dev/ | `https://api.tardis.dev/v1/`；`tardis-machine` 本地回放服务器；Node/Python 客户端 | `Authorization: Bearer`，免费层可拉每月第 1 天数据；按交易所订阅付费 | 原始 WS 消息级历史（逐笔、L2 增量、L3、清算、资金费、OI、期权 ticker/IV）自 2019 起，Binance/Bybit/OKX/Deribit/BitMEX/Coinbase/Kraken/Huobi/Gate/KuCoin/dYdX/Hyperliquid(2024+)/Bitfinex/Gemini/Bitstamp/Phemex/Delta/Woo/CoinFlex/Ascendex/Bitnomial/Crypto.com/Mango/Serum/Upbit 等 40+ | `exchanges`、`exchanges/{exchange}`（可用频道、symbol、日期范围）、`data-feeds/{exchange}?from=&offset=&filters=`（原始消息）、Datasets CSV `https://datasets.tardis.dev/v1/{exchange}/{dataType}/{yyyy}/{mm}/{dd}/{symbol}.csv.gz`（dataType：`trades`、`incremental_book_L2`、`book_snapshot_5`、`book_snapshot_25`、`quotes`、`derivative_ticker`（含 funding、OI、mark、index）、`options_chain`、`liquidations`、`book_ticker`）；`tardis-machine` 提供 `/replay?options=`、`/replay-normalized`、WS `ws-replay`、`ws-replay-normalized`、`ws-stream-normalized`（实时标准化多所流） | 盘口重建与回测标配；按交易所买 |
| CryptoCompare 企业版 / CCData Index | 见上 | | | | Exchange Benchmark（交易所评级报告）、CADLI/ CCIX 指数、定制 | |
| CoinDesk Indices（CDI，含 CMI、XBX 等；2024 并入 Bullish，2025 CCData 并入 CoinDesk） | https://www.coindesk.com/indices ；数据接口经 CCData（`index/cc/v1/latest/tick?market=cdi&instruments=XBX-USD`） | 同 CCData | 合同/CCData | CoinDesk Bitcoin Price Index (XBX)、CoinDesk 20 (CD20)、CoinDesk Market Index (CMI)、CoinDesk 5 (CD5)、Ether Price Index (ETX)、行业分类 DACS | — | 机构基准，BMR 合规 |
| Lukka、Digital Asset Research (DAR)、Bloomberg BGCI、S&P Cryptocurrency Indices、Nasdaq Crypto Index (NCI)、FTSE Russell Digital Asset、MarketVector (MVIS)、Galaxy Indices、Bitwise Indices、Compass Financial Technologies、Vinter、Kraken CF Benchmarks（见下节） | 各自官网 | 多为 Bloomberg/Refinitiv 终端或合同 | 合同 | 指数、参考价、合规报价 | DAR `https://api.digitalassetresearch.com/`、Lukka Prime、Vinter `https://www.vinter.co/api`（`https://api.vinterapi.com/api/v3/...`，部分免费） | 基金/ETF 用基准 |
| Delphi Digital、Bernstein、K33 Research、Kaiko Research、Glassnode Insights、Galaxy Research、Coinbase Institutional、Binance Research、OKX Research、CryptoQuant Research、Messari Research、The Block Research | — | 报告，无数据 API（The Block Pro 有 Data API） | — | 研究报告 | — | 研究用 |

---

## 3. Coinglass（概览）
- 文档：https://docs.coinglass.com/ ；Base `https://open-api-v4.coinglass.com/api/`（`CG-API-KEY`）；套餐 Hobbyist（免费 30 req/min，有限接口与历史）/ Startup / Standard / Professional / Enterprise。
- 覆盖：资金费率（当前/历史/加权/各所对比/套利）、OI（聚合与分所、历史 K 线、按币种分布）、清算（聚合/分所/热力图/大额清算单/清算地图）、多空比（账户/大户/主动买卖）、期权（OI、成交量、Max Pain、IV、各所分布）、ETF（BTC/ETH/SOL/XRP 现货 ETF 流入/持仓/溢价/AUM、港股 ETF、灰度）、链上（交易所余额、ERC20 转账、巨鲸转账、Hyperliquid 巨鲸持仓）、指标（恐惧贪婪、彩虹图、Puell、Stock-to-Flow、Pi Cycle、Golden Ratio、2 年 MA、Bitcoin Bubble Index、AHR999、Coinbase Premium、Bitfinex 保证金多空、借贷利率、稳定币市值、牛市高点信号）、交易所（排名、储备/资产、钱包）、现货（聚合 K 线、订单簿、主动买卖、大单）、经济日历、宏观（美股/黄金/美元指数对比）。
- 详细接口清单见 `07-derivatives.md` 第 2 节。
- 坑：免费层历史短（多为 1 个月内）、不含分钟级、不含 WS；聚合口径（如 OI 用 USD、funding 用 OI 加权）与交易所原值不同；部分接口限 `limit<=4500`。

---

## 4. 预言机价格（链上/链下参考价）

| 预言机 | 文档 | 读取方式 | 关键接口 | 备注 |
|---|---|---|---|---|
| Pyth Network | https://docs.pyth.network/price-feeds | Hermes REST/SSE `https://hermes.pyth.network/`；链上 `IPyth.getPriceNoOlderThan(id, age)`；Benchmarks `https://benchmarks.pyth.network/` | `v2/price_feeds?query=BTC&asset_type=crypto`（Feed ID 列表）、`v2/updates/price/latest?ids[]=0x...&parsed=true`（含 `price.price/expo/conf/publish_time` 与 `ema_price`）、`v2/updates/price/stream?ids[]=`（SSE）、`v2/updates/price/{publish_time}?ids[]=`（历史点查）、`v2/updates/twap/{window_seconds}/latest`；Benchmarks `v1/shims/tradingview/history?symbol=Crypto.BTC/USD&resolution=1&from=&to=`（**历史 K 线**）、`v1/updates/price/{timestamp}`、`v1/price_feeds/`；Pyth Lazer（低延迟） | 400ms 更新，1000+ feeds（含美股、外汇、商品、ETF、利率）；可做"预言机价格"数据集 |
| Chainlink | https://docs.chain.link/data-feeds | 链上 `AggregatorV3Interface.latestRoundData()` / `getRoundData(roundId)`（历史需遍历 roundId）；Data Streams（低延迟，需 key）`https://api.testnet-dataengine.chain.link` / 主网 `https://api.dataengine.chain.link`（`/api/v1/feeds`、`/api/v1/reports/latest?feedID=`、`/api/v1/reports/bulk`、`/api/v1/reports/page?feedID=&startTimestamp=`、WS `/api/v1/ws?feedIDs=`）；Feed 地址目录 `https://reference-data-directory.vercel.app/feeds-mainnet.json` 等（docs 的 JSON）；Proof of Reserve feeds；CCIP | `description()`、`decimals()`、`latestRoundData()` 返回 `(roundId, answer, startedAt, updatedAt, answeredInRound)`；Data Streams 报告含 `bid`、`ask`、`benchmarkPrice`、`validFromTimestamp`、`expiresAt` | 心跳 + 偏差阈值更新（如 ETH/USD 0.5% / 1h）；历史用 Dune `chainlink.price_feeds` 表最方便 |
| RedStone | https://docs.redstone.finance/ | `https://api.redstone.finance/prices?symbol=BTC&provider=redstone&limit=1`、`?symbols=BTC,ETH`、`?fromTimestamp=&toTimestamp=&interval=`（历史）；Pull 模型用 SDK 签名数据 | — | 支持 LST/LRT 等长尾资产 |
| Band Protocol | https://docs.bandchain.org/ | BandChain LCD `https://laozi1.bandchain.org/api/oracle/v1/request_prices?symbols=BTC&ask_count=16&min_count=10`；`StdReference.getReferenceData(base, quote)` | — | — |
| API3 | https://docs.api3.org/ | dAPI 链上 `IApi3ReaderProxy.read()`；Market `https://market.api3.org/` | — | OEV 网络 |
| Switchboard | https://docs.switchboard.xyz/ | Solana/Sui/Aptos 链上 feed 账户；Crossbar `https://crossbar.switchboard.xyz/`（`simulate/{feedHash}`、`updates/...`） | — | Solana 常用 |
| Chronicle | https://docs.chroniclelabs.org/ | 链上 `IChronicle.read()`；`https://chroniclelabs.org/dashboard` | — | Maker/Sky 系 |
| Stork | https://docs.stork.network/ | REST `https://rest.jp.stork-oracle.network/v1/prices/latest?assets=BTCUSD`、WS `wss://api.jp.stork-oracle.network/evm/subscribe` | — | 低延迟，Hyperliquid/HIP-3 相关 |
| DIA | https://docs.diadata.org/ | `https://api.diadata.org/v1/assetQuotation/{blockchain}/{address}`、`/v1/quotation/BTC`、`/v1/assetChartPoints/MA120/...`、`/v1/supply/BTC`、`/v1/exchanges`、`/v1/NFT/...`、`/v1/lastTradesAsset/...`、`/v1/foreignQuotation/{source}/{symbol}`（Coinbase/Kraken 等单一来源价）；Lumina/xReal GraphQL | — | 开源聚合，含 NFT 地板价 |
| Supra、Pragma(Starknet)、Flux、UMA（乐观预言机，Polymarket 结算）、Tellor、Witnet、Kaiko-on-chain、Chainlink Smart Data（NAV）、Edge（GMX） | 各自文档 | 链上 | — | — |

---

## 5. 指数与参考价
| 指数 | 提供方 | 访问 | 备注 |
|---|---|---|---|
| CME CF Bitcoin Reference Rate (BRR)、BRRNY、ETHUSD_RR、CF Benchmarks 全系（Kraken 子公司） | https://www.cfbenchmarks.com/ | `https://www.cfbenchmarks.com/data/indices/BRR`（页面）；API `https://api.cfbenchmarks.com/v1/values?id=BRR&start_time=&end_time=`（需账号，部分免费）；WS `wss://www.cfbenchmarks.com/ws/v4` | CME 比特币期货结算基准（伦敦 4pm）、BRRNY（纽约 4pm，美 ETF NAV 用） |
| Binance 指数成分 | Binance | `GET https://fapi.binance.com/fapi/v1/constituents?symbol=BTCUSDT`（成分交易所与权重） | 合约指数价格来源 |
| Deribit Index | Deribit | `public/get_index_price?index_name=btc_usd`、`public/get_index_price_names`、WS `deribit_price_index.btc_usd`、`deribit_price_ranking.btc_usd`（各成分所价格与权重） | — |
| Bybit / OKX / Bitget 指数成分 | 各所 | Bybit `GET /v5/market/index-price-kline`；OKX `GET /api/v5/market/index-components?index=BTC-USDT`（**成分与权重**）；Bitget `GET /api/v2/mix/market/history-index-candles` | — |
| Coinbase Core Index (COINX)、Coinbase 50 Index | Coinbase | 页面；CoinDesk/MarketVector 管理 | — |
| Bitwise 10 Index、Bitwise 其他 | Bitwise | 页面 | ETF 基准 |
| MarketVector (MVIS) CryptoCompare Digital Assets 系列 | MarketVector | `https://www.marketvector.com/`，Refinitiv/Bloomberg | VanEck 产品基准 |
| S&P Cryptocurrency Indices、Nasdaq NCI、FTSE Digital Asset、Bloomberg Galaxy (BGCI)、Wilshire、Solactive | 各自 | Bloomberg 终端等 | 传统金融 |
| Vinter | Vinter | `https://api.vinterapi.com/api/v3/single_assets/` 等（有免费层） | 欧洲 ETP 基准 |
| Compass Financial Technologies | — | 合同 | — |
| CoinDesk 指数（XBX、CD20、CMI、DACS 分类） | CoinDesk Indices | 经 CCData 接口 `market=cdi` | — |
| CMC100、CoinGecko 分类指数、Coinglass 聚合价格 | 各自 | 见各节 | — |
| TradingView 综合（CRYPTOCAP:TOTAL、TOTAL2、TOTAL3、BTC.D、USDT.D、CRYPTO:BTCUSD 等） | TradingView | **无官方 REST API**；非官方 `tvdatafeed`（Python，用账号登录拉 K 线）、`tradingview-ws`、`tradingview-scraper`；Pine 导出；TradingView Charting Library 需自备数据源 | 市值占比等指标 TradingView 口径常被引用，但不可编程获取；用 CoinGecko `global` / CMC `global-metrics` 替代 |

---

## 6. 口径与选型建议
- **做代币主数据表**：以 CoinGecko `coins/list?include_platform=true` + CMC `cryptocurrency/map` 做 id 对齐，再补 CCData `asset/v1/metadata` 的供应与社交指标。三家的流通量口径不同（CMC 核验 vs CoinGecko 自报+核验 vs CCData），表里保留来源字段。
- **做综合价格**：免费首选 CoinGecko `simple/price`（延迟分钟级）或 CCData CADLI；需要秒级用 Pyth Hermes；需要合规基准用 CF Benchmarks / Kaiko Reference Rates / CoinDesk XBX。
- **做跨所 K 线对比**：CCData `spot/v1/historical/minutes?market=`（免费可用）> CoinAPI（付费，最全）> Kaiko（机构）。免费层想要分钟级多年历史，CCData 是唯一选择；否则直接从交易所 REST 翻页。
- **做衍生品聚合**：免费先看 CoinGecko `derivatives`（快照）与 Coinglass（有历史）；付费首选 Coin Metrics / Amberdata / Kaiko（含清算）。
- **成交量真实性**：Coin Metrics Trusted Volume、Messari Real Volume、CoinGecko `trade_volume_24h_btc_normalized`、CMC `exchange_score` / `effective_liquidity` 是四种刷量过滤口径；研究用建议交叉。
- **限频现实**：免费 CoinGecko 30 req/min 做全量 10k 币扫描需 40 分钟以上；用 `coins/markets?per_page=250` 分页 + `simple/price` 批量 500 个 id 更省。

## 7. 变更记录
- 2026-10 初版。
