"use client"

import { useState } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { X, CheckCircle, Clock, AlertCircle, Loader2 } from "lucide-react"
import { surveysAPI } from "@/services/api"
import { useToast } from "@/hooks/use-toast"

interface Survey {
  id: string
  title: string
  description: string
  status: "draft" | "pending-approval" | "approved" | "archived"
  createdAt: string
  approvedAt: string | null
  responseCount: number
  approver: string | null
  form_url?: string
}

interface SurveyDetailsModalProps {
  survey: Survey
  onClose: () => void
  onRefresh: () => void
}

export function SurveyDetailsModal({ survey, onClose, onRefresh }: SurveyDetailsModalProps) {
  const [recipientEmail, setRecipientEmail] = useState("")
  const [customMessage, setCustomMessage] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const { toast } = useToast()

  const handleApprove = async () => {
    if (!recipientEmail.trim()) {
      setError("Recipient email is required")
      return
    }

    setIsLoading(true)
    setError(null)

    try {
      await surveysAPI.approve(survey.id, recipientEmail, customMessage)
      toast({
        title: "Success",
        description: `Email sent to ${recipientEmail}! Survey approved.`,
      })
      onRefresh()
      onClose()
    } catch (err: any) {
      console.error("[v0] Approval failed:", err)
      const errorMessage = err.response?.data?.detail || "Failed to approve survey. Please try again."
      setError(errorMessage)
      toast({
        title: "Error",
        description: errorMessage,
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <Card className="w-full max-w-2xl max-h-[90vh] overflow-y-auto p-6">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-2xl font-bold text-foreground">{survey.title}</h2>
            <p className="text-sm text-muted-foreground mt-1">{survey.description}</p>
          </div>
          <button onClick={onClose} className="text-muted-foreground hover:text-foreground transition-colors">
            <X className="h-6 w-6" />
          </button>
        </div>

        <div className="space-y-6">
          {/* Status and Metadata */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 p-4 bg-background rounded-lg">
            <div>
              <p className="text-xs font-medium text-muted-foreground uppercase">Status</p>
              <div className="flex items-center gap-2 mt-1">
                {survey.status === "approved" ? (
                  <CheckCircle className="h-4 w-4 text-green-500" />
                ) : (
                  <Clock className="h-4 w-4 text-yellow-500" />
                )}
                <span className="font-semibold capitalize">{survey.status.replace("-", " ")}</span>
              </div>
            </div>
            <div>
              <p className="text-xs font-medium text-muted-foreground uppercase">Created</p>
              <p className="font-semibold mt-1">{new Date(survey.createdAt).toLocaleDateString()}</p>
            </div>
            <div>
              <p className="text-xs font-medium text-muted-foreground uppercase">Responses</p>
              <p className="font-semibold mt-1">{survey.responseCount}</p>
            </div>
            <div>
              <p className="text-xs font-medium text-muted-foreground uppercase">Approver</p>
              <p className="font-semibold mt-1">{survey.approver || "Pending"}</p>
            </div>
          </div>

          {/* Form URL */}
          {survey.form_url && (
            <div className="p-4 bg-primary/5 border border-primary/20 rounded-lg">
              <label className="block text-sm font-medium text-foreground mb-2">📋 Google Form URL</label>
              <div className="flex items-center gap-2">
                <a
                  href={survey.form_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-primary hover:underline break-all text-sm flex-1"
                >
                  {survey.form_url}
                </a>
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => {
                    navigator.clipboard.writeText(survey.form_url || "")
                    toast({ title: "Copied!", description: "Form URL copied to clipboard" })
                  }}
                >
                  Copy
                </Button>
              </div>
            </div>
          )}
          
          {!survey.form_url && (
            <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
              <p className="text-sm text-yellow-900">⚠️ Google Form URL not available. The form may still be processing.</p>
            </div>
          )}

          {/* Approval Section */}
          {(survey.status === "draft" || survey.status === "pending-approval") && (
            <div className="space-y-4">
              {error && (
                <div className="p-4 bg-destructive/10 border border-destructive/20 rounded-lg flex gap-3">
                  <AlertCircle className="h-5 w-5 text-destructive shrink-0 mt-0.5" />
                  <p className="text-sm text-destructive">{error}</p>
                </div>
              )}

              <div>
                <label className="block text-sm font-medium text-foreground mb-2">Recipient Email *</label>
                <input
                  type="email"
                  value={recipientEmail}
                  onChange={(e) => {
                    setRecipientEmail(e.target.value)
                    setError(null)
                  }}
                  placeholder="reviewer@example.com"
                  className="w-full px-4 py-2 rounded-lg bg-background border border-border text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-foreground mb-2">Custom Message (Optional)</label>
                <textarea
                  value={customMessage}
                  onChange={(e) => setCustomMessage(e.target.value)}
                  placeholder="Add any feedback or instructions for the reviewer..."
                  rows={4}
                  className="w-full px-4 py-2 rounded-lg bg-background border border-border text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                />
              </div>
            </div>
          )}

          {survey.status === "approved" && (
            <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
              <p className="text-sm text-green-900">
                This survey was approved by {survey.approver} on{" "}
                {survey.approvedAt && new Date(survey.approvedAt).toLocaleDateString()}
              </p>
            </div>
          )}

          {/* Actions */}
          <div className="flex gap-3 justify-end pt-4 border-t border-border flex-wrap">
            {(survey.status === "draft" || survey.status === "pending-approval") && (
              <>
                <Button variant="outline" onClick={onClose}>
                  Cancel
                </Button>
                <Button onClick={handleApprove} disabled={isLoading || !recipientEmail.trim() || !survey.form_url} className="gap-2">
                  {isLoading && <Loader2 className="h-4 w-4 animate-spin" />}
                  <CheckCircle className="h-4 w-4" />
                  {isLoading ? "Sending..." : "Approve & Send Email"}
                </Button>
              </>
            )}
            {(survey.status === "approved" || survey.status === "archived") && (
              <Button variant="outline" onClick={onClose}>
                Close
              </Button>
            )}
          </div>
        </div>
      </Card>
    </div>
  )
}
