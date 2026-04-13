#!/usr/bin/env python3
"""
Demonstration: .sort() vs sorted()
"""

print("=" * 70)
print("DEMONSTRATION: .sort() vs sorted()")
print("=" * 70)

# ============================================================================
# EXAMPLE 1: Using .sort() (In-Place)
# ============================================================================
print("\nEXAMPLE 1: Using .sort() (In-Place Sorting)")
print("-" * 70)

songs_list = [
    ("Sunrise City", 0.99),
    ("Midnight Coding", 0.17),
    ("Storm Runner", 0.38),
    ("Gym Hero", 0.73),
    ("Rooftop Lights", 0.65),
]

print("BEFORE .sort():")
print(f"  List object ID: {id(songs_list)}")
print(f"  Contents: {songs_list}")

# Use .sort()
songs_list.sort(key=lambda x: x[1], reverse=True)

print("\nAFTER .sort():")
print(f"  List object ID: {id(songs_list)}  (SAME ID - in-place)")
print(f"  Contents: {songs_list}")
print(f"  Return value: {repr(songs_list.sort())}")

# ============================================================================
# EXAMPLE 2: Using sorted() (Creates New List)
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 2: Using sorted() (Creates New List)")
print("-" * 70)

songs_list_2 = [
    ("Sunrise City", 0.99),
    ("Midnight Coding", 0.17),
    ("Storm Runner", 0.38),
    ("Gym Hero", 0.73),
    ("Rooftop Lights", 0.65),
]

print("BEFORE sorted():")
print(f"  Original list ID: {id(songs_list_2)}")
print(f"  Contents: {songs_list_2}")

# Use sorted()
sorted_songs = sorted(songs_list_2, key=lambda x: x[1], reverse=True)

print("\nAFTER sorted():")
print(f"  Original list ID: {id(songs_list_2)}  (UNCHANGED)")
print(f"  Original contents: {songs_list_2}  (UNCHANGED)")
print(f"  New sorted list ID: {id(sorted_songs)}")
print(f"  New sorted contents: {sorted_songs}")

# ============================================================================
# EXAMPLE 3: Performance Comparison (Memory)
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 3: Memory Usage Comparison")
print("-" * 70)

import sys

# Create a larger list to see memory difference
large_songs = [(f"Song{i}", 0.99 - i*0.01) for i in range(1000)]

print(f"Created list with 1000 songs")
print(f"Size of original list: {sys.getsizeof(large_songs)} bytes")

# Method 1: .sort()
test_list_1 = large_songs.copy()
size_before_sort = sys.getsizeof(test_list_1)
test_list_1.sort(key=lambda x: x[1], reverse=True)
size_after_sort = sys.getsizeof(test_list_1)

print(f"\nMethod 1: .sort() in-place")
print(f"  Size before: {size_before_sort} bytes")
print(f"  Size after: {size_after_sort} bytes")
print(f"  Memory created: ~0 bytes (modified in-place)")

# Method 2: sorted()
test_list_2 = large_songs.copy()
size_before_sorted = sys.getsizeof(test_list_2)
sorted_test_list_2 = sorted(test_list_2, key=lambda x: x[1], reverse=True)
size_original = sys.getsizeof(test_list_2)
size_new = sys.getsizeof(sorted_test_list_2)

print(f"\nMethod 2: sorted() creates new")
print(f"  Original list size: {size_original} bytes (unchanged)")
print(f"  New sorted list size: {size_new} bytes")
print(f"  Total memory used: {size_original + size_new} bytes")
print(f"  Memory created: ~{size_new} bytes (new list)")

# ============================================================================
# EXAMPLE 4: Why We Use .sort() in recommend_songs()
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 4: Why .sort() is Better for Recommendation")
print("-" * 70)

print("""
Scenario: We score 18 songs and need to rank them

OPTION A: Using .sort() [RECOMMENDED] (Current implementation)
scored_songs = [(song1, 0.99), (song2, 0.17), ...]
scored_songs.sort(key=lambda x: x[1], reverse=True)

BENEFITS:
+ Modifies list in-place (no wasting memory)
+ Original order not needed after sorting
+ Cleaner, simpler code
+ Slightly faster for large lists


OPTION B: Using sorted() (Not used)
scored_songs = [(song1, 0.99), (song2, 0.17), ...]
scored_songs = sorted(scored_songs, key=lambda x: x[1], reverse=True)

DRAWBACKS:
- Creates a new list (wastes memory)
- Original order discarded anyway
- Longer to execute
- More memory allocation overhead

Verdict: .sort() is the right choice for recommend_songs()
""")

# ============================================================================
# EXAMPLE 5: Visual Step-by-Step
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 5: Step-by-Step Recommendation Process")
print("-" * 70)

# STEP 1: Score all songs
print("\nSTEP 1: Score all songs (scored_songs list)")
scored_songs_step1 = [
    ("Sunrise City", 0.99),
    ("Midnight Coding", 0.17),
    ("Storm Runner", 0.38),
    ("Gym Hero", 0.73),
    ("Rooftop Lights", 0.65),
]
for i, (song, score) in enumerate(scored_songs_step1):
    print(f"  [{i}] {song}: {score:.2f}")

# STEP 2: Sort by score
print("\nSTEP 2: Sort by score with .sort()")
print("  Command: scored_songs.sort(key=lambda x: x[1], reverse=True)")
scored_songs_step1.sort(key=lambda x: x[1], reverse=True)
for i, (song, score) in enumerate(scored_songs_step1):
    print(f"  [{i}] {song}: {score:.2f}")

# STEP 3: Select top-K
print("\nSTEP 3: Select top 3 (k=3)")
k = 3
top_k = scored_songs_step1[:k]
for i, (song, score) in enumerate(top_k, 1):
    print(f"  {i}. {song}: {score:.2f}")

# ============================================================================
# Conclusion
# ============================================================================
print("\n" + "=" * 70)
print("KEY TAKEAWAYS")
print("=" * 70)
print("""
1. .sort() modifies the list IN-PLACE (no return value, uses less memory)
2. sorted() creates a NEW list (returns it, uses more memory)

3. In recommend_songs(), we use .sort() because:
   - We don't need the original unsorted order
   - It's more memory efficient
   - It's slightly faster
   - It's the Pythonic choice for this use case

4. The recommendation algorithm is fundamentally:
   Loop → Score → Sort → Select → Return

5. The sorting is CRITICAL:
   Without sorting, we'd pick random songs
   With sorting, we get best matches first
""")
