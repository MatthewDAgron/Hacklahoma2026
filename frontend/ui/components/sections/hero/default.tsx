import { Button } from "../../ui/button";
import Link from "next/link";
import { ArrowRight, Github } from "lucide-react";

export default function Hero() {
  return (
    <section className="relative overflow-hidden">
      
      {/* --- THE FIX: Direct CSS Style --- */}
      <div 
        className="absolute inset-0 -z-10 h-full w-full"
        style={{
          background: "radial-gradient(ellipse 80% 50% at 50% -20%, rgba(249, 115, 22, 0.25), rgba(255, 255, 255, 0))"
        }}
      />
      
      {/* If the above is still too dim, try changing 0.25 to 0.4 
         rgba(249, 115, 22, 0.4) is BRIGHT ORANGE 
      */}

      <div className="container flex flex-col items-center gap-8 pb-8 pt-24 md:py-32">
        
        {/* 1. The Badge */}
        <div className="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/80">
          ✨ Live for Hacklahoma 2026
        </div>

        {/* 2. The Big Title */}
        <h1 className="text-center text-3xl font-bold leading-tight tracking-tighter md:text-6xl lg:leading-[1.1]">
          Visualizing the unseen trends of <br className="hidden md:block" />
          <span className="text-primary">Hacklahoma.</span>
        </h1>

        {/* 3. The Subtitle */}
        <p className="max-w-[750px] text-center text-lg text-muted-foreground sm:text-xl">
          Real-time crowd analytics, movement vectors, and environmental sensing powered by Raspberry Pi and Computer Vision.
        </p>

        {/* 4. Action Buttons */}
        <div className="flex w-full items-center justify-center gap-2 py-2">
          <Button size="lg" asChild>
            <Link href="/live-metrics">
              View Live Data <ArrowRight className="ml-2 h-4 w-4" />
            </Link>
          </Button>
          <Button variant="outline" size="lg" asChild>
            <Link href="https://github.com/MatthewDAgron/Hacklahoma2026" target="_blank">
              <Github className="mr-2 h-4 w-4" /> GitHub Repo
            </Link>
          </Button>
        </div>

        {/* 5. The Image */}
        <div className="mt-8 w-full max-w-5xl overflow-hidden rounded-xl border bg-background shadow-xl">
          <img
            src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=2670&auto=format&fit=crop"
            alt="Dashboard Preview"
            className="w-full object-cover opacity-90 dark:opacity-80"
            style={{ maxHeight: "500px" }}
          />
        </div>
        
      </div>
    </section>
  );
}