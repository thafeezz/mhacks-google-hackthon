import React, { useState } from "react";
import axios from "axios";
import TypewriterEffect from "./TypewriterEffect";
import "./App.css"; // Make sure this CSS is imported

const InputWithTypewriter = () => {
  const [inputValue, setInputValue] = useState("");
  const [apiResponse, setApiResponse] = useState("");

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  const handleKeyDown = async (e) => {
    if (e.key === "Enter") {
      try {
        const response = await axios.get(
          `http://localhost:8000/genad?q=${encodeURIComponent(inputValue)}`
        );
        setApiResponse(response.data.response);
      } catch (error) {
        console.error("Error calling API:", error);
        setApiResponse("Failed to fetch data."); // Handle error with user feedback
      }
    }
  };

  return (
    <div className="input-container">
      <input
        type="text"
        value={inputValue}
        onChange={handleInputChange}
        onKeyDown={handleKeyDown}
        placeholder="Enter a prompt here"
      />
      <div className="typewriter-container">
        <TypewriterEffect text={apiResponse} />
      </div>
    </div>
  );
};

export default InputWithTypewriter;
