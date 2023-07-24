import React, { useState } from 'react';
import SubmissionCard from './SubmittedCard';

const VideoConverter = () => {
  const [imageURLs, setImageUrls] = useState([]);
  const [voiceoverTexts, setVoiceoverTexts] = useState([]);
  const [transitionArray, setTransitionArray] = useState([]);
  const [currentImage, setCurrentImage] = useState("");
  const [currentText, setCurrentText] = useState("");
  const [currentTransition, setCurrentTransition] = useState("");
  const [backgroundMusicURL, setBackgroundMusicURL] = useState("");
  const [convertedVideoURL, setConvertedVideoURL] = useState('');
  const [loading, setLoading] = useState(false);

  const handleAddData = () => {
    if (!(currentText && currentTransition && currentImage)){
        alert("Please input all data before submitting");
        return;
    }
    setImageUrls((prevImageUrls) => [...prevImageUrls, currentImage]);
    setVoiceoverTexts((prevVoiceoverTexts) => [...prevVoiceoverTexts, currentText]);
    setTransitionArray((prevTransitionArray) => [...prevTransitionArray, currentTransition]);
    setCurrentImage("")
    setCurrentText("")
    setCurrentTransition("")
    return;
    }

    const downloadVideoFromBlob = (videoURL) => {
        const downloadLink = document.createElement('a');
        downloadLink.href = videoURL;
        downloadLink.download = 'video.mp4';
    
        document.body.appendChild(downloadLink);
    
        downloadLink.click();
    
        document.body.removeChild(downloadLink);
      };

    const handleSubmit = () => {
        setLoading(true);
        fetch('api/main/convert', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              image_urls: imageURLs,
              voiceover_texts: voiceoverTexts,
              background_music_url: backgroundMusicURL,
              transition_array: transitionArray,
            }),
          })
            .then((response) => {
              if (response.ok) {
                return response.blob();
              } else {
                throw new Error('Network response was not ok');
              }
            })
            .then((blob) => {
              // Create an object URL for the blob
              const videoURL = URL.createObjectURL(blob);
              setConvertedVideoURL(videoURL);
              console.log(blob);
              console.log(videoURL);
              setLoading(false);
            })
            .catch((error) => {
              console.error('Error:', error);
              setLoading(false);
            });
        };
      

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-100">
          <div className="bg-white shadow-lg rounded-lg p-6 max-w-md w-full">
            <div className="flex flex-wrap mb-4">
              <input
                type="text"
                value={currentImage}
                onChange={(e) => setCurrentImage(e.target.value)}
                placeholder={`Enter image URL`}
                className="w-full px-4 py-2 rounded border border-gray-300 focus:outline-none focus:border-blue-500"
              />
              <input
                type="text"
                value={currentText}
                onChange={(e) => setCurrentText(e.target.value)}
                placeholder={`Enter voiceover text`}
                className="w-full mt-2 px-4 py-2 rounded border border-gray-300 focus:outline-none focus:border-blue-500"
              />
              <select
                value={currentTransition}
                onChange={(e) => setCurrentTransition(e.target.value)}
                className="w-full mt-2 px-4 py-2 rounded border border-gray-300 focus:outline-none focus:border-blue-500"
              >
                <option value="">Select Transition</option>
                {all_transitions.map((transition) => (
                  <option key={transition} value={transition}>
                    {transition}
                  </option>
                ))}
              </select>
            </div>
            <button
              type="button"
              onClick={handleAddData}
              className="w-3/5 bg-blue-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            >
              Add scene
            </button>
            {imageURLs.length > 0 && (
          <SubmissionCard
            imageURLs={imageURLs}
            voiceoverTexts={voiceoverTexts}
            transitionArray={transitionArray}
          />
        )}
        <div className="flex flex-wrap mb-4">
        <input
                type="text"
                value={backgroundMusicURL}
                onChange={(e) => setBackgroundMusicURL(e.target.value)}
                placeholder={`Enter background music URL`}
                className="w-full mt-2 px-4 py-2 rounded border border-gray-300 focus:outline-none focus:border-blue-500"
              />
        </div>
        <div className="flex flex-row gap-x-4">
            <button
              type="button"
              onClick={handleSubmit}
              className="w-3/5 bg-blue-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            >
              Submit
            </button>
            {<button
              type="button"
              onClick={()=> downloadVideoFromBlob(convertedVideoURL)}
              className="w-3/5 bg-green-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline disabled:bg-gray-300 disabled:cursor-not-allowed"
              disabled={convertedVideoURL===""}
            >
              Download Video
            </button>}
            
        </div>
        {loading && <h1 className="text-4xl font-bold pt-5">Loading...</h1>}
          </div>
          {convertedVideoURL && (
        <div className="mt-6 flex items-center justify-center sticky position:fixed">
          <video width="640" height="360" controls key={convertedVideoURL}>
            <source src={convertedVideoURL} type="video/mp4"/>
            Your browser does not support the video tag.
          </video>
        </div>
      )}
        </div>
      );
    };
    
export default VideoConverter;

const all_transitions = [
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
]

