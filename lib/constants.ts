export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

export const SURVEY_STATUS = {
  DRAFT: "draft",
  PENDING_APPROVAL: "pending-approval",
  APPROVED: "approved",
  ARCHIVED: "archived",
} as const

export const STATUS_COLORS = {
  draft: "bg-yellow-200 text-yellow-900",
  "pending-approval": "bg-blue-200 text-blue-900",
  approved: "bg-green-200 text-green-900",
  archived: "bg-gray-200 text-gray-900",
} as const

export const TOAST_CONFIG = {
  duration: 4000,
  position: "bottom-right",
} as const
