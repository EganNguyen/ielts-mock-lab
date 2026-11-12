'use client'

import type { Question, QuestionGroup } from '@/lib/api'
import { assetUrl } from '@/lib/assets'

interface Props {
  groups: QuestionGroup[]
  questions: Question[]
  answers: Record<string, string>
  flags: Record<string, boolean>
  onAnswer: (questionId: string, value: string) => void
}

const BLANK = /\{\{(\d+)\}\}/g

export function QuestionSets({ groups, questions, answers, flags, onAnswer }: Props) {
  return (
    <>
      {groups.map((group) => {
        const groupQuestions = questions
          .filter((q) => q.groupId === group.id)
          .sort((a, b) => a.number - b.number)
        const byNumber = new Map(groupQuestions.map((q) => [q.number, q]))
        const inlineNumbers = new Set<number>()
        const lines = group.body ?? []
        lines.forEach((line) => {
          for (const match of line.matchAll(BLANK)) inlineNumbers.add(Number(match[1]))
        })
        const remaining = groupQuestions.filter((q) => !inlineNumbers.has(q.number))
        const chooseTwo = remaining.length === 2 &&
          remaining[0].type === 'mcq' &&
          remaining[0].options && remaining[1].options &&
          remaining[0].options.length === remaining[1].options.length &&
          remaining[0].options.every((option, index) => option === remaining[1].options?.[index])
        return (
          <section className="question-group" id={`group-${group.id}`} key={group.id}>
            <div className="group-head">
              {group.label && <h3>{group.label}</h3>}
              <p>{group.instructions}</p>
              {group.note && <p className="group-note">{group.note}</p>}
            </div>
            {group.figure && (
              <figure className="question-figure">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img src={assetUrl(group.figure)} alt={group.figureAlt ?? 'Figure for this question set'} loading="lazy" />
                {group.figureAlt && <figcaption>{group.figureAlt}</figcaption>}
              </figure>
            )}
            {group.sharedOptions && !group.sharedOptions.every((option) => /^[A-Z]$/.test(option.trim())) && (
              <div className={`shared-options ${group.layout === 'summary' ? 'shared-options--words' : ''}`}>
                <h4>{group.layout === 'summary' ? 'Word list' : 'Options'}</h4>
                <div>
                  {group.sharedOptions.map((option) => <div key={option}>{option}</div>)}
                </div>
              </div>
            )}
            {lines.length > 0 && (
              <div className={`group-body group-body--text `}>
                {lines.map((line, index) => (
                  <BodyLine
                    key={`${group.id}-${index}`}
                    line={line}
                    group={group}
                    byNumber={byNumber}
                    answers={answers}
                    onAnswer={onAnswer}
                  />
                ))}
              </div>
            )}
            {chooseTwo && remaining[0].options && (
              <ChooseTwo
                questions={remaining}
                options={remaining[0].options}
                answers={answers}
                onAnswer={onAnswer}
              />
            )}
            {remaining.length > 0 && !chooseTwo && (
              <div className="group-body">
                {remaining.map((question) => (
                  <QuestionRow
                    key={question.id}
                    question={question}
                    group={group}
                    value={answers[question.id] ?? ''}
                    flagged={!!flags[question.id]}
                    onAnswer={(value) => onAnswer(question.id, value)}
                  />
                ))}
              </div>
            )}
          </section>
        )
      })}
    </>
  )
}

function ChooseTwo({
  questions, options, answers, onAnswer,
}: {
  questions: Question[]
  options: string[]
  answers: Record<string, string>
  onAnswer: (questionId: string, value: string) => void
}) {
  return (
    <div className="group-body">
      <div className="choose-two">
        <p className="choose-two-hint">Choose <strong>TWO</strong> letters. Each answer is worth one mark; the order does not matter.</p>
        <ol className="choose-two-options">
          {options.map((option, index) => {
            const letter = String.fromCharCode(65 + index)
            return (
              <li key={option}><span className="option-letter">{letter}</span><span>{option}</span></li>
            )
          })}
        </ol>
        <div className="choose-two-selects">
          {questions.map((question) => (
            <label key={question.id} className="choose-two-select" data-qid={question.id}>
              <span className="q-number">{question.number}</span>
              <select
                className="select-answer"
                value={answers[question.id] ?? ''}
                onChange={(event) => onAnswer(question.id, event.target.value)}
                aria-label={`Answer for question ${question.number}`}
              >
                <option value="">Choose a letter</option>
                {options.map((_, index) => {
                  const letter = String.fromCharCode(65 + index)
                  return <option key={letter} value={letter}>{letter}</option>
                })}
              </select>
            </label>
          ))}
        </div>
      </div>
    </div>
  )
}

function BodyLine({
  line, group, byNumber, answers, onAnswer,
}: {
  line: string
  group: QuestionGroup
  byNumber: Map<number, Question>
  answers: Record<string, string>
  onAnswer: (questionId: string, value: string) => void
}) {
  if (line === '↓') {
    return <div className="flow-arrow" aria-hidden="true">↓</div>
  }
  let className = 'body-line'
  let text = line
  if (text.startsWith('## ')) {
    className = 'body-line body-line--subhead'
    text = text.slice(3)
  } else if (text.startsWith('# ')) {
    className = 'body-line body-line--head'
    text = text.slice(2)
  } else if (text.startsWith('  – ')) {
    className = 'body-line body-line--sub'
    text = text.slice(4)
  } else if (text.startsWith('• ')) {
    className = 'body-line body-line--bullet'
    text = text.slice(2)
  }
  const parts = text.split(BLANK)
  return (
    <p className={className}>
      {parts.map((part, index) => {
        if (index % 2 === 1) {
          const number = Number(part)
          const question = byNumber.get(number)
          if (!question) return <span key={index} className="blank-missing">[{number}]</span>
          return (
            <InlineBlank
              key={`${question.id}-${index}`}
              question={question}
              group={group}
              value={answers[question.id] ?? ''}
              onChange={(value) => onAnswer(question.id, value)}
            />
          )
        }
        return <span key={index}>{part}</span>
      })}
    </p>
  )
}

function InlineBlank({
  question, group, value, onChange,
}: {
  question: Question
  group: QuestionGroup
  value: string
  onChange: (value: string) => void
}) {
  const letters = lettersFor(question, group)
  if (question.type === 'select' || question.type === 'match' || question.type === 'heading') {
    return (
      <span className="blank-inline blank-inline--select" data-qid={question.id}>
        <select
          className={`select-answer select-answer--inline ${value ? '' : 'select-answer--empty'}`}
          value={value}
          onChange={(event) => onChange(event.target.value)}
          aria-label={`Answer for question ${question.number}`}
        >
          <option value="">{question.number}</option>
          {letters.map((letter) => <option key={letter} value={letter}>{letter}</option>)}
        </select>
      </span>
    )
  }
  return (
    <span className="blank-inline" data-qid={question.id}>
      <input
        className="blank-input"
        placeholder={String(question.number)}
        value={value}
        onChange={(event) => onChange(event.target.value)}
        aria-label={`Answer for question ${question.number}`}
        autoComplete="off"
        spellCheck={false}
      />
    </span>
  )
}

function QuestionRow({
  question, group, value, flagged, onAnswer,
}: {
  question: Question
  group: QuestionGroup
  value: string
  flagged: boolean
  onAnswer: (value: string) => void
}) {
  const answered = value.trim().length > 0
  return (
    <div className={`q-row ${answered ? 'q-row--answered' : ''} ${flagged ? 'q-row--flagged' : ''}`} id={`q-${question.id}`} data-qid={question.id}>
      <div className="q-number">{question.number}</div>
      <div className="q-main">
        {question.type === 'mcq' && (
          <>
            <div className="q-prompt">{question.prompt}</div>
            <div className="options-list" role="radiogroup" aria-label={`Question ${question.number}`}>
              {(question.options ?? []).map((option, index) => {
                const letter = String.fromCharCode(65 + index)
                return (
                  <button
                    type="button"
                    key={option}
                    role="radio"
                    className={`option ${value === letter ? 'option--selected' : ''}`}
                    onClick={() => onAnswer(value === letter ? '' : letter)}
                    aria-checked={value === letter}
                  >
                    <span className="option-radio" aria-hidden="true" />
                    <span className="option-letter">{letter}</span>
                    <span>{option}</span>
                  </button>
                )
              })}
            </div>
          </>
        )}

        {(question.type === 'tfng' || question.type === 'ynng') && (
          <>
            <div className="q-prompt q-prompt--serif">{question.prompt}</div>
            <div className="options-list" role="radiogroup" aria-label={`Question ${question.number}`}>
              {(question.type === 'tfng' ? ['TRUE', 'FALSE', 'NOT GIVEN'] : ['YES', 'NO', 'NOT GIVEN']).map((option) => (
                <button
                  type="button"
                  key={option}
                  role="radio"
                  className={`option ${value === option ? 'option--selected' : ''}`}
                  onClick={() => onAnswer(value === option ? '' : option)}
                  aria-checked={value === option}
                >
                  <span className="option-radio" aria-hidden="true" />
                  <span>{option}</span>
                </button>
              ))}
            </div>
          </>
        )}

        {(question.type === 'heading' || question.type === 'match' || question.type === 'select' || question.type === 'map') && (
          <div className="q-match">
            <span className="q-prompt">{question.prompt}</span>
            <select className={`select-answer ${value ? '' : 'select-answer--empty'}`} value={value} onChange={(event) => onAnswer(event.target.value)} aria-label={`Answer for question ${question.number}`}>
              <option value="">{question.number}</option>
              {lettersFor(question, group).map((letter) => <option key={letter} value={letter}>{letter}</option>)}
            </select>
          </div>
        )}

        {question.type === 'short' && <InlinePrompt prompt={question.prompt} number={question.number} value={value} onChange={onAnswer} />}
      </div>
    </div>
  )
}

function lettersFor(question: Question, group: QuestionGroup): string[] {
  if (question.type === 'map') return ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
  const shared = group.sharedOptions ?? []
  if (shared.length) {
    if (shared.every((option) => /^[A-Z]$/.test(option.trim()))) return shared.map((option) => option.trim())
    // Take the leading label, which may be a letter or a roman numeral (i, ii,
    // iii, iv...) for heading-matching questions.
    return shared.map((option) => option.trim().split(/\s+/)[0].replace(/[.)]$/, ''))
  }
  if (question.options?.length) {
    return question.options.map((_, index) => String.fromCharCode(65 + index))
  }
  return ['A', 'B', 'C', 'D', 'E', 'F', 'G']
}

function InlinePrompt({ prompt, number, value, onChange }: { prompt: string; number: number; value: string; onChange: (value: string) => void }) {
  const parts = prompt.split('[[blank]]')
  if (parts.length === 1) {
    return (
      <div style={{ display: 'flex', alignItems: 'center', gap: 10, flexWrap: 'wrap' }}>
        <span className="q-prompt">{prompt}</span>
        <input className="blank-input" placeholder={String(number)} value={value} onChange={(event) => onChange(event.target.value)} aria-label={`Answer for question ${number}`} autoComplete="off" spellCheck={false} />
      </div>
    )
  }
  return (
    <div className="q-prompt">
      {parts.map((part, index) => (
        <span key={`${part}-${index}`}>
          {part}
          {index < parts.length - 1 && (
            <input
              className="blank-input"
              placeholder={String(number)}
              value={value}
              onChange={(event) => onChange(event.target.value)}
              aria-label={`Answer for question ${number}`}
              autoComplete="off"
              spellCheck={false}
            />
          )}
        </span>
      ))}
    </div>
  )
}
