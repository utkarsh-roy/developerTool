import os
import threading
import customtkinter as ctk
import yt_dlp
import imageio_ffmpeg

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class YTDownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("YouTube Downloader")
        self.geometry("680x450")
        self.resizable(False, False)

        # Title
        self.title_label = ctk.CTkLabel(self, text="YouTube Downloader", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(pady=(20, 10))

        # Instructions
        self.instruction_label = ctk.CTkLabel(self, text="Enter a URL, select format and quality, then press download", font=ctk.CTkFont(size=14))
        self.instruction_label.pack(pady=(0, 20))

        # URL
        self.url_var = ctk.StringVar()
        self.url_entry = ctk.CTkEntry(self, width=540, height=40, placeholder_text="https://www.youtube.com/watch?v=...", textvariable=self.url_var)
        self.url_entry.pack(pady=(0, 20))

        # Options Frame
        self.options_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.options_frame.pack(pady=(0, 20))

        # Format Dropdown
        self.format_label = ctk.CTkLabel(self.options_frame, text="Format:", font=ctk.CTkFont(weight="bold"))
        self.format_label.grid(row=0, column=0, padx=(0, 10))
        self.format_var = ctk.StringVar(value="Video + Audio")
        self.format_dropdown = ctk.CTkOptionMenu(self.options_frame, values=["Video + Audio", "Audio Only (MP3)"], variable=self.format_var, command=self.on_format_change)
        self.format_dropdown.grid(row=0, column=1, padx=(0, 40))

        # Quality Dropdown
        self.quality_label = ctk.CTkLabel(self.options_frame, text="Max Quality:", font=ctk.CTkFont(weight="bold"))
        self.quality_label.grid(row=0, column=2, padx=(0, 10))
        self.quality_var = ctk.StringVar(value="1080p")
        self.quality_dropdown = ctk.CTkOptionMenu(self.options_frame, values=["1080p", "720p", "480p", "360p"], variable=self.quality_var)
        self.quality_dropdown.grid(row=0, column=3)

        # Download Button
        self.download_btn = ctk.CTkButton(self, text="Download", width=200, height=45, font=ctk.CTkFont(size=15, weight="bold"), command=self.start_download)
        self.download_btn.pack(pady=(10, 20))

        # Status
        self.status_label = ctk.CTkLabel(self, text="", text_color="gray", font=ctk.CTkFont(size=13))
        self.status_label.pack(side="bottom", pady=20)

    def on_format_change(self, choice):
        if choice == "Audio Only (MP3)":
            self.quality_dropdown.configure(state="disabled")
        else:
            self.quality_dropdown.configure(state="normal")

    def start_download(self):
        url = self.url_var.get().strip()
        if not url:
            self.status_label.configure(text="Please enter a valid YouTube URL.", text_color="#FF4C4C")
            return

        fmt = self.format_var.get()
        qty = self.quality_var.get()

        self.download_btn.configure(state="disabled", text="Downloading...")
        self.url_entry.configure(state="disabled")
        self.format_dropdown.configure(state="disabled")
        self.quality_dropdown.configure(state="disabled")
        self.status_label.configure(text="Starting download...", text_color="gray")

        thread = threading.Thread(target=self.download_video, args=(url, fmt, qty))
        thread.start()

    def download_video(self, url, fmt, qty):
        try:
            ydl_opts = {
                'outtmpl': '%(title)s.%(ext)s',
                'noplaylist': True,
                'logger': MyLogger(self),
                'ffmpeg_location': imageio_ffmpeg.get_ffmpeg_exe(),
            }

            if fmt == "Audio Only (MP3)":
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            else:
                height = ''.join(filter(str.isdigit, qty)) or "1080"
                ydl_opts['format'] = f'bestvideo[height<={height}][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
                ydl_opts['merge_output_format'] = 'mp4'

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            self.after(0, self.download_complete, "✅ Download completed successfully!", "#4CAF50")
        except Exception as e:
            self.after(0, self.download_complete, f"❌ Error: {e}", "#FF4C4C")

    def download_complete(self, message, color):
        self.status_label.configure(text=message, text_color=color)
        self.download_btn.configure(state="normal", text="Download")
        self.url_entry.configure(state="normal")
        self.format_dropdown.configure(state="normal")
        self.on_format_change(self.format_var.get())
        self.url_var.set("") # Clear entry

    def update_status(self, text):
        self.after(0, lambda: self.status_label.configure(text=text, text_color="gray"))

class MyLogger:
    def __init__(self, app):
        self.app = app
    def debug(self, msg):
        if "[download]" in msg and "Destination" not in msg:
            self.app.update_status(msg)
    def info(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): print(msg)

if __name__ == "__main__":
    app = YTDownloaderApp()
    app.mainloop()
