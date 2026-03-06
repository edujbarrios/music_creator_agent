# Music Creator Agent (MCA)

AI-powered music creation using LLM7.io agents to generate Suno AI-ready prompts.

## Features

Four specialized agents working in sequence:
- **Genre Creator** - Creates unique music genre ideas
- **Tone & BPM Creator** - Determines optimal tone and tempo
- **Lyrics Creator** - Writes song lyrics
- **Suno Prompt Creator** - Generates structured Suno AI prompts

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure your LLM7.io API key:
```bash
cp .env.example .env
# Edit .env and add your LLM7_API_KEY
```

3. Run:
```bash
python run.py
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

## Project Structure

```
MusicCreatorAgent/
├── MCA/                   # Main package
│   ├── agents.py          # Agent implementations
│   ├── llm7_client.py     # LLM7.io API client
│   ├── orchestrator.py    # Workflow orchestration
│   ├── utils.py           # Utilities
│   └── MCA.py             # Main logic
├── prompts/               # Jinja2 templates
├── outputs/               # Generated outputs
├── examples/              # Example outputs
├── run.py                 # Entry point
├── config.yaml            # Configuration
└── requirements.txt       # Dependencies
```

## Output

Results saved in `outputs/`:
- `music_creation_*.json` - Complete workflow results
- `suno_prompt_*.txt` - Ready for Suno AI

## Author

**Eduardo J. Barrios**: [@edujbarrios](https://github.com/edujbarrios)

## License

MIT License - See LICENSE file for details




