import re

def normalize_title(title: str) -> str:
    """
    Normalize titles to reduce duplicates:
    - Remove 'Season X', 'Episode Y', 'Part N'
    - Lowercase
    """
    t = title.lower()
    t = re.sub(r": season \d+", "", t)
    t = re.sub(r": episode \d+", "", t)
    t = re.sub(r"[-:]\s*episode \d+", "", t)
    t = re.sub(r"[-:]\s*part \d+", "", t)
    return t.strip()

def deduplicate_titles(titles: list[str]) -> list[str]:
    """Remove duplicates like multiple episodes of the same show."""
    seen = set()
    deduped = []
    for t in titles:
        norm = normalize_title(t)
        if norm not in seen:
            seen.add(norm)
            deduped.append(t)
    return deduped
