import CTA from "../components/sections/cta/default";
import FAQ from "../components/sections/faq/default";
import Hero from "../components/sections/hero/default";
import Navbar from "../components/sections/navbar/default";
import Stats from "../components/sections/stats/default";
import { LayoutLines } from "../components/ui/layout-lines";

export default function Home() {
  return (
    <main className="bg-background text-foreground min-h-screen w-full">
      <LayoutLines />
      <Navbar />
      
      {/* 1. The Big Intro */}
      <Hero /> 
      
      {/* 2. Show the hard numbers immediately (Trend Data) */}
      <Stats />
      
      {/* 4. Common Questions */}
      <FAQ />
      
      {/* 5. "View Dashboard" button */}
      <CTA />
      
      <div className="w-full py-8 text-center text-muted-foreground text-sm border-t border-white/10 mt-12">
        <p>Built with ☕ and 🥧 at Hacklahoma 2026</p>
      </div>
    </main>
  );
}