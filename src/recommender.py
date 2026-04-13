from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv
import math

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from CSV file, converting numeric values to floats."""
    songs = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert numeric strings to floats
            song = {
                'id': int(row['id']),
                'title': row['title'],
                'artist': row['artist'],
                'genre': row['genre'],
                'mood': row['mood'],
                'energy': float(row['energy']),
                'tempo_bpm': float(row['tempo_bpm']),
                'valence': float(row['valence']),
                'danceability': float(row['danceability']),
                'acousticness': float(row['acousticness']),
            }
            songs.append(song)
    return songs

def gaussian_score(song_value: float, target_value: float, sigma: float = 0.25) -> float:
    """Compute Gaussian proximity score: exp(-(distance²)/(2σ²)), peaking at target value."""
    distance = abs(song_value - target_value)
    return math.exp(-(distance ** 2) / (2 * sigma ** 2))


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song by weighted 7-feature matching: genre/mood (categorical) + energy/dance/valence/acoustic/tempo (proximity).

    Returns (score [0-1], reasons) where reasons show point allocation for transparency."""
    weights = {
        'genre': 0.30,
        'mood': 0.25,
        'energy': 0.15,
        'danceability': 0.10,
        'acousticness': 0.10,
        'valence': 0.07,
        'tempo': 0.03,
    }

    reasons = []

    # Categorical: Genre (exact match)
    # Handle both 'genre' and 'favorite_genre' keys
    user_genre = user_prefs.get('genre') or user_prefs.get('favorite_genre')
    genre_score = 1.0 if song['genre'] == user_genre else 0.0
    genre_points = weights['genre'] * genre_score
    if genre_score == 1.0:
        reasons.append(f"[MATCH] Genre: {song['genre']} (+{genre_points:.2f})")
    else:
        reasons.append(f"[MISMATCH] Genre: {song['genre']} (wanted {user_genre}) (+0.00)")

    # Categorical: Mood (exact match)
    # Handle both 'mood' and 'favorite_mood' keys
    user_mood = user_prefs.get('mood') or user_prefs.get('favorite_mood')
    mood_score = 1.0 if song['mood'] == user_mood else 0.0
    mood_points = weights['mood'] * mood_score
    if mood_score == 1.0:
        reasons.append(f"[MATCH] Mood: {song['mood']} (+{mood_points:.2f})")
    else:
        reasons.append(f"[MISMATCH] Mood: {song['mood']} (wanted {user_mood}) (+0.00)")

    # Numerical: Energy (proximity-based)
    energy_score = gaussian_score(song['energy'], user_prefs['target_energy'])
    energy_points = weights['energy'] * energy_score
    energy_diff = abs(song['energy'] - user_prefs['target_energy'])
    reasons.append(f"Energy: {song['energy']:.2f} vs {user_prefs['target_energy']:.2f} (+{energy_points:.2f})")

    # Numerical: Danceability
    dance_score = gaussian_score(song['danceability'], user_prefs['target_danceability'])
    dance_points = weights['danceability'] * dance_score
    reasons.append(f"Danceability: {song['danceability']:.2f} vs {user_prefs['target_danceability']:.2f} (+{dance_points:.2f})")

    # Numerical: Valence
    valence_score = gaussian_score(song['valence'], user_prefs['target_valence'])
    valence_points = weights['valence'] * valence_score
    reasons.append(f"Valence: {song['valence']:.2f} vs {user_prefs['target_valence']:.2f} (+{valence_points:.2f})")

    # Numerical: Acousticness
    acoustic_score = gaussian_score(song['acousticness'], user_prefs['target_acousticness'])
    acoustic_points = weights['acousticness'] * acoustic_score
    reasons.append(f"Acousticness: {song['acousticness']:.2f} vs {user_prefs['target_acousticness']:.2f} (+{acoustic_points:.2f})")

    # Numerical: Tempo (normalize to 0-1 first: min=60, max=180)
    tempo_norm = (song['tempo_bpm'] - 60) / (180 - 60)
    target_tempo_norm = (user_prefs['target_tempo'] - 60) / (180 - 60)
    tempo_score = gaussian_score(tempo_norm, target_tempo_norm)
    tempo_points = weights['tempo'] * tempo_score
    reasons.append(f"Tempo: {song['tempo_bpm']:.0f} vs {user_prefs['target_tempo']:.0f} BPM (+{tempo_points:.2f})")

    # Weighted sum
    total_score = (
        weights['genre'] * genre_score +
        weights['mood'] * mood_score +
        weights['energy'] * energy_score +
        weights['danceability'] * dance_score +
        weights['valence'] * valence_score +
        weights['acousticness'] * acoustic_score +
        weights['tempo'] * tempo_score
    )

    return total_score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5,
                    min_score: float = 0.0, diversity: bool = True) -> List[Tuple[Dict, float, str]]:
    """Score all songs, rank by score, filter by threshold and artist diversity, return top-K with explanations."""
    scored_songs = []

    # STEP 1: SCORE ALL SONGS
    # ─────────────────────────
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored_songs.append((song, score, reasons))

    # STEP 2: RANK BY SCORE (DESCENDING)
    # ──────────────────────────────────
    scored_songs.sort(key=lambda x: x[1], reverse=True)

    # STEP 3: APPLY FILTERS AND SELECT TOP-K
    # ──────────────────────────────────────
    results = []
    seen_artists = set()  # Track artists for diversity filtering

    for song, score, reasons in scored_songs:
        # Filter 1: Respect minimum score threshold
        if score < min_score:
            continue

        # Filter 2: Diversity - don't recommend same artist twice
        if diversity:
            if song['artist'] in seen_artists:
                continue
            seen_artists.add(song['artist'])

        # Format results: (song, score, explanation_string)
        explanation = "\n  ".join(reasons[:3])  # Show top 3 reasons
        results.append((song, score, explanation))

        # Stop when we have enough recommendations
        if len(results) >= k:
            break

    return results
