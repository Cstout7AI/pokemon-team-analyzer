#This is an app that ingests a list of pokemon a.k.a Pokemon Team and performs a general analysis on that team.
import requests
import sys
import matplotlib.pyplot as plt
import streamlit as st
import requests

# -----------------------------
# SAFE API CALL
# -----------------------------
def safe_get(url):
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException:
        return None

    if response.status_code != 200:
        return None

    return response


# -----------------------------
# GRADE LOGIC
# -----------------------------
def get_type_diversity_grade(score):
    if score >= 16:
        return "A"
    elif score >= 12:
        return "B"
    elif score >= 8:
        return "C"
    elif score >= 4:
        return "D"
    else:
        return "F"


# -----------------------------
# ANALYSIS FUNCTIONS
# -----------------------------
def analyze_team(pokemon_list):

    tallest = {"name": "", "height": 0}
    heaviest = {"name": "", "weight": 0}
    fastest = {"name": "", "speed": 0}

    all_types = set()

    for pokemon in pokemon_list:
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"
        response = safe_get(url)

        if not response:
            continue

        data = response.json()

        name = data["name"]

        # HEIGHT + WEIGHT
        height = data["height"]
        weight = data["weight"]

        if height > tallest["height"]:
            tallest = {"name": name, "height": height}

        if weight > heaviest["weight"]:
            heaviest = {"name": name, "weight": weight}

        # SPEED
        for stat in data["stats"]:
            if stat["stat"]["name"] == "speed":
                if stat["base_stat"] > fastest["speed"]:
                    fastest = {"name": name, "speed": stat["base_stat"]}

        # TYPES
        for t in data["types"]:
            all_types.add(t["type"]["name"])

    diversity_score = len(all_types)

    return {
        "tallest": tallest,
        "heaviest": heaviest,
        "fastest": fastest,
        "type_diversity": {
            "score": diversity_score,
            "grade": get_type_diversity_grade(diversity_score),
            "types": sorted(list(all_types))
        }
    }


# -----------------------------
# STREAMLIT UI
# -----------------------------
st.title("⚡ Pokémon Team Analyzer")
st.write("Enter 3 Pokémon to analyze your team stats")

col1, col2, col3 = st.columns(3)

with col1:
    p1 = st.text_input("Pokémon 1")

with col2:
    p2 = st.text_input("Pokémon 2")

with col3:
    p3 = st.text_input("Pokémon 3")

if st.button("Analyze Team"):

    team = [p1, p2, p3]
    team = [p.lower().strip() for p in team if p]

    if len(team) != 3:
        st.error("Please enter exactly 3 Pokémon.")
    else:
        with st.spinner("Analyzing team..."):
            result = analyze_team(team)

        st.subheader("📊 Team Report")

        st.write("### 🏔 Tallest Pokémon")
        st.write(result["tallest"])

        st.write("### ⚖️ Heaviest Pokémon")
        st.write(result["heaviest"])

        st.write("### ⚡ Fastest Pokémon")
        st.write(result["fastest"])

        st.write("### 🧬 Type Diversity")
        st.write(f"Score: {result['type_diversity']['score']}")
        st.write(f"Grade: {result['type_diversity']['grade']}")
        st.write(result["type_diversity"]["types"])
