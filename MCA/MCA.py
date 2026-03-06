"""
Music Creator Agent
Main entry point for the music creation workflow
"""

import argparse
import sys
from typing import Dict, Any

from MCA.orchestrator import MusicCreatorOrchestrator
from MCA.utils import print_error, print_info


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Music Creator Agent - AI-powered music creation workflow"
    )
    
    # Main input
    parser.add_argument(
        "--input",
        "-i",
        type=str,
        help="User input to guide genre creation"
    )
    
    # Genre parameters
    parser.add_argument(
        "--mood",
        type=str,
        help="Mood for the genre (e.g., 'energetic', 'melancholic')"
    )
    parser.add_argument(
        "--era",
        type=str,
        help="Musical era (e.g., '80s', '90s', 'modern')"
    )
    parser.add_argument(
        "--constraints",
        type=str,
        help="Additional constraints for genre creation"
    )
    
    # Tone/BPM parameters
    parser.add_argument(
        "--energy",
        type=str,
        help="Energy level (e.g., 'high', 'medium', 'low')"
    )
    parser.add_argument(
        "--time-signature",
        type=str,
        help="Time signature (e.g., '4/4', '3/4', '6/8')"
    )
    parser.add_argument(
        "--reference-artists",
        type=str,
        help="Reference artists for tone (comma-separated)"
    )
    
    # Lyrics parameters
    parser.add_argument(
        "--theme",
        type=str,
        help="Theme for lyrics (e.g., 'love', 'adventure', 'nostalgia')"
    )
    parser.add_argument(
        "--song-length",
        type=str,
        help="Song length (e.g., 'short (2-3 min)', 'standard (3-4 min)')"
    )
    parser.add_argument(
        "--language",
        type=str,
        default="English",
        help="Language for lyrics (default: English)"
    )
    parser.add_argument(
        "--style-reference",
        type=str,
        help="Style reference for lyrics"
    )
    
    # Suno parameters
    parser.add_argument(
        "--intro",
        type=str,
        help="Instrumental intro description"
    )
    parser.add_argument(
        "--outro",
        type=str,
        help="Instrumental outro description"
    )
    parser.add_argument(
        "--suno-instructions",
        type=str,
        help="Additional instructions for Suno prompt"
    )
    
    # Output options
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Don't save results to file"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config.yaml",
        help="Path to configuration file (default: config.yaml)"
    )
    
    return parser.parse_args()


def build_params(args) -> tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    """Build parameter dictionaries from parsed arguments"""
    
    genre_params = {}
    if args.mood:
        genre_params["mood"] = args.mood
    if args.era:
        genre_params["era"] = args.era
    if args.constraints:
        genre_params["constraints"] = args.constraints
    
    tone_params = {}
    if args.energy:
        tone_params["energy_level"] = args.energy
    if args.time_signature:
        tone_params["time_signature"] = args.time_signature
    if args.reference_artists:
        tone_params["reference_artists"] = args.reference_artists
    
    lyrics_params = {}
    if args.theme:
        lyrics_params["theme"] = args.theme
    if args.song_length:
        lyrics_params["song_length"] = args.song_length
    if args.language:
        lyrics_params["language"] = args.language
    if args.style_reference:
        lyrics_params["style_reference"] = args.style_reference
    
    suno_params = {}
    if args.intro:
        suno_params["instrumental_intro"] = args.intro
    if args.outro:
        suno_params["instrumental_outro"] = args.outro
    if args.suno_instructions:
        suno_params["additional_instructions"] = args.suno_instructions
    
    return genre_params, tone_params, lyrics_params, suno_params


def main():
    """Main entry point"""
    try:
        # Parse arguments
        args = parse_arguments()
        
        # Build parameter dictionaries
        genre_params, tone_params, lyrics_params, suno_params = build_params(args)
        
        # Create orchestrator
        orchestrator = MusicCreatorOrchestrator(config_path=args.config)
        
        # Run workflow
        results = orchestrator.run(
            user_input=args.input,
            genre_params=genre_params,
            tone_params=tone_params,
            lyrics_params=lyrics_params,
            suno_params=suno_params,
            save_to_file=not args.no_save
        )
        
        return 0
        
    except KeyboardInterrupt:
        print_info("\nWorkflow interrupted by user")
        return 130
    
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
