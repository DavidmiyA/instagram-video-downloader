import streamlit as st
import instaloader
import re
import os
import shutil

st.set_page_config(page_title="Instagram Video Downloader", layout="centered")

st.title("Instagram HD Video Downloader")

url = st.text_input("Enter Instagram Post URL (Public Posts Only):")

if st.button("Download"):
    # Clear previous downloads
    if os.path.exists("downloads"):
        shutil.rmtree("downloads")
    os.makedirs("downloads", exist_ok=True)

    try:
        # Extract shortcode from URL
        match = re.search(r"instagram.com/p/([^/]+)/", url)
        if not match:
            st.error("Invalid Instagram post URL.")
        else:
            shortcode = match.group(1)

            # Setup Instaloader
            L = instaloader.Instaloader(dirname_pattern="downloads", save_metadata=False, download_video_thumbnails=False, download_comments=False)
            post = instaloader.Post.from_shortcode(L.context, shortcode)
            L.download_post(post, target="video")

            # Find and show the .mp4 file
            for root, dirs, files in os.walk("downloads"):
                for file in files:
                    if file.endswith(".mp4"):
                        video_path = os.path.join(root, file)
                        with open(video_path, "rb") as f:
                            st.video(f.read())
                        st.success("Video downloaded and loaded successfully!")
                        break
                else:
                    continue
                break
    except Exception as e:
        st.error(f"Download failed: {e}")
