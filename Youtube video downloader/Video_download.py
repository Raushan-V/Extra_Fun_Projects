import yt_dlp
import os
import sys

if len(sys.argv) > 1:
    link = sys.argv[1]
else:
    link = input("Enter Link of Youtube Video: ")

print("Current working directory:", os.getcwd())

# Create downloads directory if it doesn't exist
os.makedirs('downloads', exist_ok=True)

# Options for extracting info without downloading
ydl_opts_info = {
    'quiet': True,
    'no_warnings': True,
}

with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
    info = ydl.extract_info(link, download=False)
    print("Title :", info.get('title'))
    print("Views :", info.get('view_count'))
    print("Duration :", info.get('duration'))
    print("Description :", info.get('description'))
    print("Ratings :", info.get('average_rating', 'N/A'))  # Ratings may not be available

# Options for downloading the highest resolution to downloads folder
ydl_opts_download = {
    'format': 'best',
    'outtmpl': 'downloads/%(title)s.%(ext)s',
}

with yt_dlp.YoutubeDL(ydl_opts_download) as ydl:
    ydl.download([link])

print("Download completed!! Video saved in 'downloads' folder.")
