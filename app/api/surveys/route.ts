import { type NextRequest, NextResponse } from "next/server"

// In-memory storage for demo purposes
// In production, this would be a database
const surveys: any[] = []

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams
  const status = searchParams.get("status")
  const page = Number.parseInt(searchParams.get("page") || "1")
  const limit = Number.parseInt(searchParams.get("limit") || "10")

  let filtered = surveys

  if (status && status !== "all") {
    filtered = surveys.filter((s) => s.status === status)
  }

  const start = (page - 1) * limit
  const end = start + limit
  const paginatedSurveys = filtered.slice(start, end)

  return NextResponse.json({
    data: paginatedSurveys,
    pagination: {
      page,
      limit,
      total: filtered.length,
      pages: Math.ceil(filtered.length / limit),
    },
  })
}

export async function POST(request: NextRequest) {
  const body = await request.json()

  const survey = {
    id: Math.random().toString(36).substr(2, 9),
    title: body.title,
    description: body.description,
    status: "draft",
    createdAt: new Date().toISOString().split("T")[0],
    approvedAt: null,
    responseCount: 0,
    approver: null,
  }

  surveys.push(survey)

  return NextResponse.json(survey, { status: 201 })
}
