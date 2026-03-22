import os
import sys
import yt_dlp

def download_video(url, output_path="."):
    """
    Downloads a YouTube video at 1080p with audio using yt-dlp.
    NOTE: ffmpeg must be installed on your system to merge 1080p video and audio.
    """
    ydl_opts = {
        # Download best video up to 1080p and best audio
        'format': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'merge_output_format': 'mp4',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'noplaylist': True,
    }

    print(f"Starting download for: {url}")
    print("This may take some time depending on your internet connection.")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("\n✅ Download completed successfully!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("\nNote: Make sure 'ffmpeg' is installed and added to your system PATH.")
        print("You can install it by running: winget install ffmpeg")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python downloader.py <YOUTUBE_URL>")
        sys.exit(1)
        
    url = sys.argv[1]
    download_video(url)
