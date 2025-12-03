"""
Test script for the Hybrid Music Generator
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.services.hybrid_generator import HybridMusicGenerator
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_generation():
    """Test arpeggio generation with various parameters"""
    
    print("=" * 60)
    print("Testing Hybrid Music Generator")
    print("=" * 60)
    
    # Initialize generator
    print("\n1. Initializing generator...")
    generator = HybridMusicGenerator()
    print("✓ Generator initialized")
    
    # Test cases
    test_cases = [
        {
            "name": "Happy C Major",
            "params": {
                "key": "C",
                "mood": "happy",
                "bpm": 120,
                "num_bars": 2,
                "pattern_style": "ai-generated"
            }
        },
        {
            "name": "Dark A Minor",
            "params": {
                "key": "A",
                "mood": "dark",
                "bpm": 90,
                "num_bars": 2,
                "pattern_style": "ai-generated"
            }
        },
        {
            "name": "Energetic G Major",
            "params": {
                "key": "G",
                "mood": "energetic",
                "bpm": 140,
                "num_bars": 4,
                "pattern_style": "ai-generated"
            }
        },
        {
            "name": "Calm Ascending",
            "params": {
                "key": "D",
                "mood": "calm",
                "bpm": 80,
                "num_bars": 2,
                "pattern_style": "ascending"
            }
        }
    ]
    
    # Run tests
    for i, test in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: {test['name']}")
        print(f"   Parameters: {test['params']}")
        
        try:
            midi, description = generator.generate_arpeggio(**test['params'])
            
            # Get info
            duration = midi.get_end_time()
            num_notes = sum(len(inst.notes) for inst in midi.instruments)
            
            # Save MIDI file
            filename = f"test_{test['name'].replace(' ', '_').lower()}.mid"
            midi.write(filename)
            
            print(f"   ✓ Generated successfully")
            print(f"   Description: {description}")
            print(f"   Duration: {duration:.2f}s")
            print(f"   Notes: {num_notes}")
            print(f"   Saved: {filename}")
            
        except Exception as e:
            print(f"   ✗ Failed: {e}")
    
    print("\n" + "=" * 60)
    print("Testing complete!")
    print("=" * 60)


def test_moods():
    """Test all available moods"""
    
    print("\n" + "=" * 60)
    print("Testing All Moods")
    print("=" * 60)
    
    generator = HybridMusicGenerator()
    moods = generator.get_available_moods()
    
    print(f"\nAvailable moods: {', '.join(moods)}")
    
    for mood in moods:
        print(f"\nGenerating {mood} arpeggio...")
        try:
            midi, description = generator.generate_arpeggio(
                key="C",
                mood=mood,
                bpm=120,
                num_bars=2,
                pattern_style="ai-generated"
            )
            
            filename = f"test_mood_{mood}.mid"
            midi.write(filename)
            print(f"✓ {description}")
            print(f"  Saved: {filename}")
            
        except Exception as e:
            print(f"✗ Failed: {e}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test the music generator")
    parser.add_argument(
        "--test",
        choices=["generation", "moods", "all"],
        default="all",
        help="Which tests to run"
    )
    
    args = parser.parse_args()
    
    if args.test in ["generation", "all"]:
        test_generation()
    
    if args.test in ["moods", "all"]:
        test_moods()