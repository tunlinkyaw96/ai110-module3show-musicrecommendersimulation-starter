#!/usr/bin/env python3
"""
Test script demonstrating ranking and filtering options
"""

import sys
sys.path.insert(0, 'src')
from recommender import load_songs, recommend_songs

def print_recommendations(title, recommendations):
    """Pretty print recommendations"""
    print(f"\n{title}")
    print("=" * 70)
    for i, (song, score, explanation) in enumerate(recommendations, 1):
        print(f"{i}. {song['title']} by {song['artist']}")
        print(f"   Score: {score:.2f} | Genre: {song['genre']} | Mood: {song['mood']}")
    print()

# Load data
songs = load_songs("data/songs.csv")
user_prefs = {
    "favorite_genre": "pop",
    "favorite_mood": "happy",
    "target_energy": 0.85,
    "target_danceability": 0.80,
    "target_valence": 0.80,
    "target_acousticness": 0.10,
    "target_tempo": 120,
}

# TEST 1: Default (Top 5, diversity enabled)
recs1 = recommend_songs(user_prefs, songs, k=5, diversity=True)
print_recommendations("TEST 1: Default (k=5, diversity=True, min_score=0.0)", recs1)

# TEST 2: High confidence only
recs2 = recommend_songs(user_prefs, songs, k=5, min_score=0.70)
print_recommendations("TEST 2: High confidence (min_score=0.70)", recs2)

# TEST 3: Allow artist repeats
recs3 = recommend_songs(user_prefs, songs, k=5, diversity=False)
print_recommendations("TEST 3: Allow artist repeats (diversity=False)", recs3)

# TEST 4: Get all qualifying songs
recs4 = recommend_songs(user_prefs, songs, k=100, min_score=0.30)
print_recommendations(f"TEST 4: All songs >= 0.30 score (found {len(recs4)} songs)", recs4)

# Descriptive summary
print("\nFILTERING SUMMARY")
print("=" * 70)
print(f"Original catalog:         18 songs")
print(f"Default (k=5, diversity): {len(recs1)} recommendations")
print(f"High confidence (0.70):   {len(recs2)} recommendations")
print(f"Allow artist repeats:     {len(recs3)} recommendations")
print(f"All >= 0.30 score:        {len(recs4)} recommendations")
