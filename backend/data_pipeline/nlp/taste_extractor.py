"""
NLP Taste Extractor — Extract taste vectors and texture tags from restaurant descriptions
"""
import re
from services.community_service import TASTE_TAG_MAP, TEXTURE_TAGS

class TasteExtractor:
    def __init__(self):
        # Build keywords from the tag map
        self.keywords = list(TASTE_TAG_MAP.keys())
        self.texture_keywords = TEXTURE_TAGS

    def extract_from_text(self, text: str) -> dict:
        """
        Extracts taste score and texture tags from a blob of text.
        Simple frequency and keyword-based approach for MVP.
        """
        if not text:
            return {
                "heat_level": 5.0, "sweet_level": 5.0, "acid_level": 5.0,
                "umami_level": 5.0, "fat_level": 5.0, "bitter_level": 5.0,
                "texture_tags": []
            }
        
        text_lower = text.lower()
        
        # Scoring components
        scores = {
            "heat_level": [], "sweet_level": [], "acid_level": [],
            "umami_level": [], "fat_level": [], "bitter_level": []
        }
        textures = []
        
        # Check for keywords and aggregate scores
        for kw, mapping in TASTE_TAG_MAP.items():
            if kw in text_lower:
                for axis, val in mapping.items():
                    if axis == "texture_tags":
                        textures.extend(val)
                    elif axis in scores:
                        scores[axis].append(val)
        
        # Check specific texture keywords
        for tkw in self.texture_keywords:
            if tkw in text_lower and tkw not in textures:
                textures.append(tkw)
        
        # Final average or neutral 5.0
        result = {}
        for axis, vals in scores.items():
            result[axis] = round(sum(vals) / len(vals), 1) if vals else 5.0
            
        result["texture_tags"] = list(set(textures))
        return result

# Global instance
taste_extractor = TasteExtractor()
