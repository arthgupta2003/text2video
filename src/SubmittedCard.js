import React from 'react';

const SubmissionCard = ({ imageURLs, voiceoverTexts, transitionArray }) => {
  // Zip the elements together
  const zippedData = imageURLs.map((url, index) => ({
    imageURL: url,
    voiceoverText: voiceoverTexts[index],
    transition: transitionArray[index],
  }));

  return (
    <div>
      {zippedData.map((data, index) => (
        <div key={index} className="mt-6 bg-gray-200 rounded-lg p-4">
          <h2 className="text-xl font-semibold mb-4">Scene {index + 1}:</h2>
          <ul>
            <li className="mb-2">
              <img src={data.imageURL}/>
            </li>
          </ul>
          <ul>
            <li className="mb-2">
              <span className="font-semibold">Voiceover Text:</span> {data.voiceoverText}
            </li>
          </ul>
          <ul>
            <li className="mb-2">
              <span className="font-semibold">Transition:</span> {data.transition}
            </li>
          </ul>
        </div>
      ))}
    </div>
  );
};

export default SubmissionCard;
