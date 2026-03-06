# Music Creator Agent (MCA)

AI-powered music creation using LLM7.io agents to generate Suno AI-ready prompts.

> [!CAUTION]
> **This software is designed for research purposes and requires substantial knowledge of both music theory and AI prompt engineering.** The purpose of this tool is to investigate the limits of AI-assisted music creation through **guided prompt engineering**. 
>
> **If you use this software without musical knowledge** or simply copy the examples from this guide literally, **the results will be very poor**. This tool is meant for **musicians, producers, and AI researchers** who understand:
> - Music theory, composition, and production concepts
> - How to craft effective prompts for AI systems
> - The iterative nature of creative AI applications
>
> **This is NOT a "push-button" solution** for instant music creation. Quality results require expertise, experimentation, and creative refinement.

## Features

Four specialized agents working in sequence:
- **Genre Creator** - Creates unique music genre ideas
- **Tone & BPM Creator** - Determines optimal tone and tempo
- **Lyrics Creator** - Writes song lyrics
- **Suno Prompt Creator** - Generates structured Suno AI prompts

## Setup

0. Clone the repo
```bash
git clone https://github.com/edujbarrios/music_creator_agent.git
cd music_creator_agent
```

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure your LLM7.io API key:
```bash
cp .env.example .env
# Edit .env and add your LLM7_API_KEY
# Set DEFAULT_MODEL to an available model (e.g., gpt-3.5-turbo, gpt-4, claude-3-sonnet)
```

3. Run:
```bash
python run.py # This creates a randomg music and genre idea, see usage for more info
```

## Usage

Basic:
```bash
python run.py --input "chill summer vibes"
```

With options:
```bash
python run.py --input "synthwave" --mood "nostalgic" --theme "sunset drive"
```

## Options

- `--input, -i` - Guide genre creation
- `--mood` - Mood (energetic, melancholic, etc.)
- `--era` - Era (80s, 90s, modern, etc.)
- `--theme` - Lyrics theme
- `--energy` - Energy level (high, medium, low)
- `--language` - Language (default: English)


## Output

Results of working agents will be saved in `outputs/`:
- `music_creation_*.json` - Complete workflow results
- `suno_prompt_*.txt` - Ready for Suno AI


# Contributions

Contributions and improvements are welcome! feel free to fork this repo and submit pull requests.

## Author

**Eduardo J. Barrios**: [@edujbarrios](https://github.com/edujbarrios)





