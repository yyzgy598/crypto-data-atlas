---
name: crypto-data-map
description: 币圈数据地图——交易所、链上、衍生品、DeFi、聚合商、新闻情绪、宏观/ETF 等全部数据源的 API 目录与检索路由。只要用户在找"某个加密数据从哪拿 / 哪个接口能查 / 哪家交易所有这个数据 / 对比几个数据源 / 写采集脚本要接哪个 API"，哪怕没说出"API"或"数据源"这几个字（例如"我想看所有交易所的资金费率"、"怎么拿 Hyperliquid 的清算数据"、"ETF 净流入每天哪里有"、"链上大户转账怎么监控"），都要先加载这个 skill 再回答。也适用于评估数据源完整性、补充采集任务的数据来源、设计数据表时核对上游字段。
---

# 币圈数据地图（Crypto Data Map）

这个 skill 是一张"数据需求 → 数据源 → 具体接口"的地图。目标是让你在用户提出一个数据需求时，**几秒内给出所有可用的数据源、优先推荐哪个、接口长什么样、认证和限频如何、有什么坑**，而不是只报一个最常见的名字。

用户通常是在做数据采集、数据表设计或指标核对（例如交易所挂单/历史订单采集、资金费率对比、ETF 流入统计）。他们要的是**全**和**准**：漏掉一个重要数据源，比多列一个无关的更糟；给错一个接口路径，比说"我不确定，请查文档 X"更糟。

## 工作流程

1. **判断数据需求属于哪一类**（可能跨多类），用下面的「快速索引」定位。
2. **只读相关的 reference 文件**（见「分类目录」），不要一次读完所有文件。每个文件开头有目录。
3. **按「回答格式」输出**：先给推荐结论，再给候选数据源表，最后给接口细节和注意事项。
4. **不确定就说明，并给文档地址**。接口路径、限频、是否收费都会随时间变化；当你对某个细节不确定时，写清楚"以 `<docs url>` 为准"，可以的话用 `scripts/probe.py` 实际探测一下公开接口。如果有 WebFetch/WebSearch 工具，查证后再给出具体路径。
5. **用户问"有没有更全的"时**，逐类扫一遍 reference 文件的目录，列出遗漏项，而不是只凭记忆补一两个。

## 快速索引：数据需求 → 去哪找

| 想要的数据 | 首选 | 备选 / 补充 | 看哪个文件 |
|---|---|---|---|
| 现货/合约 K 线、成交、盘口（单交易所） | 交易所原生 REST/WS | CCXT 统一接口；Tardis、Kaiko 历史 | `references/01-cex.md` |
| 全市场价格、市值、流通量、代币元数据 | CoinGecko、CoinMarketCap | CryptoCompare(CCData)、Coinpaprika、Mobula、DefiLlama coins | `03-aggregators.md` |
| 资金费率、持仓量(OI)、多空比、清算 | Coinglass、交易所原生 | Coinalyze、Laevitas、Velo、Amberdata | `07-derivatives.md` + `01-cex.md` |
| 期权 IV、Greeks、Skew、DVOL | Deribit、Laevitas | Amberdata、Greeks.live、Coinglass options | `07-derivatives.md` |
| 永续 DEX 订单/成交/资金费（Hyperliquid、dYdX、Lighter、Aster…） | 协议原生 API | DefiLlama derivatives 汇总 | `02-dex.md` |
| 现货 DEX 交易对价格、流动性、新币 | Dexscreener、GeckoTerminal、Birdeye | Uniswap subgraph、Codex(Defined)、DEXTools | `02-dex.md` |
| 链上交易/地址/合约/日志（EVM、BTC、Solana、TON、Tron…） | 区块浏览器 API、节点 RPC | Covalent、Moralis、Bitquery、The Graph、Dune | `04-onchain-explorers.md` |
| 链上指标（MVRV、SOPR、交易所余额、巨鲸、实体标签） | Glassnode、CryptoQuant | Santiment、IntoTheBlock、Nansen、Arkham、Coin Metrics | `05-onchain-analytics.md` |
| TVL、手续费/收入、稳定币供应、桥、解锁、融资 | DefiLlama | Token Terminal、Artemis、L2Beat、Tokenomist、RWA.xyz | `06-defi.md` |
| ETF 净流入、持仓、机构持币 | Farside、SoSoValue、Coinglass ETF | 发行方官网、SEC EDGAR、bitcointreasuries | `09-macro-institutional.md` |
| 新闻、社媒热度、恐惧贪婪指数 | CryptoPanic、LunarCrush、Alternative.me | Santiment social、X API、Reddit、Farcaster(Neynar) | `08-news-social.md` |
| 宏观数据、美股、美债、美元指数 | FRED、Yahoo Finance | Alpha Vantage、Polygon.io、Twelve Data | `09-macro-institutional.md` |
| 预测市场、质押、挖矿、MEV、NFT、安全/合约风险、Gas、法币汇率 | 见文件内分节 | | `10-misc.md` |
| 历史全量数据下载（逐笔/盘口快照/K 线归档） | 交易所数据门户、Tardis | Kaiko、CryptoDataDownload、Kaggle | `11-bulk-data.md` |

## 分类目录（references/）

| 文件 | 覆盖内容 |
|---|---|
| `01-cex.md` | 40+ 家中心化交易所的 REST/WS：Binance、OKX、Bybit、Bitget、Coinbase、Kraken、KuCoin、Gate、HTX、MEXC、Bitfinex、Deribit、BitMEX、Upbit、Bithumb、Crypto.com、BingX、Phemex、CoinEx、WhiteBIT、Backpack… 以及 CCXT |
| `02-dex.md` | 永续 DEX（Hyperliquid 重点、dYdX、GMX、Lighter、Aster、Paradex、Drift、Jupiter Perps、Vertex、Orderly…）、现货 DEX 与聚合器（Uniswap、Curve、Raydium、Jupiter、1inch、0x、CoW…）、DEX 数据商（Dexscreener、GeckoTerminal、Birdeye、Codex、DEXTools、Moralis） |
| `03-aggregators.md` | 行情聚合与市场数据商：CoinGecko、CoinMarketCap、CryptoCompare、Kaiko、Coin Metrics、Amberdata、CoinAPI、Messari、Mobula、Coinpaprika、CoinCap、LiveCoinWatch、Coinglass 概览、预言机价格（Pyth、Chainlink） |
| `04-onchain-explorers.md` | 区块浏览器 API（Etherscan V2 多链、Blockscout、Blockchair、Mempool.space、Solscan、TronGrid、Toncenter、Suiscan、Mintscan、Hypurrscan…）、节点 RPC 提供商、索引器（The Graph、Covalent、Moralis、Bitquery、Dune、Flipside、Allium、Subsquid、Goldsky、Envio） |
| `05-onchain-analytics.md` | 链上分析与标签：Glassnode、CryptoQuant、Santiment、IntoTheBlock、Nansen、Arkham、Chainalysis、Elliptic、TRM、DeBank、Zerion、Zapper、Whale Alert、Bubblemaps、Cielo、Vybe |
| `06-defi.md` | DefiLlama 全部子 API、L2Beat、借贷协议（Aave、Compound、Morpho、Sky）、LSD/再质押（Lido、EigenLayer）、Pendle、稳定币发行方透明度、RWA、跨链桥、代币解锁与融资数据 |
| `07-derivatives.md` | 衍生品专项：Coinglass 全接口、Coinalyze、Laevitas、Velo、Amberdata、Deribit 指标、Greeks.live、CME/CFTC COT、清算热力图数据口径 |
| `08-news-social.md` | 新闻与社媒：CryptoPanic、CoinDesk、The Block、Messari、LunarCrush、Santiment、Alternative.me、X/Twitter、Reddit、Telegram、Discord、Farcaster、Google Trends、治理（Snapshot、Tally） |
| `09-macro-institutional.md` | 宏观与机构：FRED、Treasury、BLS、ECB、Yahoo/yfinance、Alpha Vantage、Polygon.io、SEC EDGAR、ETF 流入（Farside、SoSoValue）、企业持币、CoinShares、Grayscale、OFAC 制裁名单 |
| `10-misc.md` | 预测市场（Polymarket、Kalshi）、质押（beaconcha.in、Rated、StakingRewards）、挖矿（Hashrate Index、mempool）、MEV（Flashbots、EigenPhi、Jito）、NFT（OpenSea、Magic Eden、Blur、NFTScan）、安全（GoPlus、De.Fi、DefiLlama hacks）、Gas、ENS、法币汇率、出入金商 |
| `11-bulk-data.md` | 历史全量数据与采集模式：交易所数据门户、Tardis、Kaiko、CryptoDataDownload、Kaggle；REST 分页/WS 断线重连/限频处理的通用做法；CCXT |

## 回答格式

对"X 数据从哪拿"这类问题，用下面的结构（可按需精简，但顺序不变）：

```
## 结论
一句话：推荐用 A（原因），需要 B 时用 C。

## 候选数据源
| 数据源 | 覆盖范围 | 认证/价格 | 限频 | 粒度/历史深度 | 备注 |

## 接口细节（只列推荐的 1–3 个）
- 数据源 A
  - 文档：<url>
  - 接口：GET <base>/<path>?<params>
  - 返回字段要点 / 分页方式 / WS 频道
  - 坑：…

## 注意事项
数据口径差异、延迟、是否需要翻墙/代理、免费层限制、历史是否可回溯。
```

写接口时**把 base URL 和路径写全**（例如 `https://fapi.binance.com/fapi/v1/fundingRate?symbol=BTCUSDT&limit=1000`），不要只写"用 Binance 的 funding rate 接口"。用户通常会直接拿去用。

## 回答时的判断原则

- **区分"原始数据"和"加工数据"**。交易所原生接口是原始源，Coinglass/CoinGecko 是加工源。要做对账或高频采集，推荐原始源；要跨所对比或快速出图，推荐加工源。两者都要列出来。
- **指出口径差异**。同一个"持仓量"，Binance 返回合约张数，Bybit 返回币本位数量，Coinglass 统一成 USD；同一个"资金费率"，有 8 小时结算也有 1 小时结算（Hyperliquid、部分 Bybit 合约）。用户拿去对比前需要知道这些。
- **注意可获得性**。有些数据商只有付费层有历史数据（Glassnode、Kaiko、Nansen）；有些接口对中国大陆 IP 有限制（Binance、OKX 部分域名）；有些需要机构合同（Chainalysis、Kaiko）。在表里的"认证/价格"列写明。
- **历史深度要说明**。例如 Hyperliquid `historicalOrders` 只返回最近 2000 条；Binance `fundingRate` 单次最多 1000 条但可以按时间翻页回溯到上线；Coinglass 免费层历史有限。
- **WebSocket 与 REST 分开写**。做实时采集的用户要的是 WS 频道名和订阅格式；做回测的用户要的是 REST 分页方式。
- **给出至少一个备选**。单一数据源会挂、会改接口、会涨价。

## 维护

这张地图的内容截至 2026 年中。接口会变，新数据源会出现。当你在使用中发现某个路径已失效或某家数据源有了新能力：
- 直接修改对应 reference 文件里的那一行，并在文件末尾的「变更记录」加一条日期+说明；
- 新增数据源时按已有表格列填写，不要只写名字。

`scripts/probe.py` 可以快速探测一个公开 REST 接口是否可用、返回什么字段，适合在给用户答案前自检：

```bash
python3 scripts/probe.py "https://api.hyperliquid.xyz/info" --post '{"type":"meta"}'
python3 scripts/probe.py "https://fapi.binance.com/fapi/v1/fundingRate?symbol=BTCUSDT&limit=2"
```
