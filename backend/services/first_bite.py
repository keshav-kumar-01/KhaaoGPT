"""
First Bite Simulator — Personalised taste description generator
No LLM required. Pure template logic.
"""


def generate_first_bite(dish, profile) -> str:
    parts = []

    # Opening — texture or dominant flavour
    texture_tags = dish.texture_tags if dish.texture_tags else []
    if texture_tags:
        parts.append(f"First thing you'll notice is the {texture_tags[0]} texture.")

    # Heat personalisation
    heat_over = dish.heat_level - profile.heat_ceiling
    if heat_over > 2:
        parts.append("This runs hotter than your usual comfort zone — the heat builds and lingers.")
    elif heat_over > 0:
        parts.append("Slightly above your usual range — you'll feel it but it should be manageable.")
    elif dish.heat_level < 3:
        parts.append("Very mild on heat — no burn at all.")
    else:
        parts.append(f"Heat sits around your {int(dish.heat_level)}/10 comfort level — right in your zone.")

    # Acid
    if dish.acid_level > 6 and profile.acid_affinity > 6:
        parts.append("The tang is strong and you'll love that.")
    elif dish.acid_level > 6 and profile.acid_affinity < 4:
        parts.append("There is notable sourness here which may feel sharp for your palate.")
    elif dish.acid_level < 3:
        parts.append("No sourness — clean and rounded flavour.")

    # Richness
    if dish.fat_level > 7:
        parts.append("Rich and heavy — one portion is a full meal.")
    elif dish.fat_level < 3:
        parts.append("Light dish — won't leave you feeling heavy.")

    # Sweet
    if dish.sweet_level > 6 and profile.sweet_tolerance < 4:
        parts.append("Worth noting — this is on the sweeter side, which you typically avoid.")

    # Umami bonus
    if dish.umami_level > 7 and profile.umami_affinity > 6:
        parts.append("Deep savoury depth here — exactly your kind of flavour.")

    # Taste summary append
    if dish.taste_summary:
        parts.append(dish.taste_summary)

    return " ".join(parts) if parts else "A well-balanced dish that should suit most palates."
