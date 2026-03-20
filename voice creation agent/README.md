# Voice Creation Agent

Generate speech audio from text with support for different person personas (voice profiles).

## Features

- Convert text to speech using OpenAI TTS
- Multi-person support via persona configs
- Built-in default personas (`narrator`, `teacher`, `podcast_host`, `calm_assistant`, `announcer`)
- Add/remove custom personas and persist them in `personas.json`
- Save generated audio files to `outputs/`
- CLI support for single and batch generation

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt --index-url https://pypi.org/simple/
```

3. Configure environment:
```bash
cp .env-example .env
# Set OPENAI_API_KEY in .env
```

## Usage

### Basic Usage

```python
from main import VoiceCreationAgent

agent = VoiceCreationAgent()
result = agent.create_voice(
    text="Hello team, welcome to this update.",
    person="narrator",
)
agent.print_result(result)
```

### Multi-Person Generation

```python
from main import VoiceCreationAgent

agent = VoiceCreationAgent()
text = "This same script can be spoken by different persons."
for person in ["narrator", "teacher", "podcast_host"]:
    agent.create_voice(text=text, person=person)
```

### Add a Custom Person

```python
from main import VoiceCreationAgent

agent = VoiceCreationAgent()
agent.add_persona(
    name="news_reader",
    voice="echo",
    style_hint="formal and informative news reading tone",
)
agent.create_voice("Top headlines for today.", person="news_reader")
```

## Run Examples

```bash
python main.py --text "Hello from voice agent" --person narrator
python main.py --text "Same text for many" --persons narrator,teacher,podcast_host --filename-prefix demo
python main.py --list-personas
python main.py --add-persona-name news_reader --add-persona-voice echo --add-persona-style "formal news delivery"
python main.py --remove-persona news_reader
python example.py
```

## Notes

- Requires `OPENAI_API_KEY`
- Audio format defaults to `mp3`
- Output files are written into `outputs/`
- You can also use `--text-file path/to/input.txt` for long scripts
