from .music_theory_engine import MusicTheoryEngine
from .pattern_generator import PatternGenerator
from .midi_processor import MidiProcessor
import pretty_midi
from typing import Optional, Tuple, List, Dict
import logging

logger = logging.getLogger(__name__)


class HybridMusicGenerator:
    """
    Compound AI system combining:
    1. GPT-2 for creative pattern generation
    2. Music theory engine for validation
    3. MIDI processor for output
    """
    
    def __init__(self):
        logger.info("Initializing Hybrid Music Generator")
        
        self.music_theory = MusicTheoryEngine()
        self.pattern_gen = PatternGenerator()
        self.midi_processor = MidiProcessor()
        
        logger.info("Hybrid Music Generator initialized successfully")
    
    def generate_arpeggio(
        self,
        key: str = 'C',
        mood: str = 'happy',
        bpm: int = 120,
        num_bars: int = 2,
        pattern_style: str = 'ai-generated',
        seed: Optional[int] = None
    ) -> Tuple[pretty_midi.PrettyMIDI, str]:
        """
        Generate complete arpeggio
        
        Returns:
            Tuple of (MIDI object, pattern description)
        """
        
        if seed is not None:
            import random
            import numpy as np
            import torch
            random.seed(seed)
            np.random.seed(seed)
            torch.manual_seed(seed)
        
        logger.info(f"Generating arpeggio: key={key}, mood={mood}, bpm={bpm}, bars={num_bars}, style={pattern_style}")
        
        # Step 1: Generate or select interval pattern
        if pattern_style == 'ai-generated':
            intervals = self._generate_ai_pattern(key, mood, num_bars)
        else:
            intervals = self.music_theory.create_pattern_from_style(
                style=pattern_style,
                key=key,
                mood=mood,
                num_bars=num_bars
            )
        
        logger.info(f"Generated interval pattern: {intervals[:16]}...")
        
        # Step 2: Convert intervals to actual notes using music theory
        notes = self.music_theory.create_arpeggio_from_intervals(
            key=key,
            mood=mood,
            intervals=intervals,
            num_bars=num_bars,
            bpm=bpm
        )
        
        logger.info(f"Created {len(notes)} notes")
        
        # Step 3: Convert to MIDI
        midi = self.midi_processor.notes_to_midi(
            notes=notes,
            bpm=bpm
        )
        
        # Generate description
        description = self.music_theory.get_mood_description(mood, intervals)
        
        logger.info(f"Successfully generated arpeggio: {description}")
        
        return midi, description
    
    def _generate_ai_pattern(self, key: str, mood: str, num_bars: int) -> List[int]:
        """Generate pattern using AI"""
        
        # Calculate target number of notes
        config = self.music_theory.mood_configs.get(mood, self.music_theory.mood_configs['happy'])
        notes_per_bar = self.music_theory._get_notes_per_bar(config['note_density'])
        num_notes = notes_per_bar * num_bars
        
        # Generate using GPT-2
        intervals = self.pattern_gen.generate_interval_pattern(
            key=key,
            mood=mood,
            num_notes=num_notes,
            temperature=0.8
        )
        
        return intervals
    
    def get_available_moods(self) -> List[str]:
        """Get list of available moods"""
        return list(self.music_theory.mood_configs.keys())