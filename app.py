import streamlit as st
import os
import asyncio
import time
import urllib.request
from PIL import Image, ImageFilter
import numpy as np

# Present Time (2026) Google GenAI Client
from google import genai
from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip

st.set_page_config(page_title="AI Masterpiece Editor", page_icon="🎬", layout="centered")

# Beautiful Custom Branding UI
st.markdown("""
    <style>
    .main-title { font-size:36px; font-weight:bold; color:#FF4B4B; text-align:center; }
    .sub-title { font-size:18px; text-align:center; margin-bottom:20px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">🎬 AI Autonomous Video Editor PRO</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Sanjit Oraw dwara nirmit - Present Time Advanced Video Agent</div>', unsafe_allow_html=True)

# 1. API Configuration & Input
GEMINI_API_KEY = st.text_input("Apni Gemini API Key Dalein:", type="password", help="Google AI Studio se free key lein")
uploaded_video = st.file_uploader("Apni Raw Screen Recording / Video Upload Karein", type=["mp4", "mov", "avi"])

if uploaded_video and GEMINI_API_KEY:
    # Initialize modern client
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    if st.button("Start Magical Professional Editing 🚀", use_container_width=True):
        with st.status("💥 AI Agent active ho raha hai...", expanded=True) as status:
            
            # Temporary file paths
            raw_path = "raw_recording.mp4"
            bgm_path = "bgm.mp3"
            blurred_path = "temp_blurred.mp4"
            voice_path = "temp_voiceover.mp3"
            final_output = "premium_final_output.mp4"
            
            # Save the uploaded file locally
            with open(raw_path, "wb") as f:
                f.write(uploaded_video.read())
            
            # --- PHASE 1: AUTO BGM FETCH ---
            st.write("🎵 Background Music fetch kiya ja raha hai...")
            url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
            urllib.request.urlretrieve(url, bgm_path)
            
            # --- PHASE 2: ULTRA FAST PILLOW BLURRING ---
            st.write("💥 Step 1/4: Video frames ko process aur smooth blur kiya ja raha hai...")
            clip = VideoFileClip(raw_path)
            
            def blur_frame(frame):
                img = Image.fromarray(frame)
                blurred_img = img.filter(ImageFilter.GaussianBlur(radius=15))
                return np.array(blurred_img)
            
            blurred_clip = clip.fl_image(blur_frame)
            blurred_clip.write_videofile(blurred_path, codec="libx264", audio=False, logger=None)
            
            # --- PHASE 3: AI VISION SCRIPTING ---
            st.write("🧠 Step 2/4: Gemini 1.5 Multimodal Engine video ko dekh kar script likh raha hai...")
            
            # Upload file using modern structure
            video_file_ai = client.files.upload(file=blurred_path)
            while video_file_ai.state.name == "PROCESSING":
                time.sleep(4)
                video_file_ai = client.files.get(name=video_file_ai.name)
                
            prompt = """
            Is video/screen recording ko dhyan se dekho. Isme jo chal raha hai use samjho.
            Iske liye ek world-class, highly engaging aur professional YouTube Voiceover script likho Hindi me.
            Sirf wahi text dena jo bolna hai. Extra technical lines mat likhna. 0% mistake chahiye.
            """
            
            response = client.models.generate_content(
                model='gemini-1.5-flash',
                contents=[video_file_ai, prompt]
            )
            ai_script = response.text
            st.text_area("✍️ AI Generated Custom Script:", value=ai_script, height=120)
            
            # --- PHASE 4: NATURAL AUDIO SYNTHESIS ---
            st.write("🎙️ Step 3/4: Natural Human Voiceover generate ho raha hai...")
            import edge_tts
            async def generate_voice(text):
                communicate = edge_tts.Communicate(text, "hi-IN-MadhurNeural")
                await communicate.save(voice_path)
            asyncio.run(generate_voice(ai_script))
            
            # --- PHASE 5: PRECISION AUDIO MIXING & DUCKING ---
            st.write("🎬 Step 4/4: Video Syncing aur Production Render chal raha hai...")
            video_clip = VideoFileClip(blurred_path)
            voice_clip = AudioFileClip(voice_path)
            
            # Precision Check
            if video_clip.duration < voice_clip.duration:
                speed_factor = video_clip.duration / voice_clip.duration
                from moviepy.video.fx.all import speedx
                video_clip = speedx(video_clip, factor=speed_factor)
            
            bgm_clip = AudioFileClip(bgm_path).multiply_volume(0.12).with_duration(voice_clip.duration)
            
            final_audio = CompositeAudioClip([voice_clip, bgm_clip])
            final_video = video_clip.with_audio(final_audio)
            final_video.write_videofile(final_output, codec="libx264", audio_codec="aac", logger=None)
            
            status.update(label="🎉 Video Successfully Processed!", state="complete", expanded=False)
            
        st.success("🏆 Aapki World-Class Premium Video Taiyar Hai!")
        with open(final_output, "rb") as file:
            st.download_button(label="Download Edited Video 📥", data=file, file_name="ai_masterpiece_output.mp4", mime="video/mp4", use_container_width=True)
