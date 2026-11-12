'use client'

import { Suspense } from 'react'
import { useSearchParams } from 'next/navigation'
import { ExamRunner } from '@/components/exam/ExamRunner'

function ExamRoute() {
  const search = useSearchParams()
  return <ExamRunner attemptId={search.get('attempt') ?? ''} />
}

export default function ExamPage() {
  return (
    <Suspense fallback={<div className="exam-loading"><div className="spinner" /><p>Opening your test…</p></div>}>
      <ExamRoute />
    </Suspense>
  )
}
