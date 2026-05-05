import React from 'react';
import { Sun, Shield, Zap, Globe, LayoutDashboard, Info } from 'lucide-react';
import { Link } from 'react-router-dom';
import solarBg from '../assets/solar-bg.jpg'; // Path to the image you provided

export default function Home() {
    return (
        <div className="relative min-h-screen w-full overflow-hidden text-white">
            {/* Full Screen Background Image */}
            <div 
                className="absolute inset-0 z-0 bg-cover bg-center"
                style={{ backgroundImage: `url(${solarBg})` }}
            >
                {/* Dark Overlay to make text readable */}
                <div className="absolute inset-0 bg-black/40 backdrop-blur-[2px]"></div>
            </div>

            {/* Content Container */}
            <div className="relative z-10 flex flex-col items-center justify-between min-h-screen px-6 py-20">
                
                {/* Hero Section */}
                <div className="flex flex-col items-center text-center mt-20 max-w-4xl">
                    {/* <div className="bg-orange-500 p-3 rounded-2xl mb-6 shadow-xl animate-pulse">
                        <Sun size={40} className="text-white" />
                    </div> */}
                    <h1 className="text-6xl font-bold tracking-tighter mb-4 drop-shadow-2xl">
                        <span className="text-5xl"> ☀️ </span>
                        Solara
                    </h1>
                    <h2 className="text-2xl font-medium text-orange-200 mb-6 uppercase tracking-widest">
                        AI-Powered Solar Intelligence Platform
                    </h2>
                    <p className="text-lg text-gray-100 max-w-2xl leading-relaxed mb-10 drop-shadow-md">
                        Optimize your energy yields with real-time atmospheric data synchronization. 
                        Our hybrid LSTM AI models provide hyperlocal forecasting and micro-climatic 
                        insights for all your solar-dependent hardware.
                    </p>

                    {/* Action Buttons */}
                    <div className="flex gap-6">
                        <Link 
                            to="/dashboard" 
                            className="flex items-center gap-2 px-8 py-4 bg-orange-500 hover:bg-orange-600 rounded-xl font-bold transition-all shadow-lg hover:scale-105"
                        >
                            <LayoutDashboard size={20} /> Open Dashboard
                        </Link>
                        <Link 
                            to="/forecast" 
                            className="flex items-center gap-2 px-8 py-4 bg-white/10 hover:bg-white/20 backdrop-blur-md border border-white/30 rounded-xl font-bold transition-all hover:scale-105"
                        >
                            <Info size={20} /> Learn More
                        </Link>
                    </div>
                </div>

                {/* Bottom Feature Cards - Glassmorphism style from reference */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8 w-full max-w-6xl mt-12">
                    <FeatureCard 
                        icon={<Globe className="text-blue-400" />} 
                        title="Live Weather Tracking" 
                        desc="Ensemble data ingestion from Tomorrow.io and Meteomatics for 100% precision."
                    />
                    <FeatureCard 
                        icon={<Zap className="text-orange-400" />} 
                        title="AI Forecasting" 
                        desc="72-hour forecast of solar yield with 15-minute granularity using LSTM layers."
                    />
                    <FeatureCard 
                        icon={<Shield className="text-green-400" />} 
                        title="Device Optimization" 
                        desc="Real-time recommendation logic for EVs, Powerwalls, and Garmin wearables."
                    />
                </div>
            </div>
        </div>
    );
}

function FeatureCard({ icon, title, desc }) {
    return (
        <div className="bg-white/10 backdrop-blur-xl border border-white/20 p-8 rounded-[32px] hover:bg-white/15 transition-all group">
            <div className="mb-4 group-hover:scale-110 transition-transform">{icon}</div>
            <h3 className="text-xl font-bold mb-2">{title}</h3>
            <p className="text-gray-300 text-sm leading-relaxed">{desc}</p>
        </div>
    );
}

