'use client'

import { useEffect, useMemo, useState } from 'react'
import { useRouter } from 'next/navigation'
import { ArrowLeft, Check, Download, RotateCcw, ShieldCheck, X } from 'lucide-react'
import { api, type Review, type Skill } from '@/lib/api'
import { assetUrl } from '@/lib/assets'
import { Badge, Button, Logo } from '@/components/ui'

const skillLabels: Record<Skill, string> = { listening: 'Listening', reading: 'Reading', writing: 'Writing', speaking: 'Speaking' }
const skillOrder: Skill[] = ['listening', 'reading', 'writing', 'speaking']

function normalize(value: string) {
  return value.toLowerCase().trim().replace(/[.,!?;:'"()]/g, '').replace(/\s+/g, ' ')
}

function isCorrect(answer: string | undefined, correct: string, accepted?: string[]) {
  if (!answer) return false
  const value = normalize(answer)
  return [correct, ...(accepted ?? [])].some((candidate) => normalize(candidate) === value)
}

export function ResultsReport({ attemptId }: { attemptId: string }) {
  const router = useRouter()
  const [review, setReview] = useState<Review | null>(null)
  const [error, setError] = useState('')
  const [tab, setTab] = useState<Skill>('listening')
  const [incorrectOnly, setIncorrectOnly] = useState(false)
  const [showModel, setShowModel] = useState<Record<number, boolean>>({})

  useEffect(() => {
    api.review(attemptId)
      .then((data) => {
        setReview(data)
        setTab(data.attempt.mode === 'full' ? 'listening' : data.attempt.mode as Skill)
      })
      .catch((err) => setError(err instanceof Error ? err.message : 'Result not available'))
  }, [attemptId])

  const stats = useMemo(() => {
    if (!review) return null
    const listening = review.exam.listening.flatMap((part) => part.questions)
    const reading = review.exam.reading.flatMap((passage) => passage.questions)
    const all = [...listening, ...reading]
    const correct = all.filter((q) => isCorrect(review.answers[q.id]?.value, q.answer ?? '', q.accepted)).length
    return { listening, reading, correct, total: all.length }
  }, [review])

  if (error) {
    return <div className="exam-loading"><p>{error}</p><Button size="sm" onClick={() => router.push('/')}>Return home</Button></div>
  }
  if (!review || !stats) {
    return <div className="exam-loading"><div className="spinner" /><p>Opening your result report…</p></div>
  }

  const { result, exam, attempt, answers, writing, speaking } = review
  const practice = attempt.mode !== 'full'
  const availableSkills: Skill[] = practice ? [attempt.mode as Skill] : skillOrder
  const selectedResult = result[tab as 'listening' | 'reading' | 'writing' | 'speaking']
  const questionSet = tab === 'listening' ? stats.listening : tab === 'reading' ? stats.reading : []
  const visibleQuestions = questionSet.filter((q) => !incorrectOnly || !isCorrect(answers[q.id]?.value, q.answer ?? '', q.accepted))
  const correctCount = questionSet.filter((q) => isCorrect(answers[q.id]?.value, q.answer ?? '', q.accepted)).length

  const sectionLine = (skill: Skill) => {
    const section = result[skill]
    if (skill === 'listening' || skill === 'reading') return `${'raw' in section ? section.raw : 0} / ${'raw' in section ? section.total : 0} correct`
    return section.label
  }
  const fmt = (value: string) => new Date(value).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })
  const candidateNo = attempt.id.replace(/[^0-9a-f]/gi, '').slice(0, 8).toUpperCase()

  return (
    <div className="results-shell">
      <header className="portal-header">
        <div className="container portal-header-inner">
          <Logo onClick={() => router.push('/')} />
          <div className="results-actions">
            <Button size="sm" variant="ghost" onClick={() => router.push('/')} icon={<ArrowLeft size={15} />}>Dashboard</Button>
            <Button size="sm" variant="secondary" onClick={() => window.print()} icon={<Download size={15} />}>Print report</Button>
            <Button size="sm" onClick={() => router.push('/')} icon={<RotateCcw size={15} />}>Take another test</Button>
          </div>
        </div>
      </header>

      <main className="container portal-main">
        <section className="panel score-report">
          <div className="score-report-head">
            <div>
              <span className="mono-label">Practice result · not an official IELTS score</span>
              <h1>{practice ? `${skillLabels[attempt.mode as Skill]} practice result` : 'Your test result'}</h1>
              <p>{result?.examTitle ?? exam.title} · Academic</p>
            </div>
            <Badge tone="green"><Check size={13} /> Completed</Badge>
          </div>
          <dl className="score-meta">
            <div><dt>Candidate</dt><dd>Demo candidate</dd></div>
            <div><dt>Candidate number</dt><dd>{candidateNo.slice(0, 4)} {candidateNo.slice(4)}</dd></div>
            <div><dt>Test date</dt><dd>{fmt(attempt.startedAt)}</dd></div>
            <div><dt>Module</dt><dd>Academic</dd></div>
          </dl>
          <div className="score-row">
            {skillOrder.map((skill) => {
              const active = !practice || attempt.mode === skill
              return (
                <div key={skill} className={`score-box ${active ? '' : 'score-box--off'}`}>
                  <span>{skillLabels[skill]}</span>
                  <strong>{active ? result[skill].band.toFixed(1) : '—'}</strong>
                  <small>{active ? sectionLine(skill) : 'Not taken'}</small>
                </div>
              )
            })}
            <div className="score-box score-box--overall">
              <span>{practice ? 'Section band' : 'Overall band score'}</span>
              <strong>{(practice ? selectedResult.band : result.overall).toFixed(1)}</strong>
              <small>Estimated</small>
            </div>
          </div>
          <div className="score-note"><ShieldCheck size={16} /> Listening and Reading are marked against the answer key and converted to bands. Writing and Speaking are local estimates, not an examiner’s judgement.</div>
        </section>

        <section className="panel">
          <div className="panel-head">
            <div><h2>Answer review</h2><p>{practice ? 'Answers for the section you took.' : `${stats.correct} of ${stats.total} Listening and Reading answers correct.`}</p></div>
          </div>
          <div className="test-selector" role="tablist" aria-label="Choose a section">
            {availableSkills.map((skill) => (
              <button key={skill} role="tab" aria-selected={tab === skill} className={`test-chip ${tab === skill ? 'test-chip--active' : ''}`} onClick={() => setTab(skill)}>
                <span>{skillLabels[skill]}</span>
                <small>Band {result[skill].band.toFixed(1)}</small>
              </button>
            ))}
          </div>

          <div className="panel-body">
            {(tab === 'listening' || tab === 'reading') && (
              <>
                <div className="filter-row">
                  <span><strong>{correctCount}</strong> correct · <strong>{questionSet.length - correctCount}</strong> incorrect · {questionSet.length} questions</span>
                  <label><input type="checkbox" checked={incorrectOnly} onChange={(e) => setIncorrectOnly(e.target.checked)} /> Show incorrect only</label>
                </div>
                <div className="review-table-wrap">
                  <table className="data-table review-table">
                    <thead><tr><th className="num">Q</th><th>Question</th><th>Your answer</th><th>Correct answer</th><th><span className="sr-only">Result</span></th></tr></thead>
                    <tbody>
                      {visibleQuestions.map((question) => {
                        const userAnswer = answers[question.id]?.value ?? ''
                        const correct = isCorrect(userAnswer, question.answer ?? '', question.accepted)
                        return (
                          <tr key={question.id} className={correct ? '' : 'is-wrong'}>
                            <td className="num"><strong>{question.number}</strong></td>
                            <td className="review-q">
                              {question.prompt.replace('[[blank]]', '_____')}
                              {question.explanation && <div className="review-explanation">{question.explanation}</div>}
                            </td>
                            <td className={correct ? 'ans-ok' : 'ans-bad'}>{userAnswer || <em>No answer</em>}</td>
                            <td><strong>{question.answer}</strong></td>
                            <td className="mark">{correct ? <Check size={18} aria-label="Correct" /> : <X size={18} aria-label="Incorrect" />}</td>
                          </tr>
                        )
                      })}
                    </tbody>
                  </table>
                  {visibleQuestions.length === 0 && <p className="empty-line">No questions match this filter.</p>}
                </div>
              </>
            )}

            {tab === 'writing' && (
              <>
                <p className="lead-line">Part 1: <strong>{result.writingEvaluation.task1Words}</strong> words · Part 2: <strong>{result.writingEvaluation.task2Words}</strong> words. Part 2 counts twice as much as Part 1.</p>
                <table className="data-table">
                  <thead><tr><th>Criterion</th><th>Feedback</th><th className="num">Band</th></tr></thead>
                  <tbody>
                    {result.writingEvaluation.criteria.map((criterion, index) => (
                      <tr key={`${criterion.name}-${index}`}>
                        <td><strong>{index < 4 ? 'Part 1' : 'Part 2'}</strong><br />{criterion.name}</td>
                        <td className="muted-cell">{criterion.feedback}</td>
                        <td className="num"><strong>{criterion.score.toFixed(1)}</strong></td>
                      </tr>
                    ))}
                  </tbody>
                </table>
                {[1, 2].map((n) => (
                  <div className="task-eval" key={n}>
                    <div className="task-eval-head">
                      <h3>Part {n}</h3>
                      <span>{exam.writing[n - 1]?.minimumWords}+ words</span>
                    </div>
                    <div className="compare">
                      <div><span className="mono-label">Your answer</span><div className="text-box">{(n === 1 ? writing.task1 : writing.task2) || <em>No answer submitted.</em>}</div></div>
                      <div>
                        <span className="mono-label">Model answer</span>
                        {showModel[n]
                          ? <div className="text-box text-box--model">{exam.writing[n - 1]?.modelAnswer}</div>
                          : <button className="btn btn--secondary btn--sm model-toggle" onClick={() => setShowModel((s) => ({ ...s, [n]: true }))}>Show model answer</button>}
                      </div>
                    </div>
                  </div>
                ))}
              </>
            )}

            {tab === 'speaking' && (
              <>
                <table className="data-table">
                  <tbody>
                    <tr><td>Questions answered</td><td className="num"><strong>{result.speakingEvaluation.answered} / {result.speakingEvaluation.totalQuestions}</strong></td></tr>
                    <tr><td>Recorded speech</td><td className="num"><strong>{Math.floor(result.speakingEvaluation.totalSeconds / 60)}m {result.speakingEvaluation.totalSeconds % 60}s</strong></td></tr>
                    <tr><td>Words in transcript</td><td className="num"><strong>{result.speakingEvaluation.words}</strong></td></tr>
                  </tbody>
                </table>
                {result.speakingEvaluation.notes.length > 0 && <ul className="note-list">{result.speakingEvaluation.notes.map((note) => <li key={note}>{note}</li>)}</ul>}
                <h3 className="sub-head">Recordings</h3>
                {speaking.length ? speaking.map((response) => (
                  <div className="recording-row" key={response.questionId}>
                    <div>
                      <strong>{response.questionId.startsWith('speaking-cue') ? 'Part 2 long turn' : response.questionId.toUpperCase()}</strong>
                      <span>{response.durationSeconds}s{response.transcript ? '' : ' · no transcript'}</span>
                      {response.transcript && <p className="transcript">“{response.transcript.slice(0, 260)}”</p>}
                    </div>
                    {response.audioUrl ? <audio controls src={assetUrl(response.audioUrl)} /> : <span>No audio saved</span>}
                  </div>
                )) : <p className="empty-line">No recordings were submitted. The estimate uses completion data only.</p>}
              </>
            )}
          </div>
        </section>

        <div className="notice">
          <div className="notice-icon"><RotateCcw size={17} /></div>
          <div>
            <strong>{result.overall >= 7 ? 'Keep the score steady' : result.overall >= 6 ? 'Aim for the next half band' : 'Build the foundations'}</strong>
            <span>{tab === 'listening' || tab === 'reading' ? 'Read the explanation for each wrong answer, then retake the section focusing on those question types.' : 'Compare your answer with the model and pick one habit to change next time.'}</span>
          </div>
          <Button size="sm" onClick={() => router.push('/')}>Take another test</Button>
        </div>
      </main>
      <footer className="site-footer"><div className="container footer-inner"><Logo /><p>Independent IELTS practice. Not affiliated with or endorsed by the IELTS partners. This report is a simulation and cannot be used as an official IELTS Test Report Form.</p></div></footer>
    </div>
  )
}
