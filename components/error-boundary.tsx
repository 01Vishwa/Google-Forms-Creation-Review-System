"use client"

import { type ReactNode, Component, type ErrorInfo } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

const AlertIcon = () => (
  <svg className="h-12 w-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={2}
      d="M12 9v2m0 4v2m0-12a9 9 0 110 18 9 9 0 010-18z"
    />
  </svg>
)

interface Props {
  children: ReactNode
}

interface State {
  hasError: boolean
  error: Error | null
}

export class ErrorBoundary extends Component<Props, State> {
  public constructor(props: Props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("[v0] Error caught by boundary:", error, errorInfo)
  }

  public render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-background flex items-center justify-center p-4">
          <Card className="w-full max-w-md p-8 text-center">
            <div className="text-destructive mx-auto mb-4 flex justify-center">
              <AlertIcon />
            </div>
            <h1 className="text-2xl font-bold text-foreground mb-2">Something went wrong</h1>
            <p className="text-muted-foreground mb-6">{this.state.error?.message}</p>
            <Button
              onClick={() => {
                this.setState({ hasError: false, error: null })
                window.location.href = "/"
              }}
              className="w-full"
            >
              Return to Home
            </Button>
          </Card>
        </div>
      )
    }

    return this.props.children
  }
}
