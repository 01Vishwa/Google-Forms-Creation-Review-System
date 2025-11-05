"use client"

import { useState, useEffect } from "react"
import { useAuth } from "@/context/auth-context"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { AlertCircle, Loader2 } from "lucide-react"

export default function LandingPage() {
  const { login, isAuthenticated } = useAuth()
  const router = useRouter()
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Redirect to dashboard if already authenticated
  useEffect(() => {
    if (isAuthenticated) {
      router.push("/dashboard")
    }
  }, [isAuthenticated, router])

  // Show loading state if authenticated (during redirect)
  if (isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="h-8 w-8 animate-spin mx-auto mb-4 text-primary" />
          <p className="text-muted-foreground">Redirecting to dashboard...</p>
        </div>
      </div>
    )
  }

  const handleGoogleSignIn = async () => {
    setIsLoading(true)
    setError(null)

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

      // In production, use proper Google OAuth library (e.g., @react-oauth/google)
      // For now, open auth window or show error if backend unavailable
      const googleAuthWindow = window.open(`${apiUrl}/auth/google`, "GoogleAuth", "width=500,height=600")

      if (!googleAuthWindow) {
        throw new Error("Could not open authentication window. Please check your popup blocker.")
      }

      // Poll for window closure
      const checkInterval = setInterval(() => {
        try {
          if (googleAuthWindow.closed) {
            clearInterval(checkInterval)
            checkUserStatus()
          }
        } catch {
          clearInterval(checkInterval)
        }
      }, 500)

      // Timeout after 5 minutes
      setTimeout(() => {
        clearInterval(checkInterval)
        if (!googleAuthWindow.closed) {
          googleAuthWindow.close()
        }
      }, 300000)
    } catch (err) {
      console.error("[v0] Google sign-in error:", err)
      setError("Unable to sign in with Google. The backend may not be running. Try the Demo Account instead.")
      setIsLoading(false)
    }
  }

  const checkUserStatus = async () => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"
      const response = await fetch(`${apiUrl}/auth/user`, {
        credentials: "include",
        signal: AbortSignal.timeout(5000),
      })

      if (response.ok) {
        const user = await response.json()
        login(user.email, user.name, user.picture)
        router.push("/dashboard")
      } else {
        setError("Authentication failed. Please try again.")
        setIsLoading(false)
      }
    } catch (err) {
      console.error("[v0] User status check failed:", err)
      setError("Backend connection failed. Please try the Demo Account instead.")
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-linear-to-br from-background via-background to-accent/5 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Logo Section */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary/10 mb-4">
            <svg className="w-8 h-8 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
          </div>
          <h1 className="text-4xl font-bold text-foreground mb-2">SurveyForge</h1>
          <p className="text-muted-foreground text-lg">Create, review, and manage surveys with ease</p>
        </div>

        {/* Main Card */}
        <Card className="p-8 shadow-lg border-0">
          <h2 className="text-2xl font-bold text-foreground mb-2 text-center">Get Started</h2>
          <p className="text-muted-foreground text-center mb-8">Sign in with your Google account to continue</p>

          {/* Error Message */}
          {error && (
            <div className="mb-6 p-4 bg-destructive/10 border border-destructive/20 rounded-lg flex gap-3">
              <AlertCircle className="h-5 w-5 text-destructive shrink-0 mt-0.5" />
              <p className="text-sm text-destructive">{error}</p>
            </div>
          )}

          {/* Google Sign In Button */}
          <Button
            onClick={handleGoogleSignIn}
            disabled={isLoading}
            size="lg"
            className="w-full mb-4 h-12 text-base font-medium"
          >
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                Signing in...
              </>
            ) : (
              <>
                <svg className="mr-2 h-5 w-5" viewBox="0 0 24 24">
                  <path
                    fill="currentColor"
                    d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                  />
                  <path
                    fill="currentColor"
                    d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                  />
                  <path
                    fill="currentColor"
                    d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                  />
                  <path
                    fill="currentColor"
                    d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                  />
                </svg>
                Sign in with Google
              </>
            )}
          </Button>

          {/* Divider */}
          <div className="relative my-6">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-border"></div>
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-2 bg-card text-muted-foreground">Or continue with</span>
            </div>
          </div>

          {/* Demo Button */}
          <Button
            onClick={() => {
              // Demo mode - simulate login without backend
              login("demo@surveyforge.com", "Demo User", "")
              router.push("/dashboard")
            }}
            variant="outline"
            size="lg"
            className="w-full h-12 text-base font-medium"
            disabled={isLoading}
          >
            Demo Account
          </Button>
        </Card>

        {/* Features List */}
        <div className="mt-12 space-y-4">
          <h3 className="text-center text-sm font-medium text-muted-foreground mb-6">Why choose SurveyForge?</h3>
          <div className="grid grid-cols-1 gap-3">
            {[
              { title: "Easy Creation", description: "Create surveys from text or JSON files" },
              { title: "Smart Approval", description: "Review and approve surveys with custom messages" },
              { title: "Full Control", description: "Manage all surveys in one unified dashboard" },
            ].map((feature) => (
              <div key={feature.title} className="flex gap-3 text-sm">
                <svg
                  className="h-5 w-5 text-primary shrink-0 mt-0.5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                <div>
                  <p className="font-medium text-foreground">{feature.title}</p>
                  <p className="text-muted-foreground">{feature.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
