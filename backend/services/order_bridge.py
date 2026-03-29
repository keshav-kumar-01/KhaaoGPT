"""
Order Bridge — Zomato, Swiggy, and Google Maps deep link builder
"""
import re
from urllib.parse import quote


def build_zomato_url(restaurant_name: str, area: str, stored_url: str = None) -> str:
    if stored_url:
        return stored_url
    slug = re.sub(r'[^a-z0-9]+', '-', restaurant_name.lower()).strip('-')
    area_slug = re.sub(r'[^a-z0-9]+', '-', area.lower()).strip('-')
    return f"https://www.zomato.com/ncr/{slug}-{area_slug}/order"


def build_swiggy_url(restaurant_name: str, area: str, stored_url: str = None) -> str:
    if stored_url:
        return stored_url
    slug = re.sub(r'[^a-z0-9]+', '-', restaurant_name.lower()).strip('-')
    return f"https://www.swiggy.com/restaurants/{slug}-{area}"


def build_order_links(restaurant) -> dict:
    zomato = build_zomato_url(
        restaurant.name, restaurant.area or "", restaurant.zomato_url
    )
    swiggy = build_swiggy_url(
        restaurant.name, restaurant.area or "", restaurant.swiggy_url
    )
    if restaurant.lat is None:
        maps = f"https://maps.google.com/?q={quote(restaurant.name + ' ' + (restaurant.area or ''))}"
    else:
        maps = f"https://maps.google.com/?q={restaurant.lat},{restaurant.lng}"

    return {
        "zomato": zomato,
        "swiggy": swiggy,
        "google_maps": maps,
        "is_community": restaurant.is_community,
        "note": "Visit in person" if restaurant.is_community and not restaurant.zomato_url else None
    }
