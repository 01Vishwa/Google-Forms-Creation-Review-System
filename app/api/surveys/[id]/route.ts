import { type NextRequest, NextResponse } from "next/server"

// Placeholder for in-memory storage reference
const surveys: any[] = []

export async function GET(request: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const survey = surveys.find((s) => s.id === id)

  if (!survey) {
    return NextResponse.json({ error: "Survey not found" }, { status: 404 })
  }

  return NextResponse.json(survey)
}

export async function PATCH(request: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const body = await request.json()

  const surveyIndex = surveys.findIndex((s) => s.id === id)

  if (surveyIndex === -1) {
    return NextResponse.json({ error: "Survey not found" }, { status: 404 })
  }

  const updatedSurvey = {
    ...surveys[surveyIndex],
    ...body,
  }

  surveys[surveyIndex] = updatedSurvey

  return NextResponse.json(updatedSurvey)
}

export async function DELETE(request: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const surveyIndex = surveys.findIndex((s) => s.id === id)

  if (surveyIndex === -1) {
    return NextResponse.json({ error: "Survey not found" }, { status: 404 })
  }

  surveys.splice(surveyIndex, 1)

  return NextResponse.json({ message: "Survey deleted" })
}
