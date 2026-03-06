# 🎵 Music Creator Agent

An AI-powered music creation workflow using multiple specialized agents on LLM7.io to generate complete song concepts with Suno AI-ready prompts.

## 🌟 Features

- **Multi-Agent Architecture**: Four specialized agents working in sequence
  - 🎸 **Genre Creator**: Generates unique music genre ideas
  - 🎹 **Tone & BPM Creator**: Determines optimal tone and tempo
  - 📝 **Lyrics Creator**: Writes complete song lyrics
  - 🎼 **Suno Prompt Creator**: Produces structured Suno AI prompts
  
- **Fully Parametrized**: All prompts use Jinja2 templates for flexibility
- **LLM7.io Integration**: Powered by LLM7.io's API
- **Configurable**: YAML-based configuration for easy customization
- **CLI Interface**: Rich command-line interface with colorful output
- **Automatic Saving**: Saves all outputs in JSON and text formats

## 📋 Requirements

- Python 3.8+
- LLM7.io API key
- Dependencies listed in `requirements.txt`

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/edujbarrios/MusicCreatorAgent.git
cd MusicCreatorAgent
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Key

Copy `.env.example` to `.env` and add your LLM7.io API key:

```bash
cp .env.example .env
```

Edit `.env`:
```env
LLM7_API_KEY=your_actual_api_key_here
LLM7_BASE_URL=https://api.llm7.io/v1
```

### 4. Run the Agent

Basic usage:
```bash
python main.py
```

With parameters:
```bash
python main.py --input "Create a chill summer vibe" --mood "relaxed" --theme "sunset beach"
```

## 💡 Usage Examples

### Example 1: Simple Genre Generation
```bash
python main.py --input "electronic dance music with jazz influences"
```

### Example 2: Full Customization
```bash
python main.py \
  --input "nostalgic 90s vibes" \
  --mood "melancholic" \
  --era "90s" \
  --energy "medium" \
  --theme "lost youth" \
  --language "English"
```

### Example 3: With Specific Musical Parameters
```bash
python main.py \
  --mood "energetic" \
  --time-signature "4/4" \
  --reference-artists "Daft Punk, Justice" \
  --theme "futuristic love"
```

## 🎛️ Command Line Options

### General Options
- `--input, -i`: User input to guide genre creation
- `--config`: Path to configuration file (default: config.yaml)
- `--no-save`: Don't save results to file

### Genre Parameters
- `--mood`: Mood for the genre (e.g., 'energetic', 'melancholic')
- `--era`: Musical era (e.g., '80s', '90s', 'modern')
- `--constraints`: Additional constraints for genre creation

### Tone/BPM Parameters
- `--energy`: Energy level ('high', 'medium', 'low')
- `--time-signature`: Time signature (e.g., '4/4', '3/4')
- `--reference-artists`: Comma-separated list of reference artists

### Lyrics Parameters
- `--theme`: Theme for lyrics (e.g., 'love', 'adventure')
- `--song-length`: Song length specification
- `--language`: Language for lyrics (default: English)
- `--style-reference`: Style reference for lyrics

### Suno Parameters
- `--intro`: Instrumental intro description
- `--outro`: Instrumental outro description
- `--suno-instructions`: Additional instructions for Suno

## 📁 Project Structure

```
MusicCreatorAgent/
├── src/
│   ├── __init__.py
│   ├── llm7_client.py       # LLM7.io API client
│   ├── agents.py             # Agent implementations
│   ├── orchestrator.py       # Workflow orchestration
│   └── utils.py              # Utility functions
├── prompts/
│   ├── genre_creator.j2      # Genre creation prompt
│   ├── tone_bpm_creator.j2   # Tone & BPM prompt
│   ├── lyrics_creator.j2     # Lyrics creation prompt
│   └── suno_prompt_creator.j2 # Suno prompt template
├── outputs/                   # Generated outputs (auto-created)
├── config.yaml               # Configuration file
├── requirements.txt          # Python dependencies
├── .env.example             # Example environment file
├── .gitignore               # Git ignore rules
├── main.py                  # Main entry point
├── README.md                # This file
└── LICENSE                  # MIT License

```

## ⚙️ Configuration

Edit `config.yaml` to customize agent behavior:

```yaml
agents:
  genre_creator:
    temperature: 0.8    # Creativity level
    max_tokens: 500     # Response length
  # ... other agents
```

## 🔧 Customizing Prompts

All prompts are Jinja2 templates in the `prompts/` directory. You can modify them to change agent behavior:

- `genre_creator.j2`: Customize genre generation logic
- `tone_bpm_creator.j2`: Adjust tone and BPM determination
- `lyrics_creator.j2`: Modify lyrics creation style
- `suno_prompt_creator.j2`: Change Suno output format

## 📤 Output

The agent generates two types of output files in the `outputs/` directory:

1. **Complete Results**: `music_creation_YYYYMMDD_HHMMSS.json` or `.txt`
   - Contains all intermediate results from each agent

2. **Suno Prompt**: `suno_prompt_YYYYMMDD_HHMMSS.txt`
   - Ready-to-use prompt for Suno AI
   - Copy-paste directly into Suno

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- Powered by [LLM7.io](https://llm7.io)
- Suno AI for music generation capabilities
- OpenAI for the foundational AI models

## 📧 Contact

For questions or support, please open an issue on GitHub.


