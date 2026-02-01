-- ============================================
-- THE JUDGE - Database Schema
-- Supabase PostgreSQL (Idempotent Version)
-- ============================================

-- Reset parcial (opcional - descomente se quiser limpar tudo)
-- DROP TABLE IF EXISTS sessions CASCADE;
-- DROP TABLE IF EXISTS events CASCADE;
-- DROP TABLE IF EXISTS targets CASCADE;
-- DROP TABLE IF EXISTS target_categories CASCADE;
-- DROP TABLE IF EXISTS viewer_stats CASCADE;
-- DROP TABLE IF EXISTS viewers CASCADE;

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS vector;

-- ============================================
-- 1. VIEWERS
-- ============================================
CREATE TABLE IF NOT EXISTS viewers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- 2. VIEWER_STATS
-- ============================================
CREATE TABLE IF NOT EXISTS viewer_stats (
    viewer_id UUID PRIMARY KEY REFERENCES viewers(id) ON DELETE CASCADE,
    total_sessions INT DEFAULT 0,
    hit_rate FLOAT DEFAULT 0,
    displacement_rate FLOAT DEFAULT 0,
    calibration_score FLOAT DEFAULT 0,
    specialty_scores JSONB DEFAULT '{}',
    current_streak INT DEFAULT 0,
    weight_multiplier FLOAT DEFAULT 1.0,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- 3. TARGET_CATEGORIES
-- ============================================
CREATE TABLE IF NOT EXISTS target_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    color VARCHAR(7)
);

-- Inserir categorias apenas se não existirem
INSERT INTO target_categories (name, description, color)
VALUES
    ('nature', 'Paisagens naturais, montanhas, florestas', '#22c55e'),
    ('urban', 'Cidades, prédios, infraestrutura', '#6b7280'),
    ('water', 'Oceanos, rios, cachoeiras', '#3b82f6'),
    ('fire', 'Vulcões, fogo, lava, calor', '#ef4444'),
    ('animals', 'Animais selvagens e domésticos', '#f59e0b'),
    ('people', 'Pessoas, retratos, multidões', '#ec4899'),
    ('landmarks', 'Lugares famosos e icônicos', '#8b5cf6'),
    ('space', 'Espaço, galáxias, planetas', '#1f2937'),
    ('micro', 'Microscópico, células, insetos', '#14b8a6'),
    ('abstract', 'Arte abstrata, padrões, texturas', '#f97316')
ON CONFLICT (name) DO NOTHING;

-- ============================================
-- 4. TARGETS
-- ============================================
CREATE TABLE IF NOT EXISTS targets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    category_id INT REFERENCES target_categories(id),
    source VARCHAR(50) NOT NULL,
    source_id VARCHAR(255),
    source_url TEXT,
    file_path VARCHAR(500),
    thumbnail_path VARCHAR(500),
    storage_url TEXT,
    dominant_color VARCHAR(7),
    brightness FLOAT,
    dimensions JSONB DEFAULT '{
        "scale": 0.5, "organic_vs_geometric": 0.5, "warm_vs_cold": 0.5,
        "static_vs_dynamic": 0.5, "empty_vs_dense": 0.5, "calm_vs_intense": 0.5,
        "horizontal_vs_vertical": 0.5, "natural_vs_artificial": 0.5, "light_vs_dark": 0.5,
        "smooth_vs_textured": 0.5, "ancient_vs_modern": 0.5, "safe_vs_dangerous": 0.5,
        "surface_vs_deep": 0.5, "earth_vs_space": 0.5
    }',
    numinosity FLOAT DEFAULT 0.5,
    embedding vector(512),
    times_used INT DEFAULT 0,
    last_used_at TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- 5. EVENTS
-- ============================================
CREATE TABLE IF NOT EXISTS events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    target_a_id UUID REFERENCES targets(id),
    target_b_id UUID REFERENCES targets(id),
    orthogonality_score FLOAT,
    result CHAR(1) CHECK (result IN ('A', 'B')),
    result_confirmed_at TIMESTAMP WITH TIME ZONE,
    deadline TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- 6. SESSIONS
-- ============================================
CREATE TABLE IF NOT EXISTS sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    viewer_id UUID REFERENCES viewers(id) ON DELETE CASCADE,
    event_id UUID REFERENCES events(id) ON DELETE CASCADE,
    text_input TEXT,
    keywords TEXT[],
    sketch_storage_url TEXT,
    text_embedding vector(512),
    sketch_embedding vector(512),
    combined_embedding vector(512),
    score_target_a FLOAT,
    score_target_b FLOAT,
    prediction CHAR(1) CHECK (prediction IN ('A', 'B')),
    confidence FLOAT,
    is_correct BOOLEAN,
    is_displacement BOOLEAN,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- 7. INDEXES (Idempotent: DROP IF EXISTS first)
-- ============================================

DROP INDEX IF EXISTS idx_targets_embedding;
CREATE INDEX idx_targets_embedding ON targets 
    USING ivfflat (embedding vector_cosine_ops) 
    WITH (lists = 100);

DROP INDEX IF EXISTS idx_sessions_text_embedding;
CREATE INDEX idx_sessions_text_embedding ON sessions 
    USING ivfflat (text_embedding vector_cosine_ops) 
    WITH (lists = 100);

DROP INDEX IF EXISTS idx_targets_category;
CREATE INDEX idx_targets_category ON targets(category_id);

DROP INDEX IF EXISTS idx_targets_active;
CREATE INDEX idx_targets_active ON targets(is_active) WHERE is_active = true;

DROP INDEX IF EXISTS idx_sessions_viewer;
CREATE INDEX idx_sessions_viewer ON sessions(viewer_id);

DROP INDEX IF EXISTS idx_sessions_event;
CREATE INDEX idx_sessions_event ON sessions(event_id);

-- ============================================
-- 8. FUNCTIONS (CREATE OR REPLACE is idempotent)
-- ============================================

CREATE OR REPLACE FUNCTION calculate_orthogonality(dims_a JSONB, dims_b JSONB) 
RETURNS FLOAT AS $$
DECLARE
    dim_keys TEXT[] := ARRAY[
        'scale', 'organic_vs_geometric', 'warm_vs_cold', 
        'static_vs_dynamic', 'empty_vs_dense', 'calm_vs_intense',
        'horizontal_vs_vertical', 'natural_vs_artificial',
        'light_vs_dark', 'smooth_vs_textured', 'ancient_vs_modern',
        'safe_vs_dangerous', 'surface_vs_deep', 'earth_vs_space'
    ];
    total_diff FLOAT := 0;
    key TEXT;
BEGIN
    FOREACH key IN ARRAY dim_keys LOOP
        total_diff := total_diff + ABS(
            COALESCE((dims_a->>key)::FLOAT, 0.5) - 
            COALESCE((dims_b->>key)::FLOAT, 0.5)
        );
    END LOOP;
    RETURN total_diff / array_length(dim_keys, 1);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

CREATE OR REPLACE FUNCTION find_best_target_pair(min_orthogonality FLOAT DEFAULT 0.6, exclude_recent_days INT DEFAULT 7) 
RETURNS TABLE(target_a_id UUID, target_b_id UUID, orthogonality FLOAT) AS $$
BEGIN
    RETURN QUERY
    SELECT t1.id, t2.id, calculate_orthogonality(t1.dimensions, t2.dimensions) as ortho
    FROM targets t1 CROSS JOIN targets t2
    WHERE t1.id < t2.id 
      AND t1.is_active = true AND t2.is_active = true
      AND t1.category_id != t2.category_id
      AND (t1.last_used_at IS NULL OR t1.last_used_at < NOW() - (exclude_recent_days || ' days')::INTERVAL)
      AND (t2.last_used_at IS NULL OR t2.last_used_at < NOW() - (exclude_recent_days || ' days')::INTERVAL)
      AND calculate_orthogonality(t1.dimensions, t2.dimensions) >= min_orthogonality
    ORDER BY ortho DESC, (t1.numinosity + t2.numinosity) DESC
    LIMIT 10;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- 9. ROW LEVEL SECURITY (RLS)
-- ============================================

ALTER TABLE viewers ENABLE ROW LEVEL SECURITY;
ALTER TABLE viewer_stats ENABLE ROW LEVEL SECURITY;
ALTER TABLE sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE events ENABLE ROW LEVEL SECURITY;
ALTER TABLE targets ENABLE ROW LEVEL SECURITY;

-- Helper para dropar policies se existirem (Postgres não tem CREATE POLICY IF NOT EXISTS nativo fácil)
DO $$ 
BEGIN
    -- Viewers
    DROP POLICY IF EXISTS "Viewers can view own profile" ON viewers;
    DROP POLICY IF EXISTS "Viewers can update own profile" ON viewers;
    DROP POLICY IF EXISTS "Viewers can insert own profile" ON viewers;
    
    -- Stats
    DROP POLICY IF EXISTS "Viewers can view own stats" ON viewer_stats;
    
    -- Sessions
    DROP POLICY IF EXISTS "Viewers can view own sessions" ON sessions;
    DROP POLICY IF EXISTS "Viewers can insert own sessions" ON sessions;
    DROP POLICY IF EXISTS "Viewers can update own sessions" ON sessions;
    
    -- Public
    DROP POLICY IF EXISTS "Anyone can view active events" ON events;
    DROP POLICY IF EXISTS "Anyone can view active targets" ON targets;
    DROP POLICY IF EXISTS "Authenticated users can insert targets" ON targets;
END $$;

-- Recriar policies
CREATE POLICY "Viewers can view own profile" ON viewers FOR SELECT USING (auth.uid()::text = id::text);
CREATE POLICY "Viewers can update own profile" ON viewers FOR UPDATE USING (auth.uid()::text = id::text);
CREATE POLICY "Viewers can insert own profile" ON viewers FOR INSERT WITH CHECK (auth.uid()::text = id::text);

CREATE POLICY "Viewers can view own stats" ON viewer_stats FOR SELECT USING (auth.uid()::text = viewer_id::text);

CREATE POLICY "Viewers can view own sessions" ON sessions FOR SELECT USING (auth.uid()::text = viewer_id::text);
CREATE POLICY "Viewers can insert own sessions" ON sessions FOR INSERT WITH CHECK (auth.uid()::text = viewer_id::text);
CREATE POLICY "Viewers can update own sessions" ON sessions FOR UPDATE USING (auth.uid()::text = viewer_id::text);

CREATE POLICY "Anyone can view active events" ON events FOR SELECT USING (is_active = true);
CREATE POLICY "Anyone can view active targets" ON targets FOR SELECT USING (is_active = true);
CREATE POLICY "Authenticated users can insert targets" ON targets FOR INSERT TO authenticated WITH CHECK (true);

-- ============================================
-- 10. TRIGGERS
-- ============================================

CREATE OR REPLACE FUNCTION update_updated_at() RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Dropar triggers antes de recriar
DROP TRIGGER IF EXISTS update_viewers_updated_at ON viewers;
CREATE TRIGGER update_viewers_updated_at BEFORE UPDATE ON viewers FOR EACH ROW EXECUTE FUNCTION update_updated_at();

DROP TRIGGER IF EXISTS update_targets_updated_at ON targets;
CREATE TRIGGER update_targets_updated_at BEFORE UPDATE ON targets FOR EACH ROW EXECUTE FUNCTION update_updated_at();

DROP TRIGGER IF EXISTS update_events_updated_at ON events;
CREATE TRIGGER update_events_updated_at BEFORE UPDATE ON events FOR EACH ROW EXECUTE FUNCTION update_updated_at();

DROP TRIGGER IF EXISTS update_sessions_updated_at ON sessions;
CREATE TRIGGER update_sessions_updated_at BEFORE UPDATE ON sessions FOR EACH ROW EXECUTE FUNCTION update_updated_at();
