import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import json
from gtts import gTTS
import shutil
import subprocess
from typing import List
import itertools
from starlette.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    image_urls: List[str]
    voiceover_texts: List[str]
    background_music_url: str
    transition_array: List[str]

@app.post("/convert", response_class=FileResponse)
async def convert_videos(item: Item):
    try:
        if os.path.exists("./temp"):
            shutil.rmtree("./temp")
        os.mkdir("./temp")
        os.chdir("./temp")
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": str(e)})
    
    image_urls = item.image_urls
    voiceover_texts = item.voiceover_texts
    background_music_url = item.background_music_url
    transition_arr = item.transition_array
    
    background_music_path = "temp_bg_music.mp3"
    if background_music_url!="":
        download_file(background_music_url, background_music_path)
    temp_video_paths = []
    
    for i, (image_url, voiceover_text) in enumerate(zip(image_urls, voiceover_texts)):
        image_path = f"temp_image_{i+1}.jpg"
        voiceover_path = f"temp_voiceover_{i+1}.mp3"
        output_video_path = f"temp_video_{i+1}.mp4"

        download_file(image_url, image_path)
        create_voiceover(voiceover_text, voiceover_path)
        convert_to_video(image_path, voiceover_path, voiceover_text, output_video_path, i)
        temp_video_paths.append(output_video_path)

    concated_path = 'output.mp4'
    if (len(image_urls)>1):
        concat_videos_with_transition_array(temp_video_paths, concated_path, transition_arr)
    elif (len(image_urls)==1):
        os.rename("temp_video_1",concated_path)
    else:
        raise SystemError("At least one scene is required")

    final_output_path = "AAAA.mp4"
    if background_music_url!="":
        add_background_music(concated_path, background_music_path, final_output_path)
    else:
        os.rename(concated_path,final_output_path)
    
    os.chdir("./..")
    return "temp/"+final_output_path

#PROBLEMS WITH hlwind, hrwind, vuwind, vdwind, coverleft, coverright, coverup, coverdown,revealleft,revealright, revealup, revealdown
all_transitions = [
    "fade",
    "fadeblack",
    "fadewhite",
    "distance",
    "wipeleft",
    "wiperight",
    "wipeup",
    "wipedown",
    "slideleft",
    "slideright",
    "slideup",
    "slidedown",
    "smoothleft",
    "smoothright",
    "smoothup",
    "smoothdown",
    "rectcrop",
    "circlecrop",
    "circleclose",
    "circleopen",
    "horzclose",
    "horzopen",
    "vertclose",
    "vertopen",
    "diagbl",
    "diagbr",
    "diagtl",
    "diagtr",
    "hlslice",
    "hrslice",
    "vuslice",
    "vdslice",
    "dissolve",
    "pixelize",
    "radial",
    "hblur",
    "fade",
]

def concat_videos_with_transition_array(segments: List[str], output_filename: str, transitions: List[str], transition_duration: float = 1.0):
    # Get the lengths of the videos in seconds
    file_lengths = [
        float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
                              'default=noprint_wrappers=1:nokey=1', f], capture_output=True,
                             text=True).stdout.strip())
        for f in segments
    ]
    files_input = [['-i', f] for f in segments]

    # Prepare the filter graph
    video_fades = ""
    audio_fades = ""
    last_fade_output = "0:v"
    last_audio_output = "0:a"
    video_length_so_far=0

    for i in range(len(segments)):
        if i == 0:
            video_length_so_far+= file_lengths[i]
            continue

        # Video graph: chain the xfade operator together
        next_fade_output = f"temp_v{i}"
        video_fades += f"[{last_fade_output}][{i}:v]xfade=transition={transitions[i-1]}: duration={transition_duration}:offset={video_length_so_far - i*transition_duration}[{next_fade_output}];"
        last_fade_output = next_fade_output
        video_length_so_far+= file_lengths[i]

        # Audio graph:
        next_audio_output = f"temp_a{i}"
        audio_fades += f"[{last_audio_output}][{i}:a]acrossfade=d={transition_duration}[{next_audio_output}];"
        last_audio_output = next_audio_output

    # Assemble the FFmpeg command arguments
    ffmpeg_args = ['ffmpeg',
                   *itertools.chain(*files_input),
                   '-filter_complex', video_fades + audio_fades,
                   '-map', f'[{last_fade_output}]',
                   '-map', f"[{last_audio_output}]",
                   '-preset', "ultrafast",
                   '-y',
                   output_filename]
    # Run FFmpeg
    subprocess.run(ffmpeg_args)

def download_file(url, output_path):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(output_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
            
def create_voiceover(text, output_path):
    tts = gTTS(text=text, lang='en')
    tts.save(output_path)
    

def convert_to_video(image_path, voiceover_path, voiceover_text, output_path, x):
    ffprobe_cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'json', voiceover_path]
    ffprobe_output = subprocess.check_output(ffprobe_cmd).decode('utf-8')
    ffprobe_data = json.loads(ffprobe_output)
    voiceover_duration = float(ffprobe_data['format']['duration'])
    caption =voiceover_text
    
    ffmpeg_cmd = [
    '/usr/local/bin/ffmpeg',
    '-loop', '1',
    '-r', '28',
    '-i', image_path,
    '-i', voiceover_path,
    '-filter_complex', f"[0:v]scale=1920:1080[v];[v]drawtext=text='{caption}':fontcolor=white:fontsize=60:x=(W-text_w)/2:y=(7*(H-text_h)/8):fontfile=/path/to/font.ttf:bordercolor=black:borderw=2[v];",
    '-map', '[v]',
    '-map', '1:a',
    '-c:v', 'libx264',
    '-preset', 'ultrafast',
    '-c:a', 'aac',
    '-b:a', '128k',
    '-t', str(voiceover_duration),
    '-pix_fmt', 'yuv420p',
    '-y', output_path
    ]
    subprocess.run(ffmpeg_cmd)


def add_background_music(input_path, background_music_path, final_output_path):
    add_background_music = [
    '/usr/local/bin/ffmpeg',
    '-i',
    input_path,
    '-i',
    background_music_path,
    '-filter_complex',
 '[0:a][1:a]amix=inputs=2[a]',
    '-map',
    '0:v',
    '-map',
    '[a]',
    '-c:v',
    'copy',
    '-ac',
    '2',
    '-shortest',
    final_output_path
]
    subprocess.run(add_background_music)
    return final_output_path