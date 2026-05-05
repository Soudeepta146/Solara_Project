import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import Forecast from './pages/Forecast';
import Signup from './pages/Signup';

export default function App() {
    const [locationName, setLocationName] = useState("Bhatpara, West Bengal");

    return (
        /* The 'future' prop here fixes the console warnings */
        <Router future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
            <div className="min-h-screen relative font-sans text-solara-text bg-solara-bg">
                <Navbar location={locationName} />
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/dashboard" element={<Dashboard />} />
                    <Route path="/forecast" element={<Forecast />} />
                    <Route path="/signup" element={<Signup />} />
                </Routes>
            </div>
        </Router>
    );
}



