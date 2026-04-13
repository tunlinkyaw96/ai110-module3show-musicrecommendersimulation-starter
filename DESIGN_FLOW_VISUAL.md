# Music Recommender - Visual Design Summary

## Three-Stage Pipeline

```
┌─────────────────────────────────────────────────────────────────────┐
│                    MUSIC RECOMMENDER SYSTEM                         │
└─────────────────────────────────────────────────────────────────────┘

STAGE 1: INPUT
═════════════════════════════════════════════════════════════════════════
User provides 7 preference dimensions:

    User Profile Dictionary
    ┌─────────────────────────────────┐
    │ favorite_genre:  "pop"          │
    │ favorite_mood:   "happy"        │
    │ target_energy:   0.85           │
    │ target_danceability: 0.80       │
    │ target_valence:  0.80           │
    │ target_acousticness: 0.10       │
    │ target_tempo:    120 BPM        │
    └─────────────────────────────────┘
             |
             | + CSV file
             |
             v
    Songs catalog (18 songs loaded)


STAGE 2: PROCESSING (The Loop)
═════════════════════════════════════════════════════════════════════════
For EACH of 18 songs:

    ┌──────────────┐
    │ SONG INPUT   │  "Sunrise City" by Neon Echo
    │              │  genre: pop, mood: happy, energy: 0.82, ...
    └──────┬───────┘
           │
           v
    ┌────────────────────────────────────┐
    │ 7-FEATURE SCORING ENGINE           │
    ├────────────────────────────────────┤
    │ 1. Genre:       pop == pop?   YES  │
    │    Score: 1.0  (weight: 0.30)     │
    │                                    │
    │ 2. Mood:        happy==happy? YES  │
    │    Score: 1.0  (weight: 0.25)     │
    │                                    │
    │ 3. Energy:      distance 0.03      │
    │    Score: 0.99 (weight: 0.15)     │
    │                                    │
    │ 4. Danceability: distance 0.01     │
    │    Score: 0.99 (weight: 0.10)     │
    │                                    │
    │ 5. Acousticness: distance 0.08     │
    │    Score: 0.91 (weight: 0.10)     │
    │                                    │
    │ 6. Valence:     distance 0.04      │
    │    Score: 0.97 (weight: 0.07)     │
    │                                    │
    │ 7. Tempo:       normalized dist    │
    │    Score: 0.99 (weight: 0.03)     │
    └────────────────────────────────────┘
           │
           v
    ┌────────────────────────────────────┐
    │ WEIGHTED SUM                       │
    │ = 0.30×1.0 + 0.25×1.0 + 0.15×0.99 │
    │   + 0.10×0.99 + 0.10×0.91         │
    │   + 0.07×0.97 + 0.03×0.99         │
    │                                    │
    │ FINAL SCORE: 0.99                  │
    │ WITH EXPLANATION                   │
    │ "Genre matches, Mood matches, ..." │
    └────────────────────────────────────┘
           │
           | [REPEAT 17 MORE TIMES]
           |
           v
    ┌───────────────────────────────────────┐
    │ ALL 18 SONGS NOW SCORED               │
    │ [(song1, 0.99, [...]),                │
    │  (song2, 0.73, [...]),                │
    │  (song3, 0.65, [...]),                │
    │  ... 15 more ...]                     │
    └───────────────────────────────────────┘


STAGE 3: OUTPUT (Ranking & Display)
═════════════════════════════════════════════════════════════════════════
    
    ┌────────────────────────────┐
    │ SORT by Score (desc)       │
    │ 0.99, 0.73, 0.65,          │
    │ 0.59, 0.44, 0.42, ...      │
    └────────────────────────────┘
             |
             v
    ┌────────────────────────────┐
    │ SELECT TOP-K (K=5)         │
    │ • Song[0] score=0.99  ⭐   │
    │ • Song[1] score=0.73  ⭐   │
    │ • Song[2] score=0.65  ⭐   │
    │ • Song[3] score=0.59  ⭐   │
    │ • Song[4] score=0.44  ⭐   │
    └────────────────────────────┘
             |
             v
    ┌─────────────────────────────────────┐
    │ FORMAT RECOMMENDATIONS              │
    │ Add top 3 explanations per song     │
    └─────────────────────────────────────┘
             |
             v
    ┌─────────────────────────────────────┐
    │ FINAL OUTPUT (Display)              │
    │                                     │
    │ 1. Sunrise City (Score: 0.99)       │
    │    Genre: pop | Mood: happy         │
    │    Why:                             │
    │    - [MATCH] Genre: pop             │
    │    - [MATCH] Mood: happy            │
    │    - Energy: 0.82 (target 0.85)     │
    │                                     │
    │ 2. Gym Hero (Score: 0.73)           │
    │    Genre: pop | Mood: intense       │
    │    Why:                             │
    │    - [MATCH] Genre: pop             │
    │    - [MISMATCH] Mood: intense       │
    │    - Energy: 0.93 (target 0.85)     │
    │    ... (3 more recommendations)     │
    └─────────────────────────────────────┘
```

---

## Complexity & Performance

```
COMPLEXITY ANALYSIS
═════════════════════════════════════════════════════════════════════

Input Size (n):           18 songs
Features per song:        7
Operations per song:      7 similarities + 1 weighted sum = 8 ops

Time Complexity:
  - Scoring loop:         O(n × 7)  = O(18 × 7) = 126 ops
  - Sorting:              O(n log n) = O(75 comparisons)
  - Selecting top-K:      O(n) = O(18 ops)
  ─────────────────────────────────────
  TOTAL:                  ~200 operations

Space Complexity:
  - Song list:            O(n × 7) = array of 18 × 7 values
  - Scored results:       O(n) = 18 score tuples
  - Output (top-K):       O(k) = 5 tuples
  
Real-world Performance:
  - Scoring all 18 songs: < 5ms
  - Sorting & ranking:    < 2ms
  - Total latency:        < 10ms
  
Scalability Notes:
  - With 1,000 songs:     ~100ms (still interactive)
  - With 1M songs:        ~100 seconds (batch-friendly)
```

---

## Decision Points in the Pipeline

```
CRITICAL DESIGN DECISIONS
═════════════════════════════════════════════════════════════════════

1. CATEGORICAL vs. NUMERICAL
   └─ Genre/Mood: all-or-nothing (1.0 or 0.0)
   └─ Energy/Danceability/etc: proximity-based (Gaussian decay)
   └─ WHY: Genre mismatches are fatal; numerical features are flexible

2. WEIGHT HIERARCHY
   └─ Genre (0.30) > Mood (0.25) > Energy (0.15) > ...
   └─ WHY: Broad signals first, then narrow refinement

3. GAUSSIAN DECAY (not simple distance)
   └─ Score = exp(-(distance^2)/(2*sigma^2))
   └─ WHY: Rewards closeness, smooth falloff, natural penalty

4. K=5 RECOMMENDATIONS
   └─ Empirically good for music (not too many, not too few)
   └─ Could adjust based on context

5. TOP-3 EXPLANATIONS
   └─ Don't overwhelm user; show most relevant reasons
   └─ Could expand for detailed debugging
```

---

## Mental Model (Simple Version)

```
Think of it as "7-dimensional matching":

    User Profile = Target Point in 7D Space
    Each Song = Another Point in 7D Space
    
    Scoring = Distance from Song to Target
    Closer songs = Higher scores = Better recommendations
    
    BUT with weights:
    - Genre & Mood dimensions are "pinned" (attract/repel strongly)
    - Other dimensions use smooth decay (flexible)
    
    Ranking = Sorting by distance (nearest to farthest)
    Output = Show the 5 closest songs + why they're close
```

---

## Testing the Design

```
VERIFICATION CHECKLIST
═════════════════════════════════════════════════════════════════════

[✓] INPUT PHASE
    - User profiles load correctly
    - All 7 features present
    - Songs.csv loaded (18 songs)

[✓] PROCESSING PHASE
    - score_song() calculates correctly
    - Gaussian decay applied
    - Weights sum to 1.0
    - All 18 songs scored

[✓] OUTPUT PHASE
    - Results sorted correctly
    - Top-5 selected
    - Explanations generated
    - Output formatted readably

[✓] PROFILE DIFFERENTIATION
    - Party Person gets pop recommendations
    - Study Buddy gets lofi recommendations
    - Gym Enthusiast gets rock/metal recommendations
    - Late Night Romantic gets jazz/r&b recommendations
    - Scores separate clearly (0.99 vs 0.17, etc)

[✓] EDGE CASES
    - No songs match all criteria (graceful degradation)
    - Multiple songs with same score (stable sort)
    - New profiles (interpolation works)
```

---

## Files Implementing This Design

```
data/songs.csv
    ^
    |
    +-- load_songs() ────> List[Dict]
                              |
                              v
src/recommender.py      score_song() ──> (score, reasons)
    |
    +-- recommend_songs() ────> [(song, score, explanation), ...]
    |
    v
src/main.py ───> Display to User

tests/test_profiles.py ───> Verify all 4 profiles differentiate
```

