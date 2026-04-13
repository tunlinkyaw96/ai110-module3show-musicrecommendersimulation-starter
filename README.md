# 🎵 Music Recommender Simulation

## Project Summary

This music recommender system uses **weighted content-based filtering** to predict which songs a user will love next. It mirrors real-world platforms like Spotify and YouTube by scoring each song across multiple dimensions (genre, mood, energy, etc.) and ranking by fit. The system prioritizes **categorical preferences** (exact genre/mood match) heavily, while using **proximity-based scoring** for numerical features, allowing flexibility. Unlike collaborative filtering (which relies on what similar users like), this approach uses only the song's audio features and the user's stated preferences, making it interpretable and transparent.

---

## How The System Works

### Song Features
Each song in the catalog has 10 features:
- **Categorical:** `genre` (e.g., pop, rock, lofi), `mood` (e.g., happy, intense, chill)
- **Numerical (0.0–1.0 scale):** 
  - `energy` — loudness and intensity
  - `danceability` — rhythm strength and beat regularity
  - `valence` — musical positivity/happiness
  - `acousticness` — acoustic vs. electronic instrumentation
- **Tempo:** `tempo_bpm` — beats per minute (e.g., 60–180 BPM)

### User Profile Features
Each user profile specifies 7 target preferences:
- **Categorical:** `favorite_genre`, `favorite_mood`
- **Numerical targets:** `target_energy`, `target_danceability`, `target_valence`, `target_acousticness`, `target_tempo`

### Scoring Algorithm
For each song in the catalog, the system calculates a **weighted composite score**:

```
SCORE = 0.30*genre_match + 0.25*mood_match + 0.15*energy_proximity 
      + 0.10*danceability_proximity + 0.10*acousticness_proximity 
      + 0.07*valence_proximity + 0.03*tempo_proximity
```

**Scoring rules:**
- **Genre & Mood:** Exact match = 1.0 points, no match = 0.0 points
- **Numerical features:** Gaussian decay based on distance from user target
  - Peak score (1.0) at exact target value
  - Smooth decline as distance increases
  - Formula: `exp(-(distance²)/(2×σ²))` where σ=0.25

**Weight hierarchy:** Genre (0.30) is weighted highest because it defines the primary listening context. Mood (0.25) ranks second as it captures emotional intent. Energy, danceability, and acousticness (0.15, 0.10, 0.10) provide secondary refinement.

### Recommendation Process
1. **Score all 18 songs** using the weighted formula above
2. **Rank by score** (highest first)
3. **Select top-K** (default K=5) recommendations
4. **Generate explanations** for each recommendation showing the top 3 matching signals

### Example
A user with profile (pop, happy, energy=0.85) would:
- Give "Sunrise City" (pop, happy, energy=0.82) a score of **0.99** ✓
- Give "Midnight Coding" (lofi, chill, energy=0.42) a score of **0.17** ✗
- Give "Storm Runner" (rock, intense, energy=0.91) a score of **0.38** ✗

---

## Finalized Algorithm Recipe

### Step-by-Step Scoring Process

**For each of the 18 songs in the catalog:**

1. **Check Genre Match**
   - If `song.genre == user.favorite_genre`: score = 1.0
   - Else: score = 0.0
   - Apply weight: `0.30 × genre_score`

2. **Check Mood Match**
   - If `song.mood == user.favorite_mood`: score = 1.0
   - Else: score = 0.0
   - Apply weight: `0.25 × mood_score`

3. **Calculate Energy Proximity**
   - Distance = |song.energy - user.target_energy|
   - Gaussian decay: `exp(-(distance²)/(2×0.25²))`
   - Apply weight: `0.15 × energy_score`

4. **Calculate Danceability Proximity**
   - Distance = |song.danceability - user.target_danceability|
   - Gaussian decay applied
   - Weight: `0.10 × dance_score`

5. **Calculate Acousticness Proximity**
   - Distance = |song.acousticness - user.target_acousticness|
   - Gaussian decay applied
   - Weight: `0.10 × acoustic_score`

6. **Calculate Valence Proximity**
   - Distance = |song.valence - user.target_valence|
   - Gaussian decay applied
   - Weight: `0.07 × valence_score`

7. **Calculate Tempo Proximity**
   - Normalize tempo to [0.0, 1.0] scale (min=60, max=180)
   - Distance = |normalized_song_tempo - normalized_user_target|
   - Gaussian decay applied
   - Weight: `0.03 × tempo_score`

8. **Sum Weighted Scores**
   - `FINAL_SCORE = 0.30×genre + 0.25×mood + 0.15×energy + 0.10×dance + 0.10×acoustic + 0.07×valence + 0.03×tempo`
   - Result: single score in [0.0, 1.0]

**After scoring all 18 songs:**
- Sort by final score (highest first)
- Select top 5
- Generate explanations for each (show top 3 matching signals)
- Display to user

---

## Expected Biases and Limitations

### Bias #1: Genre Over-Prioritization (weight: 0.30)
**Issue:** This system treats genre matching as "all-or-nothing." A user who loves "pop" will see a rock song score 0.30 points lower immediately, even if it perfectly matches their energy/mood preferences.

**Example:** A user who typically likes pop but secretly loves heavy metal will miss metal recommendations because genre mismatch eliminates 30% of the score.

**Mitigation:** In future versions, could allow secondary genres (e.g., "pop + indie pop") or fuzzy genre matching.

### Bias #2: Filter Bubble (No Exploration Strategy)
**Issue:** The system always recommends the mathematically highest-scored songs. It will never suggest a "surprising but delightful" song with a 0.65 score when a safe 0.95 match exists.

**Example:** Late Night Romantic user gets jazz recommendations every time—never discovers the perfect ambient artist hiding at 0.62 score.

**Mitigation:** Real recommenders use "exploration rate" (10–20% random picks) to balance discovery. This system does not.

### Bias #3: Preference Rigidity
**Issue:** User profiles are static. The system assumes a user's energy preference is always 0.85, but people's moods change throughout the day (morning chill ≠ evening party).

**Example:** Study Buddy who prefers low energy (0.40) gets low-energy songs at 6 PM when they want to work out.

**Mitigation:** Context-aware recommendations (time of day, location, current activity) could adjust profiles dynamically.

### Bias #4: Small Catalog (18 songs)
**Issue:** With only 18 songs, genre matches are rare. A user wanting "classical" music has only 1 song to choose from, so they'll always see "Piano Nocturne" as #1.

**Real-world impact:** In production systems with 100M songs, diversity problems are less severe because multiple songs match every preference.

### Bias #5: No Artist or Label Diversity Strategy
**Issue:** The system has no mechanism to prevent recommending the same artist multiple times or to promote underrepresented artists.

**Example:** Neon Echo appears twice in the catalog (songs #1 and #8). A matching user might see both ranked #1 and #3, monopolizing recommendations.

**Mitigation:** Add "Don't recommend >1 song per artist" rule to ranking phase.

### Bias #6: Assumes All Users Have Uniform Preference Shape
**Issue:** The Gaussian decay with σ=0.25 applies equally to all users. But some users might have a very narrow energy preference (σ=0.10) while others are flexible (σ=0.50).

**Example:** A user who likes "exactly 0.85 energy" gets penalized the same way as someone who's fine with 0.70–1.0 energy range.

**Mitigation:** Could allow per-user σ parameter, or offer preset "strict" vs. "flexible" modes.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

