"""
Agent Workers
Implements the four specialized agents for music creation
"""

import os
from typing import Dict, Any, Optional
from jinja2 import Environment, FileSystemLoader, Template
import yaml

from MCA.llm7_client import LLM7Client


class BaseAgent:
    """Base class for all agent workers"""
    
    def __init__(
        self,
        name: str,
        client: LLM7Client,
        template_path: str,
        config: Dict[str, Any]
    ):
        """
        Initialize base agent
        
        Args:
            name: Agent name
            client: LLM7Client instance
            template_path: Path to Jinja2 template
            config: Agent configuration dictionary
        """
        self.name = name
        self.client = client
        self.config = config
        self.template = self._load_template(template_path)
    
    def _load_template(self, template_path: str) -> Template:
        """Load Jinja2 template from file"""
        template_dir = os.path.dirname(template_path)
        template_name = os.path.basename(template_path)
        env = Environment(loader=FileSystemLoader(template_dir))
        return env.get_template(template_name)
    
    def render_prompt(self, **kwargs) -> str:
        """Render prompt template with given parameters"""
        return self.template.render(**kwargs)
    
    def execute(self, prompt: str) -> str:
        """
        Execute agent with given prompt.

        If the rendered prompt contains the separator ``=== TASK ===``, the
        text before the **first** occurrence is sent as a ``system`` message
        (role/persona) and the text after it is sent as a ``user`` message
        (task + context).  Only the first occurrence of the separator is used
        for splitting (``maxsplit=1``), so any subsequent ``=== TASK ===``
        text in the task body is preserved as-is in the user message.  This
        split improves instruction-following in most modern LLMs.  When no
        separator is present the entire prompt is sent as a ``user`` message
        for backward compatibility.

        Args:
            prompt: Rendered prompt text

        Returns:
            Agent response text
        """
        separator = "=== TASK ==="
        if separator in prompt:
            system_part, user_part = prompt.split(separator, 1)
            messages = [
                {"role": "system", "content": system_part.strip()},
                {"role": "user", "content": user_part.strip()},
            ]
        else:
            messages = [
                {"role": "user", "content": prompt}
            ]

        response = self.client.chat_completion(
            messages=messages,
            temperature=self.config.get("temperature", 0.7),
            max_tokens=self.config.get("max_tokens", 1000)
        )

        return self.client.get_completion_text(response)


class GenreCreatorAgent(BaseAgent):
    """Agent that creates music genre ideas"""
    
    def create_genre(
        self,
        user_input: Optional[str] = None,
        mood: Optional[str] = None,
        era: Optional[str] = None,
        constraints: Optional[str] = None
    ) -> str:
        """
        Create a music genre idea
        
        Args:
            user_input: Optional user input to guide genre creation
            mood: Optional mood specification
            era: Optional era specification
            constraints: Optional additional constraints
            
        Returns:
            Genre information as text
        """
        prompt = self.render_prompt(
            user_input=user_input,
            mood=mood,
            era=era,
            constraints=constraints
        )
        
        return self.execute(prompt)


class ToneBPMCreatorAgent(BaseAgent):
    """Agent that determines tone and BPM based on genre"""
    
    def create_tone_bpm(
        self,
        genre_info: str,
        energy_level: Optional[str] = None,
        time_signature: Optional[str] = None,
        reference_artists: Optional[str] = None
    ) -> str:
        """
        Create tone and BPM specifications
        
        Args:
            genre_info: Genre information from GenreCreatorAgent
            energy_level: Optional energy level specification
            time_signature: Optional time signature
            reference_artists: Optional reference artists
            
        Returns:
            Tone and BPM information as text
        """
        prompt = self.render_prompt(
            genre_info=genre_info,
            energy_level=energy_level,
            time_signature=time_signature,
            reference_artists=reference_artists
        )
        
        return self.execute(prompt)


class LyricsCreatorAgent(BaseAgent):
    """Agent that generates song lyrics"""
    
    def create_lyrics(
        self,
        genre_info: str,
        tone_bpm_info: str,
        theme: Optional[str] = None,
        song_length: Optional[str] = None,
        language: Optional[str] = None,
        style_reference: Optional[str] = None
    ) -> str:
        """
        Create song lyrics
        
        Args:
            genre_info: Genre information
            tone_bpm_info: Tone and BPM information
            theme: Optional theme for lyrics
            song_length: Optional song length specification
            language: Optional language for lyrics
            style_reference: Optional style reference
            
        Returns:
            Song lyrics as text
        """
        prompt = self.render_prompt(
            genre_info=genre_info,
            tone_bpm_info=tone_bpm_info,
            theme=theme,
            song_length=song_length,
            language=language,
            style_reference=style_reference
        )
        
        return self.execute(prompt)


class SunoPromptCreatorAgent(BaseAgent):
    """Agent that creates structured Suno AI prompts"""
    
    def create_suno_prompt(
        self,
        genre_info: str,
        tone_bpm_info: str,
        lyrics: str,
        instrumental_intro: Optional[str] = None,
        instrumental_outro: Optional[str] = None,
        additional_instructions: Optional[str] = None
    ) -> str:
        """
        Create Suno AI prompt
        
        Args:
            genre_info: Genre information
            tone_bpm_info: Tone and BPM information
            lyrics: Song lyrics
            instrumental_intro: Optional intro description
            instrumental_outro: Optional outro description
            additional_instructions: Optional additional instructions
            
        Returns:
            Structured Suno AI prompt as text
        """
        prompt = self.render_prompt(
            genre_info=genre_info,
            tone_bpm_info=tone_bpm_info,
            lyrics=lyrics,
            instrumental_intro=instrumental_intro,
            instrumental_outro=instrumental_outro,
            additional_instructions=additional_instructions
        )
        
        return self.execute(prompt)


class AgentFactory:
    """Factory for creating agent instances"""
    
    @staticmethod
    def create_agents(config_path: str = "config.yaml") -> Dict[str, BaseAgent]:
        """
        Create all agents from configuration
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            Dictionary mapping agent names to agent instances
        """
        # Load configuration
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Initialize LLM7 client
        client = LLM7Client()
        
        # Get prompts directory
        prompts_dir = config["prompts"]["templates_dir"]
        
        # Create agents
        agents = {
            "genre_creator": GenreCreatorAgent(
                name="Genre Creator",
                client=client,
                template_path=os.path.join(
                    prompts_dir,
                    config["prompts"]["genre_template"]
                ),
                config=config["agents"]["genre_creator"]
            ),
            "tone_bpm_creator": ToneBPMCreatorAgent(
                name="Tone and BPM Creator",
                client=client,
                template_path=os.path.join(
                    prompts_dir,
                    config["prompts"]["tone_bpm_template"]
                ),
                config=config["agents"]["tone_bpm_creator"]
            ),
            "lyrics_creator": LyricsCreatorAgent(
                name="Lyrics Creator",
                client=client,
                template_path=os.path.join(
                    prompts_dir,
                    config["prompts"]["lyrics_template"]
                ),
                config=config["agents"]["lyrics_creator"]
            ),
            "suno_prompt_creator": SunoPromptCreatorAgent(
                name="Suno Prompt Creator",
                client=client,
                template_path=os.path.join(
                    prompts_dir,
                    config["prompts"]["suno_template"]
                ),
                config=config["agents"]["suno_prompt_creator"]
            )
        }
        
        return agents
