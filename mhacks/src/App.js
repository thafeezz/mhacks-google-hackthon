// App.js
import React from "react";
import InputForm from "./InputForm";
import "./App.css"; // Importing the new styles

const App = () => {
  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Hello, there!</h1>
        <h2>Generate your custom advertisement below by answering the four question in their boxes.</h2>
      </header>
      <main className="app-main">
        <InputForm />
      </main>
    </div>
  );
};

export default App;
