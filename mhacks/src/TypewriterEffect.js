import React, { useState, useEffect } from "react";

const TypewriterEffect = ({ text }) => {
  const [currentText, setCurrentText] = useState("");

  useEffect(() => {
    let index = 0;
    const allWords = text.split(" ");
    setCurrentText(""); // Clear previous text

    const intervalId = setInterval(() => {
      if (index < allWords.length) {
        setCurrentText((prev) => prev + allWords[index] + " ");
        index++;
      } else {
        clearInterval(intervalId);
      }
    }, 100); // Set interval to 500ms or any other value to control speed

    return () => clearInterval(intervalId);
  }, [text]);

  return <div className="typewriter">{currentText}</div>;
};

export default TypewriterEffect;
