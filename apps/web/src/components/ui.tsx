import type { ButtonHTMLAttributes, ReactNode } from 'react'
import { Headphones, BookOpen, PenLine, Mic, X } from 'lucide-react'
import type { Skill } from '../lib/types'

export function Logo({ onClick, light = false }: { onClick?: () => void; light?: boolean }) {
  return (
    <button className={`brand ${light ? 'brand--light' : ''}`} onClick={onClick} aria-label="Apex IELTS home">
      <span className="brand-mark" aria-hidden="true">
        <svg viewBox="0 0 40 40" fill="none">
          <rect width="40" height="40" rx="12" fill="currentColor" />
          <path d="M11.5 28.5 20 10l8.5 18.5" stroke="var(--brand-ink)" strokeWidth="2.8" strokeLinecap="round" strokeLinejoin="round" />
          <path d="M15.2 22.5h9.6" stroke="var(--brand-ink)" strokeWidth="2.8" strokeLinecap="round" />
          <circle cx="31" cy="10" r="3.2" fill="var(--accent)" />
        </svg>
      </span>
      <span className="brand-copy">
        <span className="brand-name">APEX</span>
        <span className="brand-sub">IELTS MOCK LAB</span>
      </span>
    </button>
  )
}

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: 'primary' | 'secondary' | 'ghost' | 'dark' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  icon?: ReactNode
  iconRight?: ReactNode
  full?: boolean
}

export function Button({
  variant = 'primary',
  size = 'md',
  icon,
  iconRight,
  full,
  className = '',
  children,
  ...rest
}: ButtonProps) {
  return (
    <button
      className={`btn btn--${variant} btn--${size} ${full ? 'btn--full' : ''} ${className}`}
      {...rest}
    >
      {icon && <span className="btn-icon">{icon}</span>}
      <span>{children}</span>
      {iconRight && <span className="btn-icon btn-icon--right">{iconRight}</span>}
    </button>
  )
}

export function Badge({ children, tone = 'neutral' }: { children: ReactNode; tone?: 'neutral' | 'green' | 'amber' | 'blue' | 'red' | 'dark' }) {
  return <span className={`badge badge--${tone}`}>{children}</span>
}

const skillIcon = {
  listening: Headphones,
  reading: BookOpen,
  writing: PenLine,
  speaking: Mic,
}

export function SkillGlyph({ skill, size = 'md' }: { skill: Skill; size?: 'sm' | 'md' | 'lg' }) {
  const Icon = skillIcon[skill]
  return (
    <span className={`skill-glyph skill-glyph--${skill} skill-glyph--${size}`}>
      <Icon aria-hidden="true" strokeWidth={1.8} />
    </span>
  )
}

export function Modal({
  open,
  onClose,
  title,
  children,
  width = 'md',
}: {
  open: boolean
  onClose?: () => void
  title?: string
  children: ReactNode
  width?: 'sm' | 'md' | 'lg'
}) {
  if (!open) return null
  return (
    <div className="modal-backdrop" role="presentation" onMouseDown={(e) => { if (e.target === e.currentTarget) onClose?.() }}>
      <div className={`modal modal--${width}`} role="dialog" aria-modal="true" aria-label={title}>
        {title && (
          <div className="modal-head">
            <h3>{title}</h3>
            {onClose && (
              <button className="icon-btn" onClick={onClose} aria-label="Close">
                <X size={18} />
              </button>
            )}
          </div>
        )}
        {children}
      </div>
    </div>
  )
}

export function formatDuration(seconds: number) {
  const safe = Math.max(0, Math.floor(seconds))
  const h = Math.floor(safe / 3600)
  const m = Math.floor((safe % 3600) / 60)
  const s = safe % 60
  if (h > 0) return `${h}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
}

export function formatClock(seconds: number) {
  const safe = Math.max(0, Math.floor(seconds))
  const m = Math.floor(safe / 60)
  const s = safe % 60
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
}

export function SkillMeta({ skill }: { skill: Skill }) {
  const meta = {
    listening: { name: 'Listening', detail: '4 parts · 40 questions · 30 min' },
    reading: { name: 'Reading', detail: '3 passages · 40 questions · 60 min' },
    writing: { name: 'Writing', detail: '2 tasks · 60 min' },
    speaking: { name: 'Speaking', detail: '3 parts · 11–14 min' },
  }[skill]
  return <>{meta.name}</>
}
