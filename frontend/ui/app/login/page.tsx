import Link from "next/link";

import { LayoutLines } from "@/components/ui/layout-lines";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import Glow from "@/components/ui/glow";

export default function LoginPage() {
  return (
    <main className="bg-background text-foreground min-h-screen w-full">
      <LayoutLines />
      <div className="relative flex min-h-screen flex-col items-center justify-center px-4">
        <div className="relative w-full max-w-md">
          <Glow variant="center" className="pointer-events-none h-full min-h-[400px] w-full" />
          <Card className="glass-4 relative z-10 w-full shadow-xl">
            <CardHeader className="space-y-1 text-center">
            <CardTitle className="text-2xl font-semibold tracking-tight">
              Sign in
            </CardTitle>
            <CardDescription>
              Enter your email and password to continue
            </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
            <div className="space-y-2">
              <label
                htmlFor="email"
                className="text-foreground text-sm font-medium"
              >
                Email
              </label>
              <input
                id="email"
                type="email"
                placeholder="name@example.com"
                className="border-input bg-background text-foreground placeholder:text-muted-foreground focus-visible:ring-ring flex h-9 w-full rounded-md border px-3 py-1 text-sm shadow-xs transition-shadow focus-visible:outline-none focus-visible:ring-2"
              />
            </div>
            <div className="space-y-2">
              <label
                htmlFor="password"
                className="text-foreground text-sm font-medium"
              >
                Password
              </label>
              <input
                id="password"
                type="password"
                placeholder="••••••••"
                className="border-input bg-background text-foreground placeholder:text-muted-foreground focus-visible:ring-ring flex h-9 w-full rounded-md border px-3 py-1 text-sm shadow-xs transition-shadow focus-visible:outline-none focus-visible:ring-2"
              />
            </div>
            </CardContent>
            <CardFooter className="flex flex-col gap-4">
            <Button className="w-full" size="lg">
              Sign in
            </Button>
            <p className="text-muted-foreground text-center text-sm">
              Don&apos;t have an account?{" "}
              <Link
                href="/"
                className="text-foreground underline-offset-4 hover:underline"
              >
                Back to home
              </Link>
            </p>
            </CardFooter>
          </Card>
        </div>
      </div>
    </main>
  );
}
