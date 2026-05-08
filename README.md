[![restaurant-ai-mcp MCP server](https://glama.ai/mcp/servers/CSOAI-ORG/restaurant-ai-mcp/badges/score.svg)](https://glama.ai/mcp/servers/CSOAI-ORG/restaurant-ai-mcp)
[![MCP Registry](https://img.shields.io/badge/MCP_Registry-Published-green)](https://registry.modelcontextprotocol.io)
[![PyPI](https://img.shields.io/pypi/v/restaurant-ai-mcp)](https://pypi.org/project/restaurant-ai-mcp/)

[![restaurant-ai-mcp MCP server](https://glama.ai/mcp/servers/CSOAI-ORG/restaurant-ai-mcp/badges/card.svg)](https://glama.ai/mcp/servers/CSOAI-ORG/restaurant-ai-mcp)

<div align="center">

# Restaurant Ai MCP

**Restaurant AI MCP Server - Hospitality Intelligence**

[![PyPI](https://img.shields.io/pypi/v/meok-restaurant-ai-mcp)](https://pypi.org/project/meok-restaurant-ai-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MEOK AI Labs](https://img.shields.io/badge/MEOK_AI_Labs-MCP_Server-purple)](https://meok.ai)

</div>

## Overview

Restaurant AI MCP Server - Hospitality Intelligence
Built by MEOK AI Labs | https://meok.ai

Menu optimization, food cost calculation, reservation management,
review analysis, and allergen checking.

## Tools

| Tool | Description |
|------|-------------|
| `optimize_menu` | Analyze and optimize a menu for profitability. |
| `calculate_food_cost` | Calculate food cost for a dish from ingredients. |
| `manage_reservation` | Manage restaurant reservations - create, view, cancel. |
| `analyze_reviews` | Analyze customer reviews for sentiment, themes, and actionable insights. |
| `check_allergens` | Check dish ingredients against common allergen categories. |

## Installation

```bash
pip install meok-restaurant-ai-mcp
```

## Usage with Claude Desktop

Add to your Claude Desktop MCP config:

```json
{
  "mcpServers": {
    "restaurant-ai": {
      "command": "python",
      "args": ["-m", "meok_restaurant_ai_mcp.server"]
    }
  }
}
```

## License

MIT © [MEOK AI Labs](https://meok.ai)
<!-- mcp-name: io.github.CSOAI-ORG/restaurant-ai-mcp -->
