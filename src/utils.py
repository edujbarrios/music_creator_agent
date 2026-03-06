"""
Utility Functions
Helper functions for the Music Creator Agent
"""

import os
import json
from datetime import datetime
from typing import Dict, Any
from colorama import init, Fore, Style

# Initialize colorama
init()


def print_header(text: str):
    """Print a formatted header"""
    print(f"\n{Fore.CYAN}{'=' * 80}")
    print(f"{text.center(80)}")
    print(f"{'=' * 80}{Style.RESET_ALL}\n")


def print_section(title: str, content: str):
    """Print a formatted section"""
    print(f"{Fore.YELLOW}▶ {title}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{content}{Style.RESET_ALL}\n")


def print_success(message: str):
    """Print a success message"""
    print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")


def print_error(message: str):
    """Print an error message"""
    print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")


def print_info(message: str):
    """Print an info message"""
    print(f"{Fore.BLUE}ℹ {message}{Style.RESET_ALL}")


def save_output(
    data: Dict[str, Any],
    output_dir: str = "outputs",
    format: str = "json"
) -> str:
    """
    Save output data to file
    
    Args:
        data: Data dictionary to save
        output_dir: Directory to save to
        format: Output format (json or txt)
        
    Returns:
        Path to saved file
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate timestamp-based filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if format == "json":
        filename = f"music_creation_{timestamp}.json"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    elif format == "txt":
        filename = f"music_creation_{timestamp}.txt"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("MUSIC CREATOR AGENT - OUTPUT\n")
            f.write("=" * 80 + "\n\n")
            
            for key, value in data.items():
                f.write(f"{key.upper()}\n")
                f.write("-" * 80 + "\n")
                f.write(f"{value}\n\n")
    
    else:
        raise ValueError(f"Unsupported format: {format}")
    
    return filepath


def create_suno_file(suno_prompt: str, output_dir: str = "outputs") -> str:
    """
    Create a separate file for Suno AI prompt
    
    Args:
        suno_prompt: Suno prompt text
        output_dir: Directory to save to
        
    Returns:
        Path to saved file
    """
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"suno_prompt_{timestamp}.txt"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(suno_prompt)
    
    return filepath


def validate_config(config: Dict[str, Any]) -> bool:
    """
    Validate configuration dictionary
    
    Args:
        config: Configuration dictionary
        
    Returns:
        True if valid, raises exception otherwise
    """
    required_keys = ["agents", "prompts", "output"]
    
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required config key: {key}")
    
    required_agents = [
        "genre_creator",
        "tone_bpm_creator",
        "lyrics_creator",
        "suno_prompt_creator"
    ]
    
    for agent in required_agents:
        if agent not in config["agents"]:
            raise ValueError(f"Missing required agent config: {agent}")
    
    return True


def format_agent_params(params: Dict[str, Any]) -> str:
    """
    Format agent parameters for display
    
    Args:
        params: Parameters dictionary
        
    Returns:
        Formatted string
    """
    if not params:
        return "None"
    
    lines = []
    for key, value in params.items():
        if value is not None:
            lines.append(f"  • {key}: {value}")
    
    return "\n".join(lines) if lines else "None"
