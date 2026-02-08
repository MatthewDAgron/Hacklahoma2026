import Navbar from "../../components/sections/navbar/default";
import { LayoutLines } from "../../components/ui/layout-lines";
import { Cpu, Code, HelpCircle, ChevronDown } from "lucide-react";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "../../components/ui/accordion";

export default function SystemInfo() {
  return (
    <main className="bg-background text-foreground min-h-screen w-full relative overflow-hidden">
      <LayoutLines />
      <Navbar />

      {/* --- GLOW EFFECT --- */}
      <div 
        className="absolute top-0 left-0 w-full h-[500px] -z-10"
        style={{
          background: "radial-gradient(ellipse 80% 50% at 50% -20%, rgba(6, 182, 212, 0.15), rgba(0, 0, 0, 0))"
        }}
      />

      <div className="container mx-auto px-4 pt-32 pb-20 max-w-6xl">
        
        {/* HEADER */}
        <div className="text-center mb-16">
          <h1 className="text-4xl md:text-6xl font-bold mb-6 tracking-tight">
            System <span className="text-cyan-500">Specifications</span>
          </h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Technical documentation for the TrendVision hardware and software ecosystem.
          </p>
        </div>

        {/* --- HARDWARE & SOFTWARE GRID --- */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
            
            {/* LEFT: HARDWARE */}
            <div className="p-8 rounded-2xl border border-white/10 bg-white/5 backdrop-blur-sm shadow-2xl">
                <h2 className="text-2xl font-semibold mb-6 flex items-center gap-3">
                    <div className="p-2 bg-cyan-500/20 rounded-lg">
                        <Cpu className="text-cyan-400 w-6 h-6" />
                    </div>
                    Hardware Layer
                </h2>
                <div className="space-y-4">
                    <SpecRow label="Edge Device" value="Raspberry Pi 4 Model B (4GB)" />
                    <SpecRow label="Sensor" value="Logitech 1080p Webcam (USB)" />
                    <SpecRow label="Connectivity" value="802.11ac Wi-Fi + USB 3.0" />
                    <SpecRow label="Power" value="5V 3A via USB-C" />
                    <SpecRow label="OS" value="Raspberry Pi OS (Bookworm 64-bit)" />
                </div>
            </div>

            {/* RIGHT: SOFTWARE */}
            <div className="p-8 rounded-2xl border border-white/10 bg-white/5 backdrop-blur-sm shadow-2xl">
                <h2 className="text-2xl font-semibold mb-6 flex items-center gap-3">
                    <div className="p-2 bg-purple-500/20 rounded-lg">
                        <Code className="text-purple-400 w-6 h-6" />
                    </div>
                    Software Stack
                </h2>
                <div className="space-y-4">
                    <SpecRow label="Frontend" value="Next.js 14 + Tailwind CSS" />
                    <SpecRow label="Backend API" value="Python (Flask/FastAPI)" />
                    <SpecRow label="Computer Vision" value="OpenCV + MediaPipe" />
                    <SpecRow label="Database" value="MongoDB Atlas (Vector Search)" />
                    <SpecRow label="Deployment" value="AWS (Amplify + EC2)" />
                </div>
            </div>
        </div>

        {/* --- FAQ SECTION --- */}
        <div className="rounded-2xl border border-white/10 bg-white/5 backdrop-blur-sm p-8 shadow-2xl">
            <h2 className="text-2xl font-bold mb-8 flex items-center gap-3">
                <div className="p-2 bg-orange-500/20 rounded-lg">
                    <HelpCircle className="text-orange-400 w-6 h-6" />
                </div>
                Frequently Asked Questions
            </h2>
            
            <Accordion type="single" collapsible className="w-full space-y-4">
                <FAQItem 
                    value="item-1" 
                    q="How is the trend data calculated?" 
                    a="We utilize real-time computer vision pipelines running on edge devices. Video feeds are processed to extract crowd density and object interaction rates, which are then aggregated into our trend visualization engine."
                />
                <FAQItem 
                    value="item-2" 
                    q="Is the data truly real-time?" 
                    a="Yes. The system uses a low-latency MJPEG stream for visual verification and websockets for data transmission. The typical latency is under 200 milliseconds."
                />
                <FAQItem 
                    value="item-3" 
                    q="What happens if the internet cuts out?" 
                    a="The Raspberry Pi enters 'Local Mode,' caching all analytics data to its internal SD card. Once connection is restored, it automatically batch-uploads the stored data to MongoDB."
                />
                <FAQItem 
                    value="item-4" 
                    q="Can I export the reports?" 
                    a="All data points are stored in MongoDB and can be exported as CSV or JSON for further analysis in tools like Excel, Python Pandas, or Tableau."
                />
            </Accordion>
        </div>

        {/* FOOTER */}
        <div className="mt-20 border-t border-white/10 pt-8 text-center text-muted-foreground text-sm font-mono opacity-50">
            <p>System Version 1.0.4-beta | Build: Hacklahoma_2026</p>
        </div>

      </div>
    </main>
  );
}

// --- HELPER COMPONENTS ---

function SpecRow({ label, value }: { label: string, value: string }) {
    return (
        <div className="flex justify-between items-center border-b border-white/5 pb-3 last:border-0 last:pb-0 hover:bg-white/5 px-2 rounded transition-colors">
            {/* MATCHING SIZE FIX: Both sides use text-sm (14px) */}
            <span className="text-muted-foreground text-sm font-medium">{label}</span>
            <span className="font-mono text-sm text-foreground text-right">{value}</span>
        </div>
    )
}

function FAQItem({ value, q, a }: { value: string, q: string, a: string }) {
    return (
        <AccordionItem value={value} className="border border-white/10 rounded-lg bg-white/[0.02] px-4">
            <AccordionTrigger className="hover:no-underline hover:text-cyan-400 text-left font-medium">
                {q}
            </AccordionTrigger>
            <AccordionContent className="text-muted-foreground leading-relaxed">
                {a}
            </AccordionContent>
        </AccordionItem>
    )
}