'use client'

import { useEffect, useMemo, useState } from 'react'
import {
  ArrowLeft, BookOpen, ChevronDown, Headphones, Lock, Search, ShieldCheck,
  SlidersHorizontal, Sparkles, Unlock, Volume2,
} from 'lucide-react'
import { Badge, Button, Logo } from '@/components/ui'
import { assetUrl } from '@/lib/assets'
import rawVocabulary from '@/learning-vocabulary.json'

type SentenceImportance = 'Essential' | 'Helpful' | 'Optional'
type AnswerImportance = 'Critical' | 'Helpful' | 'Not relevant'
type AnswerRelevance = 'Correct Answer' | 'Answer Evidence' | 'Paraphrase' | 'Distractor'

type Breakdown = { text: string; vi: string; role: string }
type Reference = { book: string; test: number; skill: 'Listening' | 'Reading'; section: string; sectionTitle: string; questions: number[] }
type Answer = {
  book: string
  test: number
  skill: 'Listening' | 'Reading'
  section: string
  sectionTitle: string
  questionNumber: number
  question: string
  options: string[]
  instructions: string
  support: string
  correctAnswer: string
  correctAnswerText: string
  connection: string
  paraphrasing: string
  why: string
  mistake: string
  importance: AnswerImportance
  relevance: AnswerRelevance[]
}
type Item = {
  id: string
  term: string
  ipa: string
  pos: string
  meaningEn: string
  meaningVi: string
  synonyms: string[]
  sentence: {
    text: string
    translation: string
    breakdown: Breakdown[]
    why: string
    risk: string
    importance: SentenceImportance
  }
  answers: Answer[]
  references: Reference[]
  source: 'exam' | 'sentence'
  primary: Reference
}
type VocabularyData = {
  meta: {
    title: string
    totalItems: number
    totalTests: number
    sentenceImportance: Record<SentenceImportance, number>
    answerItems: number
    answerReferences: number
  }
  items: Item[]
}

const DATA = rawVocabulary as VocabularyData
const UNLOCK_KEY = 'apex-vocabulary-unlocked-tests'
const RELEVANCE_TAGS: AnswerRelevance[] = ['Correct Answer', 'Answer Evidence', 'Paraphrase', 'Distractor']
const RELEVANCE_COUNTS = DATA.items.reduce<Record<AnswerRelevance, number>>(
  (counts, item) => {
    for (const answer of item.answers) for (const tag of answer.relevance) counts[tag] += 1
    return counts
  },
  { 'Correct Answer': 0, 'Answer Evidence': 0, Paraphrase: 0, Distractor: 0 },
)
const ANSWER_COUNTS = DATA.items.reduce<Record<AnswerImportance, number>>(
  (counts, item) => {
    for (const answer of item.answers) counts[answer.importance] += 1
    return counts
  },
  { Critical: 0, Helpful: 0, 'Not relevant': 0 },
)

function testIndex(book: string, test: number) {
  return book === 'IELTS 20' ? test : test + 4
}

function testLabel(book: string, test: number) {
  return `${book} · Test ${test}`
}

function sectionLabel(ref: Reference) {
  return `${ref.skill === 'Listening' ? 'Listening Part' : 'Reading Passage'} ${ref.section.slice(1)}`
}

function formatQuestions(numbers: number[]) {
  if (!numbers.length) return ''
  const sorted = [...new Set(numbers)].sort((a, b) => a - b)
  if (sorted.length === 1) return `Q${sorted[0]}`
  const consecutive = sorted.every((n, i) => i === 0 || n === sorted[i - 1] + 1)
  return consecutive ? `Q${sorted[0]}–${sorted[sorted.length - 1]}` : sorted.map((n) => `Q${n}`).join(', ')
}

function speak(text: string) {
  if (typeof window === 'undefined' || !('speechSynthesis' in window)) return
  window.speechSynthesis.cancel()
  const utterance = new SpeechSynthesisUtterance(text)
  utterance.lang = 'en-GB'
  utterance.rate = 0.9
  window.speechSynthesis.speak(utterance)
}

const SENTENCE_TONE: Record<SentenceImportance, 'red' | 'amber' | 'blue'> = {
  Essential: 'red', Helpful: 'amber', Optional: 'blue',
}
const ANSWER_TONE: Record<AnswerImportance, 'red' | 'amber' | 'neutral'> = {
  Critical: 'red', Helpful: 'amber', 'Not relevant': 'neutral',
}

export default function VocabularyPage() {
  const [skill, setSkill] = useState<'All' | 'Listening' | 'Reading'>('All')
  const [test, setTest] = useState<'All' | number>('All')
  const [sentenceImportance, setSentenceImportance] = useState<'All' | SentenceImportance>('All')
  const [answerImportance, setAnswerImportance] = useState<'All' | AnswerImportance>('All')
  const [relevance, setRelevance] = useState<'All' | AnswerRelevance>('All')
  const [query, setQuery] = useState('')
  const [expanded, setExpanded] = useState<Set<string>>(new Set())
  const [collapsedTests, setCollapsedTests] = useState<Set<string>>(new Set())
  const [unlocked, setUnlocked] = useState<Set<string>>(new Set())

  useEffect(() => {
    try {
      const stored = localStorage.getItem(UNLOCK_KEY)
      if (stored) setUnlocked(new Set(JSON.parse(stored) as string[]))
    } catch {
      // ignore damaged local state
    }
  }, [])

  const filtered = useMemo(() => {
    const needle = query.trim().toLowerCase()
    return DATA.items.filter((item) => {
      if (skill !== 'All' && item.primary.skill !== skill) return false
      if (test !== 'All' && testIndex(item.primary.book, item.primary.test) !== Number(test)) return false
      if (sentenceImportance !== 'All' && item.sentence.importance !== sentenceImportance) return false
      if (answerImportance !== 'All') {
        if (!item.answers.some((answer) => answer.importance === answerImportance)) return false
      }
      if (relevance !== 'All') {
        if (!item.answers.some((answer) => answer.relevance.includes(relevance))) return false
      }
      if (!needle) return true
      const haystack = [
        item.term, item.ipa, item.pos, item.meaningEn, item.meaningVi, item.synonyms.join(' '),
        item.sentence.text, item.sentence.translation,
        item.sentence.breakdown.map((part) => `${part.text} ${part.vi}`).join(' '),
        item.primary.sectionTitle,
        item.references.map((ref) => ref.sectionTitle).join(' '),
        item.answers.map((answer) => `${answer.question} ${answer.support}`).join(' '),
      ].join(' ')
      return haystack.toLowerCase().includes(needle)
    })
  }, [skill, test, sentenceImportance, answerImportance, relevance, query])

  const groups = useMemo(() => {
    const visible = new Set(filtered.map((item) => item.id))
    const byTest = new Map<string, { book: string; test: number; sections: Array<{ key: string; ref: Reference; items: Item[] }> }>()
    for (const item of DATA.items) {
      if (!visible.has(item.id)) continue
      const ref = item.primary
      const key = `${ref.book}-${ref.test}-${ref.section}`
      const testKey = `${ref.book}-${ref.test}`
      if (!byTest.has(testKey)) byTest.set(testKey, { book: ref.book, test: ref.test, sections: [] })
      const group = byTest.get(testKey)!
      let section = group.sections.find((entry) => entry.key === key)
      if (!section) {
        section = { key, ref, items: [] }
        group.sections.push(section)
      }
      section.items.push(item)
    }
    const result = [...byTest.values()].sort((a, b) => testIndex(a.book, a.test) - testIndex(b.book, b.test))
    for (const group of result) {
      group.sections.sort((a, b) => a.ref.section.localeCompare(b.ref.section))
      for (const section of group.sections) {
        section.items.sort((a, b) => Math.min(...(a.primary.questions.length ? a.primary.questions : [99])) - Math.min(...(b.primary.questions.length ? b.primary.questions : [99])))
      }
    }
    return result
  }, [filtered])

  const answerCount = DATA.items.filter((item) => item.answers.length).length
  const priority = DATA.meta.sentenceImportance
  const total = DATA.meta.totalItems

  function toggleExpanded(id: string) {
    setExpanded((current) => {
      const next = new Set(current)
      if (next.has(id)) next.delete(id)
      else next.add(id)
      return next
    })
  }

  function toggleTest(key: string) {
    setCollapsedTests((current) => {
      const next = new Set(current)
      if (next.has(key)) next.delete(key)
      else next.add(key)
      return next
    })
  }

  function unlockAnswer(book: string, testNumber: number) {
    const key = `${book}|${testNumber}`
    setUnlocked((current) => {
      const next = new Set(current)
      next.add(key)
      try { localStorage.setItem(UNLOCK_KEY, JSON.stringify([...next])) } catch { /* ignore */ }
      return next
    })
  }

  function resetFilters() {
    setQuery('')
    setSkill('All')
    setTest('All')
    setSentenceImportance('All')
    setAnswerImportance('All')
    setRelevance('All')
  }

  return (
    <div className="home-shell vocab-shell">
      <header className="portal-header">
        <div className="container portal-header-inner">
          <Logo onClick={() => { window.location.href = assetUrl('/') }} />
          <nav className="portal-nav" aria-label="Main navigation">
            <a href={assetUrl('/#mock')}>Full test</a>
            <a href={assetUrl('/#practice')}>Practice</a>
            <a className="vocab-nav-active" href={assetUrl('/vocabulary/')}>Vocabulary</a>
            <a href={assetUrl('/#results')}>My results</a>
          </nav>
          <div className="portal-user"><span className="badge badge--dark">{total} items</span></div>
        </div>
      </header>

      <main className="container vocab-main">
        <a className="vocab-back vocab-mobile-back" href={assetUrl('/')}><ArrowLeft size={15} /> Back to the mock tests</a>

        <section className="vocab-hero vocab-hero--learning">
          <div>
            <span className="mono-label">IELTS 20 &amp; Cambridge IELTS 21 · 8 full tests</span>
            <h1>Understand the sentence. Then choose the answer.</h1>
            <p>
              {total} entries from all Listening transcripts and Reading passages. Every entry has a
              mandatory <strong>Sentence comprehension</strong> section; only entries with verified
              evidence also get an <strong>Answer selection</strong> section. Correct answers stay locked.
            </p>
            <div className="vocab-hero-actions">
              <Button size="lg" onClick={() => document.getElementById('vocab-browser')?.scrollIntoView({ behavior: 'smooth' })} icon={<BookOpen size={17} />}>Browse all entries</Button>
              <Button size="lg" variant="secondary" onClick={() => setSkill('Listening')} icon={<Headphones size={17} />}>Listening first</Button>
            </div>
          </div>
          <div className="vocab-stat-panel">
            <div><strong>{total}</strong><span>learning entries</span></div>
            <div><strong>{priority.Essential ?? 0}</strong><span>Essential sentences</span></div>
            <div><strong>{answerCount}</strong><span>with answer evidence</span></div>
            <div><strong>{DATA.meta.answerReferences}</strong><span>verified question links</span></div>
          </div>
        </section>

        <section className="panel vocab-controls" id="vocab-browser">
          <div className="vocab-controls-row">
            <div className="vocab-skill-tabs" role="group" aria-label="Skill">
              {(['All', 'Listening', 'Reading'] as const).map((value) => (
                <button key={value} className={skill === value ? 'is-active' : ''} onClick={() => setSkill(value)}>
                  {value === 'Listening' && <Headphones size={15} />}
                  {value === 'Reading' && <BookOpen size={15} />}
                  {value}
                </button>
              ))}
            </div>
            <label className="vocab-search">
              <Search size={17} aria-hidden="true" />
              <span className="sr-only">Search vocabulary</span>
              <input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search a word, phrase, meaning or sentence…" />
            </label>
            <select className="vocab-select" value={test} onChange={(event) => setTest(event.target.value === 'All' ? 'All' : Number(event.target.value))} aria-label="Test">
              <option value="All">All tests</option>
              {[1, 2, 3, 4, 5, 6, 7, 8].map((n) => <option key={n} value={n}>Test {n}</option>)}
            </select>
            <select className="vocab-select" value={sentenceImportance} onChange={(event) => setSentenceImportance(event.target.value as 'All' | SentenceImportance)} aria-label="Sentence importance">
              <option value="All">All sentence levels</option>
              <option value="Essential">Sentence: Essential ({priority.Essential ?? 0})</option>
              <option value="Helpful">Sentence: Helpful ({priority.Helpful ?? 0})</option>
              <option value="Optional">Sentence: Optional ({priority.Optional ?? 0})</option>
            </select>
            <select className="vocab-select" value={answerImportance} onChange={(event) => setAnswerImportance(event.target.value as 'All' | AnswerImportance)} aria-label="Answer importance">
              <option value="All">All answer evidence</option>
              <option value="Critical">Answer: Critical ({ANSWER_COUNTS.Critical})</option>
              <option value="Helpful">Answer: Helpful ({ANSWER_COUNTS.Helpful})</option>
              <option value="Not relevant">Answer: Not relevant ({ANSWER_COUNTS['Not relevant']})</option>
            </select>
            <select className="vocab-select" value={relevance} onChange={(event) => setRelevance(event.target.value as 'All' | AnswerRelevance)} aria-label="Answer relationship">
              <option value="All">All relationships</option>
              {RELEVANCE_TAGS.map((tag) => <option key={tag} value={tag}>{tag} ({RELEVANCE_COUNTS[tag]})</option>)}
            </select>
            <button className="vocab-reset" onClick={resetFilters} title="Reset filters"><SlidersHorizontal size={16} /><span>Reset</span></button>
          </div>
          <div className="vocab-controls-row vocab-controls-row--bottom">
            <div className="vocab-result-line"><strong>{filtered.length}</strong> of {total} entries · grouped by test, section and question</div>
            <div className="vocab-legend">
              <span><i className="dot dot--essential" />Sentence: Essential</span>
              <span><i className="dot dot--important" />Answer evidence</span>
            </div>
          </div>
        </section>

        {groups.length ? (
          <div className="vocab-test-stack">
            {groups.map((group) => {
              const testKey = `${group.book}-${group.test}`
              const open = !collapsedTests.has(testKey)
              const groupCount = group.sections.reduce((sum, section) => sum + section.items.length, 0)
              return (
                <section className="vocab-test" key={testKey}>
                  <button className="vocab-test-head" onClick={() => toggleTest(testKey)} aria-expanded={open}>
                    <div><span className="mono-label">{group.book} · Academic</span><h2>Test {group.test} <small>· Test {testIndex(group.book, group.test)} of 8</small></h2></div>
                    <div className="vocab-test-meta"><span>{group.sections.length} sections</span><span>{groupCount} entries</span><ChevronDown size={18} className={open ? 'is-open' : ''} /></div>
                  </button>
                  {open && (
                    <div className="vocab-section-stack">
                      {group.sections.map(({ key, ref, items }) => (
                        <section className="vocab-section-block" key={key}>
                          <div className="vocab-section-head">
                            <div>
                              <span className="vocab-skill-label">{ref.skill === 'Listening' ? <Headphones size={14} /> : <BookOpen size={14} />}{sectionLabel(ref)}</span>
                              <h3>{ref.sectionTitle}</h3>
                            </div>
                            <Badge tone="neutral">{items.length} entries</Badge>
                          </div>
                          <div className="vocab-item-list">
                            {items.map((item) => {
                              const openItem = expanded.has(item.id)
                              const hasAnswers = item.answers.length > 0
                              const primaryQ = item.primary.questions
                              return (
                                <article className={`vocab-item ${openItem ? 'is-open' : ''}`} key={item.id}>
                                  <button className="vocab-item-head" onClick={() => toggleExpanded(item.id)} aria-expanded={openItem}>
                                    <div className="vocab-item-term">
                                      <div className="vocab-term-line">
                                        <h4>{item.term}</h4>
                                        {item.ipa && <span>{item.ipa}</span>}
                                        <em>{item.pos}</em>
                                        {primaryQ.length > 0 && <em>{formatQuestions(primaryQ)}</em>}
                                      </div>
                                      <p>{item.meaningEn}</p>
                                    </div>
                                    <div className="vocab-item-tags">
                                      <span className={`priority priority--${item.sentence.importance === 'Essential' ? 'E' : item.sentence.importance === 'Helpful' ? 'I' : 'A'}`}>{item.sentence.importance}</span>
                                      {hasAnswers ? <span className="answer-pill"><ShieldCheck size={12} /> Answer evidence</span> : <span className="no-answer-pill">Sentence only</span>}
                                      <ChevronDown size={17} className={openItem ? 'is-open' : ''} />
                                    </div>
                                  </button>
                                  {openItem && (
                                    <div className="vocab-item-body">
                                      <section className="learning-section">
                                        <div className="learning-section-head">
                                          <div><span className="section-number">1</span><h5>Sentence comprehension</h5></div>
                                          <Badge tone={SENTENCE_TONE[item.sentence.importance]}>{item.sentence.importance}</Badge>
                                        </div>
                                        <div className="vocab-meanings">
                                          <div><span className="vocab-detail-label">English meaning</span><p>{item.meaningEn}</p></div>
                                          <div><span className="vocab-detail-label">Vietnamese meaning</span><p>{item.meaningVi}</p></div>
                                        </div>
                                        <div className="sentence-quote"><span className="vocab-detail-label">Original sentence</span><p>“{item.sentence.text}”</p></div>
                                        <div className="translation-block"><span className="vocab-detail-label">Vietnamese translation</span><p>{item.sentence.translation || 'Translation pending.'}</p></div>
                                        <div>
                                          <span className="vocab-detail-label">Sentence breakdown</span>
                                          <ul className="breakdown-list">
                                            {item.sentence.breakdown.map((part, index) => (
                                              <li key={`${item.id}-part-${index}`}>
                                                <span className="breakdown-en">{part.text}</span>
                                                <span className="breakdown-vi">{part.vi}</span>
                                                <span className="breakdown-role">{part.role}</span>
                                              </li>
                                            ))}
                                          </ul>
                                        </div>
                                        <div className="two-col-notes">
                                          <div><span className="vocab-detail-label">Why you need it</span><p>{item.sentence.why}</p></div>
                                          <div><span className="vocab-detail-label">Misunderstanding risk</span><p>{item.sentence.risk}</p></div>
                                        </div>
                                        <div className="vocab-chips-row">
                                          <span className="vocab-detail-label">Synonyms and paraphrases</span>
                                          <div className="vocab-chips">{item.synonyms.map((synonym) => <span key={synonym}>{synonym}</span>)}</div>
                                        </div>
                                      </section>

                                      {hasAnswers ? (
                                        <section className="answer-section">
                                          <div className="learning-section-head">
                                            <div><span className="section-number">2</span><h5>Answer selection</h5></div>
                                            <Badge tone="green">Verified evidence</Badge>
                                          </div>
                                          {item.answers.map((answer, index) => {
                                            const unlockKey = `${answer.book}|${answer.test}`
                                            const isUnlocked = unlocked.has(unlockKey)
                                            return (
                                              <div className="answer-card" key={`${item.id}-answer-${index}`}>
                                                <div className="answer-meta">
                                                  <span>{testLabel(answer.book, answer.test)} · {answer.skill} {answer.section.slice(1).toUpperCase()} · Q{answer.questionNumber}</span>
                                                  <Badge tone={ANSWER_TONE[answer.importance]}>{answer.importance}</Badge>
                                                </div>

                                                <div><span className="vocab-detail-label">Original question</span><p className="answer-question">{answer.question}</p>{answer.options.length > 0 && <ol className="answer-options" type="A">{answer.options.map((option, optionIndex) => <li key={`${answer.questionNumber}-opt-${optionIndex}`}>{option}</li>)}</ol>}</div>
                                                {isUnlocked ? (
                                                  <>
                                                    {answer.relevance.length > 0 && (
                                                      <div className="relevance-row">
                                                        <span className="vocab-detail-label">Answer relationship</span>
                                                        <div className="relevance-chips">
                                                          {answer.relevance.map((tag) => <span key={tag} className={`rel rel--${tag.toLowerCase().replace(/ /g, '-')}`}>{tag}</span>)}
                                                        </div>
                                                      </div>
                                                    )}
                                                    <div><span className="vocab-detail-label">Supporting text</span><p className="answer-support">“{answer.support}”</p></div>
                                                    <div className="answer-grid">
                                                      <div><span className="vocab-detail-label">Vocabulary connection</span><p>{answer.connection}</p></div>
                                                      <div><span className="vocab-detail-label">Paraphrasing</span><p>{answer.paraphrasing}</p></div>
                                                    </div>
                                                    <div className="two-col-notes">
                                                      <div><span className="vocab-detail-label">Why it matters</span><p>{answer.why}</p></div>
                                                      <div><span className="vocab-detail-label">Potential mistake</span><p>{answer.mistake}</p></div>
                                                    </div>
                                                    <div className="answer-lock">
                                                      <div className="answer-revealed">
                                                        <span className="vocab-detail-label">Correct answer</span>
                                                        <strong>{answer.correctAnswerText || answer.correctAnswer}</strong>
                                                        {answer.correctAnswerText && answer.correctAnswerText !== answer.correctAnswer && <small>Key: {answer.correctAnswer}</small>}
                                                      </div>
                                                    </div>
                                                  </>
                                                ) : (
                                                  <div className="answer-locked answer-locked--plate">
                                                    <Lock size={16} />
                                                    <div>
                                                      <strong>Evidence locked</strong>
                                                      <span>The relationship tags, supporting sentence, paraphrase and correct answer stay hidden until you confirm you have attempted {testLabel(answer.book, answer.test)}.</span>
                                                    </div>
                                                    <button onClick={() => unlockAnswer(answer.book, answer.test)}><Unlock size={14} /> I have attempted this test</button>
                                                  </div>
                                                )}
                                              </div>
                                            )
                                          })}
                                        </section>
                                      ) : (
                                        <div className="no-answer-note"><ShieldCheck size={15} /><span>No verified answer-selection evidence for this entry. It is included for sentence comprehension only.</span></div>
                                      )}

                                      <div className="vocab-source-line">
                                        <span>{item.primary.book} · Test {item.primary.test} · {sectionLabel(item.primary)} · {formatQuestions(item.primary.questions)}</span>
                                        <button className="vocab-speak-text" onClick={() => speak(item.term)}><Volume2 size={14} /> Pronounce</button>
                                      </div>
                                      {item.references.length > 1 && (
                                        <div className="vocab-crossref">
                                          <span className="vocab-detail-label">Also appears in</span>
                                          <ul>{item.references.slice(1).map((ref) => <li key={`${ref.book}-${ref.test}-${ref.section}`}>{ref.book} · Test {ref.test} · {sectionLabel(ref)} · {ref.sectionTitle} · {formatQuestions(ref.questions)}</li>)}</ul>
                                        </div>
                                      )}
                                    </div>
                                  )}
                                </article>
                              )
                            })}
                          </div>
                        </section>
                      ))}
                    </div>
                  )}
                </section>
              )
            })}
          </div>
        ) : (
          <div className="panel vocab-empty"><Sparkles size={26} /><h2>No vocabulary matches those filters</h2><p>Try a shorter search, or reset the skill, test, sentence and answer filters.</p><Button variant="secondary" onClick={resetFilters}>Reset filters</Button></div>
        )}

        <a className="vocab-back" href={assetUrl('/')}><ArrowLeft size={15} /> Back to the mock tests</a>
      </main>

      <footer className="site-footer"><div className="container footer-inner"><Logo /><p>Vocabulary and question references come from IELTS 20 Academic and Cambridge IELTS 21 Academic, © Cambridge University Press &amp; Assessment and Qunyan Press. Private study only; do not redistribute. Correct answers are stored only to support learning and remain locked until the learner confirms they have attempted that test.</p></div></footer>
    </div>
  )
}
