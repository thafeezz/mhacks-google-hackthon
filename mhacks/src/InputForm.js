import React, { useState, useRef } from "react";
import axios from "axios";
import TypewriterEffect from "./TypewriterEffect";
import "./InputForm.css"; // Ensure the CSS file is in the same directory

const InputForm = () => {
  const [formData, setFormData] = useState({
    company_name: "",
    product_details: "",
    organization_size: "",
    product_differentiator: "",
  });
  const [adScript, setAdScript] = useState("");
  const [isLoading, setIsLoading] = useState(false); // State to track loading
  const [isPlaying, setIsPlaying] = useState(false); // State to track audio playing

  const audioRef = useRef(null); // Ref for the audio element

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true); // Start loading
    try {
      const response = await axios.post(
        "http://localhost:8000/genad/",
        formData
      );
      setAdScript(response.data.ad_script);
    } catch (error) {
      console.error("Error calling API:", error);
      setAdScript("Failed to fetch data."); // Handle errors
    }
    setIsLoading(false); // End loading
  };

  // Toggle play/pause for the audio
  const togglePlayPause = () => {
    if (audioRef.current) {
      if (!isPlaying) {
        audioRef.current.play();
        setIsPlaying(true);
      } else {
        audioRef.current.pause();
        setIsPlaying(false);
      }
    }
  };

  return (
    <div className="input-form">
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="company_name"
          value={formData.company_name}
          onChange={handleChange}
          placeholder="Company Name"
        />
        <input
          type="text"
          name="product_details"
          value={formData.product_details}
          onChange={handleChange}
          placeholder="Product Details"
        />
        <input
          type="text"
          name="organization_size"
          value={formData.organization_size}
          onChange={handleChange}
          placeholder="Organization Size"
        />
        <input
          type="text"
          name="product_differentiator"
          value={formData.product_differentiator}
          onChange={handleChange}
          placeholder="Product Differentiator"
        />
        <button type="submit" disabled={isLoading}>
          {isLoading ? "Loading..." : "Generate Ad Script"}
        </button>
      </form>
      <div className="audio-player">
        <audio ref={audioRef} src="/ad_script_audio.mp3" preload="auto" />
        <button onClick={togglePlayPause}>
          {isPlaying ? "Pause" : "Play"}
        </button>
      </div>
      <div className="ad-script">
        {isLoading ? (
          <div className="loading">Loading...</div>
        ) : (
          <TypewriterEffect text={adScript} />
        )}
      </div>
    </div>
  );
};

export default InputForm;
