# Music Recommender - Quick Reference

## THE PIPELINE AT A GLANCE

```
USER INPUT (7 preferences)
        |
        v
LOAD SONGS (18 from CSV)
        |
        v
FOR EACH SONG:
  Calculate 7 scores (genre, mood, energy, dance, acoustic, valence, tempo)
  Apply weights (0.30, 0.25, 0.15, 0.10, 0.10, 0.07, 0.03)
  Get single score [0.0 to 1.0]
        |
        v
RANK all 18 scores (highest first)
        |
        v
TAKE TOP 5
        |
        v
OUTPUT with explanations
```

---

## SCORING FORMULA

```
SCORE(song) = 0.30*genre_match 
            + 0.25*mood_match
            + 0.15*energy_proximity
            + 0.10*danceability_proximity
            + 0.10*acousticness_proximity
            + 0.07*valence_proximity
            + 0.03*tempo_proximity

where:
  genre_match, mood_match ∈ {0.0, 1.0}  (exact match only)
  
  other_proximity = exp(-(distance^2)/(2*0.25^2))
                  = Gaussian decay centered on user target
```

---

## HOW IT WORKS (Example)

User wants: **pop, happy, energetic (0.85), danceable (0.80)**

Song: "Sunrise City" - pop, happy, energy 0.82, danceability 0.79

Scoring:
```
Score = 0.30*(1.0) genre match
      + 0.25*(1.0) mood match
      + 0.15*(0.99) energy close (0.82 ≈ 0.85)
      + 0.10*(0.99) danceability close (0.79 ≈ 0.80)
      + 0.10*(0.91) acousticness close
      + 0.07*(0.97) valence close
      + 0.03*(0.99) tempo close
      ─────────────────────────────
      = 0.99 MATCH!
```

---

## WHY WEIGHTS MATTER

**With current weights (genre=0.30, mood=0.25):**
- Perfect genre + mood match = 0.55 points (55% of max)
- Remaining factors can add another 0.44 points
- **Genre mismatch = hard to overcome** (lose 0.30 points!)

**Example: Gym Hero doesn't match mood (intense ≠ intense) but matches genre (pop)**
- Genre match: 0.30
- Mood mismatch: 0.0
- Energy match (0.93 vs 0.85): 0.15
- Other factors: ~0.27
- **Total: 0.73** (still ranks #2!)

---

## PROFILE DIFFERENTIATION

Each profile's top pick:

| Profile | Top Pick | Score | Why? |
|---------|----------|-------|------|
| Party Person | Sunrise City (pop, happy, 0.82E) | 0.99 | Perfect match |
| Study Buddy | Midnight Coding (lofi, chill, 0.42E) | 0.99 | Perfect match |
| Gym Enthusiast | Storm Runner (rock, intense, 0.91E) | 1.00 | Perfect match |
| Late Night Romantic | Coffee Shop Stories (jazz, relaxed, 0.37E) | 0.71 | Genre + acoustic match |

**Key metric:** When non-matching profile tests a song, score drops dramatically:
- Study Buddy tests Sunrise City (Party Person's #1): **0.16** ✗
- Party Person tests Midnight Coding (Study Buddy's #1): **0.17** ✗

---

## FILE MAP

```
data/
  songs.csv ..................... 18 songs (genre, mood, energy, etc)

src/
  recommender.py ................ Core logic
    - load_songs()         : CSV → List of dicts
    - score_song()         : User+Song → (score, reasons)
    - recommend_songs()    : User+AllSongs → TopK with explanations
    - gaussian_score()     : Proximity calculator
  
  main.py ....................... CLI runner
    - demo with Party Person profile

tests/
  test_profiles.py .............. Test all 4 profiles
    - PROFILE_PARTY_PERSON
    - PROFILE_STUDY_BUDDY
    - PROFILE_GYM_ENTHUSIAST
    - PROFILE_LATE_NIGHT_ROMANTIC
    - Runs all + prints comparison matrix

docs/
  ALGORITHM_FLOW.md ............. Detailed flowchart (Mermaid.js)
  DESIGN_FLOW_VISUAL.md ......... Visual pipeline + analysis
  QUICK_REFERENCE.md ............ This file
```

---

## RUN THE SYSTEM

```bash
# Test with Party Person example
python -m src.main

# Test with all 4 profiles + comparison matrix
python tests/test_profiles.py
```

---

## NEXT STEPS (CUSTOMIZATION)

Want different behavior? Edit these:

**1. Change weights in `score_song()` (recommender.py line 101-108)**
```python
weights = {
    'genre': 0.30,      # <-- change this
    'mood': 0.25,       # <-- or this
    'energy': 0.15,     # <-- or this
    ...
}
```

**2. Change strictness in `gaussian_score()` (recommender.py line 76)**
```python
sigma = 0.25  # <-- lower = stricter (sharper penalty for distance)
              # <-- higher = looser (more forgiving)
```

**3. Add new profiles in `main.py` or `test_profiles.py`**
```python
user_prefs = {
    "favorite_genre": "...",
    "favorite_mood": "...",
    "target_energy": 0.X,
    ...
}
```

**4. Change K (number of recommendations) in `main.py`**
```python
recommendations = recommend_songs(user_prefs, songs, k=10)  # Show 10 instead of 5
```

---

## LIMITATIONS

Current system can be improved by:
- [ ] Secondary genres (allow "pop + indie pop")
- [ ] Cold-start: profile for new users
- [ ] Diversity: avoid recommending same artist twice
- [ ] Exploration: sometimes show lower-scored "surprising" picks
- [ ] Feedback loop: learn from user skip/like behavior
- [ ] Lyrics: analyze song lyrics for semantic similarity
- [ ] Context: time of day, device type, time since last listen
