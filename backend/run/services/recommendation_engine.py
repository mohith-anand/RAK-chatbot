import re


def extract_tile_preferences(user_query: str):
    query = user_query.lower()

    preferences = {
        "color": None,
        "surface": None,
        "application": None,
        "space_type": None,
        "size": None,
        "look": None
    }

    colors = [
        "white", "black", "grey", "gray", "beige", "brown",
        "cream", "ivory", "blue", "green", "silver"
    ]

    surfaces = [
        "polished", "matt", "matte", "glossy", "gloss"
    ]

    looks = [
        "marble", "wood", "concrete", "stone", "cement"
    ]

    applications = [
        "wall", "floor", "outdoor"
    ]

    spaces = [
        "bathroom", "kitchen", "living room", "bedroom",
        "office", "commercial", "hotel", "restaurant"
    ]

    for color in colors:
        if color in query:
            preferences["color"] = color
            break

    for surface in surfaces:
        if surface in query:
            preferences["surface"] = surface
            break

    for look in looks:
        if look in query:
            preferences["look"] = look
            break

    for app in applications:
        if app in query:
            preferences["application"] = app
            break

    for space in spaces:
        if space in query:
            preferences["space_type"] = space
            break

    size_match = re.search(r'(\d{2,3}x\d{2,3})', query)
    if size_match:
        preferences["size"] = size_match.group(1)

    return preferences