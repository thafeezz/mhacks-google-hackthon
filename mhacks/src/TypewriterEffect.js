import React, { useState, useEffect } from "react";

const TypewriterEffect = ({ text }) => {
  const [currentText, setCurrentText] = useState("");

  useEffect(() => {
    let index = 0;
    const allWords = text.split(" ");
    setCurrentText(""); // Clear previous text

    console.log("Typewriter effect started: ", text); // Debug log

    const intervalId = setInterval(() => {
      if (index < allWords.length) {
        setCurrentText((prev) => prev + allWords[index] + " ");
        index++;
      } else {
        clearInterval(intervalId);
      }
    }, 100); // Adjust interval to control the speed of typewriting effect

    return () => clearInterval(intervalId);
  }, [text]); // Ensure it re-runs only when text changes

  return <div className="typewriter">{currentText}</div>;
};

export default TypewriterEffect;
