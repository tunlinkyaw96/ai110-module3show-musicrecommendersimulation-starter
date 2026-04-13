# 🎵 Model Card: SoundMatch 2.0

## 1. Model Name

**SoundMatch 2.0** — A music recommender that learns what you like and suggests songs you'll probably enjoy.

---

## 2. Goal / Task

This recommender takes what you tell it about your music taste and matches it against a song catalog. It scores each song on how well it fits your preferences, then shows you the top matches with explanations.

**What it predicts**: How much you'll like a song (score from 0.0 to 1.0).  
**What it suggests**: The 5 best songs for you and why you might like them.

---

## 3. Data Used

**Dataset Size**: 18 songs from various genres.

**What we know about each song**:
- Basic info: title, artist, genre, mood
- Sound qualities: energy level (0.0 = chill, 1.0 = intense), how danceable it is, how happy/sad it sounds (valence), how acoustic vs. electronic, tempo in BPM

**Dataset Limits**:
- Small catalog (only 18 songs — in real apps, we'd have millions)
- Not very diverse: "happy" mood shows up 3 times, but "aggressive" shows up only once
- Missing some combinations: only 1 song is both high-energy AND sad (most high-energy songs are happy)
- All songs are short clips with manually-labeled audio features (not real Spotify/Apple Music data)

---

## 4. Algorithm Summary

Here's how SoundMatch scores songs:

**Step 1: Check Category Matches**
- Does the song match your preferred genre? If yes, add 0.30 points. If no, add 0.00.
- Does the song match your mood? If yes, add 0.25 points. If no, add 0.00.

**Step 2: Score Audio Features**
For each audio feature (energy, danceability, valence, acousticness, tempo):
- Compare the song's value to your target value
- Songs very close to your target get highest points
- Songs further away get lower points (using a "bell curve" math function)
- Sum up all the audio feature scores

**Step 3: Combine Everything**
- Category match (0.55 total) + audio features (0.45 total) = final score
- Songs are ranked by final score
- Filter out songs below a minimum score
- Make sure no artist repeats (for variety)

**Step 4: Return Top 5**
- Show the 5 best matches with a breakdown of why each song scored well

**The Key Insight**: Genre and mood matter WAY more than audio features. A genre match is bigger than perfect audio alignment.

---

## 5. Observed Behavior / Biases

### Primary Bias: "Happy Music Advantage"

**What we observed**: Users who like "happy" music get recommendations that score 25% higher quality than users who like "sad" or "melancholic" music. Same app, same logic, but different outcome.

**Why it happens**: 
- The dataset has 3 "happy" songs but only 2 "sad" songs
- The mood preference has a high weight (0.25 out of 1.0)
- When we give you a 0.25 point bonus for matching your mood, it's huge for happy users who can find matches, but it's a deadly penalty for sad users who can't

**Real impact**: A happy listener got a "PERFECT" 0.99 match. A melancholic listener got a "GOOD" 0.72 match. Same recommender, identical audio targets, just different moods. The gap is literally 0.27 points from dataset imbalance + algorithm weight.

### Secondary Biases:

1. **"Dark Intense" Music Crushed**: You want high-energy but sad? Only 1 out of 6 high-energy songs has low valence. The app doesn't crash, but you'll get a mediocre recommendation because the data isn't there.

2. **Genre is King**: Perfect audio match can't save you if you pick the wrong genre. A song with your exact energy/tempo/vibe scores 0.31 points lower just because the genre is wrong.

3. **Specific Beats Vague**: If you say "I want energy 0.82," you get a 30% higher score than if you say "I dunno, maybe 0.50?" The math punishes uncertainty—which means exploring new music gets penalized.

4. **Filter Bubble**: "Sunrise City" appeared in recommendations for ALL 7 test users we tried, even users who liked completely different genres. Because it's "safe" and moderate, it appeals to everyone and dominates the list.

---

## 6. Evaluation Process

We tested this recommender with real user profiles and experiments:

### Stress Test: 7 Different User Types

We pretended to be 7 different listeners and asked for recommendations:

1. **High-Energy Pop Party Person** → Got 0.99 "PERFECT" match ✓ Works great
2. **Chill Lofi Listener** → Got 0.61 "GOOD" match ⚠ Okay, but could be better
3. **Deep Intense Rock Fan** → Got 0.93 "STRONG" match ✓ Great
4. **High-Energy BUT Sad Mood** (adversarial) → Got 0.67 "GOOD" match - system compromised
5. **Pop BUT Super Acoustic** (adversarial) → Got 0.84 "STRONG" match - genre won over acousticness demand
6. **Extreme Preferences** (energy 0.95, everything pushed to limits) → Got 0.63 "GOOD" - no perfect matches exist
7. **Ambiguous Neutral** (can't decide, everything 0.50) → Got 0.76 "STRONG" - weird, but moderate worked better than extremes

**Key Surprise**: "Sunrise City" showed up in top 5 for ALL 7 users. That's our filter bubble.

### Logic Experiments: Hypothesis Testing

We ran 5 controlled experiments to understand *why* things work:

**Experiment 1: Do Categories Really Matter More Than Audio?**
- Tested: Same song "Sunrise City" with matching genre + mood vs. mismatched genre + mood but perfect audio
- Result: Matched genre won by 0.31 points. ✓ Categories DO dominate.

**Experiment 2: Do Rare Moods Get Punished?**
- Tested: Same song scored for users liking happy, chill, melancholic, and aggressive moods
- Result: Happy got 0.97, others got 0.72. ✓ Rare moods get ~0.25 point penalty

**Experiment 3: Can You Ever Find "Dark + Energetic"?**
- Tested: Looking for high-energy, low-valence songs (metal, dark electronic)
- Result: Only 1 song matched this combo. ✓ Dataset has a valence-energy gap

**Experiment 4: Does Genre Override Everything?**
- Tested: Exact genre match with different audio vs. different genre with matching audio
- Result: Genre match won by 0.51 points. ✓ Genre is a hard filter

**Experiment 5: Are Specific Preferences Better Than Vague Ones?**
- Tested: Same song scored for user saying "I want energy 0.82" vs. "I dunno, 0.50?"
- Result: Specific won by 30.9%. ✓ System rewards confidence, punishes exploration

**All 5 experiments confirmed our hypotheses with real numbers.** We're not guessing—we have data.

---

## 7. Intended Use and Non-Intended Use

### ✅ **Designed For:**
- Learning how recommender systems work (classroom)
- Exploring music taste patterns (personal curiosity)
- Understanding scoring logic and weights (educational)
- Identifying biases and fairness issues (research)
- Testing new users with stable, predictable behavior
- Comparing different recommendation strategies

### ❌ **NOT Designed For:**
- Real Spotify/Apple Music recommendations (we only have 18 songs, not millions)
- Commercial music service (too small, too biased)
- High-stakes decisions (don't use this to decide what's "good music")
- Diverse user bases without expecting unfairness (sad music lovers will get worse recommendations)
- Replacing human music curation (our scoring is too mechanical)
- Discovering truly new music (we tend to recommend the same safe songs to everyone)

### Translation: 
**This is a tiny educational tool to learn how recommenders work and fail. It's not ready for real users who expect musical diversity.**

---

## 8. Ideas for Improvement

If we kept developing SoundMatch, here's what we'd fix:

### **Priority 1: Fix the Happy Bias**
- Add more sad/melancholic/aggressive songs to the dataset so those users get real options
- OR: Make mood weight adaptive (if a mood is rare, boost its weight to be fair)
- OR: Show users a warning when their mood preference is underrepresented

### **Priority 2: Break the Filter Bubble**
- Don't just rank by score—add randomness or diversity bonuses to new artists/genres
- Force the recommender to pick from different genres instead of always picking "Sunrise City"
- Show "runner-ups" from different genres so users see options

### **Priority 3: Support Music Discovery**
- Stop punishing vague preferences; encourage exploration
- Add a "discovery mode" where neutral targets (0.50) are treated as "open to anything" instead of "bad matches"
- Show a confidence score: "I'm 95% sure you'll like this" vs. "This is a wild guess"

**Bonus Ideas:**
- Get real user feedback ("Did you like this recommendation?") to learn what scores actually predict satisfaction
- Add artist similarity so "indie pop" recommends more indie pop neighbors, not just exact genre matches
- Support "opposite" recommendations ("Show me what energetic sad music exists")

---

## Summary

**The Bottom Line**: SoundMatch 2.0 is a fair, transparent recommender for learning purposes. It works great for mainstream users who like happy, high-energy music, but it systematically disadvantages niche music taste. The algorithm is honest about its biases—you can see exactly why it scored each song—which makes it perfect for learning how recommender systems succeed and fail in the real world.

**The Key Lesson**: Even "fair" and "neutral" algorithms carry hidden biases. SoundMatch doesn't hate sad music or indie fans—it just reflects the data and weights we gave it. That's why understanding model cards, testing edge cases, and documenting limitations matters.
