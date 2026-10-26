# 08 · 新闻、社媒、情绪、开发者活动、搜索热度

目录
1. 新闻聚合 API：CryptoPanic、CCData News、Messari News、CoinGecko News、CMC Content、NewsAPI/GNews/Bing、The Block、CoinDesk、Cointelegraph、Decrypt、Blockworks、The Defiant、Odaily/PANews/律动/金色/Foresight（中文）、Velo News、Tree of Alpha、Phoenix News、BWE、Watcher.Guru、Wu Blockchain、DB News、Unfolded
2. 情绪指数：Alternative.me F&G、CMC F&G、Coinglass F&G、Glassnode fear_greed、Santiment sentiment、LunarCrush、Augmento（退）、TheTIE（→ CoinDesk Data）、CFGI、Bitcoin Rainbow、Polymarket 情绪
3. 社媒数据：X/Twitter API、LunarCrush、Santiment social、Kaito、Cookie、Reddit、Telegram、Discord、Farcaster（Neynar/Warpcast）、Lens、YouTube、TikTok、Bluesky、Nostr、Stocktwits、Threads
4. 搜索与关注度：Google Trends、Wikipedia pageviews、App Store 排名、CoinGecko trending、CMC trending、Dexscreener boosts、GitHub stars
5. 开发者活动：Electric Capital、Santiment devActivity、CCData code-repository、Artemis dev、GitHub API、Token Terminal、CryptoMiso
6. KOL / 影响力：Kaito Yaps、Cookie Mindshare、LunarCrush creators、Kolscan、Twitter 列表
7. 口径与注意事项
8. 变更记录

---

## 1. 新闻聚合 API
| 来源 | 文档/Base | 认证/价格 | 关键接口 | 备注 |
|---|---|---|---|---|
| CryptoPanic | https://cryptopanic.com/developers/api/ ；`https://cryptopanic.com/api/developer/v2/posts/?auth_token=&public=true&currencies=BTC,ETH&filter=rising|hot|bullish|bearish|important|saved|lol&kind=news|media|all&regions=en,zh,de,es,fr,it,nl,pt,ru,tr,ar,cn,jp,ko` | 免费 Developer（有限频，延迟）；Growth/Business 更高；v1 旧接口 2025 退役 | `posts/`（标题、source、url、published_at、currencies、votes{negative,positive,important,liked,disliked,lol,toxic,saved,comments}、kind、domain、slug、panic_score（Pro）） | 带社区投票的情绪标签；中文源有限 |
| CCData News（原 CryptoCompare） | `https://data-api.ccdata.io/news/v1/article/list?lang=EN&limit=100&source_ids=coindesk,cointelegraph,...&categories=BTC,ETH&exclude_categories=&to_ts=`、`news/v1/source/list?lang=EN&status=ACTIVE`、`news/v1/category/list` | 免费层可用 | 多语言（EN/ES/TR/FR/JP/PT/DE）；返回含 `SENTIMENT`（POSITIVE/NEUTRAL/NEGATIVE）、`KEYWORDS`、`CATEGORY_DATA`、`UPVOTES/DOWNVOTES` | 老牌，源 80+ |
| Messari News | `https://api.messari.io/news/v1/news/feed?assets=&sources=&publishedAfter=&limit=`、`/news/v1/news/assets`、`/news/v1/news/sources`；Intel `intel/v1/events`（**协议事件日历**） | 付费为主 | 结构化事件 | — |
| CoinGecko News | `https://api.coingecko.com/api/v3/news`（Pro），前端 `https://www.coingecko.com/en/news` | Pro | 聚合新闻 | — |
| CoinMarketCap Content | `v1/content/latest?id=&news_type=news|alexandria|all&content_type=all|news|video|audio&category=&language=`、`v1/content/posts/top`、`v1/content/posts/latest`、`v1/community/trending/topic`、`v1/community/trending/token` | 付费层 | CMC Community 帖子 | — |
| NewsAPI.org、GNews、Bing News Search、Google News RSS（`https://news.google.com/rss/search?q=bitcoin&hl=en-US&gl=US&ceid=US:en`）、Mediastack、NewsData.io、Webz.io、Event Registry、Aylien | 各自 | 免费层有限 | 通用新闻含加密关键词 | 用于主流媒体覆盖度 |
| 主流加密媒体 RSS/API | CoinDesk `https://www.coindesk.com/arc/outboundfeeds/rss/`；Cointelegraph `https://cointelegraph.com/rss`（分类 `/rss/tag/bitcoin`）；Decrypt `https://decrypt.co/feed`；The Block `https://www.theblock.co/rss.xml`（Pro 有 Data API）；Blockworks `https://blockworks.co/feed`；The Defiant `https://thedefiant.io/api/feed`；Bitcoin Magazine `https://bitcoinmagazine.com/.rss/full/`；DL News `https://www.dlnews.com/arc/outboundfeeds/rss/`；Protos；Unchained；CryptoSlate `https://cryptoslate.com/feed/`；BeInCrypto `https://beincrypto.com/feed/`；NewsBTC；U.Today；CryptoPotato；AMBCrypto；Bankless；Milk Road；The Daily Gwei；Week in Ethereum News（停）；Rekt News `https://rekt.news/rss/feed.xml`（**黑客事件**） | 免费 RSS | 全文需抓取 | — |
| 中文媒体 | Odaily 星球日报（`https://www.odaily.news/`，API `https://www.odaily.news/v1/openapi/...` 非公开；RSS 第三方）、PANews（`https://www.panewslab.com/`，`https://www.panewslab.com/webapi/flashnews?LId=1&Rn=20&tw=0`）、律动 BlockBeats（`https://www.theblockbeats.info/`，`https://api.theblockbeats.news/v1/open-api/open-flash?size=20&page=1&type=push&lang=cn`（开放快讯 API，需申请 key）、`/v1/open-api/open-information`）、金色财经（`https://www.jinse.cn/`，`https://api.jinse.cn/noah/v2/lives?limit=20&reading=false&source=web&flag=down&id=0&category=0`）、Foresight News（`https://foresightnews.pro/`，`https://api.foresightnews.pro/v1/news?size=20`）、深潮 TechFlow（`https://www.techflowpost.com/`，`https://www.techflowpost.com/ashx/newflash_index.ashx?page=1`）、吴说 Wu Blockchain（X + `https://wublock.substack.com/`）、ChainCatcher（`https://www.chaincatcher.com/`，`https://www.chaincatcher.com/api/...`）、MarsBit、币世界（已关）、链闻（已关）、Followin（`https://followin.io/`，聚合） | 多为非公开前端接口，可能变动 | 快讯（flash news）为主 | 对中文用户最重要；接口不稳定要做容错 |
| 实时快讯/交易员新闻 | Tree of Alpha（`https://news.treeofalpha.com/api/news?limit=`、WS `wss://news.treeofalpha.com/ws`，**交易员级低延迟新闻+Binance 公告聚合，免费**）、Phoenix News（`https://phoenixnews.io/`，付费 WS）、BWE News（`https://bwenews.io/`，付费）、Velo News（见 07，付费）、Unfolded、Watcher.Guru（X）、DB News（Discord）、Tiger Research、Crypto Headlines、Cryptopanic hot、Binance 公告（`https://www.binance.com/bapi/composite/v1/public/cms/article/list/query?type=1&pageNo=1&pageSize=20&catalogId=48`（新币上市 48 / 下架 161 / 最新 49），**上币公告是最常被监控的数据**；Binance Square API）、Coinbase 上币（`https://api.exchange.coinbase.com/currencies`、Coinbase Assets 博客 RSS、X @CoinbaseAssets）、Upbit 公告（`https://api-manager.upbit.com/api/v1/announcements?os=web&page=1&per_page=20&category=trade`，**Upbit 上币常引发暴涨**）、Bithumb 公告（`https://feed.bithumb.com/notice`）、OKX 公告（`https://www.okx.com/api/v5/support/announcements?annType=announcements-new-listings`，**官方公开 API**）、Bybit 公告（`https://api.bybit.com/v5/announcements/index?locale=en-US&type=new_crypto&limit=20`，**官方**）、Bitget（`https://api.bitget.com/api/v2/public/annoucements?annType=coin_listings`）、Gate（`https://www.gate.io/apiw/v2/announcement/list`）、KuCoin（`https://api.kucoin.com/api/v3/announcements?annType=new-listings`，**官方**）、HTX（`https://www.htx.com/-/x/support/public/getList/...`）、MEXC（`https://www.mexc.com/help/announce/api/...`）、Hyperliquid 新上线（`meta` 轮询对比） | 多数免费 | 上币/下架公告、黑客、监管 | 上币监控：OKX/Bybit/KuCoin/Bitget 有官方公告 API，Binance/Upbit 走前端接口 |
| 事件日历 | CoinMarketCal（`https://developers.coinmarketcal.com/v1/events?max=75&dateRangeStart=&dateRangeEnd=&coins=&categories=&sortBy=created_desc`、`/v1/coins`、`/v1/categories`；免费 key）、Coindar（`https://coindar.org/en/api`，`https://coindar.org/api/v2/events?access_token=&page=&page_size=&filter_date_start=&filter_coins=`）、Messari Intel、Coinglass 经济日历、OKX economic-calendar、Investing.com（抓取）、ForexFactory（`https://nfs.faireconomy.media/ff_calendar_thisweek.json`，**免费宏观日历 JSON**）、TradingEconomics API（付费）、FOMC 日程（Fed 官网）、CPI 发布（BLS 日程）、Token 解锁（见 06）、ETF 审批截止（SEC EDGAR + Bloomberg ETF 分析师 X）、Mt.Gox 分发、FTX 分发、以太坊升级日程（`https://ethereum.org/en/roadmap/`、`https://github.com/ethereum/pm`）、比特币减半倒计时（区块高度计算）、Hyperliquid 解锁/HIP 投票 | 多免费 | 日历 | — |

---

## 2. 情绪指数
| 指数 | 访问 | 说明 |
|---|---|---|
| Alternative.me Fear & Greed | `https://api.alternative.me/fng/?limit=0&format=json&date_format=us`（**全历史自 2018.2，免费无 key**）；返回 `value`、`value_classification`、`timestamp`、`time_until_update` | 成分：波动率 25%、成交量 25%、社媒 15%、问卷 15%（停）、BTC 占比 10%、Google Trends 10%；每日 UTC 00:00 更新 |
| CoinMarketCap F&G | `v3/fear-and-greed/latest`、`v3/fear-and-greed/historical?start=1&limit=500`（免费层可用） | CMC 自有算法（价格动量、波动、衍生品、市场构成、社媒等），2024 上线 |
| Coinglass F&G | `index/fear-greed-history` | Coinglass 版 |
| Glassnode `indicators/fear_greed` | 付费 | 链上成分版 |
| CFGI（Crypto Fear & Greed Index by cfgi.io） | `https://cfgi.io/api/...`（需 key，按币种 F&G） | 单币情绪 |
| Santiment 情绪 | `sentimentPositiveTotal`、`sentimentNegativeTotal`、`sentimentBalanceTotal`、`sentimentVolumeConsumedTotal`、`weightedSentimentTotal`（**加权情绪**）、`socialDominance`、`socialVolume` | 来自 Twitter/Reddit/Telegram/Bitcointalk/4chan/YouTube/Farcaster |
| LunarCrush | 见下 | Galaxy Score、AltRank、Sentiment、Social Dominance |
| TheTIE（→ CoinDesk Data/Terminal）、Augmento（退）、Predicoin（退）、BittsAnalytics、StockGeist、Sentifi、Stocktwits Sentiment、Reddit 情绪自算 | 多付费/退役 | — |
| 市场情绪替代指标：Coinbase App Store 排名（`https://apps.apple.com/us/app/coinbase/id886427730` 页面 + 第三方 AppFigures/Sensor Tower；Coinglass 有 "Coinbase App Rank"）、Google Trends "bitcoin"、Polymarket 价格（见 10）、Bitfinex 多空、Coinglass 多空比、期权 PCR/Skew（见 07）、资金费率、Kimchi/Coinbase 溢价（CryptoQuant）、稳定币溢价（USDT/CNY 场外价：OKX C2C `https://www.okx.com/v3/c2c/tradingOrders/books?quoteCurrency=cny&baseCurrency=usdt&side=sell`、Binance P2P `https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search`（POST，**USDT 人民币场外价**）、Paxful/Noones、LocalBitcoins（退）、Bitpapa、HodlHodl `https://hodlhodl.com/api/v1/offers`、Bisq、Tether 场外溢价社区数据）| 混杂 | 场外溢价是法币进出需求指标 |

---

## 3. 社媒数据
| 平台/服务 | 访问 | 能力 | 备注 |
|---|---|---|---|
| X / Twitter API v2 | https://developer.x.com/en/docs/x-api ；`https://api.x.com/2/tweets/search/recent?query=bitcoin -is:retweet lang:en&max_results=100&tweet.fields=public_metrics,created_at,author_id`、`/2/tweets/search/all`（Pro+，全历史）、`/2/tweets/counts/recent`、`/2/users/by/username/{name}`（粉丝数）、`/2/users/{id}/tweets`、`/2/tweets/{id}`、Filtered Stream `/2/tweets/search/stream`（规则匹配实时）、Lists | Free（仅发帖）/Basic $200/月（15k 读）/Pro $5000/月/Enterprise；第三方：twitterapi.io（`https://api.twitterapi.io/twitter/tweet/advanced_search`，低价）、Apify、SocialData、RapidAPI | 官方贵；监控 KOL 多用第三方或 Nitter（已死）替代 |
| LunarCrush | https://lunarcrush.com/developers/api/endpoints ；`https://lunarcrush.com/api4/public/coins/list/v2?sort=galaxy_score&limit=100`（**Galaxy Score、AltRank、social_volume_24h、social_dominance、sentiment、interactions_24h、market_cap、volatility、percent_change**）、`/public/coins/{coin}/v1`、`/public/coins/{coin}/time-series/v2?bucket=hour|day&interval=1w|1m|3m|6m|1y|all&start=&end=`（**社交时序：posts_created、posts_active、interactions、contributors_active、sentiment、spam、social_dominance、galaxy_score、alt_rank**）、`/public/coins/{coin}/meta/v1`、`/public/topic/{topic}/v1`、`/public/topic/{topic}/time-series/v2`、`/public/topic/{topic}/posts/v1`（**帖子列表含互动**）、`/public/topic/{topic}/news/v1`、`/public/topic/{topic}/creators/v1`（**KOL 排名**）、`/public/topic/{topic}/whatsup/v1`（AI 摘要）、`/public/topics/list/v1`、`/public/category/{cat}/...`、`/public/creator/{network}/{id}/v1`、`/public/creator/{network}/{id}/time-series/v1`、`/public/creator/{network}/{id}/posts/v1`、`/public/creators/list/v1`、`/public/posts/{network}/{id}/v1`、`/public/posts/{network}/{id}/time-series/v1`、`/public/stocks/...`、`/public/nfts/...`、`/public/system/changes`、`/public/searches/...`（自定义搜索） | `Authorization: Bearer`；Individual $30+/月，Builder/Enterprise | 覆盖 X、Reddit、YouTube、TikTok、News；加密社交数据性价比最高 |
| Santiment social | `socialVolume_total`、`socialVolume_twitter`、`socialVolume_reddit`、`socialVolume_telegram`、`socialVolume_bitcointalk`、`socialVolume_4chan`、`socialVolume_youtube_videos`、`socialVolume_farcaster`、`socialDominance_total`、`uniqueSocialVolume_total`、`socialActiveUsers`、`trendingWords`、`wordTrendScore`、`topSocialGainersLosers`、`socialVolumeProjects`、`getTrendingStories`（2025）、`communityMessagesCount_telegram`、`twitterFollowers`、`sentiment*` | 见 05 | 热词（Emerging Trends）是经典反指 |
| Kaito | `https://api.kaito.ai/api/v1/yaps?username=`（**Yaps 公开**）；Kaito Pro/API（机构，Mindshare、Smart Followers、Narrative 热度、`https://api.kaito.ai/...` 付费）；Kaito Connect/Yapper Leaderboards（各项目 `https://yaps.kaito.ai/{project}`）| 公开仅 Yaps | Mindshare 已成行业指标 | — |
| Cookie DAO / Cookie.fun | `https://api.cookie.fun/v2/agents/agentsPaged?interval=_7Days&page=1&pageSize=25`、`/v2/agents/twitterUsername/{name}`、`/v2/agents/contractAddress/{addr}`、`/v1/hackathon/search/{word}`（旧）；DataSwarm（2025 新 API，`https://api.cookie.fun/v3/...`，需 key） | 免费层 | AI Agent 代币 Mindshare、Smart Engagement | — |
| Reddit | `https://www.reddit.com/r/cryptocurrency/new.json?limit=100`、`/r/{sub}/about.json`（订阅数、在线数）、`/r/{sub}/hot.json`、搜索 `/search.json?q=&sort=new`；官方 OAuth API（2023 起收费，免费 100 req/min 需 OAuth）；Pushshift（受限）；Arctic Shift（`https://arctic-shift.photon-reddit.com/api/...`，历史）；subredditstats | 免费有限 | 订阅增长、帖子量、情绪 | r/Bitcoin、r/CryptoCurrency、r/ethtrader、r/solana、r/wallstreetbets（MSTR/COIN） |
| Telegram | Telethon/Pyrogram（MTProto，用账号读群/频道）、Bot API（只能收自己群消息）、TGStat（`https://api.tgstat.ru/`，频道统计，付费）、Telemetr.io、Combot | 需账号 | 频道订阅数、消息量、关键词 | 中文社区主阵地 |
| Discord | Bot API（Gateway 读消息，需加入服务器）、DiscordAPI 成员数 `https://discord.com/api/v10/invites/{code}?with_counts=true`（**公开：approximate_member_count / presence_count**）、Statbot、Disboard | 公开成员数无需 token | 社区规模 | — |
| Farcaster | Neynar（`https://api.neynar.com/v2/farcaster/feed?feed_type=filter&filter_type=channel_id&channel_id=base`、`/cast/search?q=`、`/user/by_username?username=`、`/user/bulk?fids=`、`/feed/trending`、`/channel/trending`、`/notifications`、`/reactions/cast`、Webhooks；免费 Starter）、Warpcast API（`https://api.warpcast.com/v2/...` 部分公开：`user-by-username`、`cast`、`all-channels`、`channel-followers`）、Hub gRPC/HTTP（`https://hub.pinata.cloud/v1/castsByFid?fid=`、`nemes.farcaster.xyz:2281`）、Airstack（退）、Dune `farcaster.*`（Neynar 开放数据集）、Farcaster 数据 `https://farcaster.network/`、Pinata Farcaster API | 免费层可用 | Base/Farcaster 生态社交 | — |
| Lens Protocol | GraphQL `https://api-v2.lens.dev/`（v3 `https://api.lens.xyz/graphql`：`posts`、`accounts`、`feed`、`search`、`timeline`、`stats`） | 免费 | — | — |
| YouTube Data API | `https://www.googleapis.com/youtube/v3/search?q=bitcoin&type=video&order=date&publishedAfter=`、`/videos?part=statistics&id=`、`/channels?part=statistics&id=`（订阅/观看）、`/commentThreads` | 免费 10k units/天 | KOL 频道增长、视频热度 | — |
| TikTok（Research API 申请制；第三方 Apify）、Bluesky（AT Protocol `https://public.api.bsky.app/xrpc/app.bsky.feed.searchPosts?q=bitcoin&sort=latest`、`app.bsky.actor.getProfile`，**免费公开**）、Nostr（relay WS `wss://relay.damus.io`，NIP-01 REQ 过滤 kind 1；nostr.band API `https://api.nostr.band/v0/search?q=`）、Threads API（Meta，`https://graph.threads.net/`，需审核）、Stocktwits（`https://api.stocktwits.com/api/2/streams/symbol/BTC.X.json`，**免费无 key**，含 sentiment bullish/bearish）、Weibo（`https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D比特币`，抓取）、Bilibili、小红书、抖音（抓取/第三方）、知乎、Twitch、Mastodon（`/api/v1/timelines/tag/bitcoin`） | 混杂 | — | — |
| 社媒聚合/监控商：LunarCrush、Santiment、Kaito、Cookie、Brand24、Brandwatch、Meltwater、Talkwalker、Sprout、Hootsuite（通用）、Pulsar、Phantombuster、Apify（爬虫市场：Twitter/Telegram/Discord/TikTok scrapers）、Bright Data、SocialBlade（`https://socialblade.com/`，粉丝历史，付费 API）、Followerwonk、HypeAuditor、Nansen Social（退）、Messari Signal、The TIE、Sentiment.io、Augur（退） | 各自 | — | — |

---

## 4. 搜索与关注度
| 来源 | 访问 | 说明 |
|---|---|---|
| Google Trends | 非官方 `pytrends`（`TrendReq().build_payload(['bitcoin'], timeframe='today 5-y', geo='')`，`interest_over_time()`、`interest_by_region()`、`related_queries()`、`trending_searches()`）；官方 Trends API（2025 Alpha 申请制）；Glimpse（付费绝对量）；SerpApi Google Trends（`https://serpapi.com/search?engine=google_trends&q=bitcoin`，付费） | 相对指数 0–100；pytrends 常被限流（429），需代理/间隔 |
| Wikipedia Pageviews | `https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Bitcoin/daily/20240101/20241231`（**免费、无 key、绝对值**） | 散户关注度经典代理 |
| App Store / Google Play 排名 | Apple RSS `https://rss.marketingtools.apple.com/api/v2/us/apps/top-free/100/apps.json`（**免费榜 Top100 JSON**，查 Coinbase/Robinhood/Binance/Crypto.com/Phantom/MetaMask 排名）、AppFigures/Sensor Tower/data.ai（付费历史）、Coinglass "App Rankings" 页、`https://www.appfigures.com/top-apps/ios-app-store/united-states/iphone/top-overall`（页面） | Coinbase 冲进 Top10 = 散户 FOMO 信号 |
| CoinGecko `search/trending`（**热搜币/NFT/分类，15 分钟更新**）、CMC `trending/latest`/`most-visited`/`gainers-losers`、Dexscreener `token-boosts/top`、`token-profiles/latest`（**付费推广的 meme**）、GeckoTerminal `trending_pools`、Birdeye `trending`、Jupiter `tokens/v2/toptrending`、Moralis `discovery/tokens/trending`、Solana Tracker `tokens/trending`、Pump.fun king-of-the-hill、GMGN 热榜（无 API）、Photon 热榜（无）、Binance Square 热搜、OKX 热搜、Coinbase 热搜（`https://www.coinbase.com/api/v2/assets/search?...` 非公开） | 免费 | 市场内部关注度 |
| GitHub stars/forks 增长、npm 下载（`https://api.npmjs.org/downloads/point/last-week/ethers`，**开发者采用代理**）、PyPI 下载（`https://pypistats.org/api/packages/web3/recent`）、Docker pulls | 免费 | 开发者关注 |
| 域名/网站流量：SimilarWeb（付费 API；CMC `exchange/info` 的 `weekly_visits` 来自此）、Semrush、Ahrefs、Cloudflare Radar（`https://api.cloudflare.com/client/v4/radar/ranking/top?limit=100`，**免费域名排名**）、Tranco（`https://tranco-list.eu/`，免费 Top1M 列表） | 混杂 | 交易所网站流量 |

---

## 5. 开发者活动
| 来源 | 访问 | 说明 |
|---|---|---|
| Electric Capital Developer Report | `https://github.com/electric-capital/crypto-ecosystems`（**开源生态→仓库映射，TOML**，可自建统计）；`https://www.developerreport.com/`（年报 + 交互图，无公开 API） | 行业标准开发者数 |
| Santiment `devActivity`、`devActivityContributorsCount`、`githubActivity`、`githubActivityContributorsCount`、`devActivity1d` | GraphQL（免费层 1 年前） | 排除非开发事件（fork/star/watch），比原始 GitHub 事件干净 |
| CCData `asset/v1/historical/code-repository/days?asset=ETH&limit=`（stars、forks、subscribers、open_issues、commits、contributors、language） | 免费层可用 | — |
| Artemis Developer Activity（`https://app.artemisanalytics.com/developer-activity`，API 付费 `https://api.artemisxyz.com/data/dev_core_count?symbols=`、`weekly_commits_core`、`weekly_commits_sub_ecosystem`、`dev_sub_ecosystem_count`） | 付费（有免费 key 试用） | 基于 Electric Capital 映射 |
| Token Terminal `code_commits`、`active_developers`（见 06） | 付费 | — |
| GitHub REST/GraphQL（`https://api.github.com/repos/{owner}/{repo}`、`/stats/commit_activity`、`/stats/contributors`、`/commits?since=`、`/events`、Search `https://api.github.com/search/repositories?q=topic:solana&sort=stars`；GH Archive `https://www.gharchive.org/`（**全量事件 BigQuery `githubarchive.day.*`**）） | 免费 5000 req/h（token） | 原始源 |
| CryptoMiso（`https://www.cryptomiso.com/`，页面）、Coincodecap（退）、CoinGecko `developer_data`（`coins/{id}` 返回 forks/stars/subscribers/total_issues/closed_issues/pull_requests_merged/pull_request_contributors/commit_count_4_weeks/last_4_weeks_commit_activity_series）、CMC（无）、Messari `developer` 指标、DefiLlama（无） | 免费 | — |

---

## 6. KOL / 影响力
| 来源 | 说明 |
|---|---|
| Kaito Yaps（`https://api.kaito.ai/api/v1/yaps?username=`：yaps_all、yaps_l24h、yaps_l7d、yaps_l30d…）、Kaito Leaderboards（各项目 Yapper 榜）、Kaito Mindshare（付费） | 行业影响力分 |
| LunarCrush creators（`/public/topic/{t}/creators/v1`、`/public/creators/list/v1`：followers、interactions_24h、creator_rank）| 跨平台 |
| Cookie.fun（Agent/项目 Mindshare、Smart Followers）、Wallchain、Ethos Network（声誉 `https://api.ethos.network/api/v1/...`）、Arkham Public Figure 标签、Nansen Public Figure 钱包、Kolscan（KOL 钱包 PnL `https://kolscan.io/`）、Dexscreener/Bubblemaps KOL 持仓、X 加密 KOL 列表（社区维护）、Twitter Audit、SparkToro、HypeAuditor、Followerwonk | 影响力与钱包关联 |
| Polymarket/Kalshi 上的 KOL 预测市场、Friend.tech（退）、Zora/Base 创作者币、pump.fun 名人币 | 社交金融化 |

---

## 7. 口径与注意事项
- **情绪指数不可比**：Alternative.me、CMC、Coinglass、Glassnode、Santiment 成分不同，只在各自序列内看相对位置。
- **社交量 ≠ 情绪**：高社交量伴随负面情绪常见于崩盘；Santiment `weightedSentiment` = 情绪 × 量，比纯情绪更有用。
- **X API 成本**：Basic 层每月 1.5 万条读取远不够监控，多数团队用第三方（twitterapi.io/Apify）或只跟踪固定账号。
- **中文快讯接口不稳定**：Odaily/PANews/金色/律动的前端接口随时改，做采集要多源冗余 + 异常告警；BlockBeats 有正式开放 API 可申请。
- **上币公告**：OKX/Bybit/KuCoin/Bitget 官方公开 API 最稳；Binance 用 CMS 接口（偶有风控）；Upbit 走 api-manager（韩文，需翻译关键字 "거래지원"、"신규"）；监控延迟目标 < 2 秒时用 Tree of Alpha WS。
- **Google Trends** 是相对值，不同关键词组合会改变刻度；跨期对比要固定 timeframe。
- **Reddit 订阅数/Discord 成员数** 可被刷；结合在线数（`presence_count`、`active_user_count`）看。

## 8. 变更记录
- 2026-10 初版。
