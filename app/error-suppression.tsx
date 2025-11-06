"use client"

import { useEffect } from "react"

/**
 * Component to suppress non-critical Google FedCM console errors
 * These errors are harmless warnings from Google's Federated Credential Management API
 * and don't affect the functionality of the application
 */
export function ErrorSuppression() {
  useEffect(() => {
    // Save original console methods
    const originalError = console.error
    const originalWarn = console.warn

    // Override console.error to filter out FedCM errors
    console.error = (...args) => {
      const message = args[0]?.toString() || ""
      
      // List of patterns to suppress
      const suppressPatterns = [
        "[GSI_LOGGER]",
        "FedCM get() rejects with AbortError",
        "FedCM get() rejects with NetworkError",
        "Error retrieving a token",
        "signal is aborted without reason",
      ]

      // Check if error should be suppressed
      if (suppressPatterns.some(pattern => message.includes(pattern))) {
        return // Suppress this error
      }

      // Otherwise, log the error normally
      originalError.apply(console, args)
    }

    // Override console.warn for FedCM warnings
    console.warn = (...args) => {
      const message = args[0]?.toString() || ""
      
      if (message.includes("[GSI_LOGGER]") || message.includes("FedCM")) {
        return // Suppress this warning
      }

      originalWarn.apply(console, args)
    }

    // Cleanup: restore original console methods on unmount
    return () => {
      console.error = originalError
      console.warn = originalWarn
    }
  }, [])

  return null // This component doesn't render anything
}
