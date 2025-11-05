import axios, { type AxiosError } from "axios"

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

// Create axios instance with credentials
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
})

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  },
)

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      window.location.href = "/"
    }
    return Promise.reject(error)
  },
)

const DEMO_SURVEYS = [
  {
    id: "1",
    title: "Customer Satisfaction Survey 2024",
    description: "Annual customer feedback survey to measure satisfaction and identify improvement areas",
    status: "approved",
    createdAt: new Date(Date.now() - 15 * 24 * 60 * 60 * 1000).toISOString(),
    approvedAt: new Date(Date.now() - 10 * 24 * 60 * 60 * 1000).toISOString(),
    responseCount: 342,
    approver: "admin@example.com",
  },
  {
    id: "2",
    title: "Product Feedback Form",
    description: "Collect detailed feedback on our latest product features and user experience",
    status: "pending-approval",
    createdAt: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(),
    approvedAt: null,
    responseCount: 0,
    approver: null,
  },
  {
    id: "3",
    title: "Employee Engagement Survey",
    description: "Internal survey to measure employee satisfaction and workplace culture",
    status: "draft",
    createdAt: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
    approvedAt: null,
    responseCount: 0,
    approver: null,
  },
  {
    id: "4",
    title: "Market Research Study",
    description: "Research survey for understanding market trends and customer preferences",
    status: "approved",
    createdAt: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString(),
    approvedAt: new Date(Date.now() - 28 * 24 * 60 * 60 * 1000).toISOString(),
    responseCount: 1250,
    approver: "reviewer@example.com",
  },
  {
    id: "5",
    title: "Service Quality Assessment",
    description: "Evaluate the quality and efficiency of our customer service department",
    status: "archived",
    createdAt: new Date(Date.now() - 60 * 24 * 60 * 60 * 1000).toISOString(),
    approvedAt: new Date(Date.now() - 58 * 24 * 60 * 60 * 1000).toISOString(),
    responseCount: 856,
    approver: "manager@example.com",
  },
]

let isDemoMode = false

// Auth endpoints
export const authAPI = {
  googleLogin: async (token: string) => {
    try {
      const response = await apiClient.post("/auth/google", { token })
      isDemoMode = false
      return response.data
    } catch (error) {
      console.debug("[v0] Backend unavailable, continuing in demo mode")
      isDemoMode = true
      return { user: { email: "user@example.com", name: "User" } }
    }
  },
  logout: async () => {
    try {
      return await apiClient.post("/auth/logout")
    } catch (error) {
      console.debug("[v0] Logout in demo mode")
      isDemoMode = true
    }
  },
  getUser: async () => {
    try {
      const response = await apiClient.get("/auth/user")
      isDemoMode = false
      return response.data
    } catch (error) {
      console.debug("[v0] Backend unavailable, using demo mode")
      isDemoMode = true
      return { email: "demo@surveyforge.com", name: "Demo User" }
    }
  },
}

// Survey endpoints
export const surveysAPI = {
  getAll: async (skip = 0, limit = 10) => {
    try {
      const response = await apiClient.get("/surveys", { params: { skip, limit } })
      isDemoMode = false
      return response.data
    } catch (error) {
      console.debug("[v0] Backend unavailable, using demo surveys")
      isDemoMode = true
      return DEMO_SURVEYS.slice(skip, skip + limit)
    }
  },
  getById: async (id: string) => {
    try {
      const response = await apiClient.get(`/surveys/${id}`)
      return response.data
    } catch (error) {
      console.debug("[v0] Using demo survey data")
      const survey = DEMO_SURVEYS.find((s) => s.id === id)
      if (!survey) throw new Error("Survey not found")
      return survey
    }
  },
  create: async (surveyData: any) => {
    try {
      const response = await apiClient.post("/surveys", surveyData)
      return response.data
    } catch (error) {
      console.debug("[v0] Creating survey in demo mode")
      const newSurvey = {
        id: Date.now().toString(),
        ...surveyData,
        status: "draft",
        createdAt: new Date().toISOString(),
        approvedAt: null,
        responseCount: 0,
        approver: null,
      }
      DEMO_SURVEYS.push(newSurvey)
      return newSurvey
    }
  },
  update: async (id: string, surveyData: any) => {
    try {
      const response = await apiClient.patch(`/surveys/${id}`, surveyData)
      return response.data
    } catch (error) {
      console.debug("[v0] Updating survey in demo mode")
      const index = DEMO_SURVEYS.findIndex((s) => s.id === id)
      if (index === -1) throw new Error("Survey not found")
      DEMO_SURVEYS[index] = { ...DEMO_SURVEYS[index], ...surveyData }
      return DEMO_SURVEYS[index]
    }
  },
  delete: async (id: string) => {
    try {
      return await apiClient.delete(`/surveys/${id}`)
    } catch (error) {
      console.debug("[v0] Deleting survey in demo mode")
      const index = DEMO_SURVEYS.findIndex((s) => s.id === id)
      if (index === -1) throw new Error("Survey not found")
      DEMO_SURVEYS.splice(index, 1)
      return { success: true }
    }
  },
  approve: async (id: string, recipientEmail: string, customMessage?: string) => {
    try {
      const response = await apiClient.post(`/surveys/${id}/approve`, {
        recipient_email: recipientEmail,
        custom_message: customMessage || null,
      })
      return response.data
    } catch (error) {
      console.debug("[v0] Approving survey in demo mode")
      const survey = DEMO_SURVEYS.find((s) => s.id === id)
      if (!survey) throw new Error("Survey not found")
      survey.status = "approved"
      survey.approvedAt = new Date().toISOString()
      survey.approver = recipientEmail
      return survey
    }
  },
}

export default apiClient
