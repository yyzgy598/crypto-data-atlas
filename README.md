# crypto-data-atlas

币圈数据地图（Crypto Data Map）—— 一个 Claude Code skill：把"数据需求 → 数据源 → 具体接口"整理成目录，覆盖中心化交易所、DEX、行情聚合商、链上浏览器与分析、DeFi、衍生品、新闻社媒、宏观/ETF、历史全量数据等。

## 结构

```
skills/crypto-data-map/
├── SKILL.md            # 入口：快速索引、回答格式、判断原则
├── references/         # 01-cex … 11-bulk-data 分类目录
└── scripts/probe.py    # 探测公开 REST 接口是否可用、返回哪些字段
```

## 安装

```bash
git clone https://github.com/yyzgy598/crypto-data-atlas.git
cp -R crypto-data-atlas/skills/crypto-data-map ~/.claude/skills/
```

之后在 Claude Code 里用 `/crypto-data-map <问题>` 调用，或者直接问"某某数据从哪拿"，会自动触发。

## 探测脚本

```bash
python3 skills/crypto-data-map/scripts/probe.py "https://fapi.binance.com/fapi/v1/fundingRate?symbol=BTCUSDT&limit=2"
python3 skills/crypto-data-map/scripts/probe.py "https://api.hyperliquid.xyz/info" --post '{"type":"meta"}'
```

内容截至 2026 年；接口会变，用前请以各家官方文档为准。
