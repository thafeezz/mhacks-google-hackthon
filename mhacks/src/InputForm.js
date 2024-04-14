import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import "./InputForm.css"; // Ensure the CSS file is in the same directory

const InputForm = () => {
  const [adScript, setAdScript] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [error, setError] = useState(null);

  const audioRef = useRef(null);
  const formRef = useRef(null);

  const getFormData = () => {
    const formData = new FormData(formRef.current);
    return {
      company_name: formData.get("company_name"),
      product_details: formData.get("product_details"),
      organization_size: formData.get("organization_size"),
      product_differentiator: formData.get("product_differentiator"),
    };
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    const data = getFormData();

    try {
      const response = await axios.post("http://localhost:8000/genad/", data);
      const ad_script = response.data.ad_script;
      setAdScript(ad_script);
    } catch (error) {
      console.error("Error calling API:", error);
      setError("Failed to fetch data. Please try again.");
      setAdScript("");
    }

    setIsLoading(false);
  };

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

  useEffect(() => {
    console.log("InputForm mounted");
    return () => console.log("InputForm unmounted");
  }, []);

  return (
    <div className="input-form">
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

      <div className="audio-player">
        <audio ref={audioRef} src="/ad_script_audio.mp3" preload="auto" />
        <button onClick={togglePlayPause}>
          {isPlaying ? "Pause" : "Play"}
        </button>
        {adScript && !error && (
          <button
            onClick={() => {
              const link = document.createElement("a");
              link.href = audioRef.current.src;
              link.download = "GeneratedAd.mp3";
              document.body.appendChild(link);
              link.click();
              document.body.removeChild(link);
            }}
          >
            Download Audio
          </button>
        )}
      </div>

      <div className="ad-script-section">
        {error ? (
          <div className="error">{error}</div>
        ) : (
          <div className="ad-script">
            {isLoading ? (
              <div className="loading">Loading...</div>
            ) : (
              <div>{adScript}</div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default InputForm;
