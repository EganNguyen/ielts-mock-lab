import './globals.css'
import './exam.css'
import './results.css'
import './vocabulary.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Apex IELTS — Academic Mock Test',
  description: 'A complete, exam-faithful IELTS Academic simulation across Listening, Reading, Writing and Speaking.',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <html lang="en"><body>{children}</body></html>
}
