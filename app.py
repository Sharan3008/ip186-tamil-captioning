import gradio as gr
import whisper
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import tempfile
import os
import numpy as np

# Load models (will be cached on Hugging Face)
print("Loading Whisper model...")
whisper_model = whisper.load_model("base")

print("Loading Tamil translation models...")
# English -> Tamil
en2ta_tokenizer = AutoTokenizer.from_pretrained("ai4bharat/indictrans2-en-ta")
en2ta_model = AutoModelForSeq2SeqLM.from_pretrained("ai4bharat/indictrans2-en-ta")

# Tamil -> English
ta2en_tokenizer = AutoTokenizer.from_pretrained("ai4bharat/indictrans2-ta-en")
ta2en_model = AutoModelForSeq2SeqLM.from_pretrained("ai4bharat/indictrans2-ta-en")

def translate_to_tamil(text):
    """English to Tamil translation"""
    if not text.strip():
        return ""
    inputs = en2ta_tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=128)
    translated = en2ta_model.generate(**inputs, max_length=128)
    return en2ta_tokenizer.batch_decode(translated, skip_special_tokens=True)[0]

def translate_to_english(text):
    """Tamil to English translation"""
    if not text.strip():
        return ""
    inputs = ta2en_tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=128)
    translated = ta2en_model.generate(**inputs, max_length=128)
    return ta2en_tokenizer.batch_decode(translated, skip_special_tokens=True)[0]

def process_audio(audio, mode):
    """Main function for the app"""
    if audio is None:
        return "Please record audio first", "", "No audio detected"
    
    try:
        # Save audio temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            # Handle different audio formats
            if isinstance(audio, tuple):
                # Gradio sometimes returns (sample_rate, audio_data)
                import soundfile as sf
                sf.write(tmp.name, audio[1], audio[0])
            else:
                # Assume it's a file path
                tmp.write(audio)
            tmp_path = tmp.name
        
        if mode == "Tamil Speech → Tamil Text":
            # Transcribe Tamil
            result = whisper_model.transcribe(tmp_path, language="ta", task="transcribe")
            tamil_text = result["text"]
            english_text = translate_to_english(tamil_text)
            
        else:  # English Speech → Tamil Text
            # Transcribe English
            result = whisper_model.transcribe(tmp_path, language="en", task="transcribe")
            english_text = result["text"]
            tamil_text = translate_to_tamil(english_text)
        
        # Clean up
        os.unlink(tmp_path)
        
        return tamil_text, english_text, "✅ Success!"
        
    except Exception as e:
        return f"Error: {str(e)}", "", "❌ Failed"

# Create the Gradio interface
with gr.Blocks(title="IP Team 186 - Tamil Captioning", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🎯 IP Team 186 - Real-Time Tamil Captioning
    ### பேசுங்கள், தமிழில் வசனங்கள் தோன்றும்
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            # Input section
            audio_input = gr.Audio(
                source="microphone", 
                type="numpy",
                label="🎤 Speak here"
            )
            
            mode_select = gr.Radio(
                choices=[
                    "Tamil Speech → Tamil Text",
                    "English Speech → Tamil Text"
                ],
                label="Select Mode",
                value="Tamil Speech → Tamil Text"
            )
            
            submit_btn = gr.Button("Generate Captions", variant="primary")
            status = gr.Textbox(label="Status", interactive=False)
        
        with gr.Column(scale=2):
            # Output section with Tamil font
            tamil_output = gr.Textbox(
                label="📝 தமிழ் வசனங்கள் (Tamil Captions)",
                lines=6,
                elem_id="tamil-text"
            )
            english_output = gr.Textbox(
                label="English Translation (for reference)",
                lines=3
            )
    
    # Custom CSS for Tamil font
    gr.Markdown("""
    <style>
    #tamil-text textarea {
        font-family: 'Latha', 'Nirmala UI', 'Noto Sans Tamil', sans-serif;
        font-size: 22px;
        line-height: 1.6;
        color: #2c3e50;
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
    }
    .gr-button-primary {
        background-color: #4F46E5 !important;
        border: none;
        color: white;
        font-size: 16px;
        padding: 10px 20px;
        border-radius: 8px;
    }
    .gr-button-primary:hover {
        background-color: #6366F1 !important;
    }
    </style>
    """)
    
    # Connect the button
    submit_btn.click(
        fn=process_audio,
        inputs=[audio_input, mode_select],
        outputs=[tamil_output, english_output, status]
    )
    
    gr.Markdown("""
    ---
    ### 📋 How to Use
    1. Click the microphone and allow permission
    2. Speak in Tamil or English
    3. Click "Generate Captions"
    4. See Tamil captions instantly!
    
    ### 🔜 Coming Soon
    - తెలుగు (Telugu)
    - മലയാളം (Malayalam)
    - Real-time streaming (no button needed)
    
    ---
    **Project PS Number:** IP_PS-223  
    **Team:** Dharanesh, Nethra, Pennanson, Rengha Shree, Sharan.R, Sharan Subramanian
    """)

# Launch the app
demo.launch()
