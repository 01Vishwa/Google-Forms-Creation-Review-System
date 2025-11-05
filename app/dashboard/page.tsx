"use client"

import { ProtectedRoute } from "@/components/protected-route"
import { Dashboard } from "@/components/dashboard"
import { DashboardNav } from "@/components/dashboard-nav"

export default function DashboardPage() {
  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-background">
        <DashboardNav />
        <div className="pt-20 px-8 pb-8">
          <Dashboard />
        </div>
      </div>
    </ProtectedRoute>
  )
}
