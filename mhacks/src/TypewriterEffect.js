import React, { useState, useEffect } from "react";

const TypewriterEffect = ({ text }) => {
  const [currentText, setCurrentText] = useState("");

  useEffect(() => {
    let index = 0;
    const characters = text.split("");
    setCurrentText(""); // Clear previous text

    const intervalId = setInterval(() => {
      if (index < characters.length) {
        setCurrentText((prev) => prev + characters[index]);
        index++;
      } else {
        clearInterval(intervalId);
      }
    }, 100);

    return () => clearInterval(intervalId);
  }, [text]); // Only depend on text

  return currentText === undefined ? (
    <div></div>
  ) : (
    <div className="typewriter">{currentText}</div>
  );
};

export default TypewriterEffect;