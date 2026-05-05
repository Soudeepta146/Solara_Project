import React, { useState, useEffect } from 'react';
import { Sun, MapPin } from 'lucide-react';
import { NavLink, Link } from 'react-router-dom';
import Signup from '../pages/Signup';

export default function Navbar({ location }) {
    const [time, setTime] = useState(new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: false }));

    useEffect(() => {
        const timer = setInterval(() => {
            setTime(new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: false }));
        }, 1000);
        return () => clearInterval(timer);
    }, []);

    // Active link style logic
    const navLinkStyle = ({ isActive }) => 
        `px-6 py-1.5 rounded-full text-sm font-bold transition-all ${
            isActive 
            ? 'bg-white shadow-sm text-solara-text' 
            : 'text-gray-500 hover:text-solara-text'
        }`;

    return (
        <nav className="flex items-center justify-between px-8 py-4 sticky top-0 z-50 bg-solara-bg/80 backdrop-blur-md">
            {/* Logo */}
            <Link to="/" className="flex items-center gap-2">
                {/* <div className="bg-gradient-to-br from-orange-400 to-orange-600 p-2 rounded-xl">
                    <Sun className="text-white" size={20} />
                </div> */}
                <span className="font-bold text-xl tracking-tighter text-solara-text">
                   ☀️ SOLARA
                </span>
            </Link>

            {/* Navigation Links - Updated with Home */}
            <div className="flex bg-gray-200/50 p-1 rounded-full border border-gray-300/30">
                <NavLink to="/" className={navLinkStyle}>Home</NavLink>
                <NavLink to="/dashboard" className={navLinkStyle}>Dashboard</NavLink>
                <NavLink to="/forecast" className={navLinkStyle}>Forecast</NavLink>
                <NavLink to="/signup" className={navLinkStyle}>Signup</NavLink>
            </div>

            {/* Status & Location */}
            <div className="flex items-center gap-6">
                <div className="flex items-center gap-2 px-4 py-1.5 bg-green-100/50 border border-green-200 rounded-full text-green-600 font-bold text-[10px] tracking-widest">
                    <div className="w-1.5 h-1.5 bg-green-500 rounded-full animate-pulse" /> LIVE
                </div>

                <div className="flex items-center gap-2 text-gray-500 text-sm">
                    <MapPin size={16} className="text-orange-500" />
                    <span className="font-semibold">{location}</span>
                    <span className="text-gray-300">|</span>
                    <span className="font-bold text-orange-600">{time}</span>
                </div>
            </div>
        </nav>
    );
}



