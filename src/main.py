"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    # Example profile: Party Person (upbeat pop)
    # Edit this profile to test different recommendations
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.85,
        "target_danceability": 0.80,
        "target_valence": 0.80,
        "target_acousticness": 0.10,
        "target_tempo": 120,
    }

    print("=" * 70)
    print("USER PROFILE")
    print("=" * 70)
    print(f"Preferred Genre: {user_prefs['favorite_genre'].upper()}")
    print(f"Preferred Mood:  {user_prefs['favorite_mood'].upper()}")
    print(f"\nTarget Audio Features:")
    print(f"  Energy:        {user_prefs['target_energy']:.2f}")
    print(f"  Danceability:  {user_prefs['target_danceability']:.2f}")
    print(f"  Valence:       {user_prefs['target_valence']:.2f}")
    print(f"  Acousticness:  {user_prefs['target_acousticness']:.2f} (low = electronic)")
    print(f"  Tempo:         {user_prefs['target_tempo']:.0f} BPM")

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 70)
    print(f"TOP {len(recommendations)} RECOMMENDATIONS")
    print("=" * 70)

    for i, (song, score, explanation) in enumerate(recommendations, 1):
        print(f"\n[{i}] {song['title']}")
        print(f"    Artist: {song['artist']}")
        print(f"    Genre: {song['genre']} | Mood: {song['mood']}")
        print(f"    Song Audio: Energy {song['energy']:.2f} | Dance {song['danceability']:.2f} | Valence {song['valence']:.2f}")
        print(f"\n    SCORE: {score:.2f}/1.00 ({'PERFECT' if score > 0.95 else 'STRONG' if score > 0.70 else 'GOOD' if score > 0.50 else 'FAIR'})")
        print(f"\n    WHY THIS MATCH:")
        for reason in explanation.split('\n  '):
            if reason.strip():
                print(f"      {reason.strip()}")

    print("\n" + "=" * 70)
    print(f"Summary: Recommended {len(recommendations)} songs using content-based filtering")
    print("=" * 70)


if __name__ == "__main__":
    main()
