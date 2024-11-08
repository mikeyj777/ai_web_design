// App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
// import WebPageGenerator from './components/WebPageGenerator';
import WeatherDisplay from './components/WeatherDisplay';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        {/* <Route path="/web-page-generator" element=WebPageGenerator />} /> */}
        <Route path="/weather-display" element={<WeatherDisplay />} />
      </Routes>
    </Router>
  );
}

export default App;