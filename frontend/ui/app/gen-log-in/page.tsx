"use client";

import Navbar from "../../components/sections/navbar/default";
import { LayoutLines } from "../../components/ui/layout-lines";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import { Lock, User, ShieldAlert, ArrowRight } from "lucide-react";
import Link from "next/link";
import { useState } from "react";

export default function LoginPage() {
  const [role, setRole] = useState<"user" | "admin">("user");
  const [loading, setLoading] = useState(false);

  // Fake "Loading" state for realism
  const handleLogin = () => {
    setLoading(true);
    setTimeout(() => {
        // In a real app, this would redirect. 
        // For the hackathon, just link the button to /live-metrics
        window.location.href = "/live-metrics"; 
    }, 1500);
  };

  return (
    <main className="bg-background text-foreground min-h-screen w-full relative overflow-hidden flex flex-col">
      <LayoutLines />
      <Navbar />

      {/* --- BACKGROUND GLOW (Subtle Red/Blue mix) --- */}
      <div 
        className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] -z-10"
        style={{
          background: "radial-gradient(ellipse 60% 60% at 50% 50%, rgba(59, 130, 246, 0.1), rgba(0, 0, 0, 0))"
        }}
      />

      <div className="flex-1 flex items-center justify-center p-4">
        
        {/* LOGIN CARD */}
        <div className="w-full max-w-md bg-white/5 border border-white/10 rounded-2xl p-8 backdrop-blur-xl shadow-2xl relative overflow-hidden">
            
            {/* Top Decoration Line */}
            <div className={`absolute top-0 left-0 w-full h-1 ${role === 'admin' ? 'bg-red-500' : 'bg-blue-500'} transition-colors duration-500`} />

            <div className="text-center mb-8">
                <div className={`inline-flex items-center justify-center w-16 h-16 rounded-full mb-4 ${role === 'admin' ? 'bg-red-500/10 text-red-400' : 'bg-blue-500/10 text-blue-400'} transition-colors duration-500`}>
                    {role === 'admin' ? <ShieldAlert size={32} /> : <User size={32} />}
                </div>
                <h1 className="text-2xl font-bold tracking-tight">Welcome Back</h1>
                <p className="text-muted-foreground text-sm mt-2">
                    Enter your credentials to access the TrendVision portal.
                </p>
            </div>

            {/* Role Toggle */}
            <div className="flex bg-black/20 p-1 rounded-lg mb-6 border border-white/5">
                <button 
                    onClick={() => setRole("user")}
                    className={`flex-1 text-xs font-medium py-2 rounded-md transition-all ${role === "user" ? "bg-white/10 text-white shadow-sm" : "text-muted-foreground hover:text-white"}`}
                >
                    Employee
                </button>
                <button 
                    onClick={() => setRole("admin")}
                    className={`flex-1 text-xs font-medium py-2 rounded-md transition-all ${role === "admin" ? "bg-red-500/20 text-red-200 shadow-sm" : "text-muted-foreground hover:text-white"}`}
                >
                    Administrator
                </button>
            </div>

            {/* FORM */}
            <div className="space-y-4">
                <div className="space-y-2">
                    <label className="text-xs font-medium text-muted-foreground ml-1">
                        {role === 'admin' ? 'Admin ID' : 'Employee ID'}
                    </label>
                    <div className="relative">
                        <User className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground" />
                        <Input 
                            placeholder={role === 'admin' ? "ADMIN-001" : "EMP-8821"} 
                            className="pl-9 bg-black/20 border-white/10 focus-visible:ring-blue-500"
                        />
                    </div>
                </div>

                <div className="space-y-2">
                    <label className="text-xs font-medium text-muted-foreground ml-1">Password</label>
                    <div className="relative">
                        <Lock className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground" />
                        <Input 
                            type="password" 
                            placeholder="••••••••" 
                            className="pl-9 bg-black/20 border-white/10 focus-visible:ring-blue-500"
                        />
                    </div>
                </div>

                <Button 
                    className={`w-full mt-6 ${role === 'admin' ? 'bg-red-600 hover:bg-red-700' : 'bg-blue-600 hover:bg-blue-700'}`}
                    size="lg"
                    onClick={handleLogin}
                    disabled={loading}
                >
                    {loading ? (
                        <span className="animate-pulse">Authenticating...</span>
                    ) : (
                        <span className="flex items-center gap-2">Sign In <ArrowRight size={16} /></span>
                    )}
                </Button>
            </div>

            <div className="mt-6 text-center">
                <p className="text-xs text-muted-foreground">
                    Forgot your ID? Contact IT Support at <span className="text-foreground underline cursor-pointer">ext. 4402</span>
                </p>
            </div>

        </div>
      </div>
    </main>
  );
}