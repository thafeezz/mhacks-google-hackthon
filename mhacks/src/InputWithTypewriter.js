import React, { useState } from "react";
import axios from "axios";
import "./App.css"; // Ensure this CSS file is set up properly
import TypewriterEffect from "./TypewriterEffect";

const InputForm = () => {
  const [formData, setFormData] = useState({
    company_name: "",
    product_details: "",
    organization_size: "",
    product_differentiator: "",
  });
  const [adScript, setAdScript] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log(formData);
    try {
      const response = await axios.post(
        "http://localhost:8000/genad/",
        formData
      );
      setAdScript(response.data.ad_script);
    } catch (error) {
      console.error("Error calling API:", error);
      setAdScript("Failed to fetch data."); // Handle error with user feedback
    }
  };

  return (
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
      <button type="submit">Generate Ad Script</button>
      <div className="ad-script">
        <TypewriterEffect text={adScript} />
      </div>
    </form>
  );
};

export default InputForm;
