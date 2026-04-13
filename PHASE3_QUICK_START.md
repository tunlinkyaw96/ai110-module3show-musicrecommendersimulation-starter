# Phase 3: Implementation - Quick Start

## Run the System

```bash
# Load and recommend with default profile (pop, happy)
python -m src.main

# Test with all 4 profiles + comparison matrix
python tests/test_profiles.py

# See .sort() vs sorted() performance difference
python sort_vs_sorted_demo.py

# Test filtering options (score threshold, diversity)
python test_filtering.py
```

---

## Output Example

```
Loaded songs: 18

======================================================================
USER PROFILE
======================================================================
Preferred Genre: POP
Preferred Mood:  HAPPY

Target Audio Features:
  Energy:        0.85
  Danceability:  0.80
  Valence:       0.80
  Acousticness:  0.10 (low = electronic)
  Tempo:         120 BPM

======================================================================
TOP 5 RECOMMENDATIONS
======================================================================

[1] Sunrise City
    Artist: Neon Echo
    Genre: pop | Mood: happy
    
    SCORE: 0.99/1.00 (PERFECT)
    
    WHY THIS MATCH:
      [MATCH] Genre: pop (+0.30)
      [MATCH] Mood: happy (+0.25)
      Energy: 0.82 vs 0.85 (+0.15)
```

---

## Key Insights

**Scoring Formula:**
```
SCORE = 0.30*genre + 0.25*mood + 0.15*energy 
      + 0.10*dance + 0.10*acoustic + 0.07*valence + 0.03*tempo
```

**Results for pop+happy user:**
- Sunrise City (0.99): Genre ✓ Mood ✓ → PERFECT
- Gym Hero (0.73): Genre ✓ Mood ✗ → STRONG (energy saves it)
- Rooftop Lights (0.65): Genre ✗ Mood ✓ → GOOD (mood helps)
- Island Vibes (0.59): Genre ✗ Mood ✓ → GOOD (mood keeps it)
- Urban Rhythm (0.44): Genre ✗ Mood ✗ → FAIR (only energy helps)

---

## Documentation

- `PHASE3_SUMMARY.md` - Complete Phase 3 walkthrough
- `PHASE3_CLI_VERIFICATION.md` - Verification results
- `RECOMMEND_SONGS_WALKTHROUGH.md` - 3-step process detailed
- `RANKING_FILTERING_LOGIC.md` - How filtering works
- `ALGORITHM_FLOW.md` - Mermaid flowcharts

---

## Test Different Profiles

Edit `src/main.py` line 21-28 to change user profile:

```python
# Example: Study Buddy
user_prefs = {
    "favorite_genre": "lofi",
    "favorite_mood": "chill",
    "target_energy": 0.40,
    "target_danceability": 0.55,
    "target_valence": 0.60,
    "target_acousticness": 0.75,
    "target_tempo": 75,
}
```

Then run: `python -m src.main`

---

## Phase 3: COMPLETE ✓

All requirements met:
- [x] load_songs() loads 18 songs
- [x] score_song() scores 7 features with explicit points
- [x] recommend_songs() ranks and returns top-K
- [x] CLI displays professionally with transparency
- [x] Results verified & match expectations
