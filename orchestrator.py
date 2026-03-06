"""
Orchestrator
Main orchestration logic for the Music Creator Agent
"""

from typing import Dict, Any, Optional
import yaml

from agents import AgentFactory
from utils import (
    print_header,
    print_section,
    print_success,
    print_info,
    save_output,
    create_suno_file,
    validate_config
)


class MusicCreatorOrchestrator:
    """Orchestrates the music creation workflow across multiple agents"""
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize orchestrator
        
        Args:
            config_path: Path to configuration file
        """
        # Load and validate configuration
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        validate_config(self.config)
        
        # Create agents
        self.agents = AgentFactory.create_agents(config_path)
        
        # Storage for intermediate results
        self.results = {}
    
    def run(
        self,
        user_input: Optional[str] = None,
        genre_params: Optional[Dict[str, Any]] = None,
        tone_params: Optional[Dict[str, Any]] = None,
        lyrics_params: Optional[Dict[str, Any]] = None,
        suno_params: Optional[Dict[str, Any]] = None,
        save_to_file: bool = True
    ) -> Dict[str, str]:
        """
        Run the complete music creation workflow
        
        Args:
            user_input: Optional user input for genre creation
            genre_params: Additional parameters for genre creator
            tone_params: Additional parameters for tone/BPM creator
            lyrics_params: Additional parameters for lyrics creator
            suno_params: Additional parameters for Suno prompt creator
            save_to_file: Whether to save results to file
            
        Returns:
            Dictionary containing all results
        """
        print_header("🎵 MUSIC CREATOR AGENT 🎵")
        
        # Initialize parameter dictionaries
        genre_params = genre_params or {}
        tone_params = tone_params or {}
        lyrics_params = lyrics_params or {}
        suno_params = suno_params or {}
        
        # Step 1: Generate Genre
        print_info("Step 1/4: Generating genre idea...")
        genre_info = self._run_genre_creator(user_input, genre_params)
        self.results["genre"] = genre_info
        print_section("Genre Created", genre_info)
        print_success("Genre creation complete!")
        
        # Step 2: Generate Tone and BPM
        print_info("Step 2/4: Determining tone and BPM...")
        tone_bpm_info = self._run_tone_bpm_creator(genre_info, tone_params)
        self.results["tone_bpm"] = tone_bpm_info
        print_section("Tone & BPM", tone_bpm_info)
        print_success("Tone and BPM determined!")
        
        # Step 3: Generate Lyrics
        print_info("Step 3/4: Creating lyrics...")
        lyrics = self._run_lyrics_creator(genre_info, tone_bpm_info, lyrics_params)
        self.results["lyrics"] = lyrics
        print_section("Lyrics", lyrics)
        print_success("Lyrics created!")
        
        # Step 4: Generate Suno Prompt
        print_info("Step 4/4: Creating Suno AI prompt...")
        suno_prompt = self._run_suno_prompt_creator(
            genre_info,
            tone_bpm_info,
            lyrics,
            suno_params
        )
        self.results["suno_prompt"] = suno_prompt
        print_section("Suno AI Prompt", suno_prompt)
        print_success("Suno prompt created!")
        
        # Save results if configured
        if save_to_file and self.config["output"].get("save_to_file", True):
            self._save_results()
        
        print_header("✨ WORKFLOW COMPLETE ✨")
        
        return self.results
    
    def _run_genre_creator(
        self,
        user_input: Optional[str],
        params: Dict[str, Any]
    ) -> str:
        """Run genre creator agent"""
        agent = self.agents["genre_creator"]
        return agent.create_genre(
            user_input=user_input,
            mood=params.get("mood"),
            era=params.get("era"),
            constraints=params.get("constraints")
        )
    
    def _run_tone_bpm_creator(
        self,
        genre_info: str,
        params: Dict[str, Any]
    ) -> str:
        """Run tone and BPM creator agent"""
        agent = self.agents["tone_bpm_creator"]
        return agent.create_tone_bpm(
            genre_info=genre_info,
            energy_level=params.get("energy_level"),
            time_signature=params.get("time_signature"),
            reference_artists=params.get("reference_artists")
        )
    
    def _run_lyrics_creator(
        self,
        genre_info: str,
        tone_bpm_info: str,
        params: Dict[str, Any]
    ) -> str:
        """Run lyrics creator agent"""
        agent = self.agents["lyrics_creator"]
        return agent.create_lyrics(
            genre_info=genre_info,
            tone_bpm_info=tone_bpm_info,
            theme=params.get("theme"),
            song_length=params.get("song_length"),
            language=params.get("language"),
            style_reference=params.get("style_reference")
        )
    
    def _run_suno_prompt_creator(
        self,
        genre_info: str,
        tone_bpm_info: str,
        lyrics: str,
        params: Dict[str, Any]
    ) -> str:
        """Run Suno prompt creator agent"""
        agent = self.agents["suno_prompt_creator"]
        return agent.create_suno_prompt(
            genre_info=genre_info,
            tone_bpm_info=tone_bpm_info,
            lyrics=lyrics,
            instrumental_intro=params.get("instrumental_intro"),
            instrumental_outro=params.get("instrumental_outro"),
            additional_instructions=params.get("additional_instructions")
        )
    
    def _save_results(self):
        """Save results to files"""
        output_dir = self.config["output"].get("output_dir", "outputs")
        output_format = self.config["output"].get("format", "json")
        
        # Save complete results
        filepath = save_output(self.results, output_dir, output_format)
        print_success(f"Results saved to: {filepath}")
        
        # Save Suno prompt separately
        suno_filepath = create_suno_file(
            self.results["suno_prompt"],
            output_dir
        )
        print_success(f"Suno prompt saved to: {suno_filepath}")
