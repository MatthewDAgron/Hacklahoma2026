"use client";

import Navbar from "../../components/sections/navbar/default";
import { LayoutLines } from "../../components/ui/layout-lines";
import { Activity, AlertTriangle, Camera, CheckCircle, Clock, Server, User } from "lucide-react";
import { useEffect, useState } from "react";

/** Stream URL: same host as page, port 5001 (posture_stream_server) */
function PostureStream() {
  const [src, setSrc] = useState<string | null>(null);
  useEffect(() => {
    if (typeof window !== "undefined") {
      setSrc(`http://${window.location.hostname}:5001/video_feed`);
    }
  }, []);
  if (!src) return <div className="w-full h-full flex items-center justify-center text-white/40 text-sm">Loading stream...</div>;
  return <img src={src} alt="Live Posture Detection Feed" className="w-full h-full object-contain" />;
}

export default function LiveMetrics() {
  return (
    <main className="bg-background text-foreground min-h-screen w-full relative overflow-hidden">
      <LayoutLines />
      <Navbar />

      {/* --- DASHBOARD GLOW (Green/Teal for "System Online" vibe) --- */}
      <div 
        className="absolute top-0 left-0 w-full h-[500px] -z-10"
        style={{
          background: "radial-gradient(ellipse 80% 50% at 50% -20%, rgba(16, 185, 129, 0.15), rgba(0, 0, 0, 0))"
        }}
      />

      <div className="container mx-auto px-4 pt-24 pb-20">
        
        {/* HEADER */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
            <div>
                <h1 className="text-3xl font-bold tracking-tight">Live Operations Console</h1>
                <p className="text-muted-foreground">Real-time telemetry from Workstation Alpha.</p>
            </div>
            <div className="flex items-center gap-3">
                <span className="flex items-center gap-2 text-xs font-mono bg-green-500/10 text-green-400 px-3 py-1 rounded-full border border-green-500/20">
                    <span className="relative flex h-2 w-2">
                      <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                      <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
                    </span>
                    SYSTEM ONLINE
                </span>
                <span className="text-xs font-mono text-muted-foreground">Last Sync: 0s ago</span>
            </div>
        </div>

        {/* --- TOP ROW: KPI CARDS --- */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
            <StatCard 
                label="Avg. Posture Score" 
                value="94%" 
                icon={<Activity className="text-blue-400" />} 
                trend="+2.4%" 
                trendUp={true}
            />
            <StatCard 
                label="Active Alerts" 
                value="0" 
                icon={<AlertTriangle className="text-green-400" />} 
                subtext="All systems nominal"
            />
            <StatCard 
                label="Session Duration" 
                value="4h 12m" 
                icon={<Clock className="text-purple-400" />} 
            />
            <StatCard 
                label="Employee ID" 
                value="#8821" 
                icon={<User className="text-orange-400" />} 
                subtext="Workstation 01"
            />
        </div>

        {/* --- MAIN GRID: VIDEO vs DATA --- */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
            
            {/* LEFT: Live Video Feed */}
            <div className="lg:col-span-2 rounded-xl border border-white/10 bg-black/40 overflow-hidden relative group">
                <div className="absolute top-4 left-4 z-10 flex gap-2">
                    <span className="bg-red-500/80 text-white text-[10px] font-bold px-2 py-1 rounded flex items-center gap-1">
                        <Camera size={12} /> LIVE
                    </span>
                </div>
                
                {/* Live posture stream: Pi feed → posture_stream_server (bbl_test_task) → MJPEG */}
                <div className="aspect-video bg-neutral-900 relative overflow-hidden">
                    <PostureStream />
                </div>

                {/* Video Footer */}
                <div className="p-4 border-t border-white/10 flex justify-between items-center bg-white/5">
                    <div className="text-xs font-mono text-muted-foreground">
                        Posture Detection (bbl_test_task) | Live
                    </div>
                    <button className="text-xs bg-white/10 hover:bg-white/20 px-3 py-1 rounded text-white transition">
                        Expand View
                    </button>
                </div>
            </div>

            {/* RIGHT: Quick Trends (The "Manager" View) */}
            <div className="rounded-xl border border-white/10 bg-white/5 p-6 flex flex-col">
                <h3 className="font-semibold mb-6 flex items-center gap-2">
                    <Activity size={18} /> Trend Analysis
                </h3>
                
                {/* Fake Graph Bars */}
                <div className="flex-1 flex items-end gap-2 h-40 mb-4 px-2">
                    {[40, 65, 45, 80, 55, 70, 85, 60, 90, 75].map((h, i) => (
                        <div key={i} className="flex-1 bg-blue-500/20 rounded-t hover:bg-blue-500/50 transition-all relative group" style={{ height: `${h}%` }}>
                            {/* Tooltip on hover */}
                            <div className="absolute -top-8 left-1/2 -translate-x-1/2 bg-black text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition">
                                {h}%
                            </div>
                        </div>
                    ))}
                </div>
                <div className="flex justify-between text-xs text-muted-foreground font-mono">
                    <span>10:00 AM</span>
                    <span>Current</span>
                </div>

                <div className="mt-8 space-y-4">
                    <div className="flex justify-between items-center text-sm">
                        <span className="text-muted-foreground">Spine Angle</span>
                        <span className="text-green-400 font-mono">15° (Safe)</span>
                    </div>
                    <div className="w-full bg-white/10 h-1.5 rounded-full overflow-hidden">
                        <div className="bg-green-500 h-full w-[15%]"></div>
                    </div>

                    <div className="flex justify-between items-center text-sm mt-4">
                        <span className="text-muted-foreground">Neck Tilt</span>
                        <span className="text-yellow-400 font-mono">25° (Warning)</span>
                    </div>
                    <div className="w-full bg-white/10 h-1.5 rounded-full overflow-hidden">
                        <div className="bg-yellow-500 h-full w-[45%]"></div>
                    </div>
                </div>
            </div>
        </div>

        {/* --- BOTTOM ROW: LOGS --- */}
        <div className="rounded-xl border border-white/10 bg-black/20 overflow-hidden">
            <div className="bg-white/5 px-6 py-3 border-b border-white/5 flex justify-between items-center">
                <h3 className="text-sm font-semibold flex items-center gap-2">
                    <Server size={14} /> System Events
                </h3>
                <span className="text-[10px] font-mono text-muted-foreground">LIVE TAIL</span>
            </div>
            <div className="p-0">
                <table className="w-full text-sm text-left">
                    <thead className="text-xs text-muted-foreground bg-white/5 font-mono uppercase">
                        <tr>
                            <th className="px-6 py-3">Timestamp</th>
                            <th className="px-6 py-3">Level</th>
                            <th className="px-6 py-3">Message</th>
                            <th className="px-6 py-3">Source</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-white/5 font-mono text-xs">
                        <LogRow time="10:42:05" level="INFO" msg="Posture Check: OK (Score 98)" source="Worker_Node" color="text-green-400" />
                        <LogRow time="10:42:02" level="INFO" msg="Frame batch uploaded to Atlas" source="Sync_Service" color="text-blue-400" />
                        <LogRow time="10:41:55" level="WARN" msg="Neck tilt detected > 20 degrees" source="CV_Model" color="text-yellow-400" />
                        <LogRow time="10:41:50" level="INFO" msg="User session started" source="Auth_System" color="text-gray-400" />
                    </tbody>
                </table>
            </div>
        </div>

      </div>
    </main>
  );
}

// --- SUB COMPONENTS ---

function StatCard({ label, value, icon, trend, trendUp, subtext }: any) {
    return (
        <div className="p-6 rounded-xl border border-white/10 bg-white/5 backdrop-blur-sm">
            <div className="flex justify-between items-start mb-4">
                <div className="text-muted-foreground text-sm font-medium">{label}</div>
                <div className="p-2 bg-white/5 rounded-lg">{icon}</div>
            </div>
            <div className="text-3xl font-bold mb-1">{value}</div>
            
            {subtext && <div className="text-xs text-muted-foreground">{subtext}</div>}
            
            {trend && (
                <div className={`text-xs font-medium flex items-center gap-1 ${trendUp ? 'text-green-400' : 'text-red-400'}`}>
                    {trendUp ? '↑' : '↓'} {trend} vs last hour
                </div>
            )}
        </div>
    )
}

function LogRow({ time, level, msg, source, color }: any) {
    return (
        <tr className="hover:bg-white/5 transition-colors">
            <td className="px-6 py-3 text-muted-foreground">{time}</td>
            <td className={`px-6 py-3 ${color}`}>{level}</td>
            <td className="px-6 py-3 text-gray-300">{msg}</td>
            <td className="px-6 py-3 text-muted-foreground">{source}</td>
        </tr>
    )
}