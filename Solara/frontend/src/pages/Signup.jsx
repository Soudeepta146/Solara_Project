import React from 'react';
import { Sun } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function Signup() {
    return (
        <div className="min-h-[80vh] flex items-center justify-center">
            <div className="glass-card p-10 w-full max-w-md text-center">
                {/* <div className="bg-orange-500 w-12 h-12 rounded-xl flex items-center justify-center mx-auto mb-6">
                    <Sun className="text-white" />
                </div> */}
                <span className="text-4xl"> ☀️ </span>
                <h2 className="text-2xl font-serif  mb-2">Join Solara</h2>
                <p className="text-gray-500 text-sm mb-8">Start optimizing your energy today.</p>
                
                <form className="space-y-4" onSubmit={(e) => e.preventDefault()}>
                    <input type="text" placeholder="Full Name" className="w-full px-5 py-3 rounded-2xl bg-gray-100 border-none outline-none focus:ring-2 focus:ring-orange-500/20" />
                    <input type="email" placeholder="Email" className="w-full px-5 py-3 rounded-2xl bg-gray-100 border-none outline-none focus:ring-2 focus:ring-orange-500/20" />
                    <input type="password" placeholder="Password" className="w-full px-5 py-3 rounded-2xl bg-gray-100 border-none outline-none focus:ring-2 focus:ring-orange-500/20" />
                    <button className="w-full py-4 bg-orange-500 text-white rounded-full font-bold shadow-lg shadow-orange-500/20 hover:scale-105 transition-transform">
                        Create Account
                    </button>
                </form>
                
                <p className="mt-6 text-xs text-gray-400">
                    Already have an account? <Link to="/login" className="text-orange-500 font-bold">Log in</Link>
                </p>
            </div>
        </div>
    );
}