'use client'

import { Suspense } from 'react'
import { useSearchParams } from 'next/navigation'
import { ResultsReport } from '@/components/results/ResultsReport'

function ResultsRoute() {
  const search = useSearchParams()
  return <ResultsReport attemptId={search.get('attempt') ?? ''} />
}

export default function ResultsPage() {
  return (
    <Suspense fallback={<div className="exam-loading"><div className="spinner" /><p>Opening your result report…</p></div>}>
      <ResultsRoute />
    </Suspense>
  )
}
