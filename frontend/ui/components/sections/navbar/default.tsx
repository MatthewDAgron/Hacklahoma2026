import Link from "next/link";
import { Button } from "../../ui/button";
import { Navbar as NavbarComponent } from "../../ui/navbar";

export default function Navbar() {
  return (
    <NavbarComponent>
      {/* Brand Logo */}
      <div className="flex items-center gap-2">
        <Link href="/" className="flex items-center gap-2 text-xl font-bold">
            <span className="text-primary">👁️</span> TrendVision
        </Link>
      </div>
      
      {/* Center Navigation */}
      <nav className="hidden gap-6 md:flex">
        <Link href="/live-metrics" className="text-sm font-medium hover:text-primary">
          Live Metrics
        </Link>
        <Link href="/how-it-works" className="text-sm font-medium hover:text-primary">
          How it Works
        </Link>
        <Link href="/system-info" className="text-sm font-medium hover:text-primary">
          System Info
        </Link>
      </nav>

      {/* Action Buttons */}
      <div className="flex items-center gap-2">
        
        {/* Admin Login Button */}
        <Button variant="ghost" size="sm" asChild>
          <Link href="/login">Admin Login</Link>
        </Button>

        {/* Dashboard CTA */}
        <Button size="sm" asChild>
          <Link href="/live-metrics">View Dashboard</Link>
        </Button>
      </div>
    </NavbarComponent>
  );
}