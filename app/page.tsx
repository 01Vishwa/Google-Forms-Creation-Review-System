"use client"

import { useState, useEffect } from "react"
import { useAuth } from "@/context/auth-context"
import { useRouter } from "next/navigation"
import { GoogleLogin, type CredentialResponse } from "@react-oauth/google"
import { authAPI } from "@/services/api"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { AlertCircle, Loader2 } from "lucide-react"

export default function LandingPage() {
  const { login, isAuthenticated, setUser } = useAuth()
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

  const handleGoogleSuccess = async (credentialResponse: CredentialResponse) => {
    setIsLoading(true)
    setError(null)

    try {
      if (!credentialResponse.credential) {
        throw new Error("No credential received from Google")
      }

      // Send the Google ID token to your backend
      const response = await authAPI.googleLogin(credentialResponse.credential)
      
      if (response.user) {
        setUser({
          id: response.user.email,
          email: response.user.email,
          name: response.user.name,
          picture: response.user.picture,
        })
        router.push("/dashboard")
      }
    } catch (err) {
      console.error("[v0] Google sign-in error:", err)
      setError("Unable to sign in with Google. Please try again or use the Demo Account.")
    } finally {
      setIsLoading(false)
    }
  }

  const handleGoogleError = () => {
    setError("Google sign-in was cancelled or failed. Please try again.")
    setIsLoading(false)
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
          <div className="flex justify-center mb-4">
            <GoogleLogin
              onSuccess={handleGoogleSuccess}
              onError={handleGoogleError}
              useOneTap
              theme="outline"
              size="large"
              text="signin_with"
              shape="rectangular"
              logo_alignment="left"
            />
          </div>

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
