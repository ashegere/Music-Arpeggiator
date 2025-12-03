from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class ArpeggiatorRequest(BaseModel):
    key: str = Field(
        default='C',
        description="Musical key (C, D, E, F, G, A, B with # or b)",
        pattern="^[A-G](#|b)?$"
    )
    mood: Literal['happy', 'calm', 'energetic', 'dark', 'ambient', 'chaotic', 'epic', 'melancholic'] = Field(
        default='happy',
        description="Mood of the arpeggio"
    )
    bpm: int = Field(
        default=120,
        ge=40,
        le=240,
        description="Tempo in beats per minute"
    )
    num_bars: int = Field(
        default=2,
        ge=1,
        le=8,
        description="Number of bars to generate"
    )
    pattern_style: Literal['ascending', 'descending', 'alternating', 'random', 'ai-generated'] = Field(
        default='ai-generated',
        description="Arpeggio pattern style"
    )
    seed: Optional[int] = Field(
        default=None,
        description="Random seed for reproducibility"
    )


class NoteData(BaseModel):
    pitch: int = Field(description="MIDI pitch number (0-127)")
    start_time: float = Field(description="Start time in seconds")
    end_time: float = Field(description="End time in seconds")
    velocity: int = Field(description="Note velocity (0-127)")


class ArpeggiatorResponse(BaseModel):
    notes: List[NoteData]
    midi_base64: str
    tempo: int
    key: str
    mood: str
    duration: float
    pattern_description: str


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    version: str


class MoodsResponse(BaseModel):
    moods: List[str]
    default: str