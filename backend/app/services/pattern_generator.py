from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
from typing import List
import logging
import re

logger = logging.getLogger(__name__)


class PatternGenerator:
    """
    Uses GPT-2 to generate creative interval patterns
    """
    
    def __init__(self, model_name: str = "gpt2"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Loading pattern generator on {self.device}")
        
        try:
            self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
            self.model = GPT2LMHeadModel.from_pretrained(model_name)
            self.model.to(self.device)
            self.model.eval()
            
            # Set pad token
            self.tokenizer.pad_token = self.tokenizer.eos_token
            
            logger.info("Pattern generator loaded successfully")
        except Exception as e:
            logger.error(f"Error loading pattern generator: {e}")
            raise
    
    def generate_interval_pattern(
        self,
        key: str,
        mood: str,
        num_notes: int,
        temperature: float = 0.8
    ) -> List[int]:
        """
        Generate creative interval pattern using GPT-2
        
        Args:
            key: Musical key
            mood: Mood descriptor
            num_notes: Target number of intervals
            temperature: Sampling temperature
            
        Returns:
            List of interval integers (0-7 for scale degrees)
        """
        
        # Create prompt for pattern generation
        prompt = self._create_prompt(key, mood, num_notes)
        
        try:
            # Generate text
            generated_text = self._generate_text(prompt, temperature)
            
            # Extract intervals from generated text
            intervals = self._extract_intervals(generated_text, num_notes)
            
            # Fallback if extraction failed
            if not intervals or len(intervals) < num_notes // 2:
                logger.warning("Pattern extraction failed, using fallback")
                intervals = self._fallback_pattern(mood, num_notes)
            
            return intervals
        
        except Exception as e:
            logger.error(f"Error generating pattern: {e}")
            return self._fallback_pattern(mood, num_notes)
    
    def _create_prompt(self, key: str, mood: str, num_notes: int) -> str:
        """Create prompt for GPT-2"""
        
        mood_descriptions = {
            'happy': 'uplifting, bright, and joyful',
            'calm': 'peaceful, serene, and gentle',
            'energetic': 'dynamic, powerful, and exciting',
            'dark': 'mysterious, somber, and intense',
            'ambient': 'atmospheric, spacious, and ethereal',
            'chaotic': 'unpredictable, wild, and intense',
            'epic': 'grand, heroic, and dramatic',
            'melancholic': 'sad, reflective, and emotional'
        }
        
        description = mood_descriptions.get(mood, 'musical')
        
        prompt = f"""Music composition in {key} with {description} character.
Arpeggio pattern: """
        
        return prompt
    
    def _generate_text(self, prompt: str, temperature: float) -> str:
        """Generate text using GPT-2"""
        
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            padding=True,
            truncation=True
        ).to(self.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=150,
                temperature=temperature,
                top_k=50,
                top_p=0.95,
                do_sample=True,
                num_return_sequences=1,
                pad_token_id=self.tokenizer.pad_token_id
            )
        
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return generated_text
    
    def _extract_intervals(self, text: str, num_notes: int) -> List[int]:
        """
        Extract musical intervals from generated text
        Uses heuristics to find number-like patterns
        """
        
        # Look for comma-separated numbers
        pattern = r'\d+'
        matches = re.findall(pattern, text)
        
        if matches:
            # Convert to integers and constrain to valid scale degrees
            intervals = [int(m) % 8 for m in matches[:num_notes]]
            
            # Pad if needed
            while len(intervals) < num_notes:
                intervals.extend(intervals[:num_notes - len(intervals)])
            
            return intervals[:num_notes]
        
        # Try to extract from character positions (creative fallback)
        intervals = []
        for char in text[len(text)//2:]:  # Use second half of text
            if char.isdigit():
                intervals.append(int(char) % 8)
            elif char.isalpha():
                # Use character position as interval
                intervals.append(ord(char.lower()) % 8)
            
            if len(intervals) >= num_notes:
                break
        
        return intervals[:num_notes] if intervals else []
    
    def _fallback_pattern(self, mood: str, num_notes: int) -> List[int]:
        """
        Fallback patterns when AI generation fails
        """
        
        patterns = {
            'happy': [0, 2, 4, 7, 4, 2],
            'calm': [0, 2, 4, 2, 0],
            'energetic': [0, 4, 7, 12, 7, 4, 0, -5],
            'dark': [0, 3, 5, 7, 5, 3],
            'ambient': [0, 4, 7, 11, 7, 4],
            'chaotic': [0, 6, 2, 7, 1, 5, 3, 4],
            'epic': [0, 3, 7, 10, 7, 3],
            'melancholic': [0, 3, 5, 8, 5, 3]
        }
        
        base_pattern = patterns.get(mood, [0, 2, 4, 5, 7])
        
        # Repeat and extend pattern to match num_notes
        intervals = []
        while len(intervals) < num_notes:
            intervals.extend(base_pattern)
        
        return intervals[:num_notes]