# Voice Interface System for Multilingual Agricultural AI
# Handles speech-to-text and text-to-speech for Hindi, Punjabi, and English

import os
import logging
import tempfile
import asyncio
from typing import Dict, Any, Optional, List
from pathlib import Path
import base64
import json

logger = logging.getLogger(__name__)

class VoiceInterface:
    """
    Multilingual voice interface for agricultural AI
    Supports Hindi, Punjabi, and English voice processing
    """
    
    def __init__(self):
        self.supported_languages = {
            "en": {
                "name": "English",
                "speech_code": "en-US",
                "voice_id": "en-US-AriaNeural"
            },
            "hi": {
                "name": "Hindi",
                "speech_code": "hi-IN", 
                "voice_id": "hi-IN-SwaraNeural"
            },
            "pa": {
                "name": "Punjabi",
                "speech_code": "pa-IN",
                "voice_id": "pa-IN-GurpreetNeural"
            }
        }
        
        # Initialize speech recognition and synthesis
        self.speech_recognition_available = self._check_speech_recognition()
        self.text_to_speech_available = self._check_text_to_speech()
        
    def _check_speech_recognition(self) -> bool:
        """Check if speech recognition dependencies are available"""
        try:
            import speech_recognition as sr
            return True
        except ImportError:
            logger.warning("speech_recognition not available. Install with: pip install SpeechRecognition")
            return False
    
    def _check_text_to_speech(self) -> bool:
        """Check if text-to-speech dependencies are available"""
        try:
            import pyttsx3
            return True
        except ImportError:
            logger.warning("pyttsx3 not available. Install with: pip install pyttsx3")
            return False
    
    def detect_language_from_audio(self, audio_data: bytes) -> str:
        """
        Detect language from audio data
        For now, returns default language. In production, use language detection AI
        """
        # Simple heuristic - in production, use proper language detection
        # For demo purposes, we'll default to Hindi as it's most common for Indian farmers
        return "hi"
    
    async def speech_to_text(self, audio_file_path: str, language: Optional[str] = None) -> Dict[str, Any]:
        """
        Convert speech to text with language detection
        """
        if not self.speech_recognition_available:
            return {
                "success": False,
                "error": "Speech recognition not available",
                "text": "",
                "language": "en",
                "confidence": 0.0
            }
        
        try:
            import speech_recognition as sr
            
            # Initialize recognizer
            recognizer = sr.Recognizer()
            
            # Load audio file
            with sr.AudioFile(audio_file_path) as source:
                # Adjust for ambient noise
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                # Record the audio
                audio_data = recognizer.listen(source)
            
            # Detect language if not provided
            if not language:
                language = self.detect_language_from_audio(audio_data.get_wav_data())
            
            # Ensure language is supported
            if language not in self.supported_languages:
                language = "en"  # Fallback to English
            
            speech_code = self.supported_languages[language]["speech_code"]
            
            # Perform speech recognition
            try:
                # Try Google Speech Recognition (free tier)
                text = recognizer.recognize_google(audio_data, language=speech_code)
                confidence = 0.85  # Google doesn't provide confidence, estimate high
                
            except sr.RequestError:
                # Fallback to offline recognition if available
                try:
                    text = recognizer.recognize_sphinx(audio_data, language=speech_code)
                    confidence = 0.70  # Lower confidence for offline
                except:
                    # Final fallback - return error
                    return {
                        "success": False,
                        "error": "Speech recognition service unavailable",
                        "text": "",
                        "language": language,
                        "confidence": 0.0
                    }
            
            except sr.UnknownValueError:
                return {
                    "success": False,
                    "error": "Could not understand audio",
                    "text": "",
                    "language": language,
                    "confidence": 0.0
                }
            
            # Post-process text for agricultural context
            processed_text = self._post_process_agricultural_text(text, language)
            
            return {
                "success": True,
                "text": processed_text,
                "original_text": text,
                "language": language,
                "confidence": confidence,
                "processing_time": "< 1s"  # Placeholder
            }
            
        except Exception as e:
            logger.error(f"Speech-to-text error: {e}")
            return {
                "success": False,
                "error": str(e),
                "text": "",
                "language": language or "en",
                "confidence": 0.0
            }
    
    def _post_process_agricultural_text(self, text: str, language: str) -> str:
        """
        Post-process recognized text for agricultural context
        Fix common agricultural terms and spellings
        """
        # Agricultural term corrections for each language
        corrections = {
            "en": {
                "wheat": ["weed", "week", "wheat"],
                "rice": ["rise", "race", "rice"],
                "cotton": ["cotton", "cotten", "coton"],
                "fertilizer": ["fertiliser", "fertilizer"],
                "pesticide": ["pesticide", "pestacide"],
                "irrigation": ["irrigation", "irriation"]
            },
            "hi": {
                "गेहूं": ["गेहु", "गेहूं", "गहूं"],
                "चावल": ["चावल", "चाबल"],
                "कपास": ["कपास", "कापास"],
                "खाद": ["खाद", "खाध"],
                "सिंचाई": ["सिंचाई", "सिचाई"]
            },
            "pa": {
                "ਕਣਕ": ["ਕਣਕ", "ਕਨਕ"],
                "ਚਾਵਲ": ["ਚਾਵਲ", "ਚਾਬਲ"],
                "ਕਪਾਹ": ["ਕਪਾਹ", "ਕਪਾਸ"]
            }
        }
        
        if language in corrections:
            for correct_term, variations in corrections[language].items():
                for variation in variations:
                    text = text.replace(variation, correct_term)
        
        return text.strip()
    
    async def text_to_speech(self, text: str, language: str = "en", voice_speed: float = 1.0) -> Dict[str, Any]:
        """
        Convert text to speech in specified language
        """
        if not self.text_to_speech_available:
            return {
                "success": False,
                "error": "Text-to-speech not available",
                "audio_file": None,
                "duration": 0
            }
        
        try:
            import pyttsx3
            
            # Initialize TTS engine
            engine = pyttsx3.init()
            
            # Configure voice settings
            if language in self.supported_languages:
                voice_id = self.supported_languages[language]["voice_id"]
                
                # Try to set the voice (may not be available on all systems)
                voices = engine.getProperty('voices')
                for voice in voices:
                    if language in voice.id.lower() or self.supported_languages[language]["speech_code"].lower() in voice.id.lower():
                        engine.setProperty('voice', voice.id)
                        break
            
            # Set speech rate
            rate = engine.getProperty('rate')
            engine.setProperty('rate', int(rate * voice_speed))
            
            # Generate unique filename
            temp_dir = tempfile.gettempdir()
            audio_filename = f"tts_{language}_{hash(text) % 10000}.wav"
            audio_path = os.path.join(temp_dir, audio_filename)
            
            # Save to file
            engine.save_to_file(text, audio_path)
            engine.runAndWait()
            
            # Check if file was created
            if os.path.exists(audio_path):
                # Get file size for duration estimation
                file_size = os.path.getsize(audio_path)
                estimated_duration = max(len(text) * 0.1, 1.0)  # Rough estimate
                
                return {
                    "success": True,
                    "audio_file": audio_path,
                    "duration": estimated_duration,
                    "language": language,
                    "text_length": len(text),
                    "file_size": file_size
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to generate audio file",
                    "audio_file": None,
                    "duration": 0
                }
                
        except Exception as e:
            logger.error(f"Text-to-speech error: {e}")
            return {
                "success": False,
                "error": str(e),
                "audio_file": None,
                "duration": 0
            }
    
    async def process_voice_query(self, audio_file_path: str, language: Optional[str] = None) -> Dict[str, Any]:
        """
        Complete voice processing pipeline: audio -> text -> language detection
        """
        # Step 1: Convert speech to text
        stt_result = await self.speech_to_text(audio_file_path, language)
        
        if not stt_result["success"]:
            return {
                "success": False,
                "error": stt_result["error"],
                "text": "",
                "language": language or "en",
                "confidence": 0.0,
                "processing_steps": ["speech_to_text_failed"]
            }
        
        # Step 2: Validate and enhance the text
        text = stt_result["text"]
        detected_language = stt_result["language"]
        
        # Step 3: Agricultural context validation
        is_agricultural = self._validate_agricultural_context(text, detected_language)
        
        return {
            "success": True,
            "text": text,
            "original_text": stt_result.get("original_text", text),
            "language": detected_language,
            "confidence": stt_result["confidence"],
            "is_agricultural": is_agricultural,
            "processing_steps": ["speech_to_text", "language_detection", "agricultural_validation"],
            "ready_for_ai": True
        }
    
    def _validate_agricultural_context(self, text: str, language: str) -> bool:
        """
        Check if the text contains agricultural context
        """
        agricultural_keywords = {
            "en": ["crop", "farm", "soil", "plant", "harvest", "seed", "fertilizer", "pesticide", 
                   "irrigation", "wheat", "rice", "cotton", "maize", "weather", "rain", "mandi", "price"],
            "hi": ["फसल", "खेत", "मिट्टी", "पौधा", "बीज", "खाद", "सिंचाई", "गेहूं", "चावल", 
                   "कपास", "मक्का", "मौसम", "बारिश", "मंडी", "भाव"],
            "pa": ["ਫਸਲ", "ਖੇਤ", "ਮਿੱਟੀ", "ਪੌਧਾ", "ਬੀਜ", "ਖਾਦ", "ਸਿੰਚਾਈ", "ਕਣਕ", 
                   "ਚਾਵਲ", "ਕਪਾਹ", "ਮੱਕੀ", "ਮੌਸਮ", "ਮੀਂਹ", "ਮੰਡੀ"]
        }
        
        keywords = agricultural_keywords.get(language, agricultural_keywords["en"])
        text_lower = text.lower()
        
        return any(keyword.lower() in text_lower for keyword in keywords)
    
    def get_voice_capabilities(self) -> Dict[str, Any]:
        """
        Return current voice processing capabilities
        """
        return {
            "speech_to_text": self.speech_recognition_available,
            "text_to_speech": self.text_to_speech_available,
            "supported_languages": list(self.supported_languages.keys()),
            "language_details": self.supported_languages,
            "features": {
                "language_detection": True,
                "agricultural_context_validation": True,
                "noise_reduction": self.speech_recognition_available,
                "voice_speed_control": self.text_to_speech_available
            }
        }
    
    async def create_voice_response(self, text_response: str, language: str = "en") -> Dict[str, Any]:
        """
        Create a complete voice response from text
        """
        # Generate audio response
        tts_result = await self.text_to_speech(text_response, language)
        
        if tts_result["success"]:
            return {
                "success": True,
                "text": text_response,
                "audio_file": tts_result["audio_file"],
                "language": language,
                "duration": tts_result["duration"],
                "ready_for_playback": True
            }
        else:
            return {
                "success": False,
                "error": tts_result["error"],
                "text": text_response,
                "audio_file": None,
                "language": language,
                "ready_for_playback": False
            }