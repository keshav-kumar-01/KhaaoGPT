"""
Taste DNA Engine — Core scoring and learning algorithm
"""


def score_dish_for_user(dish, profile) -> float:
    """
    Returns 0-100 match score. Higher = better fit for this user's palate.
    Penalties subtract from 100. Bonuses add up to +20.
    """
    score = 100.0

    # HEAT — hard ceiling. Exceeding it is a strong penalty.
    heat_over = dish.heat_level - profile.heat_ceiling
    if heat_over > 0:
        score -= heat_over * 9
    elif heat_over < -3:
        score -= abs(heat_over) * 1.5

    # ACID — reward match, penalise mismatch
    acid_diff = abs(dish.acid_level - profile.acid_affinity)
    score -= acid_diff * 3.5

    # SWEET — reward match
    sweet_diff = abs(dish.sweet_level - profile.sweet_tolerance)
    score -= sweet_diff * 3

    # FAT / RICHNESS
    fat_diff = abs(dish.fat_level - profile.fat_palate)
    score -= fat_diff * 3

    # UMAMI — bonus if user loves it and dish has it
    umami_bonus = (dish.umami_level / 10) * (profile.umami_affinity / 10) * 15
    score += umami_bonus

    # BITTER — only penalise if user avoids it and dish has it
    if profile.bitter_tolerance < 4 and dish.bitter_level > 5:
        score -= (dish.bitter_level - 5) * 5

    # CUISINE AFFINITY
    cuisine_scores = profile.cuisine_scores or {}
    cuisine_score = cuisine_scores.get(dish.cuisine_type, 5.0) if dish.cuisine_type else 5.0
    score += (cuisine_score - 5) * 2

    return round(max(0, min(100, score)), 1)


def update_taste_dna(profile, dish, rating: int):
    """
    Nudges Taste DNA after each meal rating.
    Learning rate is small — profile evolves slowly.
    rating: 1=loved, 2=okay, 3=disliked
    """
    lr = 0.06
    d = 1 if rating == 1 else (-1 if rating == 3 else 0)

    def nudge(val, dish_val):
        return max(0.0, min(10.0, val + d * lr * dish_val))

    profile.heat_ceiling = nudge(profile.heat_ceiling, dish.heat_level)
    profile.acid_affinity = nudge(profile.acid_affinity, dish.acid_level)
    profile.fat_palate = nudge(profile.fat_palate, dish.fat_level)
    profile.sweet_tolerance = nudge(profile.sweet_tolerance, dish.sweet_level)
    profile.umami_affinity = nudge(profile.umami_affinity, dish.umami_level)

    # Cuisine score update
    cuisine_scores = profile.cuisine_scores or {}
    current = cuisine_scores.get(dish.cuisine_type, 5.0) if dish.cuisine_type else 5.0
    if dish.cuisine_type:
        cuisine_scores[dish.cuisine_type] = round(max(0, min(10, current + d * 0.4)), 2)
        profile.cuisine_scores = cuisine_scores

    profile.total_ratings = (profile.total_ratings or 0) + 1
    return profile


def process_quiz_answers(answers: list) -> dict:
    """
    Convert 5 quiz answers into initial Taste DNA profile values.
    """
    profile = {
        "heat_ceiling": 5.0,
        "sweet_tolerance": 5.0,
        "acid_affinity": 5.0,
        "umami_affinity": 5.0,
        "fat_palate": 5.0,
        "bitter_tolerance": 5.0,
        "texture_pref": "mixed",
        "cuisine_scores": {},
    }

    CUISINE_RELATIONS = {
        "north_indian": ["punjabi", "mughlai"],
        "south_indian": ["kerala", "chettinad"],
        "chinese": ["thai", "japanese"],
        "italian": ["continental"],
        "street_food": ["chaat"],
        "mughlai": ["north_indian", "kebab"],
        "punjabi": ["north_indian"],
        "bengali": ["east_indian"],
        "korean": ["japanese", "chinese"],
        "mexican": ["tex_mex"],
    }

    for ans in answers:
        q = ans.get("question_id", 0) if isinstance(ans, dict) else ans.question_id
        a = (ans.get("answer", "") if isinstance(ans, dict) else ans.answer).lower().strip()

        if q == 1:  # Chips heat preference
            if "plain" in a:
                profile["heat_ceiling"] = 3.0
            elif "masala" in a:
                profile["heat_ceiling"] = 6.0
            elif "extreme" in a:
                profile["heat_ceiling"] = 9.0

        elif q == 2:  # Lemon/acid preference
            if "brightness" in a:
                profile["acid_affinity"] = 8.0
            elif "neutral" in a:
                profile["acid_affinity"] = 5.0
            elif "sharp" in a or "annoying" in a:
                profile["acid_affinity"] = 2.0

        elif q == 3:  # Bitterness tolerance
            if "love" in a:
                profile["bitter_tolerance"] = 8.0
            elif "fine" in a:
                profile["bitter_tolerance"] = 5.0
            elif "avoid" in a:
                profile["bitter_tolerance"] = 2.0

        elif q == 4:  # Richness preference
            if "light" in a:
                profile["fat_palate"] = 2.0
                profile["umami_affinity"] = 3.0
            elif "balanced" in a:
                profile["fat_palate"] = 5.0
                profile["umami_affinity"] = 5.0
            elif "rich" in a:
                profile["fat_palate"] = 8.0
                profile["umami_affinity"] = 8.0

        elif q == 5:  # Favourite cuisine
            cuisine_key = a.replace(" ", "_").lower()
            profile["cuisine_scores"][cuisine_key] = 8.0
            related = CUISINE_RELATIONS.get(cuisine_key, [])
            for r in related:
                profile["cuisine_scores"][r] = 6.0

    profile["quiz_completed"] = True
    return profile
