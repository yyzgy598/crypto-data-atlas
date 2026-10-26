# 01 · 中心化交易所（CEX）API

目录
1. 通用说明与口径差异
2. 一线交易所详表：Binance / OKX / Bybit / Bitget / Coinbase / Kraken / KuCoin / Gate / HTX / MEXC
3. 衍生品专营：Deribit / BitMEX / Kraken Futures / CME（见 07）
4. 其他交易所速查表（Bitfinex、Gemini、Bitstamp、Crypto.com、Upbit、Bithumb、Coinone、bitFlyer、Bitso、BingX、Phemex、CoinEx、WhiteBIT、LBank、Poloniex、Backpack、WOO X、BtcTurk、Luno、Binance.US、Bullish、Bitvavo、Zaif、Independent Reserve、BTC Markets、Paribu、Coincheck）
5. CCXT 统一接口
6. 变更记录

---

## 1. 通用说明与口径差异

| 项目 | 常见差异 | 影响 |
|---|---|---|
| 持仓量 OI | Binance 返回张数（USDⓈ-M 1 张=1 币）；Bybit `openInterest` 为币数量；OKX `oi` 张数、`oiCcy` 币数量、`oiUsd` 美元；Bitget 币数量 | 跨所对比必须统一换成 USD 或币 |
| 资金费率周期 | 多数 8h（00/08/16 UTC）；部分合约 4h/1h（Bybit、Bitget、Gate 小币种；Hyperliquid 全部 1h）；OKX 部分 4h | 年化换算系数不同 |
| K 线时间戳 | Binance 开盘时间 ms；OKX 开盘时间 ms 字符串；Kraken 秒；Coinbase ISO/秒 | 对齐时统一到 UTC ms |
| 成交方向 | Binance `isBuyerMaker`；OKX `side`；Bybit `side` + `S` | 主动买卖量计算要翻转逻辑 |
| 多空比 | Binance 提供账户数比 / 大户持仓比 / 主动买卖比三种；OKX `long-short-account-ratio`；Bybit `account-ratio` | 不同口径不可直接对比 |
| 清算数据 | Binance 2021 后取消 REST 全量清算，仅 WS `!forceOrder@arr` 且每秒最多 1 条/合约；Bybit WS `liquidation`/`allLiquidation`；OKX REST `liquidation-orders` 有历史 | 全量清算需用 Coinglass/Coinalyze 等聚合 |
| 地域限制 | Binance（api.binance.com 对部分地区 451）、OKX、Bybit、KuCoin 对大陆 IP 限制；Coinbase/Kraken 对部分国家限制 | 采集机器选址或走代理 |

**认证通用模式**：绝大多数公开行情接口无需 API Key；账户/交易接口用 HMAC-SHA256（Binance、Bybit、Bitget、Gate、MEXC、KuCoin）或 HMAC-SHA256 + passphrase（OKX、KuCoin、Bitget、Coinbase Exchange）；Kraken 用 HMAC-SHA512；Coinbase Advanced Trade 用 JWT(ES256) 或旧的 CDP key。

---

## 2. 一线交易所详表

### Binance
- 文档：https://developers.binance.com/docs （Spot / USDⓈ-M Futures / COIN-M Futures / Options / Margin / Wallet 分册）；变更日志 https://developers.binance.com/docs/binance-spot-api-docs/CHANGELOG
- Base URL
  - 现货 REST：`https://api.binance.com`（备用 `api1`~`api4`、`api-gcp.binance.com`；只读行情可用 `https://data-api.binance.vision`）
  - 现货 WS：`wss://stream.binance.com:9443/ws` 与 `/stream?streams=`；行情专用 `wss://data-stream.binance.vision`；WS API（下单）`wss://ws-api.binance.com:443/ws-api/v3`
  - USDⓈ-M 合约 REST：`https://fapi.binance.com`；WS `wss://fstream.binance.com`
  - COIN-M 合约 REST：`https://dapi.binance.com`；WS `wss://dstream.binance.com`
  - 期权 REST：`https://eapi.binance.com`；WS `wss://nbstream.binance.com/eoptions`
  - 历史归档下载：`https://data.binance.vision`（见 11-bulk-data）
- 限频：按 IP 权重，现货 6000 权重/分钟（header `X-MBX-USED-WEIGHT-1M`），合约 2400/分钟；订单按 UID 限制；超限 429，再犯 418 封 IP 2min–3天。
- 关键行情接口（现货）
  - `GET /api/v3/exchangeInfo` 交易对、精度、过滤器
  - `GET /api/v3/depth?symbol=BTCUSDT&limit=5000`（limit 1–5000，权重随 limit 增长）
  - `GET /api/v3/trades`、`/historicalTrades`（需 API key，按 fromId 翻页）、`/aggTrades`（按 fromId 或 startTime/endTime 翻页，一次 1000 条）
  - `GET /api/v3/klines?symbol=&interval=1m&startTime=&endTime=&limit=1000`；`/uiKlines`
  - `GET /api/v3/ticker/24hr`、`/ticker/price`、`/ticker/bookTicker`、`/ticker?windowSize=`
  - `GET /api/v3/avgPrice`
- 关键行情接口（USDⓈ-M 合约）
  - `GET /fapi/v1/exchangeInfo`、`/fapi/v1/depth`、`/fapi/v1/aggTrades`、`/fapi/v1/klines`、`/fapi/v1/continuousKlines`、`/fapi/v1/indexPriceKlines`、`/fapi/v1/markPriceKlines`、`/fapi/v1/premiumIndexKlines`
  - `GET /fapi/v1/premiumIndex` 标记价格、指数价格、当前资金费率、下次结算时间
  - `GET /fapi/v1/fundingRate?symbol=&startTime=&endTime=&limit=1000` 历史资金费率；`GET /fapi/v1/fundingInfo` 各合约结算周期与上下限
  - `GET /fapi/v1/openInterest?symbol=` 当前 OI；`GET /futures/data/openInterestHist?symbol=&period=5m&limit=500` 历史 OI（仅最近 30 天，period 5m/15m/30m/1h/2h/4h/6h/12h/1d）
  - `GET /futures/data/topLongShortAccountRatio`、`/topLongShortPositionRatio`、`/globalLongShortAccountRatio`、`/takerlongshortRatio`（都只保留 30 天）
  - `GET /futures/data/basis?pair=BTCUSDT&contractType=PERPETUAL&period=1h`
  - `GET /futures/data/delivery-price`
  - `GET /fapi/v1/ticker/24hr`、`/fapi/v1/ticker/price`、`/fapi/v2/ticker/price`、`/fapi/v1/ticker/bookTicker`
  - `GET /fapi/v1/constituents?symbol=` 指数成分
  - `GET /fapi/v1/assetIndex` 多资产模式指数
  - 清算：仅 WS `<symbol>@forceOrder` / `!forceOrder@arr`（每秒每合约最多推 1 条，是抽样不是全量）
- WS 频道（现货/合约相似）：`<symbol>@aggTrade`、`@trade`、`@kline_<interval>`、`@miniTicker`、`!miniTicker@arr`、`@ticker`、`!ticker@arr`、`@bookTicker`、`!bookTicker`、`@depth<levels>[@100ms]`、`@depth[@100ms]`（增量深度，需配合 REST 快照同步 `U`/`u`）、合约额外 `@markPrice[@1s]`、`!markPrice@arr`、`@forceOrder`、`!forceOrder@arr`、`@compositeIndex`、`<pair>_<contractType>@continuousKline_<interval>`。单连接最多 1024 流，24h 强制断开，每 3min ping。
- 期权（eapi）：`GET /eapi/v1/exchangeInfo`、`/eapi/v1/mark`（含 IV、Greeks）、`/eapi/v1/ticker`、`/eapi/v1/klines`、`/eapi/v1/openInterest?underlyingAsset=BTC&expiration=`、`/eapi/v1/exerciseHistory`、`/eapi/v1/historicalTrades`。
- 其他数据：`GET /sapi/v1/margin/...` 杠杆利率；`GET /sapi/v1/capital/config/getall` 币种链与提现状态（需 key）；`GET /sapi/v1/asset/tradeFee`；Binance Research/Launchpool 无 API。
- 坑：`openInterestHist` 等 `/futures/data/*` 只有 30 天历史，长期需自行落库或用 Coinglass；现货 `historicalTrades` 需要 API key；451 地域限制。

### OKX
- 文档：https://www.okx.com/docs-v5/en/
- Base：`https://www.okx.com`（备用 `https://aws.okx.com`，大陆可用域名经常变化）；WS 公共 `wss://ws.okx.com:8443/ws/v5/public`、业务 `/ws/v5/business`（K 线、期权等）、私有 `/ws/v5/private`
- 限频：公共接口按 IP，一般 20 次/2s；header 无统一用量字段；私有接口按 UID。
- 关键接口（统一账户，instType = SPOT/MARGIN/SWAP/FUTURES/OPTION）
  - `GET /api/v5/public/instruments?instType=SWAP`
  - `GET /api/v5/market/tickers?instType=SWAP`、`/market/ticker?instId=`
  - `GET /api/v5/market/books?instId=&sz=400`、`/market/books-full?sz=5000`
  - `GET /api/v5/market/trades?instId=&limit=500`、`/market/history-trades?instId=&type=2&after=`（按 tradeId 翻页，仅近 3 个月）
  - `GET /api/v5/market/candles?instId=&bar=1m&limit=300`、`/market/history-candles`（历史，1m 粒度约 2 年以上）
  - `GET /api/v5/market/index-candles`、`/market/mark-price-candles`、`/market/history-index-candles`
  - `GET /api/v5/public/funding-rate?instId=`、`/public/funding-rate-history?instId=&limit=100&after=`（可翻页回溯全历史）
  - `GET /api/v5/public/open-interest?instType=SWAP&instId=`（oi 张 / oiCcy 币 / oiUsd）
  - `GET /api/v5/public/mark-price`、`/public/price-limit`、`/public/estimated-price`、`/public/delivery-exercise-history`
  - `GET /api/v5/public/liquidation-orders?instType=SWAP&uly=BTC-USDT&state=filled`（有历史，分页）
  - `GET /api/v5/public/insurance-fund`
  - `GET /api/v5/public/opt-summary?uly=BTC-USD`（期权 IV、Greeks）
  - 大数据/交易数据：`GET /api/v5/rubik/stat/taker-volume`、`/rubik/stat/margin/loan-ratio`、`/rubik/stat/contracts/long-short-account-ratio`、`/rubik/stat/contracts/long-short-account-ratio-contract`、`/rubik/stat/contracts/open-interest-volume`、`/rubik/stat/option/open-interest-volume`、`/rubik/stat/option/open-interest-volume-ratio`、`/rubik/stat/option/open-interest-volume-expiry`、`/rubik/stat/option/open-interest-volume-strike`、`/rubik/stat/option/taker-block-volume`、`/rubik/stat/trading-data/support-coin`、`/rubik/stat/contracts/open-interest-history`（OI 历史，period 5m–1D）
  - 大宗/RFQ：`GET /api/v5/rfq/public-trades`（期权大宗成交）
  - `GET /api/v5/public/economic-calendar`（需 key，宏观日历）
- WS 频道：`tickers`、`trades`、`trades-all`、`books`/`books5`/`books50-l2-tbt`/`books-l2-tbt`（tbt 需 VIP）、`candle1m`（business）、`mark-price`、`index-tickers`、`funding-rate`、`open-interest`、`liquidation-orders`、`opt-summary`、`estimated-price`、`price-limit`、`option-trades`、`public-struc-block-trades`、`adl-warning`。
- 坑：`history-trades` 只保留约 3 个月；域名对大陆 IP 时常变化；`rubik` 系列大多只给 1D/5m 粒度、历史有限。

### Bybit
- 文档：https://bybit-exchange.github.io/docs/v5/intro
- Base：`https://api.bybit.com`（备用 `api.bytick.com`、荷兰 `api.bybit.nl`、香港 `api.byhkbit.com`、土耳其 `api.bybit-tr.com`、哈萨克 `api.bybit.kz`）；WS 公共 `wss://stream.bybit.com/v5/public/{spot|linear|inverse|option|spread}`、私有 `/v5/private`、交易 `/v5/trade`
- 限频：公共 REST 按 IP 约 600 次/5s（文档为 per endpoint，每个 IP 一般 10 req/s 级）；私有按 UID，header `X-Bapi-Limit-Status`。
- 关键接口（category = spot/linear/inverse/option）
  - `GET /v5/market/instruments-info?category=linear`
  - `GET /v5/market/tickers?category=linear`（含 fundingRate、openInterest、openInterestValue、nextFundingTime、IV for option）
  - `GET /v5/market/orderbook?category=&symbol=&limit=500`（spot 200、linear 500、option 25）
  - `GET /v5/market/recent-trade?limit=1000`
  - `GET /v5/market/kline?category=&symbol=&interval=1&start=&end=&limit=1000`、`/mark-price-kline`、`/index-price-kline`、`/premium-index-price-kline`
  - `GET /v5/market/funding/history?category=linear&symbol=&limit=200&startTime=&endTime=`（翻页可回溯）
  - `GET /v5/market/open-interest?category=linear&symbol=&intervalTime=5min&limit=200&cursor=`（intervalTime 5min/15min/30min/1h/4h/1d，有 cursor 翻页，历史较深）
  - `GET /v5/market/account-ratio?category=linear&symbol=&period=5min&limit=500`
  - `GET /v5/market/risk-limit`、`/v5/market/delivery-price`、`/v5/market/insurance`
  - `GET /v5/market/historical-volatility?category=option&baseCoin=BTC&period=30`
  - 清算：WS `allLiquidation.{symbol}`（2024 后的全量频道，替代抽样的 `liquidation.{symbol}`）；无 REST 历史
  - 跨所对比：`GET /v5/market/premium-index-price-kline`
- WS 公共频道：`orderbook.{depth}.{symbol}`（1/50/200/500/1000）、`publicTrade.{symbol}`、`tickers.{symbol}`、`kline.{interval}.{symbol}`、`allLiquidation.{symbol}`、`liquidation.{symbol}`（将下线）、`lt.kline`/`lt.ticker`/`lt.nav`（杠杆代币）、`spread.*`。
- 坑：OI 单位是币；资金费率周期因合约而异（`fundingInterval` 字段，分钟）；订单簿深度 1000 档需 WS。

### Bitget
- 文档：https://www.bitget.com/api-doc/common/intro
- Base：`https://api.bitget.com`；WS 公共 `wss://ws.bitget.com/v2/ws/public`、私有 `/v2/ws/private`
- 限频：公共多为 20 req/s/IP；私有 10 req/s/UID。
- 现货 `GET /api/v2/spot/public/symbols`、`/api/v2/spot/market/tickers`、`/market/orderbook?symbol=&type=step0&limit=150`、`/market/fills`、`/market/fills-history`（近 7 天）、`/market/candles?granularity=1min&limit=1000`、`/market/history-candles`。
- 合约（productType = USDT-FUTURES / COIN-FUTURES / USDC-FUTURES）`GET /api/v2/mix/market/contracts`、`/tickers`、`/ticker`、`/merge-depth`、`/fills`、`/fills-history`、`/candles`、`/history-candles`、`/history-index-candles`、`/history-mark-candles`、`/current-fund-rate`、`/history-fund-rate?symbol=&productType=&pageSize=100&pageNo=`、`/open-interest?symbol=`、`/symbol-price`、`/funding-time`、`/discount-rate`、`/queryPositionLever`、`/position-tier`。
- WS：`ticker`、`candle1m`、`books`/`books1`/`books5`/`books15`、`trade`、`index-price`、`mark-price`、`funding-time`（合约）。
- 坑：Bitget 无公开的多空比/历史 OI REST（历史 OI 用 Coinglass）；成交历史只 7 天。

### Coinbase
- 两套接口：
  - **Advanced Trade API**（零售现货+少量永续，取代旧 Pro）：文档 https://docs.cdp.coinbase.com/advanced-trade/docs/welcome ；Base `https://api.coinbase.com/api/v3/brokerage`；公共行情 `GET /market/products`、`/market/products/{product_id}/ticker`、`/market/products/{product_id}/candles?granularity=ONE_MINUTE&start=&end=`（一次最多 350 根）、`/market/product_book?product_id=&limit=`；认证用 CDP API Key 生成 JWT(ES256)。WS `wss://advanced-trade-ws.coinbase.com`，频道 `ticker`、`ticker_batch`、`level2`、`market_trades`、`candles`、`status`、`heartbeats`、`futures_balance_summary`、`user`。限频公共 10 req/s，私有 30 req/s。
  - **Coinbase Exchange（原 Pro / Prime 机构）**：文档 https://docs.cdp.coinbase.com/exchange/docs/welcome ；Base `https://api.exchange.coinbase.com`；`GET /products`、`/products/{id}/book?level=1|2|3`（level 3 全量订单）、`/products/{id}/ticker`、`/products/{id}/trades`（按 after/before 翻页，可回溯全历史）、`/products/{id}/candles?granularity=60&start=&end=`（一次 300 根）、`/products/{id}/stats`；WS `wss://ws-feed.exchange.coinbase.com`（`level2`、`level2_batch`、`full`、`matches`、`ticker`、`ticker_batch`、`status`、`auctionfeed`、`rfq_matches`），`wss://ws-direct.exchange.coinbase.com` 低延迟。限频公共 10 req/s/IP。
  - Coinbase International Exchange（永续，非美）：`https://api.international.coinbase.com/api/v1`，`GET /instruments`、`/instruments/{id}/quote`、`/instruments/{id}/funding`、`/instruments/{id}/candles`。
  - Coinbase Derivatives（美国 CFTC 合约）通过 Advanced Trade `products` 的 `product_type=FUTURE`。
- 其他：Coinbase 公共价格 `GET https://api.coinbase.com/v2/prices/BTC-USD/spot`、`/v2/exchange-rates?currency=BTC`、`/v2/currencies`（无需 key）。Coinbase Premium 指数本身无官方 API，自己用 Coinbase BTC-USD 与 Binance BTCUSDT 计算，或用 CryptoQuant/Coinglass。

### Kraken
- 现货文档：https://docs.kraken.com/api/ ；Base `https://api.kraken.com/0/public/`；`Assets`、`AssetPairs`、`Ticker?pair=XBTUSD`、`OHLC?pair=&interval=1&since=`（只返回最近 720 根）、`Depth?pair=&count=500`、`Trades?pair=&since=<ns>`（按纳秒游标翻页，可回溯全历史）、`Spread`、`SystemStatus`、`Time`。WS v2 `wss://ws.kraken.com/v2`（`ticker`、`book`（10/25/100/500/1000）、`level3`（需认证）、`ohlc`、`trade`、`instrument`、`status`）。限频公共约 1 req/s（计数器制）。
- 期货（原 CF）：https://docs.kraken.com/api/docs/futures-api/ ；Base `https://futures.kraken.com/derivatives/api/v3/`；`instruments`、`tickers`、`orderbook?symbol=`、`history?symbol=&lastTime=`（成交）、`https://futures.kraken.com/api/charts/v1/{tick_type}/{symbol}/{resolution}?from=&to=`（trade/mark/spot 三种）、`https://futures.kraken.com/api/history/v3/market/{symbol}/executions`（历史成交，Pro）；资金费率在 `tickers` 的 `fundingRate`、`fundingRatePrediction`，历史 `GET /derivatives/api/v4/historicalfundingrates?symbol=`。WS `wss://futures.kraken.com/ws/v1`（`ticker`、`trade`、`book`、`ticker_lite`、`heartbeat`）。
- 坑：现货 OHLC 只给 720 根，历史 K 线需自己从 Trades 聚合或用第三方；交易对代码有 XBT/XXBT 别名。

### KuCoin
- 文档：https://www.kucoin.com/docs-new/
- 现货 Base `https://api.kucoin.com`：`GET /api/v2/symbols`、`/api/v1/market/allTickers`、`/api/v1/market/orderbook/level2_20|100`、`/api/v3/market/orderbook/level2`（全量，需 key）、`/api/v1/market/histories`（最近 100 笔）、`/api/v1/market/candles?type=1min&symbol=&startAt=&endAt=`（一次 1500 根）、`/api/v1/market/stats`、`/api/v3/currencies`。WS 需先 `POST /api/v1/bullet-public` 取 token。频道 `/market/ticker:`、`/market/level2:`、`/spotMarket/level2Depth5:`、`/market/match:`、`/market/candles:`。
- 合约 Base `https://api-futures.kucoin.com`：`GET /api/v1/contracts/active`、`/api/v1/contracts/{symbol}`、`/api/v1/ticker`、`/api/v1/allTickers`、`/api/v1/level2/snapshot`、`/api/v1/trade/history`、`/api/v1/kline/query?symbol=&granularity=1&from=&to=`、`/api/v1/funding-rate/{symbol}/current`、`/api/v1/contract/funding-rates?symbol=&from=&to=`（历史）、`/api/v1/mark-price/{symbol}/current`、`/api/v1/premium/query`、`/api/v1/interest/query`、`/api/v1/index/query`。OI 在 `contracts` 的 `openInterest`（张）。WS `/contractMarket/level2`、`/contractMarket/execution`、`/contractMarket/tickerV2`、`/contract/instrument:`（标记价、资金费）、`/contractMarket/limitCandle:`。
- 限频：按 UID/IP 的权重池，header `gw-ratelimit-remaining`。

### Gate.io
- 文档：https://www.gate.io/docs/developers/apiv4/
- Base `https://api.gateio.ws/api/v4`；WS 现货 `wss://api.gateio.ws/ws/v4/`、合约 `wss://fx-ws.gateio.ws/v4/ws/{usdt|btc}`、期权 `wss://op-ws.gateio.live/v4/ws`
- 现货：`GET /spot/currency_pairs`、`/spot/tickers`、`/spot/order_book?currency_pair=&limit=1000&with_id=true`、`/spot/trades?limit=1000&last_id=`（可翻页）、`/spot/candlesticks?interval=1m&limit=1000&from=&to=`、`/spot/currencies`。
- 合约（settle = usdt/btc）：`GET /futures/{settle}/contracts`、`/futures/{settle}/tickers`、`/futures/{settle}/order_book`、`/futures/{settle}/trades`、`/futures/{settle}/candlesticks?contract=&interval=1m`（也支持 `mark_`/`index_` 前缀合约名）、`/futures/{settle}/premium_index`、`/futures/{settle}/funding_rate?contract=&limit=1000`（历史）、`/futures/{settle}/insurance`、`/futures/{settle}/contract_stats?contract=&interval=1h&limit=100`（含 OI、多空账户比、大户比、顶级持仓比——Gate 是少数直接给这些统计的交易所）、`/futures/{settle}/index_constituents/{index}`、`/futures/{settle}/liq_orders?contract=&from=&to=`（历史清算，分页）、`/futures/{settle}/risk_limit_tiers`。
- 交割：`/delivery/{settle}/...`；期权：`/options/underlyings`、`/options/contracts`、`/options/tickers`、`/options/underlying/tickers/{underlying}`、`/options/candlesticks`、`/options/trades`。
- WS：`spot.tickers`、`spot.trades`、`spot.candlesticks`、`spot.order_book`/`spot.order_book_update`/`spot.book_ticker`、`futures.tickers`、`futures.trades`、`futures.order_book`、`futures.order_book_update`、`futures.candlesticks`、`futures.public_liquidates`、`futures.contract_stats`。
- 限频：公共 200 req/10s/IP。

### HTX（火币）
- 文档：https://www.htx.com/en-us/opend/newApiPages/
- 现货 Base `https://api.huobi.pro`（备 `api-aws.huobi.pro`）：`GET /v2/settings/common/symbols`、`/market/tickers`、`/market/detail/merged?symbol=`、`/market/depth?symbol=&type=step0&depth=20`、`/market/history/trade?symbol=&size=2000`、`/market/history/kline?symbol=&period=1min&size=2000`（无 from/to，只能最近 2000 根）、`/v1/common/currencys`、`/v2/reference/currencies`。WS `wss://api.huobi.pro/ws`（gzip），`market.$symbol.kline.$period`、`.depth.step0`、`.mbp.refresh.20`/`.mbp.150`（增量）、`.trade.detail`、`.ticker`、`.bbo`。
- 合约 Base `https://api.hbdm.com`：币本位交割 `/api/v1/...`、币本位永续 `/swap-api/v1/...`、USDT 本位 `/linear-swap-api/v1/...`。常用：`/linear-swap-api/v1/swap_contract_info`、`/linear-swap-ex/market/detail/merged`、`/linear-swap-ex/market/depth`、`/linear-swap-ex/market/history/kline?contract_code=&period=1min&from=&to=`、`/linear-swap-ex/market/history/trade`、`/linear-swap-api/v1/swap_funding_rate`、`/linear-swap-api/v1/swap_batch_funding_rate`、`/linear-swap-api/v1/swap_historical_funding_rate?contract_code=&page_index=&page_size=50`、`/linear-swap-api/v1/swap_open_interest`、`/linear-swap-api/v1/swap_his_open_interest?contract_code=&period=60min&size=200&amount_type=1|2`、`/linear-swap-api/v1/swap_elite_account_ratio`、`/linear-swap-api/v1/swap_elite_position_ratio`、`/linear-swap-api/v1/swap_liquidation_orders`（历史清算，需 key）、`/linear-swap-api/v1/swap_insurance_fund`、`/linear-swap-api/v1/swap_estimated_settlement_price`、`/linear-swap-api/v1/swap_premium_index_kline`、`/linear-swap-api/v1/swap_basis`。WS `wss://api.hbdm.com/linear-swap-ws`、系统状态 `/linear-swap-notification`。
- 限频：公共按 IP 约 100 req/10s；私有按 UID。

### MEXC
- 文档：https://mexcdevelop.github.io/apidocs/spot_v3_en/ 与 https://mexcdevelop.github.io/apidocs/contract_v1_en/
- 现货 Base `https://api.mexc.com`（Binance 风格）：`GET /api/v3/exchangeInfo`、`/depth?limit=5000`、`/trades`、`/aggTrades?startTime=&endTime=`、`/klines?interval=1m&limit=1000`、`/ticker/24hr`、`/ticker/price`、`/ticker/bookTicker`、`/api/v3/defaultSymbols`、`/api/v3/capital/config/getall`（需 key）。WS `wss://wbs-api.mexc.com/ws`（protobuf，2025 起 v3 新版；旧 JSON `wss://wbs.mexc.com/ws` 已下线），频道 `spot@public.aggre.deals.v3.api.pb@100ms@BTCUSDT`、`spot@public.kline.v3.api.pb@Min1@`、`spot@public.aggre.depth.v3.api.pb@100ms@`、`spot@public.limit.depth.v3.api.pb@`、`spot@public.aggre.bookTicker.v3.api.pb@`。
- 合约 Base `https://contract.mexc.com`：`GET /api/v1/contract/detail`、`/api/v1/contract/ticker`、`/api/v1/contract/depth/{symbol}`、`/api/v1/contract/deals/{symbol}`、`/api/v1/contract/kline/{symbol}?interval=Min1&start=&end=`、`/api/v1/contract/kline/index_price/`、`/api/v1/contract/kline/fair_price/`、`/api/v1/contract/funding_rate/{symbol}`、`/api/v1/contract/funding_rate/history?symbol=&page_num=&page_size=100`、`/api/v1/contract/risk_reverse`（风险准备金）、`/api/v1/contract/risk_reverse/history`。OI 在 `ticker` 的 `holdVol`。WS `wss://contract.mexc.com/edge`（`sub.ticker`、`sub.deal`、`sub.depth`、`sub.kline`、`sub.funding.rate`、`sub.index.price`、`sub.fair.price`）。
- 限频：现货 500 权重/10s/IP；合约 20 req/2s。
- 坑：合约下单接口长期"维护中"不对外；小币种多、下架频繁，`exchangeInfo` 要每日刷新。

---

## 3. 衍生品专营

### Deribit
- 文档：https://docs.deribit.com/ ；Base REST `https://www.deribit.com/api/v2/public/`，WS `wss://www.deribit.com/ws/api/v2`（JSON-RPC 2.0，REST 与 WS 方法同名）；测试网 `test.deribit.com`。
- 行情：`get_instruments?currency=BTC&kind=option|future|spot&expired=false`、`get_book_summary_by_currency?currency=BTC&kind=option`（全量期权 IV、OI、标记价、Greeks 需单个 `ticker`）、`ticker?instrument_name=`（含 greeks、iv、mark_iv、open_interest、funding_8h、current_funding）、`get_order_book?depth=`、`get_last_trades_by_currency?currency=&kind=&count=1000&start_timestamp=`、`get_last_trades_by_instrument`、`get_tradingview_chart_data?instrument_name=&resolution=1&start_timestamp=&end_timestamp=`、`get_funding_rate_history?instrument_name=BTC-PERPETUAL&start_timestamp=&end_timestamp=`、`get_funding_rate_value`、`get_funding_chart_data`、`get_historical_volatility?currency=BTC`、`get_volatility_index_data?currency=BTC&resolution=60&start_timestamp=&end_timestamp=`（**DVOL**）、`get_index_price?index_name=btc_usd`、`get_index_price_names`、`get_delivery_prices`、`get_contract_size`、`get_expirations`、`get_mark_price_history`、`get_settlement_history_by_currency`/`by_instrument`（清算/交割/结算记录）、`get_rfqs`、`get_combo_details`。
- WS 频道：`book.{instrument}.{group}.{depth}.{interval}`、`trades.{instrument|kind.currency}.{interval}`、`ticker.{instrument}.{interval}`、`chart.trades.{instrument}.{resolution}`、`deribit_price_index.{index}`、`deribit_price_ranking.{index}`、`deribit_volatility_index.{index}`、`estimated_expiration_price.{index}`、`markprice.options.{index}`（全量期权标记价/IV 推送）、`perpetual.{instrument}.{interval}`（资金费）、`platform_state`、`quote.{instrument}`、`instrument.state.{kind}.{currency}`、`block_trade_confirmations`（私有）。
- 限频：公共无认证约 20 req/s 以内；认证用户按积分（credits）制。
- 坑：期权 Greeks 只能逐合约 `ticker` 拿，全量用 WS `markprice.options.btc_usd`；历史 IV 曲面 Deribit 不提供，需 Laevitas/Amberdata/Tardis 回放。

### BitMEX
- 文档：https://www.bitmex.com/api/explorer/ ；Base `https://www.bitmex.com/api/v1`；WS `wss://ws.bitmex.com/realtime`
- `GET /instrument?symbol=XBTUSD`、`/instrument/active`、`/instrument/activeIntervals`、`/instrument/compositeIndex?symbol=.BXBT`（指数成分）、`/instrument/indices`、`/orderBook/L2?symbol=&depth=`、`/trade?symbol=&count=1000&startTime=&endTime=&start=`（全历史，可翻页回溯到 2014）、`/trade/bucketed?binSize=1m&partial=false&symbol=&count=1000&startTime=`（K 线含 vwap、homeNotional、foreignNotional）、`/funding?symbol=&count=500&startTime=&reverse=true`（历史资金费，回溯全历史）、`/insurance`、`/settlement`、`/liquidation`（当前清算挂单）、`/quote`、`/quote/bucketed`、`/stats`、`/stats/history`、`/announcement`。
- WS：`instrument`、`orderBookL2`、`orderBookL2_25`、`orderBook10`、`quote`、`trade`、`tradeBin1m`、`funding`、`insurance`、`liquidation`、`settlement`、`publicNotifications`、`announcement`。
- 限频：未认证 30 req/min，认证 120 req/min（header `x-ratelimit-remaining`）。
- 坑：限频极低，适合取历史不适合高频轮询；逐笔 trade 历史全量也可用 S3 公开归档 `https://public.bitmex.com/?prefix=data/trade/`（每日 csv.gz，2014 至今，见 11）。

### Kraken Futures / CME / Bitnomial / Cboe
见本文件 Kraken 节与 `07-derivatives.md`（CME、CFTC COT、Cboe FTX-US 遗留、Bitnomial）。

---

## 4. 其他交易所速查表

| 交易所 | 文档 | Base URL（REST / WS） | 认证 | 公共限频 | 特色数据 / 坑 |
|---|---|---|---|---|---|
| Bitfinex | https://docs.bitfinex.com/ | `https://api-pub.bitfinex.com/v2/` / `wss://api-pub.bitfinex.com/ws/2` | HMAC-SHA384 | 10–90 req/min 按接口 | `tickers?symbols=ALL`、`book/tBTCUSD/P0|R0`（R0 原始订单）、`trades/tBTCUSD/hist?limit=10000&start=&end=`（全历史）、`candles/trade:1m:tBTCUSD/hist?limit=10000`（全历史、也支持 `a`前缀 `candles/trade:1D:fUSD:p30`）、`stats1/pos.size:1m:tBTCUSD:long/hist`（多空持仓！）、`stats1/funding.size:1m:fUSD/hist`、`stats1/credits.size`、`status/deriv?keys=ALL`（永续 OI、资金费）、`calc/trade/avg`、`conf/pub:list:pair:exchange`、杠杆借贷市场 `fUSD` 全套、`pulse/hist`；WS `ticker`、`trades`、`book`（prec P0–P4 / R0、len 1/25/100/250）、`candles`、`status` |
| Gemini | https://docs.gemini.com/rest-api/ | `https://api.gemini.com/v1|v2` / `wss://api.gemini.com/v1/marketdata/{symbol}` 、`v2/marketdata` | HMAC-SHA384 | 120 req/min | `v1/symbols`、`v1/pubticker/{symbol}`、`v2/ticker/{symbol}`、`v2/candles/{symbol}/1m`、`v1/book/{symbol}?limit_bids=0`、`v1/trades/{symbol}?timestamp=&limit_trades=500`、`v1/auction/{symbol}`、`v1/pricefeed`、`v1/fundingamount/{symbol}`（永续）、`v1/feepromos`；WS v2 `l2`、`candles_1m`；也有 Gemini ActiveTrader |
| Bitstamp | https://www.bitstamp.net/api/ | `https://www.bitstamp.net/api/v2/` / `wss://ws.bitstamp.net` | HMAC-SHA256 | 400 req/s 总体 8000/10min | `ticker/`、`ticker/{pair}/`、`order_book/{pair}/?group=0|1|2`、`transactions/{pair}/?time=hour|day|minute`、`ohlc/{pair}/?step=60&limit=1000&start=&end=`（历史 K 线可回溯）、`trading-pairs-info/`、`currencies/`、`eur_usd/`；WS `live_trades_`、`live_orders_`、`order_book_`、`detail_order_book_`、`diff_order_book_` |
| Crypto.com Exchange | https://exchange-docs.crypto.com/exchange/v1/rest-ws/index.html | `https://api.crypto.com/exchange/v1/public/` / `wss://stream.crypto.com/exchange/v1/market` | HMAC-SHA256 | 100 req/s | `get-instruments`、`get-book?instrument_name=&depth=50`、`get-candlestick?timeframe=M1&count=300&start_ts=&end_ts=`、`get-trades?count=150`、`get-tickers`、`get-valuations?instrument_name=BTCUSD-INDEX&valuation_type=index_price|mark_price|funding_hist|funding_rate|estimated_funding_rate`（含历史资金费）、`get-expired-settlement-price`、`get-insurance`、`get-announcements`、`get-risk-parameters`；WS `book.{instrument}.{depth}`、`ticker.`、`trade.`、`candlestick.{tf}.`、`index.`、`mark.`、`settlement.`、`funding.`、`estimatedfunding.`、`insurance.` |
| Upbit（韩） | https://docs.upbit.com/ | `https://api.upbit.com/v1/` / `wss://api.upbit.com/websocket/v1` | JWT(HS256) | 公共 10 req/s 按组（header `Remaining-Req`） | `market/all?is_details=true`（含警示标记 market_warning）、`ticker?markets=KRW-BTC`、`ticker/all?quote_currencies=KRW`、`orderbook?markets=&level=`、`trades/ticks?market=&count=500&cursor=&days_ago=`（最多回溯 7 天）、`candles/minutes/1?market=&to=&count=200`、`candles/days`/`weeks`/`months`/`years`、`candles/seconds`；WS `ticker`、`trade`、`orderbook`、`candle.1m`；韩国溢价（Kimchi premium）需结合 USD/KRW 汇率自行计算 |
| Bithumb（韩） | https://apidocs.bithumb.com/ | `https://api.bithumb.com/v1/`（2024 新 API，Upbit 风格）与旧 `/public/` / `wss://ws-api.bithumb.com/websocket/v1` | JWT | 150 req/s | 新 API 路径与 Upbit 几乎一致：`market/all`、`ticker`、`orderbook`、`trades/ticks`、`candles/minutes/1`、`market/virtual_asset_warning`；旧 `public/ticker/ALL_KRW`、`public/transaction_history/BTC_KRW`、`public/candlestick/BTC_KRW/1m`、`public/assetsstatus/ALL`、`public/network-info` |
| Coinone（韩） | https://docs.coinone.co.kr/ | `https://api.coinone.co.kr/public/v2/` / `wss://stream.coinone.co.kr` | HMAC-SHA512 | 公共按 IP 300/min | `ticker_new/KRW`、`orderbook/KRW/BTC?size=16`、`trades/KRW/BTC?size=200`、`chart/KRW/BTC?interval=1m&timestamp=&size=500`、`markets/KRW`、`currencies`、`range_units` |
| Korbit（韩） | https://docs.korbit.co.kr/ | `https://api.korbit.co.kr/v2/` | OAuth/HMAC | 低 | `tickers`、`orderbook`、`trades`、`candles` |
| bitFlyer（日） | https://lightning.bitflyer.com/docs?lang=en | `https://api.bitflyer.com/v1/` / `wss://ws.lightstream.bitflyer.com/json-rpc`（JSON-RPC） | HMAC-SHA256 | 500 req/5min 公共 | `getmarkets`、`getticker?product_code=FX_BTC_JPY`、`getboard`、`getexecutions?count=500&before=`（回溯全历史）、`getboardstate`、`gethealth`、`getfundingrate?product_code=FX_BTC_JPY`（SFD/永续）、`getchats`；无官方 K 线接口（用 Cryptowatch 遗产或自聚合）；WS `lightning_board_snapshot_`、`lightning_board_`、`lightning_ticker_`、`lightning_executions_` |
| Coincheck（日） | https://coincheck.com/documents/exchange/api | `https://coincheck.com/api/` / `wss://ws-api.coincheck.com/` | HMAC | 低 | `ticker`、`trades?pair=btc_jpy`、`order_books`、`exchange/orders/rate`、`rate/{pair}` |
| Zaif（日） | https://zaif-api-document.readthedocs.io/ | `https://api.zaif.jp/api/1/` | HMAC-SHA512 | 低 | `ticker/btc_jpy`、`trades/`、`depth/`、`currency_pairs/all` |
| GMO Coin（日） | https://api.coin.z.com/docs/ | `https://api.coin.z.com/public/v1/` / `wss://api.coin.z.com/ws/public/v1` | HMAC | 1 req/s 公共 | `status`、`ticker?symbol=`、`orderbooks`、`trades?symbol=&page=&count=100`、`klines?symbol=&interval=1min&date=`（按日取） |
| Bitso（拉美） | https://docs.bitso.com/ | `https://api.bitso.com/v3/` 与 `/api/v3/` / `wss://ws.bitso.com` | HMAC-SHA256 | 60 req/min | `available_books`、`ticker?book=btc_mxn`、`order_book?book=&aggregate=`、`trades?book=&limit=100&marker=`、`ohlc?book=&time_bucket=60&start=&end=`（新）；拉美法币对（MXN/BRL/ARS/COP）溢价数据 |
| Mercado Bitcoin（巴西） | https://api.mercadobitcoin.net/api/v4/docs | `https://api.mercadobitcoin.net/api/v4/` | Bearer | 低 | `symbols`、`{symbol}/ticker`、`{symbol}/orderbook`、`{symbol}/trades`、`candles?symbol=&resolution=1m&from=&to=` |
| Buda（智利/哥伦比亚/秘鲁/阿根廷） | https://api.buda.com/ | `https://www.buda.com/api/v2/` | HMAC | 低 | `markets`、`markets/{id}/ticker`、`markets/{id}/order_book`、`markets/{id}/trades?timestamp=&limit=` |
| BingX | https://bingx-api.github.io/docs/ | `https://open-api.bingx.com` / `wss://open-api-swap.bingx.com/swap-market`（gzip） | HMAC-SHA256 | 公共按接口 10–100 req/s | 现货 `/openApi/spot/v1/common/symbols`、`/openApi/spot/v1/ticker/24hr`、`/openApi/spot/v1/market/depth`、`/openApi/spot/v1/market/trades`、`/openApi/spot/v2/market/kline`；永续 `/openApi/swap/v2/quote/contracts`、`/quote/price`、`/quote/depth`、`/quote/trades`、`/quote/premiumIndex`、`/quote/fundingRate?symbol=&limit=1000&startTime=`（历史）、`/quote/klines`、`/quote/openInterest`、`/quote/ticker`、`/openApi/swap/v1/market/historicalTrades`、`/openApi/swap/v1/market/markPriceKlines`；跟单/带单数据 `/openApi/copyTrading/...`（需 key）；WS `<symbol>@trade`、`@depth20`、`@kline_1m`、`@ticker`、`@bookTicker`、`@markPrice` |
| Phemex | https://phemex-docs.github.io/ | `https://api.phemex.com` / `wss://ws.phemex.com`（JSON-RPC） | HMAC-SHA256 | 公共 100 req/min 组 | `GET /public/products`、`/public/md/v2/kline/last?symbol=&resolution=60&limit=1000`、`/exchange/public/md/v2/kline?symbol=&resolution=&from=&to=`、`/md/v2/orderbook?symbol=`、`/md/v2/trade?symbol=`、`/md/v2/ticker/24hr?symbol=`、`/md/v2/ticker/24hr/all`、`/api-data/public/data/funding-rate-history?symbol=&limit=100`、`/md/v3/ticker/24hr`（含 openInterestRv、fundingRateRr、indexPriceRp、markPriceRp）；注意价格有 `Rp`（真实）与 `Ep`（放大整数）两种字段；WS `orderbook_p.subscribe`、`trade_p.subscribe`、`kline_p.subscribe`、`perp_market24h_pack_p.subscribe` |
| CoinEx | https://docs.coinex.com/api/v2/ | `https://api.coinex.com/v2/` / `wss://socket.coinex.com/v2/spot|futures` | HMAC-SHA256 | 400 req/s 总 | `spot/market`、`spot/ticker`、`spot/depth?market=&limit=50&interval=0`、`spot/deals`、`spot/kline?market=&period=1min&limit=1000`、`spot/index`；`futures/market`、`futures/ticker`、`futures/depth`、`futures/deals`、`futures/kline`、`futures/funding-rate?market=`、`futures/funding-rate-history?market=&start_time=&end_time=&limit=1000`、`futures/premium-index-history`、`futures/position-level`、`futures/liquidation-history?market=&start_time=&end_time=`（**公开历史清算**）、`futures/basis-history`、`assets/info`、`assets/deposit-withdraw-config`；OI 在 `futures/ticker` 的 `open_interest_volume` |
| WhiteBIT | https://docs.whitebit.com/public/http-v4/ | `https://whitebit.com/api/v4/public/` / `wss://api.whitebit.com/ws` | HMAC | 公共 1000 req/10s | `markets`、`ticker`、`assets`、`orderbook/{market}?limit=100&level=`、`trades/{market}?type=`、`kline?market=&interval=1m&start=&end=&limit=1440`、`futures`（含 funding_rate、open_interest、next_funding_rate_timestamp）、`fee`、`collateral/markets`、`mining-pool`；v1 `https://whitebit.com/api/v1/public/kline` |
| LBank | https://www.lbank.com/en-US/docs/index.html | `https://api.lbkex.com/v2/` 或 `https://api.lbank.info/v2/` / `wss://www.lbkex.net/ws/V2/` | RSA/HMAC | 低 | `currencyPairs.do`、`ticker/24hr.do?symbol=all`、`depth.do?symbol=&size=200`、`trades.do?symbol=&size=600&time=`、`kbar.do?symbol=&size=2000&type=minute1&time=`、`accuracy.do`、`supplement/system_status.do`；合约 `https://lbkperp.lbank.com/cfd/openApi/v1/pub/...`（`instrument`、`marketData`、`marketOrder`、`marketDepth`、`kline`、`fundingRate`） |
| Poloniex | https://api-docs.poloniex.com/spot | `https://api.poloniex.com/` / `wss://ws.poloniex.com/ws/public` | HMAC-SHA256 | 200 req/s 公共 | `markets`、`markets/{symbol}/price`、`markets/price`、`markets/{symbol}/orderBook?limit=150`、`markets/{symbol}/trades?limit=1000`、`markets/{symbol}/candles?interval=MINUTE_1&limit=500&startTime=&endTime=`、`markets/ticker24h`、`currencies?includeMultiChainCurrencies=true`、`markets/collateralInfo`、`markets/borrowRatesInfo`；永续 `https://api.poloniex.com/v3/market/...`（`allInstruments`、`tickers`、`orderBook`、`trades`、`candles`、`fundingRate`、`fundingRate/history`、`openInterest`、`riskLimit`） |
| Backpack | https://docs.backpack.exchange/ | `https://api.backpack.exchange/api/v1/` / `wss://ws.backpack.exchange` | ED25519 签名 | 公共宽松 | `markets`、`market?symbol=`、`ticker?symbol=&interval=1d`、`tickers`、`depth?symbol=`、`klines?symbol=&interval=1m&startTime=&endTime=`、`trades?symbol=&limit=1000`、`trades/history?symbol=&limit=&offset=`（全历史）、`markPrices?symbol=`（含 fundingRate、nextFundingTimestamp、indexPrice、markPrice）、`openInterest?symbol=`、`fundingRates?symbol=&limit=&offset=`（历史）、`borrowLend/markets`、`borrowLend/markets/history?interval=`、`assets`、`collateral`、`status`、`wallets`；WS `bookTicker.`、`depth.`、`depth.200ms.`、`kline.1m.`、`markPrice.`、`openInterest.`、`trade.`、`ticker.`、`liquidation`（**公开全量清算**）；Solana 系交易所，BACKPACK 积分/季度数据无 API |
| WOO X | https://docs.woox.io/ | `https://api.woox.io/v1|v3/public/` / `wss://wss.woox.io/ws/stream/{app_id}` | HMAC-SHA256 | 10 req/s 公共 | `v1/public/info`、`v1/public/market_trades?symbol=&limit=`、`v1/public/orderbook/{symbol}?max_level=`、`v1/public/kline?symbol=&type=1m&limit=1000`、`v1/public/futures`（含 est_funding_rate、open_interest、mark_price、index_price、last_funding_rate）、`v1/public/funding_rates`、`v1/public/funding_rate_history?symbol=&start_t=&end_t=`、`v1/public/token`、`v1/public/token_network`、`v3/public/insuranceFund`、`v1/public/system_info`；v3 新版 `v3/public/instruments`、`v3/public/marketTrades`、`v3/public/orderbook`、`v3/public/kline`、`v3/public/fundingRateHistory`、`v3/public/futures`、`v3/public/marketInfo`、`v3/public/predictedFunding`、`v3/public/openInterest`、`v3/public/leverageSetting`、`v3/public/campaignAssets` |
| BtcTurk（土耳其） | https://docs.btcturk.com/ | `https://api.btcturk.com/api/v2/` 、 `https://graph-api.btcturk.com/v1/` / `wss://ws-feed-pro.btcturk.com` | HMAC-SHA256 | 公共按 IP | `ticker`、`ticker/currency?symbol=TRY`、`orderbook?pairSymbol=BTCTRY&limit=100`、`trades?pairSymbol=&last=50`、`server/exchangeinfo`；K 线 `graph-api.../klines/history?symbol=&resolution=1&from=&to=`、`ohlcs?pair=`；TRY 溢价 |
| Paribu（土耳其） | 无正式公开 API 文档 | `https://www.paribu.com/ticker` | — | — | 仅 ticker JSON（非官方）；用 CoinGecko 代替 |
| Luno（非洲/亚太） | https://www.luno.com/en/developers/api | `https://api.luno.com/api/1/` 与 `/api/exchange/1/` | Basic/Key | 300 req/min 公共 | `tickers`、`ticker?pair=XBTZAR`、`orderbook_top?pair=`、`orderbook?pair=`、`trades?pair=&since=`、`candles?pair=&since=&duration=60`（需 key）、`markets`；ZAR/NGN/MYR/IDR/UGX 法币对 |
| VALR（南非） | https://docs.valr.com/ | `https://api.valr.com/v1/public/` / `wss://api.valr.com/ws/trade` | HMAC-SHA512 | 公共按 IP | `currencies`、`pairs`、`{pair}/orderbook`、`{pair}/orderbook/full`、`{pair}/trades?limit=100&skip=&beforeId=`、`{pair}/markprice`、`{pair}/futures/info`、`{pair}/futures/funding/history`、`marketsummary`、`{pair}/buckets?periodSeconds=60&startTime=&endTime=` |
| Binance.US | https://docs.binance.us/ | `https://api.binance.us` / `wss://stream.binance.us:9443` | HMAC | 1200 权重/min | 现货接口与 Binance 全球版 `/api/v3/*` 相同；无合约；适合美国价格 |
| Bullish | https://api.exchange.bullish.com/docs/api/rest/ | `https://api.exchange.bullish.com/trading-api/v1|v2/` | ECDSA/HMAC + JWT | 公共 50 req/s | `markets`、`markets/{symbol}/orderbook/hybrid`、`markets/{symbol}/trades`、`markets/{symbol}/tick`、`markets/{symbol}/candle?timeBucket=1m&createdAtDatetime[gte]=`、`assets`、`index-prices`、`market-data/...`；机构所，AMM 混合流动性 |
| Bitvavo（欧洲） | https://docs.bitvavo.com/ | `https://api.bitvavo.com/v2/` / `wss://ws.bitvavo.com/v2/` | HMAC-SHA256 | 1000 权重/min | `markets`、`assets`、`{market}/book?depth=`、`{market}/trades?limit=1000&start=&end=`、`{market}/candles?interval=1m&limit=1440&start=&end=`、`ticker/price`、`ticker/book`、`ticker/24h`、`report/...`（MiCA 披露） |
| Kraken-owned CoinDesk Indices、Bitstamp Index 等指数见 03 | | | | | |
| Independent Reserve（澳） | https://www.independentreserve.com/products/api | `https://api.independentreserve.com/Public/` | HMAC-SHA256 | 公共按 IP | `GetValidPrimaryCurrencyCodes`、`GetMarketSummary?primaryCurrencyCode=xbt&secondaryCurrencyCode=aud`、`GetOrderBook`、`GetAllOrders`、`GetRecentTrades?numberOfRecentTradesToRetrieve=50`、`GetTradeHistorySummary?numberOfHoursInThePastToRetrieve=`、`GetFxRates` |
| BTC Markets（澳） | https://docs.btcmarkets.net/ | `https://api.btcmarkets.net/v3/` / `wss://socket.btcmarkets.net/v2` | HMAC-SHA512 | 50 req/10s | `markets`、`markets/{id}/ticker`、`markets/{id}/trades?limit=200&before=`、`markets/{id}/orderbook?level=2`、`markets/{id}/candles?timeWindow=1m&from=&to=&limit=1000`、`markets/tickers?marketId=` |
| Coinbase/Kraken/Bitstamp 等法币入口均见上 | | | | | |
| HashKey Global / HashKey Exchange（香港持牌） | https://hashkeyglobal-apidoc.readme.io/ | `https://api-glb.hashkey.com` / `wss://stream-glb.hashkey.com/quote/ws/v1` | HMAC-SHA256 | 公共按 IP | `quote/v1/ticker/24hr`、`quote/v1/depth`、`quote/v1/trades`、`quote/v1/klines?symbol=&interval=1m`、`api/v1/exchangeInfo`、`quote/v1/markPrice`、`quote/v1/index`；香港持牌所价格参考 |
| OSL（香港） | https://docs.osl.com/ | `https://trade-hk.osl.com/api/v4/...` | HMAC | 低 | `instrument`、`orderbook`、`trades`、`ohlc` |
| Bitget/Bybit/OKX/Binance 的 TR、JP、ID、TH、AU、NL、EU 等本地化站点 | 同母站文档 | 域名不同（`api.binance.tr`、`api.bybit-tr.com`、`okx.com/jp` 等） | 同母站 | 同母站 | 接口基本同母站，交易对与法币不同 |

---

## 5. CCXT 统一接口

- 文档：https://docs.ccxt.com/ ；GitHub https://github.com/ccxt/ccxt ；支持 100+ 交易所，Python/JS/PHP/C#/Go。
- 统一公共方法：`load_markets()`、`fetch_ticker(s)`、`fetch_order_book(symbol, limit)`、`fetch_trades(symbol, since, limit)`、`fetch_ohlcv(symbol, timeframe, since, limit)`、`fetch_funding_rate(s)`、`fetch_funding_rate_history(symbol, since, limit)`、`fetch_open_interest(symbol)`、`fetch_open_interest_history(symbol, timeframe, since, limit)`、`fetch_liquidations` / `fetch_my_liquidations`、`fetch_long_short_ratio_history`（部分所）、`fetch_mark_ohlcv`、`fetch_index_ohlcv`、`fetch_premium_index_ohlcv`、`fetch_option(s)`、`fetch_greeks`、`fetch_volatility_history`、`fetch_currencies`、`fetch_deposit_withdraw_fees`、`fetch_status`、`fetch_time`。
- `ccxt.pro`（已并入主库）提供 WS：`watch_ticker(s)`、`watch_order_book(s)`、`watch_trades(_for_symbols)`、`watch_ohlcv(_for_symbols)`、`watch_liquidations(_for_symbols)`、`watch_funding_rate(s)`、`watch_mark_price(s)`。
- `exchange.has[...]` 查看某交易所是否支持某方法；`exchange.timeframes`；`exchange.rateLimit` + `enableRateLimit=True` 自动节流。
- 坑：统一字段会抹掉交易所特有字段（在 `info` 里保留原始响应）；OI/资金费单位 CCXT 不做统一换算，`openInterestAmount` 与 `openInterestValue` 要看是否为 None；CCXT 对新交易所（Hyperliquid、Backpack、Paradex、Lighter、Aster 等）支持程度不一，Hyperliquid 已支持。
- 类似库：`cryptofeed`（Python，WS 采集框架，支持 Binance/Bybit/OKX/Deribit/Kraken/Coinbase 等 + 写入 Kafka/Redis/Postgres/Arctic）、`cryptostore`、`tardis-machine`（本地 WS 回放）、`hummingbot` 连接器、`nautilus_trader` 适配器、`freqtrade`（基于 CCXT）。

---

## 6. 变更记录
- 2026-10 初版。
