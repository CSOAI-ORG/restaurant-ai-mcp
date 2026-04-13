"""
Restaurant AI MCP Server - Hospitality Intelligence
Built by MEOK AI Labs | https://meok.ai

Menu optimization, food cost calculation, reservation management,
review analysis, and allergen checking.
"""

import time
from datetime import datetime, timezone
from typing import Optional

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "restaurant-ai",
    version="1.0.0",
    description="Restaurant AI - menu optimization, food costs, reservations, reviews, allergens",
)

# ---------------------------------------------------------------------------
# Rate limiting
# ---------------------------------------------------------------------------
_RATE_LIMITS = {"free": {"requests_per_hour": 60}, "pro": {"requests_per_hour": 5000}}
_request_log: list[float] = []
_tier = "free"


def _check_rate_limit() -> bool:
    now = time.time()
    _request_log[:] = [t for t in _request_log if now - t < 3600]
    if len(_request_log) >= _RATE_LIMITS[_tier]["requests_per_hour"]:
        return False
    _request_log.append(now)
    return True


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
_ALLERGENS = {
    "gluten": ["wheat", "barley", "rye", "spelt", "kamut", "flour", "breadcrumbs", "pasta", "couscous", "soy_sauce"],
    "dairy": ["milk", "cream", "cheese", "butter", "yoghurt", "whey", "casein", "ghee", "lactose"],
    "nuts": ["almond", "walnut", "cashew", "pecan", "pistachio", "macadamia", "hazelnut", "pine_nut", "peanut"],
    "shellfish": ["shrimp", "prawn", "crab", "lobster", "crayfish", "mussel", "clam", "oyster", "scallop"],
    "eggs": ["egg", "eggs", "mayonnaise", "meringue", "aioli", "hollandaise"],
    "soy": ["soy", "soya", "tofu", "tempeh", "edamame", "miso", "soy_sauce"],
    "fish": ["salmon", "tuna", "cod", "haddock", "anchovy", "sardine", "fish_sauce", "worcestershire"],
    "sesame": ["sesame", "tahini", "hummus"],
}

_FOOD_COSTS: dict[str, float] = {
    "chicken_breast": 4.50, "beef_sirloin": 12.00, "salmon_fillet": 9.50,
    "pasta_dry": 0.80, "rice": 0.60, "potatoes": 1.20, "mixed_greens": 2.50,
    "tomatoes": 1.80, "onions": 0.70, "garlic": 0.40, "olive_oil": 0.50,
    "butter": 0.80, "cream": 1.50, "cheese_parmesan": 3.00, "eggs_dozen": 3.60,
    "bread_loaf": 1.50, "flour_kg": 0.90, "sugar_kg": 1.00, "herbs_fresh": 1.00,
    "lemon": 0.50, "wine_cooking": 2.00, "stock_litre": 1.20, "mushrooms": 3.00,
}

_RESERVATIONS: list[dict] = []


@mcp.tool()
def optimize_menu(
    items: list[dict],
    target_food_cost_pct: float = 30.0,
) -> dict:
    """Analyze and optimize a menu for profitability.

    Args:
        items: List of menu items, each with keys: name, price, food_cost, category.
              Example: [{"name": "Caesar Salad", "price": 14.0, "food_cost": 3.50, "category": "starter"}]
        target_food_cost_pct: Target food cost percentage (industry standard 28-32%).
    """
    if not _check_rate_limit():
        return {"error": "Rate limit exceeded. Upgrade to pro tier."}

    if not items:
        return {"error": "Provide at least one menu item."}

    analyzed = []
    total_cost = 0
    total_revenue = 0
    stars = []
    dogs = []

    for item in items:
        name = item.get("name", "Unknown")
        price = item.get("price", 0)
        cost = item.get("food_cost", 0)
        category = item.get("category", "main")

        if price <= 0:
            continue

        cost_pct = round((cost / price) * 100, 1)
        margin = round(price - cost, 2)
        total_cost += cost
        total_revenue += price

        classification = "standard"
        if cost_pct <= target_food_cost_pct - 5 and margin > 8:
            classification = "star"
            stars.append(name)
        elif cost_pct > target_food_cost_pct + 10:
            classification = "dog"
            dogs.append(name)
        elif margin > 12:
            classification = "plowhouse"

        recommendation = "maintain"
        if classification == "dog":
            suggested_price = round(cost / (target_food_cost_pct / 100), 2)
            recommendation = f"increase price to ${suggested_price:.2f} or reduce portion"
        elif classification == "star":
            recommendation = "promote prominently on menu"

        analyzed.append({
            "name": name, "category": category, "price": price,
            "food_cost": cost, "cost_pct": cost_pct, "margin": margin,
            "classification": classification, "recommendation": recommendation,
        })

    overall_pct = round((total_cost / total_revenue) * 100, 1) if total_revenue else 0

    return {
        "menu_analysis": analyzed,
        "summary": {
            "total_items": len(analyzed),
            "avg_food_cost_pct": overall_pct,
            "target_pct": target_food_cost_pct,
            "on_target": abs(overall_pct - target_food_cost_pct) <= 3,
            "stars": stars,
            "dogs": dogs,
        },
        "recommendations": [
            f"Overall food cost is {overall_pct}% vs target {target_food_cost_pct}%",
            f"{len(stars)} star items to promote" if stars else "No standout stars - consider high-margin specials",
            f"{len(dogs)} items need repricing" if dogs else "All items within cost targets",
        ],
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


@mcp.tool()
def calculate_food_cost(
    ingredients: list[dict],
    portions: int = 1,
    target_price: Optional[float] = None,
) -> dict:
    """Calculate food cost for a dish from ingredients.

    Args:
        ingredients: List with keys: name, quantity_kg (or use known items from DB).
                    Example: [{"name": "chicken_breast", "quantity_kg": 0.25}]
        portions: Number of portions this recipe makes.
        target_price: Target menu price to calculate cost percentage.
    """
    if not _check_rate_limit():
        return {"error": "Rate limit exceeded. Upgrade to pro tier."}

    total_cost = 0.0
    breakdown = []

    for ing in ingredients:
        name = ing.get("name", "unknown")
        qty = ing.get("quantity_kg", 0.5)
        unit_cost = _FOOD_COSTS.get(name, ing.get("cost_per_kg", 5.0))
        cost = round(unit_cost * qty, 2)
        total_cost += cost
        breakdown.append({"ingredient": name, "quantity_kg": qty, "cost": cost})

    cost_per_portion = round(total_cost / max(1, portions), 2)

    result: dict = {
        "total_recipe_cost": round(total_cost, 2),
        "portions": portions,
        "cost_per_portion": cost_per_portion,
        "ingredient_breakdown": breakdown,
    }

    if target_price:
        cost_pct = round((cost_per_portion / target_price) * 100, 1)
        result["pricing"] = {
            "target_price": target_price,
            "food_cost_pct": cost_pct,
            "healthy": cost_pct <= 32,
            "suggested_prices": {
                "25_pct": round(cost_per_portion / 0.25, 2),
                "30_pct": round(cost_per_portion / 0.30, 2),
                "35_pct": round(cost_per_portion / 0.35, 2),
            },
        }

    result["generated_at"] = datetime.now(timezone.utc).isoformat()
    return result


@mcp.tool()
def manage_reservation(
    action: str,
    guest_name: Optional[str] = None,
    party_size: int = 2,
    date: Optional[str] = None,
    time_slot: Optional[str] = None,
    reservation_id: Optional[str] = None,
    special_requests: Optional[str] = None,
) -> dict:
    """Manage restaurant reservations - create, view, cancel.

    Args:
        action: create | list | cancel | check_availability.
        guest_name: Guest name (required for create).
        party_size: Number of guests.
        date: Date in YYYY-MM-DD format.
        time_slot: Time in HH:MM format (e.g. 19:30).
        reservation_id: ID for cancel action.
        special_requests: Dietary needs, celebrations, etc.
    """
    if not _check_rate_limit():
        return {"error": "Rate limit exceeded. Upgrade to pro tier."}

    if action == "create":
        if not guest_name or not date or not time_slot:
            return {"error": "guest_name, date, and time_slot required for create."}

        res_id = f"RES-{len(_RESERVATIONS)+1:04d}"
        reservation = {
            "id": res_id, "guest_name": guest_name, "party_size": party_size,
            "date": date, "time": time_slot, "special_requests": special_requests or "",
            "status": "confirmed", "created_at": datetime.now(timezone.utc).isoformat(),
        }
        _RESERVATIONS.append(reservation)
        return {"status": "confirmed", "reservation": reservation}

    elif action == "list":
        filtered = _RESERVATIONS
        if date:
            filtered = [r for r in filtered if r["date"] == date and r["status"] != "cancelled"]
        return {
            "reservations": filtered, "count": len(filtered),
            "total_covers": sum(r["party_size"] for r in filtered),
        }

    elif action == "cancel":
        for r in _RESERVATIONS:
            if r["id"] == reservation_id:
                r["status"] = "cancelled"
                return {"status": "cancelled", "reservation": r}
        return {"error": f"Reservation {reservation_id} not found."}

    elif action == "check_availability":
        if not date or not time_slot:
            return {"error": "date and time_slot required."}
        booked = sum(
            r["party_size"] for r in _RESERVATIONS
            if r["date"] == date and r["time"] == time_slot and r["status"] != "cancelled"
        )
        capacity = 60
        available = max(0, capacity - booked)
        return {
            "date": date, "time": time_slot, "booked_covers": booked,
            "available_covers": available, "can_seat": available >= party_size,
        }

    return {"error": f"Unknown action: {action}. Use create|list|cancel|check_availability."}


@mcp.tool()
def analyze_reviews(
    reviews: list[str],
) -> dict:
    """Analyze customer reviews for sentiment, themes, and actionable insights.

    Args:
        reviews: List of review text strings to analyze.
    """
    if not _check_rate_limit():
        return {"error": "Rate limit exceeded. Upgrade to pro tier."}

    if not reviews:
        return {"error": "Provide at least one review."}

    positive_words = {"great", "excellent", "amazing", "delicious", "wonderful", "fantastic", "loved",
                      "perfect", "best", "fresh", "friendly", "recommend", "outstanding", "superb"}
    negative_words = {"terrible", "awful", "horrible", "disgusting", "rude", "slow", "cold", "stale",
                      "overpriced", "dirty", "worst", "disappointing", "bland", "raw", "undercooked"}
    theme_keywords = {
        "food_quality": {"food", "dish", "taste", "flavor", "fresh", "delicious", "bland", "raw", "cooked"},
        "service": {"service", "waiter", "staff", "friendly", "rude", "slow", "attentive", "helpful"},
        "ambiance": {"atmosphere", "ambiance", "decor", "music", "noise", "cozy", "romantic", "loud"},
        "value": {"price", "value", "expensive", "cheap", "worth", "overpriced", "portion", "portions"},
        "cleanliness": {"clean", "dirty", "hygiene", "bathroom", "restroom", "tidy"},
    }

    results = []
    theme_counts = {t: 0 for t in theme_keywords}
    sentiments = []

    for review in reviews:
        words = set(review.lower().split())
        pos = len(words & positive_words)
        neg = len(words & negative_words)

        if pos > neg:
            sentiment = "positive"
            score = min(1.0, 0.5 + pos * 0.15)
        elif neg > pos:
            sentiment = "negative"
            score = max(-1.0, -0.5 - neg * 0.15)
        else:
            sentiment = "neutral"
            score = 0.0

        themes = []
        for theme, kws in theme_keywords.items():
            if words & kws:
                themes.append(theme)
                theme_counts[theme] += 1

        sentiments.append(score)
        results.append({"text_preview": review[:100], "sentiment": sentiment, "score": round(score, 2), "themes": themes})

    avg_sentiment = round(sum(sentiments) / len(sentiments), 2)
    top_themes = sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)[:3]

    return {
        "reviews_analyzed": len(reviews),
        "overall_sentiment": avg_sentiment,
        "sentiment_label": "positive" if avg_sentiment > 0.2 else "negative" if avg_sentiment < -0.2 else "mixed",
        "theme_breakdown": dict(top_themes),
        "individual_results": results,
        "action_items": [
            f"Focus on {top_themes[0][0].replace('_', ' ')}" if top_themes else "Gather more reviews",
            "Address negative service mentions" if theme_counts.get("service", 0) > 0 and avg_sentiment < 0 else "Service feedback is positive",
        ],
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


@mcp.tool()
def check_allergens(
    ingredients: list[str],
    customer_allergens: Optional[list[str]] = None,
) -> dict:
    """Check dish ingredients against common allergen categories.

    Args:
        ingredients: List of ingredients in the dish.
        customer_allergens: Specific allergens to check (e.g. gluten, dairy, nuts).
                          If omitted, checks all 8 major allergen categories.
    """
    if not _check_rate_limit():
        return {"error": "Rate limit exceeded. Upgrade to pro tier."}

    check_categories = customer_allergens if customer_allergens else list(_ALLERGENS.keys())
    ingredients_lower = [i.lower().replace(" ", "_") for i in ingredients]

    alerts = []
    safe_categories = []
    details = {}

    for category in check_categories:
        allergen_items = _ALLERGENS.get(category, [])
        found = []
        for ing in ingredients_lower:
            for allergen in allergen_items:
                if allergen in ing or ing in allergen:
                    found.append(ing)
                    break

        if found:
            alerts.append({"allergen": category, "triggered_by": list(set(found)), "severity": "AVOID"})
            details[category] = {"safe": False, "triggers": list(set(found))}
        else:
            safe_categories.append(category)
            details[category] = {"safe": True, "triggers": []}

    return {
        "ingredients_checked": ingredients,
        "allergen_alerts": alerts,
        "safe_categories": safe_categories,
        "has_allergens": len(alerts) > 0,
        "details": details,
        "disclaimer": "Always verify with kitchen staff. This is advisory only.",
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    mcp.run()
