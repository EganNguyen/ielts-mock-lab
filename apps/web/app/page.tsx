'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { AlertTriangle, ArrowRight, Check, Clock3, History, Monitor, ShieldCheck } from 'lucide-react'
import { api, type ExamSummary, type Skill, type User } from '@/lib/api'
import { Button, Logo, SkillGlyph } from '@/components/ui'
import { ShareControl } from '@/components/ShareLink'

const skills: Array<{ key: Skill; name: string; duration: string; count: string; blurb: string; content: string }> = [
  { key: 'listening', name: 'Listening', duration: '30 min', count: '40 questions', blurb: 'Four recordings, played once only.', content: '4 parts · form, map, matching and multiple-choice questions' },
  { key: 'reading', name: 'Reading', duration: '60 min', count: '40 questions', blurb: 'Three academic passages side by side with the questions.', content: '3 passages · headings, TRUE/FALSE/NOT GIVEN, matching, completion' },
  { key: 'writing', name: 'Writing', duration: '60 min', count: '2 parts', blurb: 'A data report and an essay with a live word count.', content: 'Part 1: 150+ words · Part 2: 250+ words' },
  { key: 'speaking', name: 'Speaking', duration: '11–14 min', count: '3 parts', blurb: 'A recorded interview with an examiner voice.', content: 'Interview · task card with 1 minute preparation · discussion' },
]

export default function Dashboard() {
  const router = useRouter()
  const [exams, setExams] = useState<ExamSummary[]>([])
  const [history, setHistory] = useState<Array<{ id: string; mode: string; startedAt: string; completedAt: string; overall: number; listening: number; reading: number; writing: number; speaking: number }>>([])
  const [me, setMe] = useState<User | null>(null)
  const [active, setActive] = useState<{ id: string; mode: string; currentSkill: string; title: string; status: string; startedAt: string } | null>(null)
  const [selectedId, setSelectedId] = useState('')
  const [starting, setStarting] = useState<string | null>(null)
  const [error, setError] = useState('')

  useEffect(() => {
    Promise.allSettled([api.exams(), api.history(), api.me(), api.activeAttempt()])
      .then(([e, h, m, a]) => {
        if (e.status === 'fulfilled') setExams([...e.value.exams].sort((a, b) => a.id.localeCompare(b.id)))
        else setError(e.reason instanceof Error ? e.reason.message : 'The exam service is unavailable')
        if (h.status === 'fulfilled') setHistory(h.value.attempts)
        if (m.status === 'fulfilled') setMe(m.value.user)
        if (a.status === 'fulfilled') setActive(a.value.attempt)
      })
  }, [])

  async function start(examId: string, mode: 'full' | Skill) {
    setStarting(mode)
    setError('')
    try {
      const state = await api.createAttempt(examId, mode)
      router.push(`/exam/${state.attempt.id}`)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to start the test')
      setStarting(null)
    }
  }

  const exam = exams.find((item) => item.id === selectedId) ?? exams[0]
  const best = history.length ? Math.max(...history.map((h) => h.overall)) : null
  const name = me?.displayName ?? 'Demo Candidate'
  const initials = name.split(/\s+/).map((part) => part[0]).join('').slice(0, 2).toUpperCase()
  const fmtDate = (value: string) => new Date(value).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })

  return (
    <div className="home-shell">
      <header className="portal-header">
        <div className="container portal-header-inner">
          <Logo />
          <nav className="portal-nav" aria-label="Main navigation">
            <a href="#mock">Full test</a>
            <a href="#practice">Practice</a>
            <a href="#results">My results</a>
          </nav>
          <div className="portal-user">
            <ShareControl />
            <div className="portal-candidate"><strong>{name}</strong><span>Local demo · Academic</span></div>
            <span className="portal-avatar" aria-hidden="true">{initials}</span>
          </div>
        </div>
      </header>

      <main className="container portal-main">
        {active && (
          <div className="notice" role="status">
            <div className="notice-icon"><History size={18} /></div>
            <div><strong>You have a test in progress</strong><span>{active.title} · {active.currentSkill[0].toUpperCase() + active.currentSkill.slice(1)} · started {new Date(active.startedAt).toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' })}. The section clock keeps running while you are away.</span></div>
            <Button size="sm" onClick={() => router.push(`/exam/${active.id}`)} iconRight={<ArrowRight size={15} />}>Resume test</Button>
          </div>
        )}
        {error && (
          <div className="notice notice--warn" role="alert">
            <div className="notice-icon"><AlertTriangle size={18} /></div>
            <div><strong>Could not reach the exam service</strong><span>{error}</span></div>
          </div>
        )}

        <section className="panel welcome">
          <div>
            <span className="mono-label">IELTS Academic · Computer-delivered mock</span>
            <h1>The full test, as it runs on test day</h1>
            <p>Listening, Reading and Writing back to back on screen, then the Speaking test. Timings, one-play audio and the on-screen tools match the computer-delivered exam.</p>
            <div className="welcome-facts">
              <span><Clock3 size={15} /> 2 h 44 min in total</span>
              <span><Monitor size={15} /> Use a computer with headphones</span>
              <span><ShieldCheck size={15} /> Answers saved automatically</span>
            </div>
          </div>
          <div className="welcome-actions">
            <Button size="lg" onClick={() => exam && start(exam.id, 'full')} disabled={!exam || !!starting} iconRight={<ArrowRight size={17} />}>
              {starting === 'full' ? 'Preparing exam…' : 'Start full mock test'}
            </Button>
            <Button size="lg" variant="secondary" onClick={() => document.getElementById('practice')?.scrollIntoView({ behavior: 'smooth' })}>Practise one skill</Button>
          </div>
        </section>

        <section className="panel" id="mock">
          <div className="panel-head">
            <div><h2>Choose a test</h2><p>Each test is a complete paper. You can stop and resume; the clock keeps running.</p></div>
          </div>
          {exams.length > 0 && (
            <div className="test-selector" role="tablist" aria-label="Choose an IELTS test">
              {exams.map((item, index) => {
                const [book, test] = item.title.includes(' · ') ? [item.title.split(' · ')[0], item.title.split(' · ').slice(1).join(' · ').replace(/^Academic\s+/, '')] : ['', `Test ${index + 1}`]
                return (
                  <button
                    key={item.id}
                    role="tab"
                    aria-selected={exam?.id === item.id}
                    className={`test-chip ${exam?.id === item.id ? 'test-chip--active' : ''}`}
                    onClick={() => setSelectedId(item.id)}
                  >
                    <span>{book ? `${book.startsWith('Cambridge') ? 'C21' : 'IELTS 20'} · ${test}` : test}</span>
                    <small>{item.listeningQuestions} L · {item.readingQuestions} R</small>
                  </button>
                )
              })}
            </div>
          )}
          <article className="mock-card">
            <div className="mock-card-body">
              <span className="mono-label">Academic module</span>
              <h3>{exam?.title ?? 'Academic Mock Test'}</h3>
              <p>Four listening parts, three reading passages, two writing parts and a three-part speaking test.</p>
              <table className="data-table">
                <thead><tr><th>Section</th><th className="hide-sm">Content</th><th className="num">Time</th></tr></thead>
                <tbody>
                  {skills.map((skill) => (
                    <tr key={skill.key}>
                      <td><span className="skill-cell"><SkillGlyph skill={skill.key} size="sm" />{skill.name}</span></td>
                      <td className="hide-sm">{skill.content}</td>
                      <td className="num">{skill.duration}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <aside className="mock-card-side">
              <div className="total"><span>Total test time</span><strong>2 h 44 min</strong></div>
              <ul className="check-list">
                <li><Check size={15} /><span>Audio plays once and cannot be paused</span></li>
                <li><Check size={15} /><span>Timer, highlighter, notes and Review flags</span></li>
                <li><Check size={15} /><span>Sections close automatically at time</span></li>
                <li><Check size={15} /><span>Answer key only after you finish</span></li>
              </ul>
              <Button size="lg" full onClick={() => exam && start(exam.id, 'full')} disabled={!exam || !!starting} iconRight={<ArrowRight size={17} />}>
                {starting === 'full' ? 'Preparing…' : 'Begin full test'}
              </Button>
            </aside>
          </article>
        </section>

        <section className="panel" id="practice">
          <div className="panel-head">
            <div><h2>Practise one skill</h2><p>{exam ? `Uses ${exam.title}. ` : ''}Same screens and timing as the full test.</p></div>
          </div>
          <div className="practice-grid">
            {skills.map((skill) => (
              <button key={skill.key} className="practice-card" onClick={() => exam && start(exam.id, skill.key)} disabled={!exam || !!starting}>
                <SkillGlyph skill={skill.key} />
                <h3>{skill.name}</h3>
                <p>{skill.blurb}</p>
                <div className="practice-meta"><span><Clock3 size={13} /> {skill.duration}</span><span>{skill.count}</span></div>
                <span className="practice-link">{starting === skill.key ? 'Preparing…' : `Start ${skill.name}`} <ArrowRight size={15} /></span>
              </button>
            ))}
          </div>
        </section>

        <section className="panel" id="results">
          <div className="panel-head">
            <div><h2>My results</h2><p>Completed attempts are saved on this computer.</p></div>
          </div>
          {history.length ? (
            <div className="results-summary">
              <div className="results-best">
                <span className="mono-label">Best overall</span>
                <strong>{best!.toFixed(1)}</strong>
                <small>from {history.length} completed attempt{history.length === 1 ? '' : 's'}</small>
              </div>
              <div className="results-table">
                <table className="data-table">
                  <thead><tr><th>Date</th><th className="num">L</th><th className="num">R</th><th className="num">W</th><th className="num">S</th><th className="num">Overall</th><th className="num"><span className="sr-only">Report</span></th></tr></thead>
                  <tbody>
                    {history.slice(0, 8).map((item) => (
                      <tr key={item.id}>
                        <td>{fmtDate(item.completedAt)}</td>
                        <td className="num">{item.listening.toFixed(1)}</td>
                        <td className="num">{item.reading.toFixed(1)}</td>
                        <td className="num">{item.writing.toFixed(1)}</td>
                        <td className="num">{item.speaking.toFixed(1)}</td>
                        <td className="num"><strong>{item.overall.toFixed(1)}</strong></td>
                        <td className="num"><a href={`/results/${item.id}`}>View</a></td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          ) : (
            <div className="results-empty">
              <span>No completed tests yet. Your results will appear here after your first test.</span>
              <Button size="sm" variant="secondary" onClick={() => exam && start(exam.id, 'full')} disabled={!exam || !!starting}>Start a test</Button>
            </div>
          )}
        </section>
      </main>

      <footer className="site-footer"><div className="container footer-inner"><Logo /><p>Independent IELTS practice. Not affiliated with or endorsed by the IELTS partners. Band scores are estimates for practice only. Cambridge IELTS 21 and IELTS 20 material © Cambridge University Press &amp; Assessment and Qunyan Press, included for private study only — not for redistribution.</p><div className="footer-meta"><span>{exam?.version ?? '2026.1'}</span><span>Academic</span></div></div></footer>
    </div>
  )
}
