"use client"

import type React from "react"

import { useState } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { SurveyDetailsModal } from "./survey-details-modal"
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

interface SurveyListProps {
  surveys: Survey[]
  onRefresh: () => void
}

const statusConfig = {
  draft: { label: "Draft", color: "bg-yellow-200 text-yellow-900" },
  "pending-approval": { label: "Pending Review", color: "bg-blue-200 text-blue-900" },
  approved: { label: "Approved", color: "bg-green-200 text-green-900" },
  archived: { label: "Archived", color: "bg-gray-200 text-gray-900" },
}

const FileTextIcon = () => (
  <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={2}
      d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"
    />
  </svg>
)

const ClockIcon = () => (
  <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={2}
      d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
    />
  </svg>
)

const CheckCircleIcon = () => (
  <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={2}
      d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
    />
  </svg>
)

const TrashIcon = () => (
  <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={2}
      d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
    />
  </svg>
)

const ExternalLinkIcon = () => (
  <svg className="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={2}
      d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4m-4-4l8-8m0 0H8m8 0v8"
    />
  </svg>
)

const statusIcons = {
  draft: <FileTextIcon />,
  "pending-approval": <ClockIcon />,
  approved: <CheckCircleIcon />,
  archived: <FileTextIcon />,
}

export function SurveyList({ surveys, onRefresh }: SurveyListProps) {
  const [selectedSurvey, setSelectedSurvey] = useState<Survey | null>(null)
  const [deletingId, setDeletingId] = useState<string | null>(null)
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false)
  const { toast } = useToast()

  const handleDeleteClick = (e: React.MouseEvent, id: string) => {
    e.stopPropagation()
    setDeletingId(id)
    setShowDeleteConfirm(true)
  }

  const handleConfirmDelete = async () => {
    if (!deletingId) return

    try {
      await surveysAPI.delete(deletingId)
      toast({
        title: "Success",
        description: "Survey deleted successfully.",
      })
      setShowDeleteConfirm(false)
      setDeletingId(null)
      onRefresh()
    } catch (error) {
      console.error("[v0] Delete failed:", error)
      toast({
        title: "Error",
        description: "Failed to delete survey. Please try again.",
        variant: "destructive",
      })
    }
  }

  if (surveys.length === 0) {
    return (
      <Card className="p-12 text-center">
        <div className="h-12 w-12 text-muted-foreground mx-auto mb-4 opacity-50">
          <FileTextIcon />
        </div>
        <p className="text-lg font-medium text-foreground mb-2">No surveys found</p>
        <p className="text-muted-foreground">Create your first survey to get started</p>
      </Card>
    )
  }

  return (
    <>
      <div className="space-y-3">
        {surveys.map((survey) => (
          <Card
            key={survey.id}
            className="p-4 hover:shadow-lg transition-shadow cursor-pointer"
            onClick={() => setSelectedSurvey(survey)}
          >
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-2">
                  <h3 className="text-lg font-semibold text-foreground">{survey.title}</h3>
                  <span
                    className={`px-2 py-1 rounded-full text-xs font-medium flex items-center gap-1 ${statusConfig[survey.status].color}`}
                  >
                    {statusIcons[survey.status]}
                    {statusConfig[survey.status].label}
                  </span>
                </div>
                <p className="text-sm text-muted-foreground mb-3">{survey.description}</p>
                <div className="flex items-center gap-6 text-xs text-muted-foreground flex-wrap">
                  <span>Created: {new Date(survey.createdAt).toLocaleDateString()}</span>
                  <span>Responses: {survey.responseCount}</span>
                  {survey.approver && <span>Approved by: {survey.approver}</span>}
                  {survey.form_url && (
                    <a
                      href={survey.form_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      onClick={(e) => e.stopPropagation()}
                      className="flex items-center gap-1 text-primary hover:underline"
                    >
                      <ExternalLinkIcon />
                      View Form
                    </a>
                  )}
                </div>
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={(e) => handleDeleteClick(e, survey.id)}
                className="text-destructive hover:text-destructive hover:bg-destructive/10"
              >
                <TrashIcon />
              </Button>
            </div>
          </Card>
        ))}
      </div>

      {/* Delete Confirmation Dialog */}
      {showDeleteConfirm && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <Card className="w-full max-w-md p-6">
            <h3 className="text-lg font-bold text-foreground mb-2">Delete Survey</h3>
            <p className="text-muted-foreground mb-6">
              Are you sure you want to delete this survey? This action cannot be undone.
            </p>
            <div className="flex gap-3 justify-end">
              <Button variant="outline" onClick={() => setShowDeleteConfirm(false)}>
                Cancel
              </Button>
              <Button variant="destructive" onClick={handleConfirmDelete}>
                Delete Survey
              </Button>
            </div>
          </Card>
        </div>
      )}

      {/* Survey Details Modal */}
      {selectedSurvey && (
        <SurveyDetailsModal survey={selectedSurvey} onClose={() => setSelectedSurvey(null)} onRefresh={onRefresh} />
      )}
    </>
  )
}
