import Navbar from "../../components/sections/navbar/default";
import { LayoutLines } from "../../components/ui/layout-lines";
import { Cpu, Activity, ShieldCheck, BarChart3, Server, Terminal } from "lucide-react";

export default function HowItWorks() {
  return (
    <main className="bg-background text-foreground min-h-screen w-full relative overflow-hidden">
      <LayoutLines />
      <Navbar />

      {/* --- BACKGROUND GLOW (Purple/Blue enterprise feel) --- */}
      <div 
        className="absolute top-0 left-0 w-full h-[500px] -z-10"
        style={{
          background: "radial-gradient(ellipse 80% 50% at 50% -20%, rgba(124, 58, 237, 0.15), rgba(0, 0, 0, 0))"
        }}
      />

      <div className="container mx-auto px-4 pt-32 pb-20">
        
        {/* HEADER */}
        <div className="text-center mb-20">
          <h1 className="text-4xl md:text-6xl font-bold mb-6 tracking-tight">
            Dual-Stream <span className="text-purple-500">Architecture</span>
          </h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            A hybrid system that protects the employee in real-time while empowering management with long-term insights.
          </p>
        </div>

        {/* --- THE PIPELINE GRID --- */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-24 relative">
            
            {/* Connector Line (Desktop Only) */}
            <div className="hidden md:block absolute top-1/2 left-0 w-full h-0.5 bg-gradient-to-r from-purple-500/0 via-purple-500/50 to-purple-500/0 -z-10 transform -translate-y-1/2" />

            {/* Step 1: Capture */}
            <PipelineCard 
                icon={<Activity className="w-8 h-8 text-blue-400" />}
                title="1. Edge Capture"
                desc="Raspberry Pi streams raw video directly to the local workstation via low-latency MJPEG."
                badge="Raspberry Pi"
            />

            {/* Step 2: Processing */}
            <PipelineCard 
                icon={<Cpu className="w-8 h-8 text-purple-400" />}
                title="2. Pose Estimation"
                desc="Local machine runs MediaPipe to detect skeletal landmarks and calculate spine curvature."
                badge="Python + CV"
            />

            {/* Step 3: User Loop */}
            <PipelineCard 
                icon={<ShieldCheck className="w-8 h-8 text-green-400" />}
                title="3. Live Protection"
                desc="Immediate visual feedback alerts the user if their posture deviates from safe ergonomics."
                badge="Real-time"
            />

            {/* Step 4: Manager Loop */}
            <PipelineCard 
                icon={<BarChart3 className="w-8 h-8 text-orange-400" />}
                title="4. Business Trends"
                desc="Aggregated health data is anonymized and sent to the cloud for management reporting."
                badge="MongoDB"
            />
        </div>

        {/* --- SPLIT SECTION: TERMINAL & SPECS --- */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            
            {/* LEFT: The "Fake" Terminal */}
            <div className="rounded-xl overflow-hidden border border-white/10 bg-[#0d1117] shadow-2xl font-mono text-sm">
                <div className="bg-[#161b22] px-4 py-2 border-b border-white/5 flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full bg-red-500/80" />
                    <div className="w-3 h-3 rounded-full bg-yellow-500/80" />
                    <div className="w-3 h-3 rounded-full bg-green-500/80" />
                    <span className="ml-2 text-xs text-muted-foreground">worker@workstation:~/security_audit</span>
                </div>
                <div className="p-6 text-gray-300 space-y-2">
                    <p className="text-green-400">$ python3 posture_guard.py --audit-mode</p>
                    <p>[INIT] Video Stream established (10ms latency)</p>
                    <p>[MEDIAPIPE] Skeletal tracking active...</p>
                    <br />
                    {/* The "Live" part */}
                    <p className="text-gray-500"># User Feedback Loop</p>
                    <p>[INFO] Posture Score: 98% (Good)</p>
                    <p>[INFO] Posture Score: 95% (Good)</p>
                    <p className="text-red-400 font-bold">⚠ [ALERT] SLOUCH DETECTED! (Spine Angle: 45°)</p>
                    <p className="text-red-400"># Sending HUD Notification to User...</p>
                    <br />
                    {/* The "Manager" part */}
                    <p className="text-gray-500"># Business Intelligence Loop</p>
                    <p className="text-blue-400 animate-pulse">● [UPLOAD] Pushing trend_batch_04.json to MongoDB...</p>
                    <p className="text-blue-400"># Manager Dashboard updated.</p>
                </div>
            </div>

            {/* RIGHT: Technical Specs */}
            <div className="space-y-8">
                <div>
                    <h3 className="text-2xl font-semibold mb-2 flex items-center gap-2">
                        <Server className="w-6 h-6" /> Enterprise Ready
                    </h3>
                    <p className="text-muted-foreground">
                        Designed for the modern office. We separate immediate ergonomic correction from long-term health analytics, ensuring privacy and speed.
                    </p>
                </div>

                <div className="grid grid-cols-2 gap-4">
                    <SpecItem label="Feedback Speed" value="< 50ms" />
                    <SpecItem label="Privacy" value="Anonymized" />
                    <SpecItem label="AI Model" value="MediaPipe" />
                    <SpecItem label="Data Retention" value="30 Days" />
                </div>
            </div>

        </div>

        {/* FOOTER AREA */}
        <div className="mt-32 border-t border-white/10 pt-8 text-center text-muted-foreground text-sm">
            <p>Engineered at Hacklahoma 2026</p>
        </div>

      </div>
    </main>
  );
}

// --- HELPER COMPONENTS ---

function PipelineCard({ icon, title, desc, badge }: { icon: any, title: string, desc: string, badge: string }) {
    return (
        <div className="relative p-6 rounded-2xl border border-white/10 bg-white/5 backdrop-blur-sm hover:bg-white/10 transition-all duration-300 group h-full">
            <div className="mb-4 bg-white/5 w-12 h-12 rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform shadow-lg shadow-black/50">
                {icon}
            </div>
            <div className="absolute top-4 right-4 text-xs font-mono px-2 py-1 rounded bg-white/10 text-muted-foreground border border-white/5">
                {badge}
            </div>
            <h3 className="text-lg font-semibold mb-2 text-foreground">{title}</h3>
            <p className="text-sm text-muted-foreground leading-relaxed">
                {desc}
            </p>
        </div>
    )
}

function SpecItem({ label, value }: { label: string, value: string }) {
    return (
        <div className="p-4 rounded-lg border border-white/5 bg-white/[0.02]">
            <div className="text-sm text-muted-foreground mb-1">{label}</div>
            <div className="text-xl font-mono font-bold text-foreground">{value}</div>
        </div>
    )
}