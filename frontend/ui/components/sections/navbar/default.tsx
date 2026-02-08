import Link from "next/link";
import { Button } from "../../ui/button";
import { Navbar as NavbarComponent } from "../../ui/navbar";

export default function Navbar() {
  return (
    <div className="w-full max-w-container mx-auto px-4 sm:px-6">
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
          <Button variant="ghost" size="sm" className="text-sm" asChild>
            <Link href="/login">Login</Link>
          </Button>
        </div>
      </NavbarComponent>
    </div>
  );
}