"""
Community Service — Taste tag inference and submission handling
"""
import cloudinary
import cloudinary.uploader
from config import CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET

TASTE_TAG_MAP = {
    "spicy":       {"heat_level": 7.5},
    "very spicy":  {"heat_level": 9.0},
    "mild":        {"heat_level": 2.0},
    "no heat":     {"heat_level": 0.0},
    "tangy":       {"acid_level": 7.5},
    "sour":        {"acid_level": 8.0},
    "fresh":       {"acid_level": 5.0},
    "rich":        {"fat_level": 8.0},
    "heavy":       {"fat_level": 8.5},
    "light":       {"fat_level": 2.5},
    "oily":        {"fat_level": 8.0},
    "sweet":       {"sweet_level": 8.0},
    "not sweet":   {"sweet_level": 1.5},
    "umami":       {"umami_level": 8.0},
    "savoury":     {"umami_level": 7.0},
    "smoky":       {"umami_level": 7.5},
    "crispy":      {"texture_tags": ["crispy"]},
    "crunchy":     {"texture_tags": ["crunchy"]},
    "soft":        {"texture_tags": ["soft"]},
    "chewy":       {"texture_tags": ["chewy"]},
    "street_style": {},
    "cheap":       {},
    "filling":     {"fat_level": 7.0, "umami_level": 6.0},
    "cheap & filling": {"fat_level": 7.0, "umami_level": 6.0},
    "street style": {},
}

TEXTURE_TAGS = ["crispy", "crunchy", "soft", "chewy", "fluffy", "juicy"]

# Configure Cloudinary
cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
    secure=True
)


def upload_to_cloudinary(file_path_or_url: str, folder="khaogpt_community"):
    """
    Uploads an image to Cloudinary and returns the URL.
    """
    try:
        response = cloudinary.uploader.upload(file_path_or_url, folder=folder)
        return response.get("secure_url")
    except Exception as e:
        print(f"Cloudinary upload failed: {e}")
        return None


def infer_taste_vector(taste_tags: list) -> dict:
    """
    Converts user's taste tags into a numeric taste vector.
    Averages overlapping values when multiple tags map to same axis.
    """
    axis_values = {
        "heat_level": [], "sweet_level": [], "acid_level": [],
        "umami_level": [], "fat_level": [], "bitter_level": []
    }
    texture = []

    for tag in taste_tags:
        mapping = TASTE_TAG_MAP.get(tag.lower().strip(), {})
        for axis, val in mapping.items():
            if axis == "texture_tags":
                texture.extend(val)
            elif axis in axis_values:
                axis_values[axis].append(val)

    result = {}
    for axis, vals in axis_values.items():
        result[axis] = round(sum(vals) / len(vals), 1) if vals else 5.0

    result["texture_tags"] = texture
    return result
