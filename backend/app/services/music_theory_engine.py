from music21 import scale, pitch, chord
from typing import List, Dict, Tuple
import random
import logging

logger = logging.getLogger(__name__)


class MusicTheoryEngine:
    """
    Core music theory system for generating valid musical structures
    """
    
    def __init__(self):
        self.mood_configs = {
            'happy': {
                'scale_type': 'major',
                'chord_progression': ['I', 'IV', 'V', 'I'],
                'rhythm_patterns': [
                    [0.25, 0.25, 0.25, 0.25],  # Sixteenth notes
                    [0.5, 0.25, 0.25],          # Mixed
                ],
                'velocity_range': (80, 110),
                'octave_range': (0, 1),
                'note_density': 'high'
            },
            'calm': {
                'scale_type': 'major',
                'chord_progression': ['I', 'vi', 'IV', 'V'],
                'rhythm_patterns': [
                    [0.5, 0.5],                 # Half notes
                    [1.0],                      # Whole notes
                ],
                'velocity_range': (50, 80),
                'octave_range': (0, 0),
                'note_density': 'low'
            },
            'energetic': {
                'scale_type': 'major',
                'chord_progression': ['I', 'V', 'vi', 'IV'],
                'rhythm_patterns': [
                    [0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125],
                ],
                'velocity_range': (90, 127),
                'octave_range': (0, 2),
                'note_density': 'very_high'
            },
            'dark': {
                'scale_type': 'minor',
                'chord_progression': ['i', 'iv', 'v', 'i'],
                'rhythm_patterns': [
                    [0.5, 0.5],
                    [0.75, 0.25],
                ],
                'velocity_range': (40, 70),
                'octave_range': (-1, 0),
                'note_density': 'medium'
            },
            'ambient': {
                'scale_type': 'major',
                'chord_progression': ['I', 'IV', 'I', 'V'],
                'rhythm_patterns': [
                    [1.0],
                    [2.0],
                ],
                'velocity_range': (30, 60),
                'octave_range': (0, 1),
                'note_density': 'very_low'
            },
            'chaotic': {
                'scale_type': 'chromatic',
                'chord_progression': ['I', 'bII', 'V', 'i'],
                'rhythm_patterns': [
                    [0.125, 0.25, 0.125, 0.5],
                    [0.25, 0.125, 0.125, 0.25, 0.25],
                ],
                'velocity_range': (60, 120),
                'octave_range': (-1, 2),
                'note_density': 'high'
            },
            'epic': {
                'scale_type': 'minor',
                'chord_progression': ['i', 'VI', 'III', 'VII'],
                'rhythm_patterns': [
                    [0.5, 0.25, 0.25],
                    [0.25, 0.25, 0.5],
                ],
                'velocity_range': (80, 120),
                'octave_range': (0, 2),
                'note_density': 'high'
            },
            'melancholic': {
                'scale_type': 'minor',
                'chord_progression': ['i', 'iv', 'VI', 'v'],
                'rhythm_patterns': [
                    [0.75, 0.25],
                    [0.5, 0.5],
                ],
                'velocity_range': (45, 75),
                'octave_range': (0, 1),
                'note_density': 'medium'
            }
        }
    
    def get_scale_notes(self, key: str, scale_type: str) -> List[int]:
        """Get MIDI pitches for a scale"""
        try:
            key_pitch = pitch.Pitch(key)
            
            if scale_type == 'major':
                s = scale.MajorScale(key_pitch)
            elif scale_type == 'minor':
                s = scale.MinorScale(key_pitch)
            elif scale_type == 'chromatic':
                s = scale.ChromaticScale(key_pitch)
            else:
                s = scale.MajorScale(key_pitch)
            
            # Get 3 octaves of the scale
            pitches = []
            for octave in range(-1, 3):
                for p in s.pitches:
                    midi = p.midi + (octave * 12)
                    if 21 <= midi <= 108:  # Piano range
                        pitches.append(midi)
            
            return sorted(list(set(pitches)))
        
        except Exception as e:
            logger.error(f"Error getting scale: {e}")
            # Fallback to C major
            return [60, 62, 64, 65, 67, 69, 71, 72]
    
    def create_arpeggio_from_intervals(
        self,
        key: str,
        mood: str,
        intervals: List[int],
        num_bars: int,
        bpm: int
    ) -> List[Dict]:
        """
        Create arpeggio notes from interval pattern
        
        Args:
            key: Musical key
            mood: Mood configuration
            intervals: List of scale degree intervals
            num_bars: Number of bars
            bpm: Tempo
            
        Returns:
            List of note dictionaries
        """
        config = self.mood_configs.get(mood, self.mood_configs['happy'])
        
        # Get scale
        scale_notes = self.get_scale_notes(key, config['scale_type'])
        root_midi = self._key_to_midi(key)
        
        # Calculate notes per bar based on mood
        notes_per_bar = self._get_notes_per_bar(config['note_density'])
        total_notes = notes_per_bar * num_bars
        
        # Get rhythm pattern
        rhythm_pattern = random.choice(config['rhythm_patterns'])
        
        # Generate notes
        notes = []
        current_time = 0.0
        
        for i in range(total_notes):
            # Get interval (loop if necessary)
            interval = intervals[i % len(intervals)]
            
            # Get pitch from scale
            scale_index = interval % len(scale_notes)
            base_pitch = scale_notes[scale_index]
            
            # Add octave variation based on mood
            octave_offset = random.randint(*config['octave_range']) * 12
            pitch = base_pitch + octave_offset
            
            # Clamp to valid MIDI range
            pitch = max(21, min(108, pitch))
            
            # Get duration
            duration = rhythm_pattern[i % len(rhythm_pattern)]
            
            # Get velocity
            velocity = random.randint(*config['velocity_range'])
            
            notes.append({
                'pitch': pitch,
                'start': current_time,
                'end': current_time + duration,
                'velocity': velocity
            })
            
            current_time += duration
        
        return notes
    
    def create_pattern_from_style(
        self,
        style: str,
        key: str,
        mood: str,
        num_bars: int
    ) -> List[int]:
        """
        Create interval pattern based on style
        
        Args:
            style: Pattern style (ascending, descending, etc.)
            key: Musical key
            mood: Mood
            num_bars: Number of bars
            
        Returns:
            List of intervals
        """
        config = self.mood_configs.get(mood, self.mood_configs['happy'])
        notes_per_bar = self._get_notes_per_bar(config['note_density'])
        total_notes = notes_per_bar * num_bars
        
        if style == 'ascending':
            # Simple ascending pattern
            return [i % 8 for i in range(total_notes)]
        
        elif style == 'descending':
            # Simple descending pattern
            return [7 - (i % 8) for i in range(total_notes)]
        
        elif style == 'alternating':
            # Up and down
            pattern = []
            ascending = True
            for i in range(total_notes):
                if ascending:
                    pattern.append(i % 8)
                else:
                    pattern.append(7 - (i % 8))
                if (i + 1) % 8 == 0:
                    ascending = not ascending
            return pattern
        
        elif style == 'random':
            # Random intervals
            return [random.randint(0, 7) for _ in range(total_notes)]
        
        else:
            # Default ascending
            return [i % 8 for i in range(total_notes)]
    
    def _get_notes_per_bar(self, density: str) -> int:
        """Get number of notes per bar based on density"""
        density_map = {
            'very_low': 2,
            'low': 4,
            'medium': 8,
            'high': 16,
            'very_high': 32
        }
        return density_map.get(density, 8)
    
    def _key_to_midi(self, key: str) -> int:
        """Convert key name to MIDI pitch (middle octave)"""
        key_map = {
            'C': 60, 'C#': 61, 'Db': 61,
            'D': 62, 'D#': 63, 'Eb': 63,
            'E': 64,
            'F': 65, 'F#': 66, 'Gb': 66,
            'G': 67, 'G#': 68, 'Ab': 68,
            'A': 69, 'A#': 70, 'Bb': 70,
            'B': 71
        }
        return key_map.get(key, 60)
    
    def get_mood_description(self, mood: str, intervals: List[int]) -> str:
        """Generate description of the pattern"""
        config = self.mood_configs.get(mood, self.mood_configs['happy'])
        
        pattern_movement = self._analyze_pattern_movement(intervals)
        
        return f"{mood.capitalize()} {config['scale_type']} arpeggio with {pattern_movement} movement"
    
    def _analyze_pattern_movement(self, intervals: List[int]) -> str:
        """Analyze the general movement of the pattern"""
        if len(intervals) < 2:
            return "static"
        
        ascending = sum(1 for i in range(len(intervals)-1) if intervals[i+1] > intervals[i])
        descending = sum(1 for i in range(len(intervals)-1) if intervals[i+1] < intervals[i])
        
        if ascending > descending * 1.5:
            return "ascending"
        elif descending > ascending * 1.5:
            return "descending"
        else:
            return "alternating"