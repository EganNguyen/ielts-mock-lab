'use client'

import { useCallback, useEffect, useRef, useState } from 'react'
import { ArrowRight, Mic, MicOff, Play, SkipForward, Square, Volume2 } from 'lucide-react'
import { api, type AttemptState } from '@/lib/api'
import { assetUrl } from '@/lib/assets'
import { Button, formatClock } from '@/components/ui'

type Phase = 'intro' | 'question' | 'prep' | 'longturn' | 'done'
type Turn = { part: number; questionId: string; text: string; maxSeconds: number }

export function SpeakingRoom({ state, onSubmitted, onSkip }: { state: AttemptState; onSubmitted: (next: AttemptState) => void; onSkip: () => void }) {
  const parts = state.exam.speaking
  const part1 = parts.find((p) => p.number === 1)
  const part2 = parts.find((p) => p.number === 2)
  const part3 = parts.find((p) => p.number === 3)
  const cue = part2?.cueCard
  const [phase, setPhase] = useState<Phase>('intro')
  const [started, setStarted] = useState(false)
  const [muted, setMuted] = useState(false)
  const [part, setPart] = useState(1)
  const [index, setIndex] = useState(0)
  const [recording, setRecording] = useState(false)
  const [recordSeconds, setRecordSeconds] = useState(0)
  const [prepSeconds, setPrepSeconds] = useState(cue?.preparationSeconds ?? 60)
  const [permissionError, setPermissionError] = useState('')
  const [uploadError, setUploadError] = useState('')
  const [notes, setNotes] = useState('')
  const [uploaded, setUploaded] = useState(0)
  const [finishing, setFinishing] = useState(false)
  const [micStream, setMicStream] = useState<MediaStream | null>(null)
  const [examinerSpeaking, setExaminerSpeaking] = useState(false)
  const micLevel = useMicLevel(micStream)

  const streamRef = useRef<MediaStream | null>(null)
  const recorderRef = useRef<MediaRecorder | null>(null)
  const chunksRef = useRef<Blob[]>([])
  const speechRef = useRef<any>(null)
  const transcriptRef = useRef('')
  const recordStartRef = useRef(0)
  const recordTimerRef = useRef<number | null>(null)
  const prepTimerRef = useRef<number | null>(null)
  const uploadQueueRef = useRef<Promise<void>>(Promise.resolve())
  const currentTurnRef = useRef<Turn | null>(null)
  const autoStopRef = useRef(false)

  const allQuestions = [...(part1?.questions ?? []), ...(part3?.questions ?? [])]
  const totalTurns = allQuestions.length + 1
  const doneTurns = (part - 1 === 0 ? index : part === 2 ? part1?.questions.length ?? 0 : (part1?.questions.length ?? 0) + 1 + index)

  const examinerAudioRef = useRef<HTMLAudioElement | null>(null)
  const speak = useCallback((text: string, asset?: string) => {
    if (muted || typeof window === 'undefined') return
    const fallback = () => {
      if (!text || !('speechSynthesis' in window)) return
      window.speechSynthesis.cancel()
      const utterance = new SpeechSynthesisUtterance(text)
      utterance.rate = 0.92
      utterance.onstart = () => setExaminerSpeaking(true)
      utterance.onend = () => setExaminerSpeaking(false)
      utterance.onerror = () => setExaminerSpeaking(false)
      const voices = window.speechSynthesis.getVoices()
      const preferred = voices.find((voice) => voice.lang === 'en-GB') ?? voices.find((voice) => voice.lang.startsWith('en'))
      if (preferred) utterance.voice = preferred
      window.speechSynthesis.speak(utterance)
    }
    if (asset) {
      examinerAudioRef.current?.pause()
      const audio = new Audio(assetUrl(`/media/speaking/examiner/${state.exam.id}/${asset}.mp3`))
      examinerAudioRef.current = audio
      audio.onerror = () => { setExaminerSpeaking(false); fallback() }
      audio.onplay = () => setExaminerSpeaking(true)
      audio.onended = () => setExaminerSpeaking(false)
      audio.onpause = () => setExaminerSpeaking(false)
      audio.play().catch(() => {
        // Autoplay may be blocked; the "Hear question" control re-triggers it.
      })
      return
    }
    fallback()
  }, [muted, state.exam.id])

  useEffect(() => () => {
    if (recordTimerRef.current) window.clearInterval(recordTimerRef.current)
    if (prepTimerRef.current) window.clearInterval(prepTimerRef.current)
    streamRef.current?.getTracks().forEach((track) => track.stop())
    if (speechRef.current) speechRef.current.stop()
    examinerAudioRef.current?.pause()
    if (typeof window !== 'undefined') window.speechSynthesis?.cancel()
  }, [])

  async function testMic() {
    setPermissionError('')
    if (streamRef.current) return true
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      streamRef.current = stream
      setMicStream(stream)
      return true
    } catch {
      setPermissionError('Microphone access was denied. You can still continue with a clearly labelled no-recording speaking session, but the estimate will be less reliable.')
      return false
    }
  }

  async function begin() {
    setPermissionError('')
    try {
      if (!(await testMic())) return
      setStarted(true)
      setPhase('question')
      setPart(1)
      setIndex(0)
      speak('Good morning. My name is Emma, and I will be your examiner today. This is the speaking test. Let us begin.', 'intro')
      setTimeout(() => speak(part1?.questions[0]?.text ?? 'Let’s begin.', part1?.questions[0]?.id), 12500)
    } catch {
      setPermissionError('Microphone access was denied. You can still continue with a clearly labelled no-recording speaking session, but the estimate will be less reliable.')
    }
  }

  function beginNoRecording() {
    setStarted(true)
    setPhase('question')
    setPart(1)
    setIndex(0)
  }

  function currentQuestion() {
    if (part === 1) return part1?.questions[index]
    if (part === 3) return part3?.questions[index]
    return null
  }

  function currentTurn(): Turn | null {
    if (part === 2) {
      return { part: 2, questionId: 'speaking-cue', text: cue?.topic ?? '', maxSeconds: cue?.speakingSeconds ?? 120 }
    }
    const question = currentQuestion()
    if (!question) return null
    return { part, questionId: question.id, text: question.text, maxSeconds: part === 1 ? 60 : 90 }
  }

  function startSpeechRecognition() {
    transcriptRef.current = ''
    const Recognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition
    if (!Recognition) return
    try {
      const recognition = new Recognition()
      recognition.continuous = true
      recognition.interimResults = true
      recognition.lang = 'en-GB'
      recognition.onresult = (event: any) => {
        let text = ''
        for (let i = 0; i < event.results.length; i++) text += event.results[i][0].transcript + ' '
        transcriptRef.current = text.trim()
      }
      recognition.onerror = () => {}
      recognition.start()
      speechRef.current = recognition
    } catch {
      speechRef.current = null
    }
  }

  function stopSpeechRecognition() {
    try { speechRef.current?.stop() } catch {}
    speechRef.current = null
  }

  async function startRecording(turn: Turn) {
    if (!streamRef.current) return
    setUploadError('')
    currentTurnRef.current = turn
    chunksRef.current = []
    transcriptRef.current = ''
    const recorder = new MediaRecorder(streamRef.current)
    recorderRef.current = recorder
    recorder.ondataavailable = (event) => { if (event.data.size > 0) chunksRef.current.push(event.data) }
    recorder.onstop = () => {
      const duration = Math.max(1, Math.round((Date.now() - recordStartRef.current) / 1000))
      const blob = new Blob(chunksRef.current, { type: recorder.mimeType || 'audio/webm' })
      const form = new FormData()
      form.append('questionId', turn.questionId)
      form.append('part', String(turn.part))
      form.append('durationSeconds', String(duration))
      form.append('transcript', transcriptRef.current)
      form.append('audio', blob, `${turn.questionId}.webm`)
      uploadQueueRef.current = uploadQueueRef.current.then(async () => {
        try {
          await api.speaking(state.attempt.id, form)
          setUploaded((n) => n + 1)
        } catch (err) {
          setUploadError(err instanceof Error ? err.message : 'Could not upload the recording')
        }
      })
    }
    recorder.start()
    startSpeechRecognition()
    recordStartRef.current = Date.now()
    setRecording(true)
    setRecordSeconds(0)
    recordTimerRef.current = window.setInterval(() => {
      const seconds = Math.round((Date.now() - recordStartRef.current) / 1000)
      setRecordSeconds(seconds)
      if (seconds >= turn.maxSeconds) {
        autoStopRef.current = true
        stopRecording()
      }
    }, 250)
  }

  function stopRecording() {
    if (recordTimerRef.current) window.clearInterval(recordTimerRef.current)
    recordTimerRef.current = null
    try { recorderRef.current?.stop() } catch {}
    recorderRef.current = null
    stopSpeechRecognition()
    setRecording(false)
  }

  function nextTurn() {
    if (recording) stopRecording()
    if (part === 1) {
      const next = index + 1
      if (next < (part1?.questions.length ?? 0)) {
        setIndex(next)
        const question = part1?.questions[next]
        if (question) setTimeout(() => speak(question.text, question.id), 350)
      } else {
        setPart(2)
        setPhase('prep')
        setPrepSeconds(cue?.preparationSeconds ?? 60)
        startPrep()
      }
      return
    }
    if (part === 2) {
      setPart(3)
      setIndex(0)
      setPhase('question')
      const question = part3?.questions[0]
      if (question) setTimeout(() => speak(question.text, question.id), 350)
      return
    }
    const next = index + 1
    if (next < (part3?.questions.length ?? 0)) {
      setIndex(next)
      const question = part3?.questions[next]
      if (question) setTimeout(() => speak(question.text, question.id), 350)
    } else {
      finishSpeaking()
    }
  }

  function startPrep() {
    if (prepTimerRef.current) window.clearInterval(prepTimerRef.current)
    const end = Date.now() + (cue?.preparationSeconds ?? 60) * 1000
    setPrepSeconds(cue?.preparationSeconds ?? 60)
    const cueSpeech = cue
      ? `Now I would like you to talk about a topic. Here is your cue card. ${cue.topic} You should say: ${cue.bullets.join('. ')}. ${cue.rounding}`
      : 'Here is your cue card.'
    speak(cueSpeech, 'cue')
    setTimeout(() => speak('You have one minute to prepare. You can make some notes if you wish. I will tell you when to begin.', 'prep'), 7200)
    prepTimerRef.current = window.setInterval(() => {
      const seconds = Math.max(0, Math.round((end - Date.now()) / 1000))
      setPrepSeconds(seconds)
      if (seconds <= 0) {
        window.clearInterval(prepTimerRef.current!)
        prepTimerRef.current = null
        setPhase('longturn')
        const turn: Turn = { part: 2, questionId: 'speaking-cue', text: cue?.topic ?? '', maxSeconds: cue?.speakingSeconds ?? 120 }
        setTimeout(() => startRecording(turn), 300)
      }
    }, 250)
  }

  function beginLongTurnNow() {
    if (prepTimerRef.current) window.clearInterval(prepTimerRef.current)
    prepTimerRef.current = null
    setPhase('longturn')
    const turn: Turn = { part: 2, questionId: 'speaking-cue', text: cue?.topic ?? '', maxSeconds: cue?.speakingSeconds ?? 120 }
    setTimeout(() => startRecording(turn), 250)
  }

  async function finishSpeaking() {
    if (finishing) return
    setFinishing(true)
    stopRecording()
    try {
      await uploadQueueRef.current
      const next = await api.submitSection(state.attempt.id, 'speaking')
      setPhase('done')
      onSubmitted(next)
    } catch (err) {
      setUploadError(err instanceof Error ? err.message : 'Could not finish the speaking test')
      setFinishing(false)
    }
  }


  const partTitles: Record<number, string> = { 1: 'Introduction and interview', 2: 'Individual long turn', 3: 'Two-way discussion' }
  const partCounts: Record<number, number> = { 1: part1?.questions.length ?? 0, 2: 1, 3: part3?.questions.length ?? 0 }

  if (phase === 'intro') {
    return (
      <div className="speaking-layout">
        <div className="section-intro">
          <div className="section-intro-card">
            <h1>IELTS Speaking</h1>
            <p className="intro-time"><strong>Time:</strong> 11 to 14 minutes</p>
            <h2>Instructions to candidates</h2>
            <ul>
              <li>Answer the examiner’s questions. Speak clearly and at a natural pace.</li>
              <li>The examiner will not correct you or give you a score during the test.</li>
              <li>Press <strong>Record answer</strong> when you start speaking and <strong>Stop</strong> when you finish.</li>
            </ul>
            <h2>Information for candidates</h2>
            <ul>
              <li>There are three parts to the test.</li>
              <li>Part 1: the examiner asks questions about yourself and familiar topics.</li>
              <li>Part 2: you receive a task card and have one minute to prepare, then speak for up to two minutes.</li>
              <li>Part 3: the examiner asks further questions connected to the topic in Part 2.</li>
              <li>Your recordings and any on-device transcript stay with this attempt.</li>
            </ul>
            <div className="sound-check">
              {micStream ? <Mic size={22} /> : <MicOff size={22} />}
              <div>
                <strong>Check your microphone</strong>
                <span>{micStream ? 'Say a few words. The bar should move when you speak.' : 'Allow microphone access, then say a few words.'}</span>
                {micStream && <MicMeter level={micLevel} wide />}
              </div>
              {!micStream && <Button variant="secondary" size="sm" onClick={testMic} icon={<Mic size={15} />}>Test microphone</Button>}
            </div>
            {permissionError && <div className="speaking-error">{permissionError}</div>}
            <div className="intro-candidate">
              <span>Candidate: <strong>Demo candidate</strong></span>
              <span>Test: <strong>{state.exam.title}</strong></span>
            </div>
            <div className="intro-actions">
              <Button size="lg" onClick={begin}>Start test</Button>
              {permissionError && <Button variant="secondary" size="lg" onClick={beginNoRecording}>Continue without recording</Button>}
              <button className="speak-link" onClick={onSkip}>Skip Speaking and see results</button>
            </div>
          </div>
        </div>
      </div>
    )
  }

  if (phase === 'done') {
    return (
      <div className="speaking-layout">
        <div className="section-intro">
          <div className="section-intro-card speaking-done">
            <h1>End of the Speaking test</h1>
            <p className="intro-time">Thank you. That is the end of the Speaking test.</p>
            <p>Your {uploaded} recording{uploaded === 1 ? '' : 's'} and any available transcript have been saved.</p>
            <div className="intro-actions"><Button size="lg" onClick={finishSpeaking} disabled={finishing}>{finishing ? 'Preparing results…' : 'View my results'} <ArrowRight size={15} /></Button></div>
          </div>
        </div>
      </div>
    )
  }

  const question = currentQuestion()
  const status = recording
    ? <span className="speak-status speak-status--rec"><i /> Recording {formatClock(recordSeconds)}</span>
    : examinerSpeaking
      ? <span className="speak-status"><Volume2 size={16} /> Examiner is speaking</span>
      : phase === 'prep'
        ? <span className="speak-status">Preparation time</span>
        : <span className="speak-status">Your turn</span>
  const banner = part === 2
    ? (phase === 'prep' ? `You have one minute to prepare. You can make notes.` : `Talk about the topic for one to two minutes.`)
    : part === 1 ? 'The examiner will ask you some questions about yourself.' : 'The examiner will ask you some more general questions.'

  return (
    <div className="speaking-layout">
      <div className="part-banner">
        <div className="part-banner-text">
          <strong>Part {part}: {partTitles[part]}</strong>
          <span>{banner}</span>
        </div>
        {status}
      </div>

      <div className="speaking-stage">
        <div className="speaking-video" aria-label="Video call">
          <div className={`video-tile video-tile--examiner ${examinerSpeaking ? 'video-tile--talking' : ''}`}>
            <div className="video-avatar" aria-hidden="true">E</div>
            <span className="video-name">Examiner</span>
          </div>
          <div className={`video-tile video-tile--self ${recording ? 'video-tile--talking' : ''}`}>
            <div className="video-avatar video-avatar--self" aria-hidden="true">{micStream ? <Mic size={24} /> : <MicOff size={24} />}</div>
            <span className="video-name">You{micStream && <MicMeter level={recording ? micLevel : micLevel * 0.6} />}</span>
          </div>
        </div>

        <div className="speaking-panel">
          {(part === 1 || part === 3) && question && (
            <>
              <span className="speaking-qno">Question {index + 1} of {partCounts[part]}</span>
              <p className="speaking-question">{question.text}</p>
              <div className="speaking-actions">
                {!recording
                  ? <button className="rec-btn" onClick={() => startRecording({ part, questionId: question.id, text: question.text, maxSeconds: part === 1 ? 60 : 90 })} disabled={!micStream}><Mic size={17} /> Record answer</button>
                  : <button className="rec-btn rec-btn--stop" onClick={stopRecording}><Square size={14} /> Stop</button>}
                <button className="speak-ghost" onClick={() => speak(question.text, question.id)}><Volume2 size={16} /> Repeat question</button>
              </div>
              <p className="speaking-sub">{part === 1 ? 'Answer naturally and give a reason or an example. Recording stops after one minute.' : 'Give an extended answer with reasons and examples. Recording stops after 90 seconds.'}</p>
            </>
          )}

          {part === 2 && cue && (
            <>
              <div className="cue-card">
                <p className="cue-label">Task card</p>
                <h2>{cue.topic}</h2>
                <p className="cue-prompt">You should say:</p>
                <ul>{cue.bullets.map((bullet) => <li key={bullet}>{bullet}</li>)}</ul>
                <p className="cue-round">{cue.rounding}</p>
              </div>
              {phase === 'prep' ? (
                <>
                  <div className="prep-row">
                    <div className="prep-timer" role="timer"><span>{formatClock(prepSeconds)}</span> preparation time left</div>
                    <button className="rec-btn" onClick={beginLongTurnNow}><Play size={15} /> Start speaking now</button>
                  </div>
                  <label className="notes-label" htmlFor="speaking-notes">Notes (not assessed)</label>
                  <textarea id="speaking-notes" className="notes-area" value={notes} onChange={(e) => setNotes(e.target.value)} placeholder="Make notes here…" />
                </>
              ) : (
                <>
                  <div className="speaking-actions">
                    {!recording
                      ? <button className="rec-btn" onClick={() => startRecording({ part: 2, questionId: 'speaking-cue', text: cue.topic, maxSeconds: cue.speakingSeconds })} disabled={!micStream}><Mic size={17} /> Start long turn</button>
                      : <button className="rec-btn rec-btn--stop" onClick={stopRecording}><Square size={14} /> Stop</button>}
                    <span className="speak-timer">{formatClock(recordSeconds)} / {formatClock(cue.speakingSeconds)}</span>
                  </div>
                  <div className="long-turn-bar" aria-hidden="true"><i style={{ width: `${Math.min(100, (recordSeconds / Math.max(1, cue.speakingSeconds)) * 100)}%` }} /></div>
                  {notes && <div className="notes-readonly"><strong>Your notes</strong><p>{notes}</p></div>}
                </>
              )}
            </>
          )}

          {!micStream && phase !== 'prep' && <div className="speaking-error">No microphone — answers are not being recorded.</div>}
          {uploadError && <div className="speaking-error">{uploadError}</div>}
        </div>
      </div>

      <div className="exam-footer-wrap">
        <div className="footer-nav">
          {part === 1 && <button className="speak-next" onClick={() => { if (recording) stopRecording(); setTimeout(nextTurn, recording ? 250 : 0) }}>{index === partCounts[1] - 1 ? 'Go to Part 2' : 'Next question'} <SkipForward size={16} /></button>}
          {part === 2 && phase === 'longturn' && <button className="speak-next" onClick={() => { if (recording) stopRecording(); setTimeout(nextTurn, 250) }}>Go to Part 3 <ArrowRight size={16} /></button>}
          {part === 3 && <button className="speak-next" onClick={() => { if (recording) stopRecording(); setTimeout(nextTurn, recording ? 250 : 0) }} disabled={finishing}>{index === partCounts[3] - 1 ? 'Finish Speaking' : 'Next question'} <ArrowRight size={16} /></button>}
        </div>
        <nav className="exam-footer" aria-label="Speaking progress">
          <div className="part-buttons">
            {[1, 2, 3].map((n) => {
              const done = n < part ? partCounts[n] : n === part ? (n === 2 ? 0 : index) : 0
              return n === part ? (
                <div key={n} className="part-btn part-btn--active part-btn--open" aria-current="step">
                  <b>Part {n}</b>
                  <div className="palette">
                    {Array.from({ length: partCounts[n] }).map((_, i) => (
                      <span key={i} className={`palette-dot ${i < done ? 'answered' : ''} ${i === done ? 'active' : ''}`}>{n === 2 ? 'Task' : i + 1}</span>
                    ))}
                  </div>
                </div>
              ) : (
                <div key={n} className="part-btn">
                  <b>Part {n}</b>
                  <span>{n < part ? 'Complete' : `${partCounts[n]} ${n === 2 ? 'task' : 'questions'}`}</span>
                </div>
              )
            })}
          </div>
        </nav>
      </div>
    </div>
  )
}

function MicMeter({ level, wide = false }: { level: number; wide?: boolean }) {
  const bars = wide ? 16 : 6
  const lit = Math.round(level * bars)
  return (
    <span className={`mic-meter ${wide ? 'mic-meter--wide' : ''}`} aria-hidden="true">
      {Array.from({ length: bars }).map((_, i) => <i key={i} className={i < lit ? 'on' : ''} />)}
    </span>
  )
}

function useMicLevel(stream: MediaStream | null) {
  const [level, setLevel] = useState(0)
  useEffect(() => {
    if (!stream) return
    let raf = 0
    let last = 0
    let ctx: AudioContext | null = null
    try {
      const Ctx = window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext
      ctx = new Ctx()
      const analyser = ctx.createAnalyser()
      analyser.fftSize = 512
      ctx.createMediaStreamSource(stream).connect(analyser)
      const data = new Uint8Array(analyser.fftSize)
      const tick = (t: number) => {
        if (t - last > 80) {
          last = t
          analyser.getByteTimeDomainData(data)
          let sum = 0
          for (let i = 0; i < data.length; i++) { const v = (data[i] - 128) / 128; sum += v * v }
          setLevel(Math.min(1, Math.sqrt(sum / data.length) * 5))
        }
        raf = requestAnimationFrame(tick)
      }
      raf = requestAnimationFrame(tick)
    } catch { /* the meter is optional */ }
    return () => { cancelAnimationFrame(raf); ctx?.close().catch(() => {}) }
  }, [stream])
  return level
}
