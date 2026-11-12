CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  display_name TEXT NOT NULL DEFAULT '',
  role TEXT NOT NULL DEFAULT 'candidate' CHECK (role IN ('candidate', 'administrator', 'evaluator')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  token_hash TEXT NOT NULL UNIQUE,
  expires_at TIMESTAMPTZ NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS sessions_user_idx ON sessions(user_id);

CREATE TABLE IF NOT EXISTS exams (
  id TEXT PRIMARY KEY,
  code TEXT NOT NULL UNIQUE,
  title TEXT NOT NULL,
  module TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS exam_versions (
  id TEXT PRIMARY KEY,
  exam_id TEXT NOT NULL REFERENCES exams(id),
  version_label TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('draft', 'published', 'retired')),
  content JSONB NOT NULL,
  content_checksum TEXT NOT NULL,
  configuration JSONB NOT NULL DEFAULT '{}'::jsonb,
  published_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (exam_id, version_label)
);

CREATE TABLE IF NOT EXISTS attempts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  exam_version_id TEXT NOT NULL REFERENCES exam_versions(id),
  mode TEXT NOT NULL CHECK (mode IN ('full', 'listening', 'reading', 'writing', 'speaking')),
  status TEXT NOT NULL DEFAULT 'ready' CHECK (status IN ('ready', 'in_progress', 'core_submitted', 'completed', 'expired', 'abandoned')),
  current_skill TEXT,
  started_at TIMESTAMPTZ,
  completed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS attempts_user_idx ON attempts(user_id, created_at DESC);

CREATE TABLE IF NOT EXISTS attempt_sections (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  attempt_id UUID NOT NULL REFERENCES attempts(id) ON DELETE CASCADE,
  skill TEXT NOT NULL CHECK (skill IN ('listening', 'reading', 'writing', 'speaking')),
  status TEXT NOT NULL DEFAULT 'not_started' CHECK (status IN ('not_started', 'in_progress', 'submitted', 'expired')),
  duration_seconds INTEGER NOT NULL,
  started_at TIMESTAMPTZ,
  deadline_at TIMESTAMPTZ,
  submitted_at TIMESTAMPTZ,
  UNIQUE (attempt_id, skill)
);

CREATE TABLE IF NOT EXISTS answers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  attempt_id UUID NOT NULL REFERENCES attempts(id) ON DELETE CASCADE,
  skill TEXT NOT NULL,
  question_id TEXT NOT NULL,
  answer TEXT NOT NULL DEFAULT '',
  version INTEGER NOT NULL DEFAULT 1,
  saved_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (attempt_id, question_id)
);
CREATE INDEX IF NOT EXISTS answers_attempt_idx ON answers(attempt_id);

CREATE TABLE IF NOT EXISTS section_submissions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  attempt_id UUID NOT NULL REFERENCES attempts(id) ON DELETE CASCADE,
  skill TEXT NOT NULL,
  snapshot JSONB NOT NULL,
  content_checksum TEXT NOT NULL,
  submitted_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (attempt_id, skill)
);

CREATE TABLE IF NOT EXISTS speaking_recordings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  attempt_id UUID NOT NULL REFERENCES attempts(id) ON DELETE CASCADE,
  part_number INTEGER NOT NULL,
  question_id TEXT NOT NULL,
  storage_key TEXT NOT NULL,
  duration_seconds INTEGER NOT NULL DEFAULT 0,
  transcript TEXT NOT NULL DEFAULT '',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (attempt_id, question_id)
);

CREATE TABLE IF NOT EXISTS results (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  attempt_id UUID NOT NULL UNIQUE REFERENCES attempts(id) ON DELETE CASCADE,
  listening_band NUMERIC(2,1) NOT NULL,
  reading_band NUMERIC(2,1) NOT NULL,
  writing_band NUMERIC(2,1) NOT NULL,
  speaking_band NUMERIC(2,1) NOT NULL,
  overall_band NUMERIC(2,1) NOT NULL,
  details JSONB NOT NULL,
  rubric_version TEXT NOT NULL,
  generated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS audit_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE SET NULL,
  action TEXT NOT NULL,
  entity TEXT NOT NULL,
  entity_id TEXT NOT NULL,
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
