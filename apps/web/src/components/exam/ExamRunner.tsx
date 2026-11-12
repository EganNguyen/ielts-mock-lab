'use client'

import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { useRouter } from 'next/navigation'
import {
  AlertTriangle, ArrowRight, Check, ChevronLeft, ChevronRight, Clock3, FileText, Headphones,
  HelpCircle, LogOut, Menu, ShieldAlert, Volume2, Wifi, WifiOff,
} from 'lucide-react'
import { api, ApiError, type AttemptState, type Question, type Skill } from '@/lib/api'
import { assetUrl } from '@/lib/assets'
import { Button, Logo, Modal, formatClock } from '@/components/ui'
import { QuestionSets } from '@/components/exam/Questions'
import { SpeakingRoom } from '@/components/exam/SpeakingRoom'

const skills: Skill[] = ['listening', 'reading', 'writing', 'speaking']
const skillNames: Record<Skill, string> = { listening: 'Listening', reading: 'Reading', writing: 'Writing', speaking: 'Speaking' }

export function ExamRunner({ attemptId }: { attemptId: string }) {
  const router = useRouter()

  const [state, setState] = useState<AttemptState | null>(null)
  const [answers, setAnswers] = useState<Record<string, string>>({})
  const [versions, setVersions] = useState<Record<string, number>>({})
  const [flags, setFlags] = useState<Record<string, boolean>>({})
  const [loading, setLoading] = useState(true)
  const [fatal, setFatal] = useState('')
  const [autosave, setAutosave] = useState<'idle' | 'saving' | 'saved' | 'error'>('idle')
  const [remaining, setRemaining] = useState(0)
  const [viewedPart, setViewedPart] = useState(1)
  const [viewedPassage, setViewedPassage] = useState(1)
  const [activeTask, setActiveTask] = useState(1)
  const [confirmSubmit, setConfirmSubmit] = useState(false)
  const [transition, setTransition] = useState<{ from: Skill; next?: Skill; auto?: boolean; answered?: number } | null>(null)
  const [submitting, setSubmitting] = useState(false)
  const [helpOpen, setHelpOpen] = useState(false)
  const [notesOpen, setNotesOpen] = useState(false)
  const [notes, setNotes] = useState('')
  const [submitError, setSubmitError] = useState('')
  const [audioPart, setAudioPart] = useState(1)
  const [audioPlaying, setAudioPlaying] = useState(false)
  const [audioBlocked, setAudioBlocked] = useState(false)
  const [audioComplete, setAudioComplete] = useState(false)
  const [volume, setVolume] = useState(0.9)
  const [audioProgress, setAudioProgress] = useState(0)
  const [highlightCount, setHighlightCount] = useState(0)
  const [contextMenu, setContextMenu] = useState<{ x: number; y: number; canHighlight: boolean } | null>(null)
  const [activeQid, setActiveQid] = useState<string | null>(null)
  const [split, setSplit] = useState(50)
  const [audioResumeAt, setAudioResumeAt] = useState(0)
  const audioResumeRef = useRef(0)
  const audioStoreKey = `apex-audio-${attemptId}`

  const timers = useRef<Record<string, ReturnType<typeof setTimeout>>>({})
  const savingCount = useRef(0)
  const audioRef = useRef<HTMLAudioElement | null>(null)
  const expiredHandled = useRef(false)
  const submittingRef = useRef(false)
  const passageRef = useRef<HTMLDivElement | null>(null)
  const savedRange = useRef<Range | null>(null)

  const load = useCallback(async () => {
    try {
      const next = await api.attempt(attemptId)
      setState(next)
      const values: Record<string, string> = {}
      const vers: Record<string, number> = {}
      Object.values(next.answers).forEach((answer) => { values[answer.questionId] = answer.value; vers[answer.questionId] = answer.version })
      setAnswers(values)
      setVersions(vers)
      const storedFlags = localStorage.getItem(`apex-flags-${attemptId}`)
      if (storedFlags) setFlags(JSON.parse(storedFlags))
      const storedNotes = localStorage.getItem(`apex-notes-${attemptId}`)
      if (storedNotes) setNotes(storedNotes)
      setLoading(false)
    } catch (err) {
      setFatal(err instanceof Error ? err.message : 'Unable to load the attempt')
      setLoading(false)
    }
  }, [attemptId])

  useEffect(() => { load() }, [load])

  useEffect(() => {
    document.querySelectorAll<HTMLElement>('.listening-main, .passage-pane, .question-pane').forEach((el) => el.scrollTo({ top: 0 }))
  }, [viewedPart, viewedPassage])

  const skill = state?.attempt.currentSkill
  const section = state?.attempt.sections.find((item) => item.skill === skill)

  useEffect(() => {
    if (!section?.deadlineAt || section.status !== 'in_progress') {
      if (section?.status === 'not_started') setRemaining(section.durationSeconds)
      return
    }
    const tick = () => {
      const seconds = Math.max(0, Math.floor((new Date(section.deadlineAt!).getTime() - Date.now()) / 1000))
      setRemaining(seconds)
      if (seconds <= 0 && !expiredHandled.current && skill) {
        expiredHandled.current = true
        handleSectionEnd(skill, true)
      }
    }
    tick()
    const interval = window.setInterval(tick, 1000)
    return () => window.clearInterval(interval)
  }, [section?.deadlineAt, section?.status, skill])

  useEffect(() => {
    if (flags && Object.keys(flags).length) localStorage.setItem(`apex-flags-${attemptId}`, JSON.stringify(flags))
  }, [flags, attemptId])

  useEffect(() => {
    localStorage.setItem(`apex-notes-${attemptId}`, notes)
  }, [notes, attemptId])

  useEffect(() => {
    if (!audioRef.current) return
    audioRef.current.volume = volume
  }, [volume, audioPart])

  // Restore the one-play audio position after a refresh. The audio is never
  // replayed from the beginning once the candidate has started it.
  useEffect(() => {
    if (!state || skill !== 'listening') return
    try {
      const raw = localStorage.getItem(audioStoreKey)
      if (!raw) return
      const saved = JSON.parse(raw) as { part?: number; time?: number; complete?: boolean }
      if (saved.complete) {
        setAudioComplete(true)
        setAudioPart(4)
        return
      }
      if (saved.part) setAudioPart(saved.part)
      if (saved.time && saved.time > 0) {
        audioResumeRef.current = saved.time
        setAudioResumeAt(saved.time)
        setAudioBlocked(true)
      }
    } catch {
      // A corrupt position should not block the exam.
    }
  }, [state?.attempt.id, skill, audioStoreKey])

  useEffect(() => {
    if (skill !== 'listening' || !state || audioComplete || section?.status !== 'in_progress') return
    try {
      const saved = JSON.parse(localStorage.getItem(audioStoreKey) || '{}')
      if (saved.complete) return
    } catch {}
    const audio = audioRef.current
    if (!audio) return
    audio.src = assetUrl(`${state.exam.audioUrl ?? '/media/listening'}/part${audioPart}.mp3`)
    audio.onloadedmetadata = () => {
      if (audioResumeRef.current > 0) {
        audio.currentTime = Math.min(audioResumeRef.current, Math.max(0, (audio.duration || 0) - 0.5))
      }
    }
    audio.load()
    if (audioResumeRef.current > 0) {
      setAudioBlocked(true)
      setAudioPlaying(false)
      return
    }
    const attemptPlay = async () => {
      try {
        await audio.play()
        setAudioPlaying(true)
        setAudioBlocked(false)
      } catch {
        setAudioBlocked(true)
        setAudioPlaying(false)
      }
    }
    attemptPlay()
  }, [audioPart, skill, state?.attempt.id, section?.status])

  async function handleSectionEnd(target: Skill, auto = false) {
    if (submittingRef.current) return
    submittingRef.current = true
    setSubmitting(true)
    setConfirmSubmit(false)
    setSubmitError('')
    try {
      await new Promise((resolve) => setTimeout(resolve, 700))
      const next = await api.submitSection(attemptId, target)
      setState(next)
      if (next.attempt.mode !== 'full') {
        setTransition(null)
        await api.complete(attemptId)
        router.push(`/results/?attempt=${attemptId}`)
      } else {
        const nextSkill: Skill | undefined =
          target === 'listening' ? 'reading' : target === 'reading' ? 'writing' : undefined
        setTransition({ from: target, next: nextSkill, auto, answered: answeredCount })
      }
      setSubmitting(false)
      submittingRef.current = false
      expiredHandled.current = false
    } catch (err) {
      setSubmitError(err instanceof Error ? err.message : 'Could not submit the section')
      setSubmitting(false)
      submittingRef.current = false
    }
  }

  function startNext() {
    setTransition(null)
  }

  function handleAnswer(questionId: string, value: string) {
    if (!skill) return
    setAnswers((current) => ({ ...current, [questionId]: value }))
    setAutosave('saving')
    savingCount.current += 1
    window.clearTimeout(timers.current[questionId])
    timers.current[questionId] = setTimeout(async () => {
      try {
        const saved = await api.saveAnswer(attemptId, skill, questionId, value, versions[questionId] ?? 0)
        setVersions((current) => ({ ...current, [questionId]: saved.version }))
        savingCount.current = Math.max(0, savingCount.current - 1)
        if (savingCount.current === 0) setAutosave('saved')
      } catch (err) {
        savingCount.current = Math.max(0, savingCount.current - 1)
        setAutosave('error')
        if (err instanceof ApiError && err.status === 409 && err.code !== 'SECTION_CLOSED') {
          const refreshed = await api.attempt(attemptId)
          setState(refreshed)
        }
      }
    }, 420)
  }

  function toggleFlag(questionId: string) {
    setFlags((current) => ({ ...current, [questionId]: !current[questionId] }))
  }

  function navigateToQuestion(question: Question) {
    if (!state) return
    if (skill === 'listening') {
      const part = state.exam.listening.find((p) => p.questions.some((q) => q.id === question.id))
      if (part) setViewedPart(part.number)
    }
    if (skill === 'reading') {
      const passage = state.exam.reading.find((p) => p.questions.some((q) => q.id === question.id))
      if (passage) setViewedPassage(passage.number)
    }
    setActiveQid(question.id)
    window.setTimeout(() => {
      const row = document.querySelector<HTMLElement>(`[data-qid="${question.id}"]`)
      if (!row) return
      row.scrollIntoView({ behavior: 'smooth', block: 'center' })
      row.querySelector<HTMLElement>('input, select, textarea, button')?.focus({ preventScroll: true })
    }, 90)
  }

  function trackActive(event: React.SyntheticEvent) {
    const holder = (event.target as HTMLElement).closest?.('[data-qid]')
    const id = holder?.getAttribute('data-qid')
    if (id) setActiveQid(id)
  }

  function startSplitDrag(event: React.PointerEvent<HTMLDivElement>) {
    const container = event.currentTarget.parentElement
    if (!container) return
    event.currentTarget.setPointerCapture(event.pointerId)
    const rect = container.getBoundingClientRect()
    const move = (e: PointerEvent) => setSplit(Math.min(75, Math.max(25, ((e.clientX - rect.left) / rect.width) * 100)))
    const up = () => { window.removeEventListener('pointermove', move); window.removeEventListener('pointerup', up) }
    window.addEventListener('pointermove', move)
    window.addEventListener('pointerup', up)
  }

  function openContextMenu(event: React.MouseEvent) {
    if ((event.target as HTMLElement).closest('input, textarea, select')) return
    const selection = window.getSelection()
    const range = selection && !selection.isCollapsed && selection.rangeCount ? selection.getRangeAt(0) : null
    const inside = !!range && !!passageRef.current?.contains(range.commonAncestorContainer)
    savedRange.current = inside ? range!.cloneRange() : null
    if (!inside && !highlightCount) return
    event.preventDefault()
    setContextMenu({ x: Math.min(event.clientX, window.innerWidth - 190), y: Math.min(event.clientY, window.innerHeight - 110), canHighlight: inside })
  }

  function addHighlight() {
    const range = savedRange.current
    setContextMenu(null)
    if (!range) return
    const HighlightCtor = (window as any).Highlight
    const highlights = (CSS as any).highlights
    if (!HighlightCtor || !highlights) return
    const existing = highlights.get('apex-hl')
    if (existing) existing.add(range)
    else highlights.set('apex-hl', new HighlightCtor(range))
    setHighlightCount((n) => n + 1)
    window.getSelection()?.removeAllRanges()
    savedRange.current = null
  }

  function clearHighlights() {
    const highlights = (CSS as any).highlights
    if (!highlights) return
    for (const key of Array.from(highlights.keys() as Iterable<string>)) {
      if (key.startsWith('apex-')) highlights.delete(key)
    }
    setHighlightCount(0)
    setContextMenu(null)
  }

  useEffect(() => {
    if (!contextMenu) return
    const close = () => setContextMenu(null)
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') close() }
    window.addEventListener('pointerdown', close)
    window.addEventListener('keydown', onKey)
    window.addEventListener('resize', close)
    return () => { window.removeEventListener('pointerdown', close); window.removeEventListener('keydown', onKey); window.removeEventListener('resize', close) }
  }, [contextMenu])

  if (loading) return <div className="exam-loading"><div className="spinner" /><p>Preparing your exam…</p></div>
  if (fatal || !state || !skill) {
    return (
      <div className="exam-loading">
        <ShieldAlert size={30} />
        <p>{fatal || 'This attempt could not be loaded.'}</p>
        <Button size="sm" onClick={() => router.push('/')}>Return to dashboard</Button>
      </div>
    )
  }

  const allQuestions: Question[] = skill === 'listening'
    ? state.exam.listening.flatMap((part) => part.questions)
    : skill === 'reading'
      ? state.exam.reading.flatMap((passage) => passage.questions)
      : []
  const answeredCount = allQuestions.filter((q) => (answers[q.id] ?? '').trim()).length
  const activeListeningPart = state.exam.listening.find((part) => part.number === viewedPart) ?? state.exam.listening[0]
  const activeReadingPassage = state.exam.reading.find((passage) => passage.number === viewedPassage) ?? state.exam.reading[0]
  const activeWritingTask = state.exam.writing.find((task) => task.number === activeTask) ?? state.exam.writing[0]
  const partList: { number: number; questions: Question[] }[] = skill === 'listening' ? state.exam.listening : skill === 'reading' ? state.exam.reading : []
  const activePartNumber = skill === 'listening' ? viewedPart : viewedPassage
  const activePart = partList.find((p) => p.number === activePartNumber) ?? partList[0]
  const currentQuestion = activePart ? (activePart.questions.find((q) => q.id === activeQid) ?? activePart.questions[0]) : undefined
  const qRange = (qs: Question[]) => qs.length ? `${Math.min(...qs.map((q) => q.number))}–${Math.max(...qs.map((q) => q.number))}` : ''
  function selectPart(number: number) {
    const first = partList.find((p) => p.number === number)?.questions[0]
    if (skill === 'listening') setViewedPart(number)
    else setViewedPassage(number)
    setActiveQid(first?.id ?? null)
  }
  function stepQuestion(delta: number) {
    if (!currentQuestion) return
    const index = allQuestions.findIndex((q) => q.id === currentQuestion.id)
    const target = allQuestions[Math.min(allQuestions.length - 1, Math.max(0, index + delta))]
    if (target) navigateToQuestion(target)
  }
  const timerClass = remaining <= 60 ? 'exam-timer--danger' : remaining <= 300 ? 'exam-timer--warning' : ''
  const currentFlagged = !!(currentQuestion && flags[currentQuestion.id])

  const transitionModal = (
    <Modal open={transition !== null} title={transition ? `${skillNames[transition.from]} complete` : ''} onClose={() => {}}>
      {transition && (
        <>
          <div className="modal-body">
            <div className="exam-summary-grid">
              <div><span>Section</span><strong>{skillNames[transition.from]}</strong></div>
              <div><span>Answered</span><strong>{transition.answered ?? answeredCount}</strong></div>
              <div><span>Status</span><strong style={{ color: 'var(--green)' }}>Locked</strong></div>
            </div>
            {transition.auto && <div className="unanswered-note">Time expired. Your answers were submitted automatically.</div>}
            <p style={{ fontSize: 12, color: '#697578', marginTop: 14 }}>
              {transition.next ? `The next section is ${skillNames[transition.next]}. Read the instructions, then start when you are ready.` : 'Your core test is complete. Continue to the speaking session.'}
            </p>
          </div>
          <div className="exam-modal-actions">
            <Button variant="secondary" size="sm" onClick={() => router.push('/')}>Save & exit</Button>
            <Button size="sm" onClick={startNext}>{transition.next ? `Continue to ${skillNames[transition.next]}` : 'Continue'} <ArrowRight size={15} /></Button>
          </div>
        </>
      )}
    </Modal>
  )

  if (skill === 'speaking') {
    return (
      <ExamChrome
        state={state} skill={skill} remaining={remaining} timerClass={timerClass} autosave={autosave}
        onExit={() => router.push('/')} onHelp={() => setHelpOpen(true)} onNotes={() => setNotesOpen(true)}
      >
        <SpeakingRoom
          state={state}
          onSubmitted={(next) => {
            setState(next)
            if (next.attempt.mode === 'full') setTransition({ from: 'speaking', next: undefined })
            else api.complete(attemptId).then(() => router.push(`/results/?attempt=${attemptId}`))
          }}
          onSkip={async () => {
            const result = await api.complete(attemptId)
            router.push(`/results/?attempt=${attemptId}`)
          }}
        />
        {transition?.from === 'speaking' ? (
          <Modal open title="Speaking complete" onClose={() => {}}>
            <div className="modal-body"><p style={{ fontSize: 13, color: 'var(--muted)' }}>Your speaking responses have been saved. You can now generate your result report.</p></div>
            <div className="exam-modal-actions"><Button onClick={() => api.complete(attemptId).then(() => router.push(`/results/?attempt=${attemptId}`))}>View my results <ArrowRight size={15} /></Button></div>
          </Modal>
        ) : transitionModal}
        <Modal open={helpOpen} title="Test help" onClose={() => setHelpOpen(false)}>
          <HelpBody />
        </Modal>
        <Modal open={notesOpen} title="Notes" onClose={() => setNotesOpen(false)}>
          <div className="modal-body"><p style={{ fontSize: 11, color: 'var(--muted)', marginBottom: 10 }}>Notes are private and not assessed.</p><textarea className="notes-area" style={{ color: '#24343c', background: '#f8f7f2', borderColor: '#ddd' }} value={notes} onChange={(e) => setNotes(e.target.value)} placeholder="Write notes here…" /></div>
        </Modal>
      </ExamChrome>
    )
  }

  if (section?.status === 'not_started') {
    return (
      <ExamChrome state={state} skill={skill} remaining={remaining} timerClass="" autosave={autosave} onExit={() => router.push('/')} onHelp={() => setHelpOpen(true)} onNotes={() => setNotesOpen(true)}>
        <SectionIntro skill={skill} onStart={startNextFromState} state={state} submitting={submitting} />
        {transitionModal}
        <Modal open={helpOpen} title="Test help" onClose={() => setHelpOpen(false)}><HelpBody /></Modal>
      </ExamChrome>
    )

    async function startNextFromState() {
      if (!skill) return
      setSubmitting(true)
      try {
        const next = await api.startSection(attemptId, skill)
        setState(next)
      } catch (err) {
        setFatal(err instanceof Error ? err.message : 'Could not start the section')
      } finally {
        setSubmitting(false)
      }
    }
  }

  return (
    <ExamChrome
      state={state} skill={skill} remaining={remaining} timerClass={timerClass} autosave={autosave}
      onExit={() => router.push('/')} onHelp={() => setHelpOpen(true)} onNotes={() => setNotesOpen(true)}
      tools={skill === 'listening' ? (
        <label className="header-volume" title="Volume">
          <Volume2 size={18} />
          <input type="range" min="0" max="1" step=".05" value={volume} onChange={(e) => setVolume(Number(e.target.value))} aria-label="Audio volume" />
        </label>
      ) : null}
    >
      {submitError && <div className="exam-error" role="alert">{submitError}</div>}

      {skill === 'listening' && (
        <div className="listening-layout" onFocusCapture={trackActive} onClickCapture={trackActive}>
          <div className="part-banner">
            <div className="part-banner-text">
              <strong>Part {activeListeningPart.number}</strong>
              <span>Listen and answer questions {qRange(activeListeningPart.questions)}.</span>
            </div>
            <div className={`audio-state ${audioPlaying ? 'audio-state--on' : ''}`} role="status">
              <div className={`audio-equalizer ${audioPlaying ? '' : 'audio-equalizer--paused'}`} aria-hidden="true"><i /><i /><i /><i /><i /></div>
              <span>{audioComplete ? 'Recording finished' : audioPlaying ? 'Recording is playing' : audioBlocked ? 'Recording waiting' : 'Recording'}</span>
            </div>
            <audio
              ref={audioRef}
              onTimeUpdate={(event) => {
                const audio = event.currentTarget
                setAudioProgress(audio.duration ? audio.currentTime / audio.duration : 0)
                try { localStorage.setItem(audioStoreKey, JSON.stringify({ part: audioPart, time: audio.currentTime, complete: false })) } catch {}
              }}
              onPlay={() => { setAudioPlaying(true); setAudioBlocked(false) }}
              onPause={(event) => { if (!event.currentTarget.ended) setAudioPlaying(false) }}
              onEnded={() => {
                setAudioPlaying(false)
                setAudioProgress(0)
                audioResumeRef.current = 0
                setAudioResumeAt(0)
                if (audioPart < 4) {
                  try { localStorage.setItem(audioStoreKey, JSON.stringify({ part: audioPart + 1, time: 0, complete: false })) } catch {}
                  setAudioPart((part) => part + 1)
                } else {
                  try { localStorage.setItem(audioStoreKey, JSON.stringify({ complete: true })) } catch {}
                  setAudioComplete(true)
                }
              }}
              preload="auto"
            />
          </div>
          {audioBlocked && !audioComplete && (
            <div className="audio-play-overlay">
              <Headphones size={40} />
              <h2>{audioResumeAt > 0 ? 'Resume the recording' : 'Ready to listen?'}</h2>
              <p>{audioResumeAt > 0 ? 'The recording continues where you left off. It will not replay.' : 'The recording is played once only. Make sure your headphones are on, then press the button.'}</p>
              <Button size="lg" onClick={() => {
                const audio = audioRef.current
                if (!audio) return
                if (audioResumeAt > 0 && audio.readyState >= 1) audio.currentTime = Math.min(audioResumeAt, Math.max(0, (audio.duration || 0) - 0.5))
                audio.play().then(() => { audioResumeRef.current = 0; setAudioResumeAt(0); setAudioBlocked(false) }).catch(() => setAudioBlocked(true))
              }}>{audioResumeAt > 0 ? 'Resume recording' : 'Play recording'}</Button>
            </div>
          )}
          <div className="listening-main">
            <div className="listening-content">
              <div className="part-heading">
                <h2>{activeListeningPart.title}</h2>
                <p>{activeListeningPart.context}</p>
              </div>
              <QuestionSets
                groups={activeListeningPart.groups}
                questions={activeListeningPart.questions}
                answers={answers}
                flags={flags}
                onAnswer={handleAnswer}
              />
            </div>
          </div>
          <ExamFooter
            label="Part" parts={partList.map((p) => ({ number: p.number, questions: p.questions }))}
            activePart={activePartNumber} currentQuestionId={currentQuestion?.id ?? null}
            answers={answers} flags={flags}
            onSelectPart={selectPart} onNavigate={navigateToQuestion}
            onPrevious={() => stepQuestion(-1)} onNext={() => stepQuestion(1)}
            onSubmit={() => setConfirmSubmit(true)}
            reviewChecked={currentFlagged} onToggleReview={() => currentQuestion && toggleFlag(currentQuestion.id)}
          />
        </div>
      )}

      {skill === 'reading' && (
        <div className="reading-layout" onFocusCapture={trackActive} onClickCapture={trackActive}>
          <div className="part-banner">
            <div className="part-banner-text">
              <strong>Part {activeReadingPassage.number}</strong>
              <span>Read the text and answer questions {qRange(activeReadingPassage.questions)}.</span>
            </div>
            <span className="banner-hint">Select text and right-click to highlight</span>
          </div>
          <div className="reading-columns" style={{ gridTemplateColumns: `${split}% 10px 1fr` }}>
            <div className="passage-pane" ref={passageRef} onContextMenu={openContextMenu}>
              <div className="passage-inner">
                <div className="passage-heading">
                  <h1>{activeReadingPassage.title}</h1>
                  <p>{activeReadingPassage.subtitle}</p>
                </div>
                <div className="passage-body">
                  {activeReadingPassage.paragraphs.map((paragraph, index) => (
                    <p key={`${paragraph.label}-${index}`}>{paragraph.label?.trim() && <span className="para-label">{paragraph.label}</span>}{paragraph.text}</p>
                  ))}
                </div>
              </div>
            </div>
            <div className="pane-divider" role="separator" aria-orientation="vertical" aria-label="Resize passage and questions" onPointerDown={startSplitDrag}><i aria-hidden="true"><ChevronLeft size={13} /><ChevronRight size={13} /></i></div>
            <div className="question-pane">
              <div className="question-pane-inner">
                <QuestionSets groups={activeReadingPassage.groups} questions={activeReadingPassage.questions} answers={answers} flags={flags} onAnswer={handleAnswer} />
              </div>
            </div>
          </div>
          <ExamFooter
            label="Part" parts={partList.map((p) => ({ number: p.number, questions: p.questions }))}
            activePart={activePartNumber} currentQuestionId={currentQuestion?.id ?? null}
            answers={answers} flags={flags}
            onSelectPart={selectPart} onNavigate={navigateToQuestion}
            onPrevious={() => stepQuestion(-1)} onNext={() => stepQuestion(1)}
            onSubmit={() => setConfirmSubmit(true)}
            reviewChecked={currentFlagged} onToggleReview={() => currentQuestion && toggleFlag(currentQuestion.id)}
          />
          {contextMenu && (
            <div className="exam-context-menu" role="menu" style={{ left: contextMenu.x, top: contextMenu.y }} onPointerDown={(e) => e.stopPropagation()}>
              <button role="menuitem" onClick={addHighlight} disabled={!contextMenu.canHighlight}>Highlight</button>
              <button role="menuitem" onClick={clearHighlights} disabled={!highlightCount}>Clear all highlights</button>
            </div>
          )}
        </div>
      )}

      {skill === 'writing' && (
        <div className="writing-layout">
          <div className="part-banner">
            <div className="part-banner-text">
              <strong>Part {activeTask}</strong>
              <span>You should spend about {activeWritingTask.suggestedMinutes} minutes on this task. Write at least {activeWritingTask.minimumWords} words.</span>
            </div>
          </div>
          <div className="writing-columns" style={{ gridTemplateColumns: `${split}% 10px 1fr` }}>
            <div className="writing-prompt">
              <div className="writing-prompt-inner">
                <h1>{activeWritingTask.title}</h1>
                <div className="writing-prompt-text">{activeWritingTask.prompt}</div>
                {activeWritingTask.figure && (
                  <figure className="writing-figure">
                    {/* eslint-disable-next-line @next/next/no-img-element */}
                    <img src={assetUrl(activeWritingTask.figure)} alt={activeWritingTask.figureAlt ?? 'Task 1 figure'} />
                  </figure>
                )}
                <ul className="writing-instructions">
                  {activeWritingTask.instructions.map((instruction) => <li key={instruction}><Check size={14} /><span>{instruction}</span></li>)}
                </ul>
              </div>
            </div>
            <div className="pane-divider" role="separator" aria-orientation="vertical" aria-label="Resize prompt and answer" onPointerDown={startSplitDrag}><i aria-hidden="true"><ChevronLeft size={13} /><ChevronRight size={13} /></i></div>
            <div className="editor-pane">
              <textarea
                className="writing-textarea"
                value={activeTask === 1 ? answers['writing-task-1'] ?? '' : answers['writing-task-2'] ?? ''}
                onChange={(event) => handleAnswer(activeTask === 1 ? 'writing-task-1' : 'writing-task-2', event.target.value)}
                placeholder="Type your answer here"
                spellCheck={false}
                aria-label={`Task ${activeTask} answer`}
              />
              <div className="editor-footer">
                <span className={`word-count ${wordCount(activeTask === 1 ? answers['writing-task-1'] ?? '' : answers['writing-task-2'] ?? '') < activeWritingTask.minimumWords ? 'word-count--under' : ''}`}>
                  Word count: <strong>{wordCount(activeTask === 1 ? answers['writing-task-1'] ?? '' : answers['writing-task-2'] ?? '')}</strong>
                </span>
              </div>
            </div>
          </div>
          <div className="exam-footer-wrap">
            <div className="footer-nav">
              <button className="nav-square" onClick={() => setActiveTask(1)} disabled={activeTask === 1} aria-label="Previous part"><ChevronLeft size={22} /></button>
              <button className="nav-square" onClick={() => setActiveTask(2)} disabled={activeTask === 2} aria-label="Next part"><ChevronRight size={22} /></button>
            </div>
            <nav className="exam-footer" aria-label="Part navigation">
              <div className="part-buttons">
                {state.exam.writing.map((task) => (
                  <button key={task.id} className={`part-btn ${activeTask === task.number ? 'part-btn--active' : ''}`} onClick={() => setActiveTask(task.number)} aria-current={activeTask === task.number ? 'step' : undefined}>
                    <b>Part {task.number}</b>
                    <span>{wordCount(task.number === 1 ? answers['writing-task-1'] ?? '' : answers['writing-task-2'] ?? '')} words</span>
                  </button>
                ))}
              </div>
              <button className="finish-btn" onClick={() => setConfirmSubmit(true)} aria-label="Finish section" title="Finish section"><Check size={22} strokeWidth={2.6} /></button>
            </nav>
          </div>
        </div>
      )}

      <Modal open={confirmSubmit} title={`Finish ${skillNames[skill]}?`} onClose={() => setConfirmSubmit(false)}>
        <div className="modal-body">
          <div className="exam-summary-grid">
            <div><span>Answered</span><strong>{skill === 'writing' ? [answers['writing-task-1'], answers['writing-task-2']].filter((v) => (v ?? '').trim()).length : answeredCount}</strong></div>
            <div><span>Unanswered</span><strong>{skill === 'writing' ? 2 - [answers['writing-task-1'], answers['writing-task-2']].filter((v) => (v ?? '').trim()).length : 40 - answeredCount}</strong></div>
            <div><span>Time left</span><strong>{formatClock(remaining)}</strong></div>
          </div>
          <p style={{ fontSize: 12, color: '#697578' }}>Once submitted, this section is locked and cannot be reopened. {skill === 'listening' && audioComplete ? 'The audio has finished.' : ''}</p>
          {skill !== 'writing' && 40 - answeredCount > 0 && <div className="unanswered-note"><AlertTriangle size={13} style={{ display: 'inline', marginRight: 5 }} />You still have {40 - answeredCount} unanswered question{40 - answeredCount === 1 ? '' : 's'}.</div>}
        </div>
        <div className="exam-modal-actions">
          <Button variant="secondary" size="sm" onClick={() => setConfirmSubmit(false)}>Keep working</Button>
          <Button size="sm" onClick={() => handleSectionEnd(skill)} disabled={submitting}>{submitting ? 'Submitting…' : `Submit ${skillNames[skill]}`}</Button>
        </div>
      </Modal>

      {transitionModal}

      <Modal open={helpOpen} title="Test help" onClose={() => setHelpOpen(false)}><HelpBody /></Modal>
      <Modal open={notesOpen} title="Notes" onClose={() => setNotesOpen(false)}>
        <div className="modal-body"><p style={{ fontSize: 11, color: 'var(--muted)', marginBottom: 10 }}>Notes are private and are not assessed.</p><textarea className="notes-area" style={{ color: '#24343c', background: '#f8f7f2', borderColor: '#ddd' }} value={notes} onChange={(e) => setNotes(e.target.value)} placeholder="Write notes here…" /></div>
      </Modal>
    </ExamChrome>
  )
}

type TextSize = 'standard' | 'large' | 'xlarge'
type Contrast = 'standard' | 'inverse' | 'yellow'

function timerLabel(remaining: number) {
  if (remaining <= 60) return { value: String(Math.max(0, remaining)), unit: remaining === 1 ? 'second left' : 'seconds left' }
  const minutes = Math.ceil(remaining / 60)
  return { value: String(minutes), unit: minutes === 1 ? 'minute left' : 'minutes left' }
}

function ExamChrome({
  state, skill, remaining, timerClass, autosave, onExit, onHelp, onNotes, tools, children,
}: {
  state: AttemptState
  skill: Skill
  remaining: number
  timerClass: string
  autosave: string
  onExit: () => void
  onHelp: () => void
  onNotes: () => void
  tools?: React.ReactNode
  children: React.ReactNode
}) {
  const [confirmExit, setConfirmExit] = useState(false)
  const [hideTimer, setHideTimer] = useState(false)
  const [menuOpen, setMenuOpen] = useState(false)
  const [textSize, setTextSize] = useState<TextSize>('standard')
  const [contrast, setContrast] = useState<Contrast>('standard')
  const menuRef = useRef<HTMLDivElement | null>(null)
  const [displayLoaded, setDisplayLoaded] = useState(false)

  useEffect(() => {
    try {
      const saved = JSON.parse(localStorage.getItem('apex-exam-display') || '{}') as { textSize?: TextSize; contrast?: Contrast }
      if (saved.textSize) setTextSize(saved.textSize)
      if (saved.contrast) setContrast(saved.contrast)
    } catch { /* display preferences are optional */ }
    setDisplayLoaded(true)
  }, [])
  useEffect(() => {
    if (!displayLoaded) return
    try { localStorage.setItem('apex-exam-display', JSON.stringify({ textSize, contrast })) } catch {}
  }, [textSize, contrast, displayLoaded])
  useEffect(() => {
    if (!menuOpen) return
    const close = (e: PointerEvent) => { if (!menuRef.current?.contains(e.target as Node)) setMenuOpen(false) }
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') setMenuOpen(false) }
    window.addEventListener('pointerdown', close)
    window.addEventListener('keydown', onKey)
    return () => { window.removeEventListener('pointerdown', close); window.removeEventListener('keydown', onKey) }
  }, [menuOpen])

  const label = timerLabel(remaining)
  const candidateNo = state.attempt.id.replace(/[^0-9a-f]/gi, '').slice(0, 8).toUpperCase()
  const offline = autosave === 'error'
  return (
    <div className={`exam-shell exam-shell--text-${textSize} exam-shell--contrast-${contrast}`}>
      <header className="exam-topbar">
        <div className="exam-topbar-left">
          <div className="exam-brand"><Logo /></div>
          <div className="exam-candidate">
            <strong>Demo candidate</strong>
            <span>{candidateNo.slice(0, 4)} {candidateNo.slice(4)} · {skillNames[skill]}</span>
          </div>
        </div>
        <div className="exam-topbar-center">
          <button
            type="button"
            className={`exam-timer ${hideTimer ? 'exam-timer--hidden' : timerClass}`}
            role="timer"
            aria-live="off"
            aria-label={hideTimer ? 'Timer hidden. Click to show time remaining' : `${label.value} ${label.unit}. Click to hide`}
            title={hideTimer ? 'Show time' : 'Hide time'}
            onClick={() => setHideTimer((v) => !v)}
          >
            <Clock3 size={18} />
            {hideTimer ? <span className="exam-timer-unit">Show time</span> : <><span className="exam-timer-clock">{label.value}</span><span className="exam-timer-unit">{label.unit}</span></>}
          </button>
        </div>
        <div className="exam-topbar-right">
          <span className={`exam-autosave ${autosave === 'saved' ? 'exam-autosave--saved' : offline ? 'exam-autosave--error' : ''}`} title={offline ? 'Answers not saved — check your connection' : autosave === 'saving' ? 'Saving…' : 'All answers saved'} role="status">
            {offline ? <WifiOff size={19} /> : <Wifi size={19} />}
            <span className="sr-only">{autosave === 'saving' ? 'Saving…' : offline ? 'Save failed' : 'Saved'}</span>
          </span>
          {tools}
          <button className="exam-icon-button" onClick={onHelp} aria-label="Help" title="Help"><HelpCircle size={20} /></button>
          <div className="exam-menu" ref={menuRef}>
            <button className={`exam-icon-button ${menuOpen ? 'exam-icon-button--on' : ''}`} onClick={() => setMenuOpen((v) => !v)} aria-label="Options" aria-haspopup="menu" aria-expanded={menuOpen} title="Options"><Menu size={21} /></button>
            {menuOpen && (
              <div className="exam-menu-panel" role="menu">
                <button role="menuitem" onClick={() => { setMenuOpen(false); onNotes() }}><FileText size={16} /> Notes</button>
                <button role="menuitem" onClick={() => { setMenuOpen(false); onHelp() }}><HelpCircle size={16} /> Help</button>
                <div className="exam-menu-group">
                  <span>Text size</span>
                  <div className="exam-menu-seg">
                    {(['standard', 'large', 'xlarge'] as TextSize[]).map((size) => (
                      <button key={size} role="menuitemradio" aria-checked={textSize === size} className={textSize === size ? 'on' : ''} onClick={() => setTextSize(size)}>
                        {size === 'standard' ? 'Standard' : size === 'large' ? 'Large' : 'Extra large'}
                      </button>
                    ))}
                  </div>
                </div>
                <div className="exam-menu-group">
                  <span>Colour</span>
                  <div className="exam-menu-seg">
                    {(['standard', 'inverse', 'yellow'] as Contrast[]).map((c) => (
                      <button key={c} role="menuitemradio" aria-checked={contrast === c} className={`swatch swatch--${c} ${contrast === c ? 'on' : ''}`} onClick={() => setContrast(c)}>
                        {c === 'standard' ? 'Black on white' : c === 'inverse' ? 'White on black' : 'Yellow on black'}
                      </button>
                    ))}
                  </div>
                </div>
                <button role="menuitem" className="exam-menu-exit" onClick={() => { setMenuOpen(false); setConfirmExit(true) }}><LogOut size={16} /> Exit test</button>
              </div>
            )}
          </div>
        </div>
      </header>
      {children}
      <Modal open={confirmExit} title="Leave this test?" onClose={() => setConfirmExit(false)}>
        <div className="modal-body">
          <p style={{ fontSize: 15, lineHeight: 1.7 }}>Your answers are already saved. The section clock will continue while you are away, so you can resume from the dashboard.</p>
          <div className="unanswered-note" style={{ marginTop: 12 }}><AlertTriangle size={14} style={{ display: 'inline', marginRight: 6 }} />Leaving does not pause the exam.</div>
        </div>
        <div className="exam-modal-actions">
          <Button variant="secondary" size="sm" onClick={() => setConfirmExit(false)}>Stay in the test</Button>
          <Button size="sm" onClick={onExit}>Save & exit</Button>
        </div>
      </Modal>
    </div>
  )
}

function ExamFooter({
  label, parts, activePart, currentQuestionId, answers, flags, onSelectPart, onNavigate, onPrevious, onNext, onSubmit, reviewChecked, onToggleReview,
}: {
  label: string
  parts: { number: number; questions: Question[] }[]
  activePart: number
  currentQuestionId: string | null
  answers: Record<string, string>
  flags: Record<string, boolean>
  onSelectPart: (number: number) => void
  onNavigate: (question: Question) => void
  onPrevious: () => void
  onNext: () => void
  onSubmit: () => void
  reviewChecked: boolean
  onToggleReview: () => void
}) {
  return (
    <div className="exam-footer-wrap">
      <div className="footer-nav">
        <button className="nav-square" onClick={onPrevious} aria-label="Previous question"><ChevronLeft size={22} /></button>
        <button className="nav-square" onClick={onNext} aria-label="Next question"><ChevronRight size={22} /></button>
      </div>
      <nav className="exam-footer" aria-label="Question navigation">
        <label className={`review-toggle ${reviewChecked ? 'review-toggle--on' : ''}`} title="Mark the current question so you can come back to it">
          <input type="checkbox" checked={reviewChecked} onChange={onToggleReview} />
          <span>Review</span>
        </label>
        <div className="part-buttons">
          {parts.map((part) => {
            const answered = part.questions.filter((q) => (answers[q.id] ?? '').trim()).length
            const isActive = part.number === activePart
            return isActive ? (
              <div key={part.number} className="part-btn part-btn--active part-btn--open" aria-current="step">
                <b>{label} {part.number}</b>
                <div className="palette">
                  {part.questions.map((question) => (
                    <button
                      key={question.id}
                      className={`${(answers[question.id] ?? '').trim() ? 'answered' : ''} ${flags[question.id] ? 'flagged' : ''} ${currentQuestionId === question.id ? 'active' : ''}`}
                      onClick={() => onNavigate(question)}
                      title={flags[question.id] ? 'Marked for review' : `Question ${question.number}`}
                      aria-label={`Question ${question.number}${(answers[question.id] ?? '').trim() ? ', answered' : ''}${flags[question.id] ? ', marked for review' : ''}`}
                      aria-current={currentQuestionId === question.id ? 'true' : undefined}
                    >
                      {question.number}
                    </button>
                  ))}
                </div>
              </div>
            ) : (
              <button key={part.number} className="part-btn" onClick={() => onSelectPart(part.number)}>
                <b>{label} {part.number}</b>
                <span>{answered} of {part.questions.length}</span>
              </button>
            )
          })}
        </div>
        <button className="finish-btn" onClick={onSubmit} aria-label="Finish section" title="Finish section"><Check size={22} strokeWidth={2.6} /></button>
      </nav>
    </div>
  )
}

function SectionIntro({ skill, onStart, state, submitting }: { skill: Skill; onStart: () => void; state: AttemptState; submitting: boolean }) {
  const info: Record<Skill, { time: string; instructions: string[]; information: string[] }> = {
    listening: {
      time: 'Approximately 30 minutes',
      instructions: ['Answer all the questions.', 'You can change your answers at any time during the test.'],
      information: ['There are 40 questions in this test.', 'Each question carries one mark.', 'There are four parts to the test.', 'Please note you will hear each part once only.', 'For each part of the test there will be time for you to look through the questions and time for you to check your answers.'],
    },
    reading: {
      time: '1 hour',
      instructions: ['Answer all the questions.', 'You can change your answers at any time during the test.'],
      information: ['There are 40 questions in this test.', 'Each question carries one mark.', 'There are three parts to the test.', 'The test clock will show you when there are 10 minutes and 5 minutes remaining.'],
    },
    writing: {
      time: '1 hour',
      instructions: ['Answer both parts.', 'You can change your answers at any time during the test.'],
      information: ['There are two parts in this test.', 'Part 2 contributes twice as much as Part 1 to the writing score.', 'The test clock will show you when there are 10 minutes and 5 minutes remaining.'],
    },
    speaking: {
      time: '11 to 14 minutes',
      instructions: ['Answer the examiner’s questions.', 'Speak clearly and at a natural pace.'],
      information: ['There are three parts to the test.', 'In Part 2 you will have one minute to prepare before you speak.'],
    },
  }
  const selected = info[skill]
  const [tone, setTone] = useState(false)
  function playTone() {
    try {
      const Ctx = window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext
      const ctx = new Ctx()
      const osc = ctx.createOscillator()
      const gain = ctx.createGain()
      osc.frequency.value = 440
      gain.gain.value = 0.12
      osc.connect(gain).connect(ctx.destination)
      osc.start()
      setTone(true)
      window.setTimeout(() => { osc.stop(); ctx.close(); setTone(false) }, 1200)
    } catch { /* sound check is optional */ }
  }
  return (
    <div className="section-intro">
      <div className="section-intro-card">
        <h1>IELTS Academic {skillNames[skill]}</h1>
        <p className="intro-time"><strong>Time:</strong> {selected.time}</p>
        <h2>Instructions to candidates</h2>
        <ul>{selected.instructions.map((line) => <li key={line}>{line}</li>)}</ul>
        <h2>Information for candidates</h2>
        <ul>{selected.information.map((line) => <li key={line}>{line}</li>)}</ul>
        {skill === 'listening' && (
          <div className="sound-check">
            <Headphones size={22} />
            <div><strong>Check your sound</strong><span>Put on your headphones, play the test sound and set the volume with the slider at the top of the screen.</span></div>
            <Button variant="secondary" size="sm" onClick={playTone} icon={<Volume2 size={15} />}>{tone ? 'Playing…' : 'Play sound'}</Button>
          </div>
        )}
        <div className="intro-candidate">
          <span>Candidate: <strong>Demo candidate</strong></span>
          <span>Test: <strong>{state.exam.title}</strong></span>
        </div>
        <div className="intro-actions">
          <Button size="lg" onClick={onStart} disabled={submitting}>{submitting ? 'Starting…' : 'Start test'}</Button>
          <span>The timer starts when you press Start test.</span>
        </div>
      </div>
    </div>
  )
}

function HelpBody() {
  return (
    <div className="modal-body help-body">
      <p><strong>Moving around:</strong> use the question numbers at the bottom of the screen, or the arrow buttons above them. Click a part name to open that part.</p>
      <p><strong>Review:</strong> tick <em>Review</em> to mark the current question. Marked questions show a dot above their number.</p>
      <p><strong>Highlighting (Reading):</strong> select text in the passage, right-click and choose <em>Highlight</em>.</p>
      <p><strong>Display:</strong> open the menu (☰) to change the text size or colours, or to open your notes.</p>
      <p><strong>Timer:</strong> click the timer to hide or show it. When it reaches zero the section is submitted automatically.</p>
      <p><strong>Saving:</strong> every answer is saved as you type. The connection icon turns red if saving fails.</p>
    </div>
  )
}

function wordCount(text: string) {
  return (text.trim().match(/[A-Za-z0-9'’-]+/g) ?? []).length
}
