import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import TypewriterEffect from "./TypewriterEffect";
import "./InputForm.css";

const InputForm = () => {
  // State variables
  const [adScript, setAdScript] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);

  // Refs
  const audioRef = useRef(null);
  const formRef = useRef(null);

  // Function to extract form data
  const getFormData = () => {
    const formData = new FormData(formRef.current);
    return {
      company_name: formData.get("company_name"),
      product_details: formData.get("product_details"),
      organization_size: formData.get("organization_size"),
      product_differentiator: formData.get("product_differentiator"),
    };
  };

  // Function to handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    const data = getFormData();

    try {
      const response = await axios.post("http://localhost:8000/genad/", data);
      const ad_script = response.data.ad_script;
      setAdScript(ad_script);
    } catch (error) {
      console.error("Error calling API:", error);
      setAdScript("Failed to fetch data.");
    }

    setIsLoading(false);
  };

  // Function to toggle play/pause of the audio
  const togglePlayPause = () => {
    if (audioRef.current) {
      if (!isPlaying) {
        console.log("ABOUT TO PRINT");
        console.log(audioRef.current);
        audioRef.current.play();
        setIsPlaying(true);
      } else {
        audioRef.current.pause();
        setIsPlaying(false);
      }
    }
  };

  // useEffect hook to log component mount and unmount
  useEffect(() => {
    console.log("InputForm mounted");
    return () => console.log("InputForm unmounted");
  }, []);

  return (
    <div className="input-form">
      {/* Form */}
      <form ref={formRef} onSubmit={handleSubmit}>
        <input type="text" name="company_name" placeholder="Company Name" />
        <input
          type="text"
          name="product_details"
          placeholder="Product Details"
        />
        <input
          type="text"
          name="organization_size"
          placeholder="Organization Size"
        />
        <input
          type="text"
          name="product_differentiator"
          placeholder="Product Differentiator"
        />
        <button type="submit" disabled={isLoading}>
          {isLoading ? "Loading..." : "Generate Ad Script"}
        </button>
      </form>

      {/* Audio player */}
      <div className="audio-player">
        <audio ref={audioRef} src="/ad_script_audio.mp3" preload="auto" />
        <button onClick={togglePlayPause}>
          {isPlaying ? "Pause" : "Play"}
        </button>
      </div>

      {/* Ad script display */}
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