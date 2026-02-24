# 🎯 IP Team 186 - Real-Time Tamil Captioning System

## Project PS Number: IP_PS-223

### Team Members
- Dharanesh.V (24BME406)
- Nethra. S. K (24BEI044)
- Pennanson jebamani.P (24BBT046)
- Rengha shree.R (24BEC139)
- Sharan.R (24BIT111)
- Sharan Subramanian.P (24BCS260)

## Features
- 🎤 **Tamil Speech → Tamil Text** - Speak in Tamil, get Tamil captions
- 🔊 **English Speech → Tamil Text** - Speak in English, get Tamil captions
- 📝 **Bilingual Display** - Shows both Tamil and English for reference
- 🎯 **Real-time Processing** - Instant caption generation
- 💯 **100% Free** - Built with open-source tools

## How It Works
1. **Speech Recognition**: OpenAI Whisper (trained on 96+ languages including Tamil)
2. **Translation**: AI4Bharat IndicTrans2 (developed by IIT Madras)
3. **Interface**: Gradio web app
4. **Deployment**: Ready for Hugging Face Spaces

## Tech Stack
| Component | Technology |
|-----------|------------|
| Frontend | Gradio |
| Speech-to-Text | OpenAI Whisper |
| Translation | IndicTrans2 (AI4Bharat) |
| Backend | Python, PyTorch |
| Hosting | GitHub, Hugging Face |

## Setup Instructions
1. Clone this repository
2. Install requirements: `pip install -r requirements.txt`
3. Run: `python app.py`
4. Open browser at `http://localhost:7860`

## Future Expansion
- 🇮🇳 Telugu (తెలుగు)
- 🇮🇳 Malayalam (മലയാളം)
- 🇮🇳 Kannada (ಕನ್ನಡ)
- 🇮🇳 Hindi (हिंदी)

## License
MIT
