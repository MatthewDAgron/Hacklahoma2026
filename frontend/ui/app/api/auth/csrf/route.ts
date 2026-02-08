import { NextResponse } from "next/server";

const DJANGO_URL = process.env.NEXT_PUBLIC_DJANGO_URL ?? "http://localhost:8000";

/**
 * Proxy CSRF from Django. Returns the token and sets the same cookie on our origin
 * so the browser sends it when posting to /api/auth/login (same-origin).
 */
export async function GET() {
  const res = await fetch(`${DJANGO_URL}/api/csrf/`, {
    credentials: "include",
    headers: { Accept: "application/json" },
  });

  if (!res.ok) {
    return NextResponse.json(
      { error: "Failed to get CSRF token" },
      { status: 502 }
    );
  }

  const data = (await res.json()) as { csrfToken?: string };
  const token = data.csrfToken ?? "";

  const response = NextResponse.json({ csrfToken: token });
  // Set cookie on our origin so the next request (login POST) sends it
  response.cookies.set("csrftoken", token, {
    path: "/",
    sameSite: "lax",
    maxAge: 60 * 60 * 24,
    httpOnly: false, // so we can read it if needed; Django accepts token in body
  });

  return response;
}
