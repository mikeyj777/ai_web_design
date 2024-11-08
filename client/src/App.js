// App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import WebPageGenerator from './components/WebPageGenerator';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/web-page-generator" element=WebPageGenerator />} />
      </Routes>
    </Router>
  );
}

export default App;