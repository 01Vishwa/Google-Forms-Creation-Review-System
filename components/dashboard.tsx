"use client"

import { useState, useEffect } from "react"
import { SurveyList } from "./survey-list"
import { PaginationControls } from "./pagination-controls"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { surveysAPI } from "@/services/api"
import { CreateSurveyModal } from "./create-survey-modal"
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

const FilterIcon = () => (
  <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={2}
      d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"
    />
  </svg>
)

const ChevronDownIcon = () => (
  <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
  </svg>
)

const PlusIcon = () => (
  <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
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

export function Dashboard() {
  const [surveys, setSurveys] = useState<Survey[]>([])
  const [filterStatus, setFilterStatus] = useState<string>("all")
  const [sortBy, setSortBy] = useState<"recent" | "name" | "responses">("recent")
  const [currentPage, setCurrentPage] = useState(1)
  const [itemsPerPage, setItemsPerPage] = useState(10)
  const [showStatusDropdown, setShowStatusDropdown] = useState(false)
  const [showSortDropdown, setShowSortDropdown] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [showCreateModal, setShowCreateModal] = useState(false)
  const { toast } = useToast()

  useEffect(() => {
    fetchSurveys()
  }, [])

  const fetchSurveys = async () => {
    try {
      setIsLoading(true)
      setError(null)
      const data = await surveysAPI.getAll(0, 1000)
      console.debug("[v0] Surveys loaded:", data)
      setSurveys(Array.isArray(data) ? data : data.surveys || [])
    } catch (err) {
      console.error("[v0] Failed to fetch surveys:", err)
      setError("Demo mode: Using sample data. Connect backend for live surveys.")
      setSurveys([])
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    setCurrentPage(1)
  }, [filterStatus, sortBy])

  const stats = {
    total: surveys.length,
    draft: surveys.filter((s) => s.status === "draft").length,
    pending: surveys.filter((s) => s.status === "pending-approval").length,
    approved: surveys.filter((s) => s.status === "approved").length,
  }

  const filteredSurveys = surveys.filter((s) => filterStatus === "all" || s.status === filterStatus)

  const sortedSurveys = [...filteredSurveys].sort((a, b) => {
    switch (sortBy) {
      case "recent":
        return new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
      case "name":
        return a.title.localeCompare(b.title)
      case "responses":
        return b.responseCount - a.responseCount
      default:
        return 0
    }
  })

  const totalPages = Math.ceil(sortedSurveys.length / itemsPerPage)
  const startIndex = (currentPage - 1) * itemsPerPage
  const endIndex = startIndex + itemsPerPage
  const paginatedSurveys = sortedSurveys.slice(startIndex, endIndex)

  const sortOptions = [
    { label: "Most Recent", value: "recent" },
    { label: "Alphabetical", value: "name" },
    { label: "Most Responses", value: "responses" },
  ]

  const statusOptions = [
    { label: "All Surveys", value: "all" },
    { label: "Draft", value: "draft" },
    { label: "Pending Review", value: "pending-approval" },
    { label: "Approved", value: "approved" },
    { label: "Archived", value: "archived" },
  ]

  const handleCreateSurvey = async (surveyData: any) => {
    try {
      await surveysAPI.create(surveyData)
      toast({
        title: "Success",
        description: "Survey created! Awaiting review.",
      })
      fetchSurveys()
      setShowCreateModal(false)
    } catch (err) {
      console.error("[v0] Failed to create survey:", err)
      toast({
        title: "Error",
        description: "Failed to create survey. Please try again.",
        variant: "destructive",
      })
    }
  }

  if (isLoading && surveys.length === 0) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
          <p className="mt-4 text-muted-foreground">Loading surveys...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold text-foreground">Survey Dashboard</h2>
          <p className="text-muted-foreground">Manage and review all your surveys</p>
        </div>
        <Button onClick={() => setShowCreateModal(true)} className="gap-2">
          <PlusIcon />
          New Survey
        </Button>
      </div>

      {/* Error Message */}
      {error && (
        <div className="p-4 bg-destructive/10 border border-destructive/20 rounded-lg flex gap-3">
          <AlertIcon />
          <p className="text-sm text-destructive">{error}</p>
        </div>
      )}

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {[
          { label: "Total Surveys", value: stats.total, color: "text-primary" },
          { label: "Drafts", value: stats.draft, color: "text-yellow-600" },
          { label: "Pending Review", value: stats.pending, color: "text-blue-600" },
          { label: "Approved", value: stats.approved, color: "text-green-600" },
        ].map((stat) => (
          <Card key={stat.label} className="p-6">
            <p className="text-sm font-medium text-muted-foreground">{stat.label}</p>
            <p className={`text-3xl font-bold mt-2 ${stat.color}`}>{stat.value}</p>
          </Card>
        ))}
      </div>

      {/* Filters and Sort */}
      <div className="flex items-center gap-3 bg-card border border-border rounded-lg p-4 flex-wrap">
        <FilterIcon />

        {/* Status Filter Dropdown */}
        <div className="relative">
          <button
            onClick={() => setShowStatusDropdown(!showStatusDropdown)}
            className="px-3 py-2 rounded-md bg-background border border-border text-foreground text-sm flex items-center gap-2 hover:bg-accent hover:text-accent-foreground transition-colors"
          >
            {statusOptions.find((o) => o.value === filterStatus)?.label}
            <ChevronDownIcon />
          </button>
          {showStatusDropdown && (
            <div className="absolute top-full left-0 mt-2 bg-card border border-border rounded-lg shadow-lg z-10 min-w-48">
              {statusOptions.map((option) => (
                <button
                  key={option.value}
                  onClick={() => {
                    setFilterStatus(option.value)
                    setShowStatusDropdown(false)
                  }}
                  className={`w-full text-left px-4 py-2 text-sm transition-colors ${
                    filterStatus === option.value
                      ? "bg-primary text-primary-foreground"
                      : "hover:bg-accent hover:text-accent-foreground"
                  }`}
                >
                  {option.label}
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Sort Dropdown */}
        <div className="relative ml-auto">
          <button
            onClick={() => setShowSortDropdown(!showSortDropdown)}
            className="px-3 py-2 rounded-md bg-background border border-border text-foreground text-sm flex items-center gap-2 hover:bg-accent hover:text-accent-foreground transition-colors"
          >
            Sort: {sortOptions.find((o) => o.value === sortBy)?.label}
            <ChevronDownIcon />
          </button>
          {showSortDropdown && (
            <div className="absolute top-full right-0 mt-2 bg-card border border-border rounded-lg shadow-lg z-10 min-w-48">
              {sortOptions.map((option) => (
                <button
                  key={option.value}
                  onClick={() => {
                    setSortBy(option.value as "recent" | "name" | "responses")
                    setShowSortDropdown(false)
                  }}
                  className={`w-full text-left px-4 py-2 text-sm transition-colors ${
                    sortBy === option.value
                      ? "bg-primary text-primary-foreground"
                      : "hover:bg-accent hover:text-accent-foreground"
                  }`}
                >
                  {option.label}
                </button>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Results Info */}
      {surveys.length > 0 && (
        <div className="text-sm text-muted-foreground">
          Showing {startIndex + 1} to {Math.min(endIndex, sortedSurveys.length)} of {sortedSurveys.length} surveys
        </div>
      )}

      {/* Empty State */}
      {surveys.length === 0 && !isLoading && (
        <Card className="p-12 text-center">
          <p className="text-muted-foreground mb-4">No surveys yet. Create one to get started!</p>
          <Button onClick={() => setShowCreateModal(true)} className="gap-2">
            <PlusIcon />
            Create Your First Survey
          </Button>
        </Card>
      )}

      {/* Survey List */}
      {surveys.length > 0 && <SurveyList surveys={paginatedSurveys} onRefresh={fetchSurveys} />}

      {/* Pagination Controls */}
      {totalPages > 1 && (
        <PaginationControls
          currentPage={currentPage}
          totalPages={totalPages}
          onPageChange={setCurrentPage}
          itemsPerPage={itemsPerPage}
          onItemsPerPageChange={setItemsPerPage}
        />
      )}

      {/* Create Survey Modal */}
      {showCreateModal && <CreateSurveyModal onClose={() => setShowCreateModal(false)} onSubmit={handleCreateSurvey} />}
    </div>
  )
}
