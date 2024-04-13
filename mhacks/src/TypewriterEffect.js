import React, { useState, useEffect } from "react";

const TypewriterEffect = ({ text }) => {
  const [currentText, setCurrentText] = useState("");

  useEffect(() => {
    let index = 0;
    const characters = text.split("");
    setCurrentText(""); // Clear previous text

    console.log("Typewriter effect started: ", text); // Debug log

    const intervalId = setInterval(() => {
      if (index < characters.length) {
        setCurrentText((prev) => prev + characters[index]);
        index++;
      } else {
        clearInterval(intervalId);
      }
    }, 50); // Faster interval for character-by-character

    return () => clearInterval(intervalId);
  }, [text]); // Ensure it re-runs only when text changes

  return <div className="typewriter">{currentText}</div>;
};

export default TypewriterEffect;