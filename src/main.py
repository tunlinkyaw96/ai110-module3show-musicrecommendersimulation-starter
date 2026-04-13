"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


def print_recommendations(profile_name: str, user_prefs: dict, songs: list) -> None:
    """Helper function to print recommendations for a single profile."""
    print("\n" + "=" * 80)
    print(f"PROFILE: {profile_name}")
    print("=" * 80)
    print(f"Genre:         {user_prefs['favorite_genre'].upper()}")
    print(f"Mood:          {user_prefs['favorite_mood'].upper()}")
    print(f"\nTarget Audio Features:")
    print(f"  Energy:        {user_prefs['target_energy']:.2f}")
    print(f"  Danceability:  {user_prefs['target_danceability']:.2f}")
    print(f"  Valence:       {user_prefs['target_valence']:.2f}")
    print(f"  Acousticness:  {user_prefs['target_acousticness']:.2f} (low = electronic)")
    print(f"  Tempo:         {user_prefs['target_tempo']:.0f} BPM")

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "-" * 80)
    print(f"TOP {len(recommendations)} RECOMMENDATIONS")
    print("-" * 80)

    for i, (song, score, explanation) in enumerate(recommendations, 1):
        print(f"\n[{i}] {song['title']}")
        print(f"    Artist: {song['artist']}")
        print(f"    Genre: {song['genre']} | Mood: {song['mood']}")
        print(f"    Song Audio: Energy {song['energy']:.2f} | Dance {song['danceability']:.2f} | Valence {song['valence']:.2f}")
        print(f"    Tempo: {song['tempo_bpm']:.0f} BPM | Acousticness: {song['acousticness']:.2f}")

        rating = 'PERFECT' if score > 0.95 else 'STRONG' if score > 0.70 else 'GOOD' if score > 0.50 else 'FAIR'
        print(f"\n    SCORE: {score:.2f}/1.00 ({rating})")
        print(f"\n    WHY THIS MATCH:")
        for reason in explanation.split('\n  '):
            if reason.strip():
                print(f"      {reason.strip()}")


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"\n{'=' * 80}")
    print(f"MUSIC RECOMMENDER STRESS TEST - PHASE 4")
    print(f"{'=' * 80}")
    print(f"Loaded {len(songs)} songs from CSV\n")

    # =========================================================================
    # NORMAL PROFILES
    # =========================================================================

    # Profile 1: High-Energy Pop Party Person
    profile_1 = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.85,
        "target_danceability": 0.80,
        "target_valence": 0.80,
        "target_acousticness": 0.10,
        "target_tempo": 120,
    }

    # Profile 2: Chill Lofi Listener
    profile_2 = {
        "favorite_genre": "lofi",
        "favorite_mood": "melancholic",
        "target_energy": 0.25,
        "target_danceability": 0.15,
        "target_valence": 0.30,
        "target_acousticness": 0.75,
        "target_tempo": 85,
    }

    # Profile 3: Deep Intense Rock Fan
    profile_3 = {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.90,
        "target_danceability": 0.40,
        "target_valence": 0.70,
        "target_acousticness": 0.05,
        "target_tempo": 140,
    }

    # =========================================================================
    # ADVERSARIAL / EDGE CASE PROFILES
    # =========================================================================

    # Profile 4: ADVERSARIAL - Contradictory preferences (high energy but sad)
    # This user wants energetic music but with sad mood - these typically conflict
    profile_4 = {
        "favorite_genre": "pop",
        "favorite_mood": "sad",
        "target_energy": 0.90,          # Very high energy
        "target_danceability": 0.80,    # Very danceable
        "target_valence": 0.15,         # Low valence (sad/depressing)
        "target_acousticness": 0.20,
        "target_tempo": 130,
    }

    # Profile 5: ADVERSARIAL - Genre-Acousticness conflict
    # Pop is typically electronic, but this user wants pop with high acousticness (conflicting)
    profile_5 = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.60,
        "target_danceability": 0.70,
        "target_valence": 0.75,
        "target_acousticness": 0.90,   # Very high acousticness for pop (unusual!)
        "target_tempo": 100,
    }

    # Profile 6: EDGE CASE - Extreme values (very extreme preferences)
    # Testing if the scorer handles extreme preference combinations
    profile_6 = {
        "favorite_genre": "rock",
        "favorite_mood": "happy",
        "target_energy": 0.95,          # Maximum energy
        "target_danceability": 0.95,    # Maximum danceability
        "target_valence": 0.05,         # Very low valence
        "target_acousticness": 0.02,    # Almost no acousticness
        "target_tempo": 175,            # Very fast
    }

    # Profile 7: EDGE CASE - Neutral ambiguous profile
    # All preferences are around 0.5 - what happens?
    profile_7 = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.50,
        "target_danceability": 0.50,
        "target_valence": 0.50,
        "target_acousticness": 0.50,
        "target_tempo": 100,
    }

    # Run all profiles
    print_recommendations("Profile 1: High-Energy Pop Party Person", profile_1, songs)
    print_recommendations("Profile 2: Chill Lofi Listener", profile_2, songs)
    print_recommendations("Profile 3: Deep Intense Rock Fan", profile_3, songs)
    print_recommendations("Profile 4 [ADVERSARIAL]: High-Energy BUT Sad Mood", profile_4, songs)
    print_recommendations("Profile 5 [ADVERSARIAL]: Pop with High Acousticness", profile_5, songs)
    print_recommendations("Profile 6 [EDGE CASE]: Extreme Preferences", profile_6, songs)
    print_recommendations("Profile 7 [EDGE CASE]: Neutral Ambiguous Profile", profile_7, songs)

    print("\n" + "=" * 80)
    print("STRESS TEST COMPLETE")
    print("=" * 80)
    print("\nObservations to note:")
    print("  • Profile 4: Check if contradictory preferences (energetic + sad) resolve well")
    print("  • Profile 5: Check if genre mismatch (pop + high acousticness) penalizes correctly")
    print("  • Profile 6: Check if extreme values break the scoring or produce sensible results")
    print("  • Profile 7: Check if neutral preferences spread across diverse songs")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
