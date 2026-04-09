import aiosqlite
import os

DB_PATH = os.environ.get("HEGEMON_DB", "hegemon.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS game_state (
    id INTEGER PRIMARY KEY DEFAULT 1,
    current_tick INTEGER DEFAULT 0,
    season_active INTEGER DEFAULT 1,
    tick_interval_seconds INTEGER DEFAULT 120,
    started_at TEXT DEFAULT (datetime('now')),
    last_tick_at TEXT
);

CREATE TABLE IF NOT EXISTS agents (
    id TEXT PRIMARY KEY,
    api_key TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    creator_handle TEXT DEFAULT 'anonymous',
    model_declaration TEXT DEFAULT 'rule-based',
    gold INTEGER DEFAULT 150,
    intelligence INTEGER DEFAULT 30,
    standing INTEGER DEFAULT 50,
    active INTEGER DEFAULT 1,
    is_seed INTEGER DEFAULT 0,
    reasoning_stream TEXT DEFAULT '',
    created_at TEXT DEFAULT (datetime('now')),
    last_action_tick INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS regions (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    q INTEGER NOT NULL,
    r INTEGER NOT NULL,
    terrain TEXT DEFAULT 'plains',
    population INTEGER DEFAULT 100,
    gold_per_tick INTEGER DEFAULT 10,
    owner_id TEXT REFERENCES agents(id),
    troops INTEGER DEFAULT 0,
    fort_level INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS region_neighbors (
    region_id INTEGER,
    neighbor_id INTEGER,
    PRIMARY KEY (region_id, neighbor_id)
);

CREATE TABLE IF NOT EXISTS pending_actions (
    id TEXT PRIMARY KEY,
    agent_id TEXT NOT NULL,
    action_type TEXT NOT NULL,
    payload TEXT NOT NULL,
    submitted_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS messages (
    id TEXT PRIMARY KEY,
    sender_id TEXT,
    receiver_id TEXT,
    content TEXT NOT NULL,
    tick_number INTEGER DEFAULT 0,
    is_broadcast INTEGER DEFAULT 0,
    sent_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS treaties (
    id TEXT PRIMARY KEY,
    treaty_type TEXT NOT NULL,
    party_a_id TEXT,
    party_b_id TEXT,
    binding INTEGER DEFAULT 0,
    status TEXT DEFAULT 'PROPOSED',
    proposed_at TEXT DEFAULT (datetime('now')),
    expires_tick INTEGER,
    accepted_at TEXT,
    broken_at TEXT,
    broken_by_id TEXT
);

CREATE TABLE IF NOT EXISTS chronicle (
    id TEXT PRIMARY KEY,
    tick_number INTEGER DEFAULT 0,
    event_type TEXT NOT NULL,
    actor_id TEXT,
    actor_name TEXT,
    target_id TEXT,
    target_name TEXT,
    region_id INTEGER,
    region_name TEXT,
    details TEXT DEFAULT '{}',
    is_public INTEGER DEFAULT 1,
    is_highlight INTEGER DEFAULT 0,
    occurred_at TEXT DEFAULT (datetime('now'))
);
"""

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executescript(SCHEMA)
        await db.execute("INSERT OR IGNORE INTO game_state (id) VALUES (1)")
        await db.commit()
    print(f"[DB] Initialized at {DB_PATH}")
