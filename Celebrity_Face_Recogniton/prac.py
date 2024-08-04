import os
import yt_dlp

def download_video(video_url, output_path='C:/Users/Lagan/Downloads/downloded_videos'):
    # Ensure the output directory exists
    os.makedirs(output_path, exist_ok=True)
    
    ydl_opts = {
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'format': 'best',
        'ffmpeg_location': 'C:/Users/Lagan/Downloads/ffmpeg-master-latest-win64-gpl/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe',  # Update this to the path where ffmpeg.exe is located
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        print(f"Title: {info['title']}")
        print(f"URL: {info['webpage_url']}")
        print(f"Downloaded to: {output_path}")

# Example usage
video_urls = [
    'https://www.youtube.com/shorts/nGFHDXn7kU8',
    'https://www.youtube.com/shorts/jv8YRJ6-zuU',
    'https://www.youtube.com/shorts/xVLrZlMcG8I',
    'https://www.youtube.com/shorts/gn8VEO_KzBA',
    'https://www.youtube.com/shorts/O9WJX_pApBo'
]

for url in video_urls:
    download_video(url)
