import os
import threading
import customtkinter as ctk
import yt_dlp

# Set modern look
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class YTDownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("YouTube 1080p Downloader")
        self.geometry("600x350")
        self.resizable(False, False)

        # Title Label
        self.title_label = ctk.CTkLabel(self, text="YouTube Downloader", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(pady=(30, 10))

        # Instructions Label
        self.instruction_label = ctk.CTkLabel(self, text="Enter a YouTube URL below to download it in 1080p with audio", font=ctk.CTkFont(size=14))
        self.instruction_label.pack(pady=(0, 20))

        # URL Input
        self.url_var = ctk.StringVar()
        self.url_entry = ctk.CTkEntry(self, width=450, height=40, placeholder_text="https://www.youtube.com/watch?v=...", textvariable=self.url_var)
        self.url_entry.pack(pady=(0, 20))

        # Download Button
        self.download_btn = ctk.CTkButton(self, text="Download Video", width=200, height=40, command=self.start_download)
        self.download_btn.pack(pady=(0, 20))

        # Status Label
        self.status_label = ctk.CTkLabel(self, text="", text_color="gray", font=ctk.CTkFont(size=13))
        self.status_label.pack(side="bottom", pady=20)

    def start_download(self):
        url = self.url_var.get().strip()
        if not url:
            self.status_label.configure(text="Please enter a valid YouTube URL.", text_color="#FF4C4C")
            return

        # Disable button and entry while downloading
        self.download_btn.configure(state="disabled", text="Downloading...")
        self.url_entry.configure(state="disabled")
        self.status_label.configure(text="Starting download... please wait.", text_color="gray")

        # Start download in a separate thread so GUI doesn't freeze
        download_thread = threading.Thread(target=self.download_video, args=(url,))
        download_thread.start()

    def download_video(self, url):
        try:
            ydl_opts = {
                # Download best video up to 1080p and best audio
                'format': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'merge_output_format': 'mp4',
                'outtmpl': '%(title)s.%(ext)s',
                'noplaylist': True,
                'logger': MyLogger(self),
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            self.after(0, self.download_complete, "✅ Download completed successfully!", "#4CAF50")
        except Exception as e:
            self.after(0, self.download_complete, f"❌ Error: Make sure FFmpeg is installed and URL is valid.", "#FF4C4C")

    def download_complete(self, message, color):
        self.status_label.configure(text=message, text_color=color)
        self.download_btn.configure(state="normal", text="Download Video")
        self.url_entry.configure(state="normal")
        self.url_var.set("") # Clear entry

    def update_status(self, text):
        # Allow logger to update status label safely
        self.after(0, lambda: self.status_label.configure(text=text, text_color="gray"))

class MyLogger:
    def __init__(self, app):
        self.app = app

    def debug(self, msg):
        # yt-dlp sends progress info to debug
        if "[download]" in msg and "Destination" not in msg:
            self.app.update_status(msg)

    def info(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

if __name__ == "__main__":
    app = YTDownloaderApp()
    app.mainloop()
