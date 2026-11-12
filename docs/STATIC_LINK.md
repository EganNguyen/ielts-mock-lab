# Permanent share link (Cloudflare named tunnel)

The **Share** button creates an anonymous Cloudflare quick tunnel. Its random
`*.trycloudflare.com` name is temporary by design: stop the tunnel or restart the
API and the hostname is gone.

For a stable address such as `https://ielts.example.com`, use a **named
Cloudflare tunnel** attached to a domain in your Cloudflare account. The example
below uses `example.com`; substitute your own domain.

A named tunnel is independent of the Go API, so restarting the API does not
change the URL. The Mac and the local web app must still be running.

## One-time setup

1. Authenticate `cloudflared` and authorise the zone in the browser:

   ```bash
   cloudflared tunnel login
   ```

   Choose `example.com` when prompted. This writes `~/.cloudflared/cert.pem`.

2. Create a named tunnel:

   ```bash
   cloudflared tunnel create apex-ielts
   ```

   Note the tunnel UUID it prints. Credentials are written to
   `~/.cloudflared/<UUID>.json`.

3. Point a DNS name at the tunnel:

   ```bash
   cloudflared tunnel route dns apex-ielts ielts.example.com
   ```

   This creates a proxied CNAME for `ielts.example.com`. Run it only once;
   if the record already exists, skip this step.

4. Create `~/.cloudflared/config.yml`:

   ```yaml
   tunnel: apex-ielts
   credentials-file: ~/.cloudflared/<UUID>.json

   ingress:
     - hostname: ielts.example.com
       service: http://127.0.0.1:3000
     - service: http_status:404
   ```

   Replace `<UUID>` with the value from step 2.

5. Start the tunnel:

   ```bash
   cloudflared tunnel run apex-ielts
   ```

   Open <https://ielts.example.com>. Because the local app is served at
   `127.0.0.1:3000`, start it first with `./scripts/dev.sh`.

## Keep it running

- Start the tunnel with the command above, or install it as a system service:

  ```bash
  sudo cloudflared service install
  ```

  The service uses `~/.cloudflared/config.yml` and starts at boot/login.

- A LaunchAgent is an alternative that does not need `sudo`:

  ```bash
  mkdir -p ~/Library/LaunchAgents
  cat > ~/Library/LaunchAgents/com.apex.ielts-tunnel.plist <<'PLIST'
  <?xml version="1.0" encoding="UTF-8"?>
  <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
    "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
  <plist version="1.0">
  <dict>
    <key>Label</key><string>com.apex.ielts-tunnel</string>
    <key>ProgramArguments</key>
    <array>
      <string>/opt/homebrew/bin/cloudflared</string>
      <string>tunnel</string>
      <string>run</string>
      <string>apex-ielts</string>
    </array>
    <key>RunAtLoad</key><true/>
    <key>KeepAlive</key><true/>
    <key>StandardOutPath</key><string>/tmp/apex-tunnel.log</string>
    <key>StandardErrorPath</key><string>/tmp/apex-tunnel.log</string>
  </dict>
  </plist>
  PLIST
  launchctl load ~/Library/LaunchAgents/com.apex.ielts-tunnel.plist
  ```

  On Apple Silicon, `cloudflared` is usually at `/opt/homebrew/bin/cloudflared`;
  check with `command -v cloudflared`.

- The Mac must be awake and online, and `./scripts/dev.sh` must be running.
  If the local web server is down, the static URL returns Cloudflare error 502.
- Confirm the tunnel with `cloudflared tunnel list` and `cloudflared tunnel info apex-ielts`.

## Protect the link

A named hostname is discoverable. The included Cambridge IELTS 21 content is
private local test data, so do not publish the URL.

Add **Cloudflare Access** (free for small teams) to require an email one-time
code:

1. Open <https://one.dash.cloudflare.com> → **Access → Applications**.
2. **Add an application → Self-hosted**.
3. Domain: `ielts.example.com`.
4. Add an **Allow** policy with your email and your friend's email.
5. Save. Visitors receive a one-time PIN by email before reaching the app.

Without Access, anyone who learns the URL can open the full demo.

## Why not keep the quick tunnel?

Cloudflare's `*.trycloudflare.com` quick tunnels are anonymous and deliberately
random. There is no way to reserve a static quick-tunnel name. A named tunnel
is the account-backed equivalent and is the right tool for a stable address.

## Alternatives

- **Tailscale Funnel** — a stable `https://<machine>.<tailnet>.ts.net` URL with
  no domain purchase. Requires a Tailscale account and Funnel enabled in the
  admin console.
- **Deploy the app** — run Next.js and PostgreSQL on a host such as Fly.io,
  Railway or a VPS. That removes the Mac dependency but requires a real
  deployment and database migration; the tunnel approach keeps the local-first
  design.
