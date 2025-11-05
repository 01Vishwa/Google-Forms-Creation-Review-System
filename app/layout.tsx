import type React from "react"
import type { Metadata } from "next"
import { Geist, Geist_Mono } from "next/font/google"
import { Analytics } from "@vercel/analytics/next"
import { GoogleOAuthProvider } from "@react-oauth/google"
import { AuthProvider } from "@/context/auth-context"
import { Toaster } from "@/components/ui/toaster"
import "./globals.css"

const _geist = Geist({ subsets: ["latin"] })
const _geistMono = Geist_Mono({ subsets: ["latin"] })

const GOOGLE_CLIENT_ID = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID || "331931690873-9sarog6q4rjjiedp1glq35t832l5gkgj.apps.googleusercontent.com"

export const metadata: Metadata = {
  title: "SurveyForge - Survey Creation & Review System",
  description: "Create, review, and manage surveys with ease using Google OAuth authentication",
  generator: "v0.app",
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`font-sans antialiased`}>
        <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}>
          <AuthProvider>
            {children}
            <Toaster />
          </AuthProvider>
        </GoogleOAuthProvider>
        <Analytics />
      </body>
    </html>
  )
}
