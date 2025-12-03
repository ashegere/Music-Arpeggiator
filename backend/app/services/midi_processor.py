import pretty_midi
from typing import List, Dict
import io
import base64
import logging

logger = logging.getLogger(__name__)


class MidiProcessor:
    """
    Handles MIDI file creation and conversion
    """
    
    def __init__(self):
        self.default_instrument = 0  # Acoustic Grand Piano
    
    def notes_to_midi(
        self,
        notes: List[Dict],
        bpm: int,
        instrument_program: int = None
    ) -> pretty_midi.PrettyMIDI:
        """
        Convert note dictionaries to PrettyMIDI object
        
        Args:
            notes: List of note dictionaries with pitch, start, end, velocity
            bpm: Tempo in beats per minute
            instrument_program: MIDI program number (0-127)
            
        Returns:
            PrettyMIDI object
        """
        
        if instrument_program is None:
            instrument_program = self.default_instrument
        
        try:
            # Create MIDI object
            midi = pretty_midi.PrettyMIDI(initial_tempo=bpm)
            
            # Create instrument
            instrument = pretty_midi.Instrument(program=instrument_program)
            
            # Add notes
            for note_data in notes:
                note = pretty_midi.Note(
                    velocity=note_data['velocity'],
                    pitch=note_data['pitch'],
                    start=note_data['start'],
                    end=note_data['end']
                )
                instrument.notes.append(note)
            
            midi.instruments.append(instrument)
            
            return midi
        
        except Exception as e:
            logger.error(f"Error creating MIDI: {e}")
            raise
    
    def midi_to_bytes(self, midi: pretty_midi.PrettyMIDI) -> bytes:
        """Convert PrettyMIDI to bytes"""
        midi_io = io.BytesIO()
        midi.write(midi_io)
        return midi_io.getvalue()
    
    def midi_to_base64(self, midi: pretty_midi.PrettyMIDI) -> str:
        """Convert PrettyMIDI to base64 string"""
        midi_bytes = self.midi_to_bytes(midi)
        return base64.b64encode(midi_bytes).decode('utf-8')
    
    def get_midi_info(self, midi: pretty_midi.PrettyMIDI) -> Dict:
        """Extract information from MIDI"""
        return {
            'duration': midi.get_end_time(),
            'num_notes': sum(len(inst.notes) for inst in midi.instruments),
            'tempo': midi.estimate_tempo()
        }