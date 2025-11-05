"use client"

import type React from "react"

import { useState } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

const UploadIcon = () => (
  <svg className="h-10 w-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={2}
      d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3V10"
    />
  </svg>
)

const UploadIconSmall = () => (
  <svg className="h-12 w-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={2}
      d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3V10"
    />
  </svg>
)

const XIcon = () => (
  <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
  </svg>
)

const FileTextIcon = () => (
  <svg className="h-12 w-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={2}
      d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"
    />
  </svg>
)

const AlertIcon = () => (
  <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={2}
      d="M12 9v2m0 4v2m0-12a9 9 0 110 18 9 9 0 010-18z"
    />
  </svg>
)

const LoaderIcon = () => (
  <svg className="h-4 w-4 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={2}
      d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
    />
  </svg>
)

interface CreateSurveyModalProps {
  onClose: () => void
  onSubmit: (survey: any) => void
}

export function CreateSurveyModal({ onClose, onSubmit }: CreateSurveyModalProps) {
  const [method, setMethod] = useState<"file" | "manual" | null>(null)
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    candidateEmails: "",
    questions: "",
  })
  const [fileName, setFileName] = useState("")
  const [preview, setPreview] = useState<string[]>([])
  const [showPreview, setShowPreview] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const parseQuestions = (input: string): string[] => {
    return input
      .split("\n")
      .map((q) => q.trim())
      .filter((q) => q.length > 0)
  }

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    setFileName(file.name)
    setError(null)

    try {
      const text = await file.text()
      let questions: string[] = []

      if (file.name.endsWith(".json")) {
        const json = JSON.parse(text)
        questions = json.questions || []
      } else {
        questions = parseQuestions(text)
      }

      setPreview(questions)
      setFormData({ ...formData, questions: questions.join("\n") })
    } catch (err) {
      console.error("[v0] File parse error:", err)
      setError("Failed to parse file. Please ensure it is valid JSON or plain text.")
    }
  }

  const handlePreviewQuestions = () => {
    if (!formData.title.trim()) {
      setError("Survey title is required")
      return
    }

    const questions = parseQuestions(formData.questions)
    if (questions.length === 0) {
      setError("Please enter at least one question")
      return
    }

    setPreview(questions)
    setShowPreview(true)
    setError(null)
  }

  const handleSubmit = async () => {
    if (!formData.title.trim()) {
      setError("Survey title is required")
      return
    }

    if (!formData.candidateEmails.trim()) {
      setError("At least one candidate email is required")
      return
    }

    const questions = parseQuestions(formData.questions)
    if (questions.length === 0) {
      setError("Please enter at least one question")
      return
    }

    const emails = formData.candidateEmails
      .split("\n")
      .map((email) => email.trim())
      .filter((email) => email.length > 0)

    if (emails.length === 0) {
      setError("Please enter at least one valid email address")
      return
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    const invalidEmails = emails.filter((email) => !emailRegex.test(email))
    if (invalidEmails.length > 0) {
      setError(`Invalid email addresses: ${invalidEmails.join(", ")}`)
      return
    }

    setIsLoading(true)
    setError(null)

    try {
      await onSubmit({
        title: formData.title,
        description: formData.description,
        candidateEmails: emails,
        questions: questions,
      })
    } catch (err) {
      console.error("[v0] Submit error:", err)
      setError("Failed to create survey. Please try again.")
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <Card className="w-full max-w-2xl max-h-[90vh] overflow-y-auto p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-foreground">Create New Survey</h2>
          <button onClick={onClose} className="text-muted-foreground hover:text-foreground transition-colors">
            <XIcon />
          </button>
        </div>

        {!method ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <button
              onClick={() => setMethod("file")}
              className="p-8 border-2 border-dashed border-border rounded-lg hover:border-primary transition-colors group"
            >
              <div className="text-muted-foreground group-hover:text-primary mx-auto mb-3 transition-colors flex justify-center">
                <UploadIcon />
              </div>
              <h3 className="font-semibold text-foreground mb-2">Upload File</h3>
              <p className="text-sm text-muted-foreground">Import from CSV or JSON</p>
            </button>
            <button
              onClick={() => setMethod("manual")}
              className="p-8 border-2 border-dashed border-border rounded-lg hover:border-primary transition-colors group"
            >
              <div className="text-muted-foreground group-hover:text-primary mx-auto mb-3 transition-colors flex justify-center">
                <FileTextIcon />
              </div>
              <h3 className="font-semibold text-foreground mb-2">Manual Entry</h3>
              <p className="text-sm text-muted-foreground">Create and configure manually</p>
            </button>
          </div>
        ) : showPreview ? (
          <div className="space-y-4">
            <div>
              <h3 className="text-lg font-semibold text-foreground mb-3">Survey Preview</h3>
              <div className="space-y-4 bg-background p-4 rounded-lg border border-border">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Title</p>
                  <p className="text-foreground font-semibold">{formData.title}</p>
                </div>
                {formData.description && (
                  <div>
                    <p className="text-sm font-medium text-muted-foreground">Description</p>
                    <p className="text-foreground">{formData.description}</p>
                  </div>
                )}
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Candidate Emails ({preview.length})</p>
                  <p className="text-foreground text-sm">
                    {formData.candidateEmails.split("\n").filter((e) => e.trim()).length} recipients
                  </p>
                </div>
              </div>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-foreground mb-3">Question Preview</h3>
              <div className="space-y-2 max-h-80 overflow-y-auto bg-background p-4 rounded-lg border border-border">
                {preview.map((q, i) => (
                  <div key={i} className="text-sm text-foreground">
                    <span className="font-medium">{i + 1}.</span> {q}
                  </div>
                ))}
              </div>
            </div>

            <div className="flex gap-3 justify-end pt-4">
              <Button variant="outline" onClick={() => setShowPreview(false)}>
                Edit
              </Button>
              <Button onClick={handleSubmit} disabled={isLoading} className="gap-2">
                {isLoading && <LoaderIcon />}
                {isLoading ? "Creating..." : "Create Survey"}
              </Button>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            {error && (
              <div className="p-4 bg-destructive/10 border border-destructive/20 rounded-lg flex gap-3">
                <AlertIcon />
                <p className="text-sm text-destructive">{error}</p>
              </div>
            )}

            <div>
              <label className="block text-sm font-medium text-foreground mb-2">Survey Title *</label>
              <input
                type="text"
                value={formData.title}
                onChange={(e) => {
                  setFormData({ ...formData, title: e.target.value })
                  setError(null)
                }}
                placeholder="e.g., Customer Feedback Survey"
                className="w-full px-4 py-2 rounded-lg bg-background border border-border text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-foreground mb-2">Description</label>
              <textarea
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                placeholder="Describe the purpose of this survey"
                rows={2}
                className="w-full px-4 py-2 rounded-lg bg-background border border-border text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-foreground mb-2">
                Candidate Email List * (one per line)
              </label>
              <textarea
                value={formData.candidateEmails}
                onChange={(e) => {
                  setFormData({ ...formData, candidateEmails: e.target.value })
                  setError(null)
                }}
                placeholder="john@example.com&#10;jane@example.com&#10;bob@example.com"
                rows={4}
                className="w-full px-4 py-2 rounded-lg bg-background border border-border text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary font-mono text-sm"
              />
            </div>

            {method === "file" && (
              <div>
                <label className="block text-sm font-medium text-foreground mb-2">Select File</label>
                <div className="border-2 border-dashed border-border rounded-lg p-8 text-center hover:border-primary transition-colors cursor-pointer">
                  <div className="flex justify-center mb-2">
                    <UploadIconSmall />
                  </div>
                  <p className="font-medium text-foreground mb-1">Drop your file here</p>
                  <p className="text-sm text-muted-foreground mb-4">or click to browse (CSV, JSON)</p>
                  <input
                    type="file"
                    accept=".json,.csv,.txt"
                    className="hidden"
                    id="file-input"
                    onChange={handleFileUpload}
                  />
                  <Button variant="outline" onClick={() => document.getElementById("file-input")?.click()}>
                    Browse Files
                  </Button>
                  {fileName && <p className="text-xs text-muted-foreground mt-2">Selected: {fileName}</p>}
                </div>
              </div>
            )}

            {method === "manual" && (
              <div>
                <label className="block text-sm font-medium text-foreground mb-2">Questions (one per line) *</label>
                <textarea
                  value={formData.questions}
                  onChange={(e) => {
                    setFormData({ ...formData, questions: e.target.value })
                    setError(null)
                  }}
                  placeholder="What is your name?&#10;How satisfied are you with our service?&#10;Would you recommend us?"
                  rows={6}
                  className="w-full px-4 py-2 rounded-lg bg-background border border-border text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary font-mono text-sm"
                />
              </div>
            )}

            <div className="flex items-center justify-between pt-4">
              <Button variant="outline" onClick={() => (method === null ? onClose() : setMethod(null))}>
                {method === null ? "Cancel" : "Back"}
              </Button>
              <div className="flex gap-3">
                <Button variant="outline" onClick={() => setShowPreview(false)}>
                  Cancel
                </Button>
                <Button onClick={handlePreviewQuestions} className="gap-2">
                  Preview Questions
                </Button>
              </div>
            </div>
          </div>
        )}
      </Card>
    </div>
  )
}
