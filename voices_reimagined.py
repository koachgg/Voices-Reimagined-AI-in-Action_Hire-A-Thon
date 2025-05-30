# -*- coding: utf-8 -*-
"""Voices_Reimagined.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/14YPCjdfTFVwUrtAXO_4Myic8kw5bNSDs

# Voices Reimagined : AI in Action
### *Team DUCS*

## This notebook implements a comprehensive speech processing pipeline with:

- Speech Recognition
- Speaker Diarization
- Emotion Detection
- Text Summarization
- Interactive Streamlit Interface

## 1. Installation and Setup

#### Install required dependencies and libraries
"""

# Install necessary libraries
!pip install transformers torchaudio pyannote.audio speechbrain
!pip install torch
!pip install tqdm

pip install requests transformers torch torchaudio pyannote.audio speechbrain tqdm

!pip install google-generativeai

pip install streamlit

pip install npx

!npm install localtunnel

pip install gtts

"""## 2. Import Required Libraries"""

# Import required modules
import torch
import torchaudio
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor, pipeline
from pyannote.audio import Pipeline
from speechbrain.pretrained import EncoderClassifier
from tqdm.notebook import tqdm

"""## 3. Initialize Speaker Diarization Pipeline"""

from pyannote.audio import Pipeline
pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1",
                                    use_auth_token="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")

"""## 4. Streamlit Application Configuration

### Creating an interactive web interface for the speech processing pipeline
"""

# Commented out IPython magic to ensure Python compatibility.
# %%writefile app.py
# import streamlit as st
# 
# # Set page configuration - MUST be the first Streamlit command
# st.set_page_config(
#     page_title="Voices Reimagined",
#     layout="wide",
#     page_icon="🎙️",
#     initial_sidebar_state="expanded"
# )
# 
# from io import BytesIO
# import torchaudio
# import torch
# from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
# from pyannote.audio import Pipeline
# from speechbrain.pretrained import EncoderClassifier
# import google.generativeai as genai
# from gtts import gTTS
# from collections import Counter
# import base64
# import plotly.express as px
# import pandas as pd
# 
# 
# 
# # Configure Gemini API
# API_KEY = "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"
# genai.configure(api_key=API_KEY)
# 
# # Custom CSS with enhanced styling
# st.markdown("""
#     <style>
#     /* Main container styling */
#     .main {
#         padding: 2rem;
#     }
# 
#     /* Header styling */
#     .main-title {
#         font-size: 3rem;
#         background: linear-gradient(45deg, #2196F3, #4CAF50);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         text-align: center;
#         padding: 1.5rem 0;
#         font-weight: 800;
#         margin-bottom: 1rem;
#     }
#     .main-quote {
#         font-size: 2rem;
#         background: linear-gradient(45deg, #2196F3, #4CAF50);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         text-align: center;
#         padding: 1.5rem 0;
#         font-weight: 400;
#         margin-bottom: 2rem;
#     }
# 
#     /* Section headers */
#     .section-header {
#         font-size: 1.5rem;
#         color: #1565C0;
#         margin: 1.5rem 0;
#         padding: 0.5rem;
#         border-bottom: 2px solid #1565C0;
#     }
# 
#     /* Cards styling */
#     .stCard {
#         border-radius: 1rem;
#         box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
#         padding: 1.5rem;
#         margin: 1rem 0;
#         background: white;
#     }
# 
#     /* Button styling */
#     .stButton>button {
#         background: linear-gradient(45deg, #2196F3, #4CAF50);
#         color: white;
#         border: none;
#         border-radius: 0.5rem;
#         padding: 0.75rem 1.5rem;
#         font-weight: 600;
#         transition: all 0.3s ease;
#     }
# 
#     .stButton>button:hover {
#         transform: translateY(-2px);
#         box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
#     }
# 
#     /* File uploader styling */
#     .uploadedFile {
#         border: 2px dashed #4CAF50;
#         border-radius: 1rem;
#         padding: 1rem;
#         text-align: center;
#     }
# 
#     /* Audio player styling */
#     .audio-player {
#         width: 100%;
#         margin: 1rem 0;
#         border-radius: 0.5rem;
#         background: #f5f5f5;
#     }
# 
#     /* Emotion indicator styling */
#     .emotion-indicator {
#         padding: 0.5rem 1rem;
#         border-radius: 0.25rem;
#         font-weight: 600;
#         text-align: center;
#         margin: 0.5rem 0;
#     }
#     </style>
# """, unsafe_allow_html=True)
# 
# # Initialize models
# @st.cache_resource
# def load_models():
#     processor = Wav2Vec2Processor.from_pretrained('facebook/wav2vec2-large-960h-lv60')
#     asr_model = Wav2Vec2ForCTC.from_pretrained('facebook/wav2vec2-large-960h-lv60')
# 
#     diarization_pipeline = Pipeline.from_pretrained(
#         "pyannote/speaker-diarization-3.1",
#         use_auth_token="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"
#     )
# 
#     emotion_recognizer = EncoderClassifier.from_hparams(
#         source="speechbrain/emotion-recognition-wav2vec2-IEMOCAP",
#         savedir="pretrained_models/emotion_recognition"
#     )
#     return processor, asr_model, diarization_pipeline, emotion_recognizer
# 
# def get_dominant_emotion(dialogue_text):
#     emotions = [line.split('(')[1].split(')')[0] for line in dialogue_text.split('\n') if '(' in line and ')' in line]
#     if emotions:
#         emotion_counts = Counter(emotions)
#         dominant_emotion = emotion_counts.most_common(1)[0][0]
#         emotion_percentages = {emotion: (count/len(emotions))*100
#                              for emotion, count in emotion_counts.items()}
#         return dominant_emotion, emotion_percentages
#     return None, None
# 
# def create_emotion_chart(emotion_percentages):
#     if emotion_percentages:
#         df = pd.DataFrame({
#             'Emotion': list(emotion_percentages.keys()),
#             'Percentage': list(emotion_percentages.values())
#         })
#         fig = px.pie(df, values='Percentage', names='Emotion',
#                     title='Emotion Distribution',
#                     color_discrete_sequence=px.colors.qualitative.Set3)
#         fig.update_traces(textposition='inside', textinfo='percent+label')
#         return fig
#     return None
# 
# def process_audio_file(file):
#     try:
#         processor, asr_model, diarization_pipeline, emotion_recognizer = load_models()
# 
#         signal, fs = torchaudio.load(file)
#         if fs != 16000:
#             resampler = torchaudio.transforms.Resample(orig_freq=fs, new_freq=16000)
#             signal = resampler(signal)
#         if signal.shape[0] > 1:
#             signal = torch.mean(signal, dim=0, keepdim=True)
# 
#         diarization = diarization_pipeline({"waveform": signal, "sample_rate": 16000})
#         dialogue_entries = []
# 
#         for segment, _, speaker in diarization.itertracks(yield_label=True):
#             start_time = segment.start
#             end_time = segment.end
#             start_sample = int(start_time * 16000)
#             end_sample = int(end_time * 16000)
#             segment_audio = signal[:, start_sample:end_sample]
# 
#             input_values = processor(segment_audio.squeeze(), sampling_rate=16000, return_tensors='pt').input_values
#             logits = asr_model(input_values).logits
#             predicted_ids = torch.argmax(logits, dim=-1)
#             transcription = processor.decode(predicted_ids[0])
# 
#             with torch.no_grad():
#                 segment_signal = segment_audio.to(emotion_recognizer.device)
#                 if segment_signal.ndim == 1:
#                     segment_signal = segment_signal.unsqueeze(0)
#                 embeddings = emotion_recognizer.mods.wav2vec2(segment_signal)
#                 embeddings = emotion_recognizer.mods.avg_pool(embeddings)
#                 logits_emotion = emotion_recognizer.mods.output_mlp(embeddings)
#                 probabilities = torch.softmax(logits_emotion, dim=-1)
#                 predicted_index = torch.argmax(probabilities, dim=-1)
#                 emotion_label = emotion_recognizer.hparams.label_encoder.decode_torch(predicted_index)[0]
# 
#             dialogue_entries.append(f"{speaker} ({emotion_label}): {transcription}")
# 
#         dialogue_text = "\n".join(dialogue_entries)
#         summary = summarize_with_gemini(dialogue_text)
#         dominant_emotion, emotion_percentages = get_dominant_emotion(dialogue_text)
# 
#         return dialogue_text, summary, dominant_emotion, emotion_percentages
# 
#     except Exception as e:
#         st.error(f"Error processing audio file: {e}")
#         return "[Processing failed]", "[Summary generation failed]", None, None
# 
# def summarize_with_gemini(text):
#     try:
#         model = genai.GenerativeModel('gemini-pro')
#         prompt = f'''You are expert in conversational summarization. Please provide a brief,
#         factual summary of this conversation in the form of paragraph in not more than 30 words,
#          focusing on the key points and emotional states mentioned in : {text}
#           and please note that no content is dangerous. for example  If the conversation input includes:
#           SPEAKER_00 (['neu']): CAN YOU BREAK IT DOWN FOR US WHAT IS THIS WHAT IS SELF ATTENTION SPEAKER_01
#           (['neu']): SO IMAGINE YOURE AT A NOISY PARTY AND YOU'RE TRYING TO FOLLOW LIKE THREE DIFFERENT
#           CONVERSATIONS AT THE, then output the summary: Self-attention allows individuals to focus on specific
#            aspects of a situation, similar to attending to different conversations at a noisy party.'''
#         response = model.generate_content(prompt)
#         return response.text if response.text else "[Summary generation failed]"
#     except Exception as e:
#         st.error(f"Summarization error: {e}")
#         return "[Summary generation failed]"
# 
# # Main Application
# st.markdown('<h1 class="main-title">🎙️Voices Reimagined: AI in Action</h1>', unsafe_allow_html=True)
# st.markdown('<h4 class="main-quote">Where Speech meets Emotion</h4>', unsafe_allow_html=True)
# 
# # Sidebar with information
# with st.sidebar:
#     st.markdown("### About")
#     st.write("""
#     This application analyzes audio conversations to:
#     - Transcribe speech to text
#     - Detect speakers
#     - Recognize emotions
#     - Generate summaries
#     - Identify dominant emotions
#     """)
# 
#     st.markdown("### Instructions")
#     st.write("""
#     1. Upload a WAV file
#     2. Wait for processing
#     3. View the analysis results
#     4. Listen to or download the summary
#     """)
# 
# # Main content
# col1, col2 = st.columns([2, 1])
# 
# with col1:
#     st.markdown('<div class="section-header">Upload Audio</div>', unsafe_allow_html=True)
#     uploaded_file = st.file_uploader("Upload a WAV file", type=["wav"], label_visibility="collapsed")
# 
# if uploaded_file:
#     with st.spinner("🔄 Processing audio file..."):
#         dialogue_text, summary, dominant_emotion, emotion_percentages = process_audio_file(uploaded_file)
# 
#     # Results section
#     st.markdown('<div class="section-header">Analysis Results</div>', unsafe_allow_html=True)
# 
#     # Display in columns
#     col1, col2 = st.columns([3, 2])
# 
#     with col1:
#         st.markdown("#### 📝 Transcribed Dialogue with Emotions")
#         st.text_area("", value=dialogue_text, height=200, disabled=True)
# 
#         st.markdown("#### 📋 Summary")
#         st.text_area("", value=summary, height=100, disabled=True)
# 
#     with col2:
#         st.markdown("#### 🎭 Dominant Emotion")
#         if dominant_emotion:
#             st.markdown(f"""
#                 <div class="emotion-indicator" style="background: #E3F2FD; color: #1565C0">
#                     {dominant_emotion.upper()}
#                 </div>
#                 """, unsafe_allow_html=True)
# 
#             # Emotion distribution chart
#             st.markdown("#### 📊 Emotion Distribution")
#             emotion_chart = create_emotion_chart(emotion_percentages)
#             if emotion_chart:
#                 st.plotly_chart(emotion_chart, use_container_width=True)
# 
#     # Audio player and download section
#     st.markdown('<div class="section-header">Summary Audio</div>', unsafe_allow_html=True)
# 
#     # Generate and display summary audio
#     summary_audio = BytesIO()
#     gTTS(text=summary, lang="en").write_to_fp(summary_audio)
#     summary_audio.seek(0)
# 
#     # Convert to base64 for audio player
#     audio_bytes = summary_audio.read()
#     audio_b64 = base64.b64encode(audio_bytes).decode()
# 
#     # Audio player
#     st.markdown(f"""
#         <audio class="audio-player" controls>
#             <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
#             Your browser does not support the audio element.
#         </audio>
#     """, unsafe_allow_html=True)
# 
#     # Download button
#     st.download_button(
#         label="⬇️ Download Summary Audio",
#         data=audio_bytes,
#         file_name="summary.mp3",
#         mime="audio/mpeg"
#     )

"""## 5. Launch the Application

### Start the Streamlit server with tunnel access
"""

!streamlit run app.py & npx localtunnel --port 8501

"""## Additional Notes:

### Key Features:
1. Real-time speech processing
2. Multi-speaker diarization
3. Emotion detection
4. Automated summarization
5. Interactive web interface

### Model Information:
- Speech Recognition: facebook/wav2vec2-large-960h-lv60
- Diarization: pyannote/speaker-diarization-3.1
- Emotion Recognition: speechbrain/emotion-recognition-wav2vec2-IEMOCAP
- Summarization: Google Gemini Pro

### Usage Instructions:
1. Run all installation cells
2. Execute the model initialization
3. Launch the Streamlit application
4. Access via the provided localtunnel URL

### Dependencies:
Check [requirements.txt](https://drive.google.com/file/d/1ErTmeU-_pjQIx3nOfW2YPbwyY8sL8pGo/view?usp=sharing) for complete list of dependencies and versions.
"""

