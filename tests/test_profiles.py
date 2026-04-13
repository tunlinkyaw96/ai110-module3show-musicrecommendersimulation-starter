"""
Test all 4 user profiles to demonstrate differentiation.

Each profile represents a distinct listening context and taste preference.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from recommender import load_songs, recommend_songs


# ============================================================================
# DEFINE ALL 4 USER PROFILES
# ============================================================================

PROFILE_PARTY_PERSON = {
    "name": "Party Person",
    "favorite_genre": "pop",
    "favorite_mood": "happy",
    "target_energy": 0.85,
    "target_danceability": 0.80,
    "target_valence": 0.80,
    "target_acousticness": 0.10,
    "target_tempo": 120,
    "description": "Wants upbeat, danceable pop for social settings. Prefers electronic/produced sounds."
}

PROFILE_STUDY_BUDDY = {
    "name": "Study Buddy",
    "favorite_genre": "lofi",
    "favorite_mood": "chill",
    "target_energy": 0.40,
    "target_danceability": 0.55,
    "target_valence": 0.60,
    "target_acousticness": 0.75,
    "target_tempo": 75,
    "description": "Wants low-energy background music for focus. Prefers acoustic textures."
}

PROFILE_GYM_ENTHUSIAST = {
    "name": "Gym Enthusiast",
    "favorite_genre": "rock",
    "favorite_mood": "intense",
    "target_energy": 0.90,
    "target_danceability": 0.70,
    "target_valence": 0.50,
    "target_acousticness": 0.10,
    "target_tempo": 140,
    "description": "Wants high-energy, intense music for workouts. Doesn't need happiness—just power."
}

PROFILE_LATE_NIGHT_ROMANTIC = {
    "name": "Late Night Romantic",
    "favorite_genre": "jazz",
    "favorite_mood": "romantic",
    "target_energy": 0.45,
    "target_danceability": 0.60,
    "target_valence": 0.65,
    "target_acousticness": 0.70,
    "target_tempo": 90,
    "description": "Wants smooth, acoustic, emotionally warm music. Moderate energy—not too intense, not too chill."
}

ALL_PROFILES = [
    PROFILE_PARTY_PERSON,
    PROFILE_STUDY_BUDDY,
    PROFILE_GYM_ENTHUSIAST,
    PROFILE_LATE_NIGHT_ROMANTIC,
]


# ============================================================================
# TEST FUNCTION
# ============================================================================

def test_all_profiles():
    """
    Load songs and test all 4 profiles to show differentiation.
    """
    # Load songs
    songs = load_songs("data/songs.csv")
    print(f"[OK] Loaded {len(songs)} songs from data/songs.csv\n")

    # Test each profile
    for profile in ALL_PROFILES:
        print("=" * 80)
        print(f"\n{profile['name']}")
        print(f"Description: {profile['description']}")
        print(f"\nPreferences:")
        print(f"  Genre: {profile['favorite_genre']}")
        print(f"  Mood: {profile['favorite_mood']}")
        print(f"  Energy: {profile['target_energy']:.2f}")
        print(f"  Danceability: {profile['target_danceability']:.2f}")
        print(f"  Valence: {profile['target_valence']:.2f}")
        print(f"  Acousticness: {profile['target_acousticness']:.2f}")
        print(f"  Tempo: {profile['target_tempo']:.0f} BPM")

        # Get recommendations for this profile
        # Remove name and description before passing to recommend_songs
        user_prefs = {k: v for k, v in profile.items() if k not in ['name', 'description']}
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print(f"\n=> Top 5 Recommendations:")
        for i, (song, score, explanation) in enumerate(recommendations, 1):
            print(f"\n  {i}. {song['title']} by {song['artist']} (Score: {score:.2f})")
            print(f"     Genre: {song['genre']} | Mood: {song['mood']}")
            print(f"     Why:")
            for reason in explanation.split('\n  '):
                if reason:
                    print(f"       - {reason}")

        print("\n")


def show_song_scores_table():
    """
    Show a comparison matrix: Songs × Profiles.
    """
    songs = load_songs("data/songs.csv")
    from recommender import score_song

    print("\n" + "=" * 80)
    print("SCORE COMPARISON MATRIX: All Profiles vs Key Songs")
    print("=" * 80 + "\n")

    # Select a few representative songs to show in the matrix
    key_songs = [
        "Sunrise City",
        "Midnight Coding",
        "Storm Runner",
        "Coffee Shop Stories",
        "Thunder Strike",
        "Piano Nocturne",
        "Urban Rhythm",
        "Neon Pulse",
    ]

    # Header
    print(f"{'Song':<25}", end="")
    for profile in ALL_PROFILES:
        print(f" | {profile['name']:<15}", end="")
    print()
    print("-" * 120)

    # Each song
    for song in songs:
        if song['title'] not in key_songs:
            continue

        print(f"{song['title']:<25}", end="")

        for profile in ALL_PROFILES:
            user_prefs = {k: v for k, v in profile.items() if k not in ['name', 'description']}
            score, _ = score_song(user_prefs, song)
            print(f" | {score:>6.2f}           ", end="")

        print()


if __name__ == "__main__":
    test_all_profiles()
    show_song_scores_table()
    print("\n[OK] Test completed!")
