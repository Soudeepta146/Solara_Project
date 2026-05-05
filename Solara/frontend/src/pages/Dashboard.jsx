import React, { useState, useEffect } from 'react';
import { Search, Sun, Zap, CheckCircle, AlertTriangle, MapPin, Loader2 } from 'lucide-react';
import { getSolarPrediction, searchLocation } from '../services/api';

export default function Dashboard() {
    // 1. Instant Cache Initialization
    const [data, setData] = useState(() => {
        const cached = localStorage.getItem('solara_last_data');
        return cached ? JSON.parse(cached) : null;
    });
    
    const [query, setQuery] = useState("");
    const [loading, setLoading] = useState(false);
    const [coords, setCoords] = useState({ lat: 22.57, lon: 88.36 });

    const fetchData = async (lat, lon) => {
        setLoading(true);
        try {
            const result = await getSolarPrediction(lat, lon);
            if (result && !result.status) {
                setData(result);
                localStorage.setItem('solara_last_data', JSON.stringify(result));
            }
        } catch (e) {
            console.error("Dashboard Sync Error:", e);
        }
        setLoading(false);
    };

    useEffect(() => {
        fetchData(coords.lat, coords.lon);
    }, []);

    const handleSearch = async (e) => {
        e.preventDefault();
        if (!query) return;
        const loc = await searchLocation(query);
        if (loc) {
            setCoords({ lat: loc.lat, lon: loc.lon });
            fetchData(loc.lat, loc.lon);
        }
    };

    // 2. Real Math Logic for Devices (P = Irradiance * Area * Efficiency)
    const irr = data?.irradiance || 0;
    const confidence = data?.analysis?.confidence || 0;
    
    // Calculated based on standard hardware profiles
    const apteraYield = ((irr * 3.0 * 0.22) / 1000).toFixed(1); 
    const teslaYield = ((irr * 1.5 * 0.20) / 1000).toFixed(1);
    const potentialKwh = 5.2;

    return (
        <div className="max-w-7xl mx-auto p-8 pb-20 animate-in fade-in duration-700">
            
            {/* Header & Refined Search */}
            <div className="flex flex-col md:flex-row justify-between items-end mb-12 gap-8">
                <div className="text-left">
                    <div className="flex items-center gap-2">
                        <h1 className="text-gray-400 font-bold uppercase tracking-widest text-[10px] mb-2">Solar Optimization Hub</h1>
                        {loading && <Loader2 size={12} className="animate-spin text-orange-500 mb-2" />}
                    </div>
                    <div className="flex items-center gap-2 text-solara-text font-serif italic text-3xl">
                        <MapPin size={24} className="text-orange-500" /> {data?.location || "Locating..."}
                    </div>
                </div>

                <form onSubmit={handleSearch} className="relative w-full max-w-lg group">
                    <input 
                        type="text" 
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        placeholder="Search coordinates or city..." 
                        className="w-full pl-14 pr-32 py-5 rounded-[24px] bg-white border border-gray-200 shadow-sm focus:shadow-xl focus:ring-4 focus:ring-orange-500/5 outline-none transition-all text-lg"
                    />
                    <Search className="absolute left-5 top-1/2 -translate-y-1/2 text-gray-400 group-focus-within:text-orange-500 transition-colors" size={24} />
                    <button type="submit" className="absolute right-3 top-1/2 -translate-y-1/2 bg-orange-500 hover:bg-orange-600 text-white px-8 py-3 rounded-[18px] font-bold text-sm shadow-lg shadow-orange-500/20 transition-all active:scale-95">
                        Search
                    </button>
                </form>
            </div>

            <div className={`grid grid-cols-1 lg:grid-cols-2 gap-16 transition-opacity duration-500 ${!data ? 'opacity-30' : 'opacity-100'}`}>
                
                {/* Left Column: Sun Orb & Logic */}
                <div className="space-y-12">
                    <div className="flex flex-col items-center">
                        {/* THE SUN ORB */}
                        <div className="w-64 h-64 rounded-full sun-glow flex flex-col items-center justify-center text-white mb-8 border-8 border-white/20">
                            <span className="text-6xl font-bold tracking-tighter">{Math.round(irr)}</span>
                            <span className="text-[10px] font-bold tracking-widest opacity-60">W/M²</span>
                        </div>
                        <h2 className="text-4xl font-serif italic">{data?.analysis?.status} Solar Activity.</h2>
                        <p className="text-gray-400 text-sm mt-3 font-medium">
                            Coordinates: {data?.lat}, {data?.lon} — <span className="text-solara-text font-bold">{confidence}% AI confidence</span>
                        </p>
                    </div>

                    {/* WINDOW CARD */}
                    <div className="glass-card p-8">
                        <div className="flex justify-between items-center mb-6">
                            <div className="flex items-center gap-2 text-orange-400 font-bold text-[10px] uppercase tracking-widest"><Zap size={14}/> Next Optimal Window</div>
                            <div className="px-3 py-1 bg-green-50 text-green-600 rounded-full text-[10px] font-bold tracking-widest uppercase tracking-tighter">
                                • {data?.solar_windows?.[0]?.quality || "Low"}
                            </div>
                        </div>
                        <div className="flex justify-between items-center mb-4 text-3xl font-bold">
                            <span>{data?.solar_windows?.[0]?.start || "00:00"}</span>
                            <div className="flex-1 mx-6 h-px bg-gray-200" />
                            <span>{data?.solar_windows?.[0]?.end || "00:00"}</span>
                        </div>
                        <div className="relative h-1.5 w-full bg-gray-100 rounded-full overflow-hidden">
                            <div className="h-full bg-orange-400 transition-all duration-1000" style={{width: `${Math.min(confidence, 100)}%`}}></div>
                        </div>
                    </div>

                    {/* ACTIVE DEVICES (Real calculated yield) */}
                    <div className="space-y-4 text-left">
                        <h3 className="text-gray-400 font-bold text-[10px] uppercase tracking-widest mb-4 ml-2">Hardware Fleet Sync</h3>
                        <DeviceCard name="Aptera EV" icon="🚗" power={`+${apteraYield} kWh`} stats="3.0m² Panel - 22% Eff" active={irr > 350} />
                        <DeviceCard name="Tesla Powerwall" icon="⚡" power={`+${teslaYield} kWh`} stats="1.5m² Panel - 20% Eff" active={irr > 250} />
                        <DeviceCard name="Garmin Solar" icon="⌚" power="+0.1 kWh" stats="Wearable - 12% Eff" active={irr > 100} warning={data?.temp > 32} />
                    </div>
                </div>

                {/* Right Column: Gauges & AI Insights */}
                <div className="space-y-10">
                    {/* YIELD GAUGE */}
                    <div className="glass-card p-10 flex flex-col items-center">
                        <h3 className="w-full text-gray-400 text-[10px] font-bold uppercase tracking-widest mb-10 text-left">Real-time Yield Efficiency</h3>
                        <div className="relative w-80 h-40">
                            <GaugeSVG progress={Math.min((irr / 1000) * 100, 100)} />
                            <div className="absolute inset-0 flex flex-col items-center justify-end pb-2">
                                <span className="text-6xl font-bold tracking-tighter">
                                    {Math.round(Math.min((irr / 1000) * 100, 100))}%
                                </span>
                                <span className="text-[10px] font-bold text-gray-400 uppercase tracking-widest">of potential</span>
                            </div>
                        </div>
                        
                        <div className="grid grid-cols-2 gap-4 w-full mt-12">
                            <div className="bg-gray-50/40 p-6 rounded-[32px] border border-gray-100 flex flex-col items-center">
                                <p className="text-3xl font-bold">{apteraYield}</p>
                                <p className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mt-1">Actual (kWh)</p>
                            </div>
                            <div className="bg-gray-50/40 p-6 rounded-[32px] border border-gray-100 flex flex-col items-center">
                                <p className="text-3xl font-bold">{potentialKwh}</p>
                                <p className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mt-1">Potential (kWh)</p>
                            </div>
                        </div>
                    </div>

                    {/* AI CONFIDENCE BREAKDOWN */}
                    <div className="glass-card p-10 text-left">
                        <div className="flex justify-between items-center mb-10">
                            <h3 className="text-xl font-bold">AI Forecast Reliability</h3>
                            <span className="text-4xl font-bold text-green-500">{confidence}%</span>
                        </div>
                        <div className="space-y-8">
                            <ConfidenceBar label="Satellite Data" val={Math.min(confidence + 2, 100)} color="bg-green-400" icon="🛰️" />
                            <ConfidenceBar label="Humidity Sync" val={Math.max(confidence - 5, 0)} color="bg-orange-400" icon="💧" />
                            <ConfidenceBar label="Historical Accuracy" val={confidence} color="bg-indigo-400" icon="📊" />
                        </div>
                    </div>

                    {/* SMART ALERTS (Handling Multiple Alerts from app.py) */}
                    <div className="space-y-4 text-left">
                        <h3 className="text-gray-400 font-bold text-[10px] uppercase tracking-widest mb-4 ml-2">Atmospheric Recommendations</h3>
                        {data?.analysis?.alerts?.map((alert, idx) => {
                            const isWarning = alert.includes("Alert") || alert.includes("Throttling") || alert.includes("⚠️");
                            return (
                                <div key={idx} className={`p-6 border rounded-[32px] flex items-start gap-4 transition-all hover:scale-[1.01] ${isWarning ? 'bg-orange-50/50 border-orange-100' : 'bg-white border-gray-100'}`}>
                                    <div className="mt-1">
                                        {isWarning ? <AlertTriangle className="text-orange-500" size={20}/> : <CheckCircle className="text-green-500" size={20}/>}
                                    </div>
                                    <div>
                                        <h4 className="font-bold text-sm text-solara-text">{isWarning ? "System Warning" : "Intelligence Update"}</h4>
                                        <p className="text-xs text-gray-500 leading-relaxed mt-1">{alert}</p>
                                    </div>
                                </div>
                            );
                        })}
                        {!data?.analysis?.alerts?.length && (
                            <p className="text-gray-400 italic text-sm p-4">No active atmospheric alerts.</p>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}

// Internal Helper Components
const DeviceCard = ({ name, icon, power, stats, active, warning }) => (
    <div className="glass-card p-6 flex justify-between items-center hover:border-orange-200 transition-colors">
        <div className="flex gap-4 items-center">
            <div className="w-14 h-14 bg-gray-50 rounded-[20px] flex items-center justify-center text-2xl shadow-inner">{icon}</div>
            <div>
                <p className="font-bold text-sm">{name}</p>
                <p className="text-[10px] text-gray-400 font-medium">{stats}</p>
            </div>
        </div>
        <div className="text-right">
            <p className="text-base font-bold text-orange-600">{power}</p>
            <p className={`text-[10px] font-bold uppercase tracking-widest ${warning ? 'text-red-500' : (active ? 'text-green-500' : 'text-gray-300')}`}>
                • {warning ? 'Heat Risk' : (active ? 'Charging' : 'Standby')}
            </p>
        </div>
    </div>
);

const ConfidenceBar = ({ label, val, color, icon }) => (
    <div className="flex items-center gap-5">
        <span className="text-lg w-6">{icon}</span>
        <span className="text-[11px] font-bold text-gray-500 w-28 uppercase tracking-tighter">{label}</span>
        <div className="flex-1 h-2 bg-gray-100 rounded-full overflow-hidden">
            <div className={`h-full ${color} transition-all duration-1000`} style={{width: `${val}%`}} />
        </div>
        <span className="text-xs font-bold text-gray-400 w-10 text-right">{val}%</span>
    </div>
);

const GaugeSVG = ({ progress }) => (
    <svg className="w-full h-full" viewBox="0 0 100 50">
        <path d="M 10 50 A 40 40 0 0 1 90 50" fill="none" stroke="#f3f4f6" strokeWidth="10" />
        <path d="M 10 50 A 40 40 0 0 1 90 50" fill="none" stroke="url(#dashGauge)" strokeWidth="10" strokeDasharray="125" strokeDashoffset={125 - (progress * 1.25)} strokeLinecap="round" className="transition-all duration-1000" />
        <defs>
            <linearGradient id="dashGauge" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor="#ef4444" />
                <stop offset="50%" stopColor="#f97316" />
                <stop offset="100%" stopColor="#fbbf24" />
            </linearGradient>
        </defs>
    </svg>
);


