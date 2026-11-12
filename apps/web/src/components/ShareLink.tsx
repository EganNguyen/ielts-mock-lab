'use client'

import { useEffect, useState } from 'react'
import { Check, Copy, ExternalLink, Globe2, Loader2, Share2, ShieldAlert, Square } from 'lucide-react'
import { api, type ShareStatus } from '@/lib/api'
import { Button, Modal } from '@/components/ui'

function isLoopbackPage() {
  if (typeof window === 'undefined') return false
  return ['127.0.0.1', 'localhost', '::1', '[::1]'].includes(window.location.hostname)
}

export function ShareControl() {
  const [open, setOpen] = useState(false)
  const [status, setStatus] = useState<ShareStatus | null>(null)
  const [busy, setBusy] = useState(false)
  const [copied, setCopied] = useState(false)
  const [error, setError] = useState('')

  const active = Boolean(status?.active && status.url)
  const available = status?.available !== false
  const localPage = isLoopbackPage()

  useEffect(() => {
    let live = true
    api.share()
      .then((next) => { if (live) setStatus(next) })
      .catch(() => { /* the dialog surfaces errors when opened */ })
    return () => { live = false }
  }, [])

  useEffect(() => {
    if (!open) return
    let cancelled = false
    const load = () => {
      api.share()
        .then((next) => {
          if (cancelled) return
          setStatus(next)
          setError('')
        })
        .catch((err) => {
          if (!cancelled) setError(err instanceof Error ? err.message : 'Could not read the share status')
        })
    }
    load()
    const timer = window.setInterval(load, 5000)
    return () => {
      cancelled = true
      window.clearInterval(timer)
    }
  }, [open])

  async function generate() {
    setBusy(true)
    setError('')
    try {
      const next = await api.startShare()
      setStatus(next)
      setError('')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not create a share link')
      try {
        setStatus(await api.share())
      } catch {
        /* keep the original error */
      }
    } finally {
      setBusy(false)
    }
  }

  async function stop() {
    setBusy(true)
    setError('')
    try {
      const next = await api.stopShare()
      setStatus(next)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not stop the share link')
    } finally {
      setBusy(false)
    }
  }

  async function copy() {
    if (!status?.url) return
    try {
      await navigator.clipboard.writeText(status.url)
    } catch {
      const field = document.createElement('textarea')
      field.value = status.url
      field.style.position = 'fixed'
      field.style.opacity = '0'
      document.body.appendChild(field)
      field.select()
      document.execCommand('copy')
      document.body.removeChild(field)
    }
    setCopied(true)
    window.setTimeout(() => setCopied(false), 1800)
  }

  async function shareNative() {
    if (!status?.url) return
    if (typeof navigator.share === 'function') {
      try {
        await navigator.share({
          title: 'Apex IELTS — Academic Mock Lab',
          text: 'Take a look at this IELTS Academic mock test showcase.',
          url: status.url,
        })
        return
      } catch {
        /* the user dismissed the share sheet */
      }
    }
    await copy()
  }

  const startedAt = status?.startedAt
    ? new Date(status.startedAt).toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' })
    : null

  return (
    <>
      <Button
        size="sm"
        variant="secondary"
        onClick={() => setOpen(true)}
        icon={<Share2 size={14} />}
        aria-label="Share this showcase"
      >
        {active ? 'Sharing' : 'Share'}
      </Button>
      <Modal open={open} onClose={() => setOpen(false)} title="Share this showcase" width="md">
        <div className="modal-body share-dialog">
          <div className="share-hero">
            <span className={`share-orb ${active ? 'share-orb--live' : ''}`} aria-hidden="true">
              <Globe2 size={21} />
            </span>
            <div>
              <strong>{active ? 'Your showcase is live' : 'Show this site to a friend'}</strong>
              <p>
                {active
                  ? localPage
                    ? 'Send the link below. It opens this local app from anywhere until you stop sharing.'
                    : 'This showcase was shared from a local machine. The link stays live while the host keeps it running.'
                  : 'Generate a temporary public link to this local demo. No account or deployment needed.'}
              </p>
            </div>
          </div>

          {active && status?.url ? (
            <>
              <div className="share-link-row">
                <input
                  readOnly
                  value={status.url}
                  aria-label="Public share link"
                  onFocus={(event) => event.currentTarget.select()}
                />
                <Button
                  variant={copied ? 'dark' : 'primary'}
                  onClick={copy}
                  icon={copied ? <Check size={15} /> : <Copy size={15} />}
                >
                  {copied ? 'Copied' : 'Copy'}
                </Button>
              </div>
              <div className="share-actions">
                <Button variant="dark" onClick={shareNative} icon={<Share2 size={15} />}>Share via device</Button>
                <a className="btn btn--secondary btn--md" href={status.url} target="_blank" rel="noreferrer">
                  <ExternalLink size={15} /> Open link
                </a>
                {localPage && (
                  <Button variant="danger" onClick={stop} disabled={busy} icon={busy ? <Loader2 size={15} className="spin" /> : <Square size={13} />}>
                    {busy ? 'Stopping…' : 'Stop sharing'}
                  </Button>
                )}
              </div>
              <div className="share-meta">
                <span className="share-live-dot" /> Live{startedAt ? ` since ${startedAt}` : ''} · Cloudflare quick tunnel
              </div>
            </>
          ) : (
            <>
              <ul className="share-bullets">
                <li>Free Cloudflare quick tunnel — no account or DNS setup.</li>
                <li>Your Mac and this local app must stay running while the link is used.</li>
                <li>The random link dies as soon as you stop sharing.</li>
              </ul>
              {localPage ? (
                available ? (
                  <Button size="lg" onClick={generate} disabled={busy} icon={busy ? <Loader2 size={16} className="spin" /> : <Globe2 size={16} />}>
                    {busy ? 'Opening the tunnel…' : 'Generate public link'}
                  </Button>
                ) : (
                  <div className="share-error">
                    <strong>cloudflared is not installed.</strong>
                    <span>Install it with <code>brew install cloudflared</code>, then reopen this dialog.</span>
                  </div>
                )
              ) : (
                <div className="share-note">
                  <Globe2 size={17} />
                  <div>
                    <strong>Generate this link on the host machine.</strong>
                    <span>Open <code>http://127.0.0.1:3000</code> on the computer running the lab, or run <code>./scripts/share.sh</code>.</span>
                  </div>
                </div>
              )}
            </>
          )}

          {active && status?.message && <div className="share-note">{status.message}</div>}
          {!active && status?.message && status.message !== 'The share link was stopped' && (
            <div className="share-note">{status.message}</div>
          )}

          <div className="share-note share-note--warn">
            <ShieldAlert size={17} />
            <div>
              <strong>Private showcase, shared demo candidate.</strong>
              <span>
                Visitors use the same demo account and can start attempts. Finish or discard any test in progress first,
                and only share the link with people you trust.
              </span>
            </div>
          </div>

          {error && <div className="share-error">{error}</div>}
        </div>
      </Modal>
    </>
  )
}
