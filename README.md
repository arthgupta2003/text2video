# Image to Video Convertor using FFMEG
This project is a Video Converter using FFMPEG. It allows users to create video clips by combining images, voiceover texts, and transitions. The generated video can be downloaded and previewed on the page.

# Local Usage
1. Install required packages with ```npm install```
2. Start back-end server with ```uvicorn main:app```
3. Start web-application with ```vercel dev```
4. Open web-application (likely at `localhost:3000`)

# Hosting and Configuration
1. Front end application available at: https://text2video-fc6v.vercel.app/
2. Host backend server by: 
* `cd Backend` 
* `docker build -t t2v_backend `
* `docker run -d -p 8000:8000 t2v_backend`
3. Need to call `/deletelocalimages` endpoint at regular intervals to free up extra disk space
