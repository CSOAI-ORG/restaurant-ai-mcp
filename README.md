# Restaurant AI MCP Server

**Hospitality Intelligence**

Built by [MEOK AI Labs](https://meok.ai)

---

An MCP server for restaurant owners and hospitality professionals. Optimize menus for profitability, calculate food costs, manage reservations, analyze customer reviews, and check allergens in dishes.

## Tools

| Tool | Description |
|------|-------------|
| `optimize_menu` | Analyze menu items for profitability - classify as stars, dogs, or plowhorses |
| `calculate_food_cost` | Calculate dish food cost from ingredients with pricing suggestions |
| `manage_reservation` | Create, list, cancel reservations and check availability |
| `analyze_reviews` | Analyze customer reviews for sentiment and actionable themes |
| `check_allergens` | Check ingredients against 8 major allergen categories |

## Quick Start

```bash
pip install restaurant-ai-mcp
```

### Claude Desktop

```json
{
  "mcpServers": {
    "restaurant-ai": {
      "command": "python",
      "args": ["-m", "server"],
      "cwd": "/path/to/restaurant-ai-mcp"
    }
  }
}
```

### Direct Usage

```bash
python server.py
```

## Rate Limits

| Tier | Requests/Hour |
|------|--------------|
| Free | 60 |
| Pro | 5,000 |

## License

MIT - see [LICENSE](LICENSE)

---

*Part of the MEOK AI Labs MCP Marketplace*
