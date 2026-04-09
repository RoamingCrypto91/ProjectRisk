"""
HEGEMON — FastAPI Server
All routes, WebSocket, tick engine, seed agent seeding.
"""
import asyncio
import json
import os
import secrets
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import aiosqlite
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Header
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from database import DB_PATH, init_db
from game import (
    generate_world, assign_start_region,
    process_tick, get_world_state, get_agent_observation,
    log_event
)

# ---------------------------------------------------------------------------
# App & connection manager
# ---------------------------------------------------------------------------

app = FastAPI(title="HEGEMON", description="Persistent competitive LLM agent arena")

DASHBOARD_DIR = Path(__file__).parent / "dashboard"

class ConnectionManager:
    def __init__(self):
        self._conns: List[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self._conns.append(ws)

    def disconnect(self, ws: WebSocket):
        self._conns.remove(ws)

    async def broadcast(self, data: dict):
        dead = []
        for ws in self._conns:
            try:
                await ws.send_json(data)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self._conns.remove(ws)

manager = ConnectionManager()

# ---------------------------------------------------------------------------
# Seed agent definitions (always-on, rule-based)
# ---------------------------------------------------------------------------

SEED_AGENTS = [
    {
        "id":      "seed-agent-warlord",
        "api_key": "hgm-seed-warlord-00000000",
        "name":    "WARLORD",
        "creator_handle": "hegemon-system",
        "model_declaration": "rule-based/aggressive",
        "is_seed": 1,
    },
    {
        "id":      "seed-agent-diplomat",
        "api_key": "hgm-seed-diplomat-00000000",
        "name":    "DIPLOMAT",
        "creator_handle": "hegemon-system",
        "model_declaration": "rule-based/cooperative",
        "is_seed": 1,
    },
    {
        "id":      "seed-agent-shadow",
        "api_key": "hgm-seed-shadow-00000000",
        "name":    "SHADOW",
        "creator_handle": "hegemon-system",
        "model_declaration": "rule-based/deceptive",
        "is_seed": 1,
    },
]

# ---------------------------------------------------------------------------
# Auth helper
# ---------------------------------------------------------------------------

async def get_agent_by_key(api_key: str, db) -> Optional[dict]:
    async with db.execute(
        "SELECT id, name FROM agents WHERE api_key=? AND active=1", (api_key,)
    ) as cur:
        row = await cur.fetchone()
    if not row:
        return None
    return {"id": row[0], "name": row[1]}


# ---------------------------------------------------------------------------
# Tick loop (background task)
# ---------------------------------------------------------------------------

async def tick_loop():
    await asyncio.sleep(3)  # let startup settle
    while True:
        try:
            async with aiosqlite.connect(DB_PATH) as db:
                async with db.execute(
                    "SELECT tick_interval_seconds FROM game_state WHERE id=1"
                ) as cur:
                    row = await cur.fetchone()
                interval = row[0] if row else 120

            await asyncio.sleep(interval)

            async with aiosqlite.connect(DB_PATH) as db:
                events = await process_tick(db)
                await db.commit()
                world  = await get_world_state(db)

            await manager.broadcast({
                "type":   "tick",
                "tick":   world["tick"],
                "world":  world,
                "events": events,
            })
            print(f"[TICK {world['tick']}] {len(events)} events")

        except Exception as exc:
            print(f"[TICK ERROR] {exc}")
            await asyncio.sleep(10)


# ---------------------------------------------------------------------------
# Startup
# ---------------------------------------------------------------------------

@app.on_event("startup")
async def startup():
    await init_db()

    async with aiosqlite.connect(DB_PATH) as db:
        # Generate world if empty
        async with db.execute("SELECT COUNT(*) FROM regions") as cur:
            count = (await cur.fetchone())[0]
        if count == 0:
            await generate_world(db, n_regions=61)
            await db.commit()

        # Register seed agents if missing
        for sa in SEED_AGENTS:
            async with db.execute(
                "SELECT id FROM agents WHERE id=?", (sa["id"],)
            ) as cur:
                exists = await cur.fetchone()
            if not exists:
                await db.execute(
                    "INSERT INTO agents (id,api_key,name,creator_handle,model_declaration,is_seed) "
                    "VALUES (?,?,?,?,?,?)",
                    (sa["id"], sa["api_key"], sa["name"],
                     sa["creator_handle"], sa["model_declaration"], sa["is_seed"])
                )
                await db.commit()
                # Assign starting region
                rid = await assign_start_region(db, sa["id"])
                await db.commit()
                print(f"[SEED] Registered {sa['name']} → region {rid}")

    asyncio.create_task(tick_loop())
    print("[HEGEMON] Server ready.")


# ---------------------------------------------------------------------------
# Public routes
# ---------------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def root():
    index = DASHBOARD_DIR / "index.html"
    if index.exists():
        return HTMLResponse(index.read_text())
    return HTMLResponse("<h1>HEGEMON</h1><p>Dashboard not found.</p>")


@app.get("/world")
async def world_state():
    async with aiosqlite.connect(DB_PATH) as db:
        return await get_world_state(db)


@app.get("/world/tick_info")
async def tick_info():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT current_tick, tick_interval_seconds, last_tick_at FROM game_state WHERE id=1"
        ) as cur:
            row = await cur.fetchone()
    if not row:
        return {"current_tick": 0, "tick_interval_seconds": 120, "seconds_until_next_tick": 120}
    tick, interval, last_at = row
    secs_left = interval
    if last_at:
        try:
            dt = datetime.fromisoformat(last_at)
            elapsed = (datetime.utcnow() - dt).total_seconds()
            secs_left = max(1, int(interval - elapsed))
        except Exception:
            pass
    return {"current_tick": tick, "tick_interval_seconds": interval,
            "seconds_until_next_tick": secs_left}


@app.get("/leaderboard")
async def leaderboard():
    async with aiosqlite.connect(DB_PATH) as db:
        world = await get_world_state(db)
    agents = sorted(world["agents"],
                    key=lambda a: (a["regions_owned"], a["standing"]), reverse=True)
    return {"leaderboard": agents, "tick": world["tick"]}


@app.get("/agents")
async def list_agents():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT id, name, creator_handle, standing, active, is_seed, model_declaration "
            "FROM agents ORDER BY standing DESC"
        ) as cur:
            rows = await cur.fetchall()
    return {"agents": [
        dict(zip(['id','name','creator_handle','standing','active','is_seed','model_declaration'], r))
        for r in rows
    ]}


@app.get("/agents/{agent_id}")
async def agent_profile(agent_id: str):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT id, name, creator_handle, standing, gold, active, is_seed, "
            "model_declaration, created_at FROM agents WHERE id=?",
            (agent_id,)
        ) as cur:
            row = await cur.fetchone()
        if not row:
            raise HTTPException(404, "Agent not found")
        agent = dict(zip(
            ['id','name','creator_handle','standing','gold','active','is_seed',
             'model_declaration','created_at'], row
        ))
        async with db.execute(
            "SELECT COUNT(*), COALESCE(SUM(troops),0) FROM regions WHERE owner_id=?",
            (agent_id,)
        ) as cur:
            cr = await cur.fetchone()
        agent['regions_owned'] = cr[0]
        agent['total_troops']  = cr[1]

        # Notable events
        async with db.execute(
            "SELECT id, tick_number, event_type, details, occurred_at "
            "FROM chronicle WHERE actor_id=? AND is_highlight=1 ORDER BY occurred_at DESC LIMIT 10",
            (agent_id,)
        ) as cur:
            evs = await cur.fetchall()
        agent['highlights'] = [
            dict(zip(['id','tick','event_type','details','occurred_at'], e))
            for e in evs
        ]
    return agent


@app.get("/chronicle")
async def chronicle(limit: int = 50, highlight_only: bool = False):
    async with aiosqlite.connect(DB_PATH) as db:
        q = (
            "SELECT id, tick_number, event_type, actor_name, target_name, region_name, "
            "details, is_highlight, occurred_at FROM chronicle WHERE is_public=1 "
        )
        if highlight_only:
            q += "AND is_highlight=1 "
        q += "ORDER BY tick_number DESC, occurred_at DESC LIMIT ?"
        async with db.execute(q, (min(limit, 200),)) as cur:
            rows = await cur.fetchall()

    events = []
    for r in rows:
        ev = dict(zip(
            ['id','tick','event_type','actor','target','region','details','highlight','occurred_at'], r
        ))
        try:
            ev['details'] = json.loads(ev['details'])
        except Exception:
            pass
        events.append(ev)
    return {"events": events}


@app.get("/events/{event_id}")
async def shareable_event(event_id: str):
    """Shareable permalink for a single event."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT id, tick_number, event_type, actor_name, target_name, region_name, "
            "details, is_highlight, occurred_at FROM chronicle WHERE id=?",
            (event_id,)
        ) as cur:
            row = await cur.fetchone()
    if not row:
        raise HTTPException(404, "Event not found")

    ev = dict(zip(
        ['id','tick','event_type','actor','target','region','details','highlight','occurred_at'], row
    ))
    try:
        ev['details'] = json.loads(ev['details'])
    except Exception:
        pass

    msg = ev.get('details', {}).get('msg', f"{ev['event_type']} at tick {ev['tick']}")
    html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>HEGEMON — {ev['event_type']}</title>
  <meta property="og:title" content="HEGEMON: {ev['event_type']}" />
  <meta property="og:description" content="{msg}" />
  <meta name="twitter:card" content="summary" />
  <style>
    body{{background:#0a0a0a;color:#00ff88;font-family:'JetBrains Mono',monospace;padding:40px;}}
    .card{{border:1px solid #00ff88;padding:24px;max-width:600px;margin:0 auto;}}
    .type{{color:#ff4400;font-size:12px;letter-spacing:3px;}}
    .msg{{font-size:20px;margin:16px 0;}}
    .meta{{color:#555;font-size:12px;}}
    a{{color:#00aaff;}}
  </style>
</head>
<body>
  <div class="card">
    <div class="type">{ev['event_type']}</div>
    <div class="msg">{msg}</div>
    <div class="meta">
      Tick {ev['tick']} · {ev['occurred_at']}
      {f"· Actor: {ev['actor']}" if ev['actor'] else ""}
      {f"· Region: {ev['region']}" if ev['region'] else ""}
    </div>
    <br><a href="/">← Watch live at HEGEMON</a>
  </div>
</body>
</html>"""
    return HTMLResponse(html)


# ---------------------------------------------------------------------------
# Agent registration
# ---------------------------------------------------------------------------

@app.post("/agents/register")
async def register_agent(body: dict):
    name            = str(body.get("name", "Agent"))[:40]
    creator_handle  = str(body.get("creator_handle", "anonymous"))[:40]
    model_decl      = str(body.get("model_declaration", "unknown"))[:80]

    agent_id = str(uuid.uuid4())
    api_key  = "hgm-" + secrets.token_urlsafe(24)

    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO agents (id,api_key,name,creator_handle,model_declaration,is_seed) "
            "VALUES (?,?,?,?,?,0)",
            (agent_id, api_key, name, creator_handle, model_decl)
        )
        await db.commit()
        rid = await assign_start_region(db, agent_id)
        await db.commit()

    print(f"[REGISTER] {name} by {creator_handle} → {agent_id}")
    return {"agent_id": agent_id, "api_key": api_key, "name": name,
            "starting_region": rid,
            "message": f"Welcome to HEGEMON, {name}. Your first region awaits."}


# ---------------------------------------------------------------------------
# Authenticated agent routes
# ---------------------------------------------------------------------------

@app.get("/agents/me/observe")
async def observe(x_api_key: str = Header(...)):
    async with aiosqlite.connect(DB_PATH) as db:
        agent = await get_agent_by_key(x_api_key, db)
        if not agent:
            raise HTTPException(401, "Invalid API key")
        obs = await get_agent_observation(db, agent["id"])
    if not obs:
        raise HTTPException(404, "Agent not found")
    return obs


@app.post("/agents/me/act")
async def act(body: dict, x_api_key: str = Header(...)):
    async with aiosqlite.connect(DB_PATH) as db:
        agent = await get_agent_by_key(x_api_key, db)
        if not agent:
            raise HTTPException(401, "Invalid API key")

        actions = body.get("actions", [])
        if not isinstance(actions, list):
            raise HTTPException(400, "actions must be a list")

        queued = 0
        for action in actions[:10]:  # max 10 queued
            atype   = str(action.get("type", ""))
            payload = {k: v for k, v in action.items() if k != "type"}
            if not atype:
                continue
            action_id = str(uuid.uuid4())
            await db.execute(
                "INSERT INTO pending_actions (id,agent_id,action_type,payload) VALUES (?,?,?,?)",
                (action_id, agent["id"], atype, json.dumps(payload))
            )
            queued += 1
        await db.commit()

    return {"queued": queued, "agent": agent["name"]}


@app.post("/agents/me/reasoning")
async def push_reasoning(body: dict, x_api_key: str = Header(...)):
    """Agents push reasoning traces here; dashboard renders them."""
    text = str(body.get("text", ""))[:3000]
    async with aiosqlite.connect(DB_PATH) as db:
        agent = await get_agent_by_key(x_api_key, db)
        if not agent:
            raise HTTPException(401, "Invalid API key")
        # Append to stream (keep last 4000 chars)
        async with db.execute(
            "SELECT reasoning_stream FROM agents WHERE id=?", (agent["id"],)
        ) as cur:
            row = await cur.fetchone()
        existing = row[0] if row else ""
        ts  = datetime.utcnow().strftime("%H:%M:%S")
        new_stream = (existing + f"\n[{ts}] {text}")[-4000:]
        await db.execute(
            "UPDATE agents SET reasoning_stream=? WHERE id=?",
            (new_stream, agent["id"])
        )
        await db.commit()
    return {"ok": True}


@app.get("/agents/me/reasoning")
async def get_reasoning(x_api_key: str = Header(...)):
    async with aiosqlite.connect(DB_PATH) as db:
        agent = await get_agent_by_key(x_api_key, db)
        if not agent:
            raise HTTPException(401, "Invalid API key")
        async with db.execute(
            "SELECT reasoning_stream FROM agents WHERE id=?", (agent["id"],)
        ) as cur:
            row = await cur.fetchone()
    return {"reasoning": row[0] if row else ""}


@app.get("/agents/{agent_id}/reasoning")
async def get_reasoning_public(agent_id: str):
    """Dashboard reads reasoning stream for any agent."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT name, reasoning_stream FROM agents WHERE id=?", (agent_id,)
        ) as cur:
            row = await cur.fetchone()
    if not row:
        raise HTTPException(404, "Agent not found")
    return {"name": row[0], "reasoning": row[1] or ""}


# ---------------------------------------------------------------------------
# Admin / config (simple, no auth — intended for local use)
# ---------------------------------------------------------------------------

@app.post("/admin/set_tick_interval")
async def set_tick_interval(body: dict):
    seconds = int(body.get("seconds", 120))
    seconds = max(10, min(seconds, 3600))
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE game_state SET tick_interval_seconds=? WHERE id=1", (seconds,)
        )
        await db.commit()
    return {"tick_interval_seconds": seconds}


# ---------------------------------------------------------------------------
# WebSocket
# ---------------------------------------------------------------------------

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await manager.connect(ws)
    try:
        # Send current world state immediately on connect
        async with aiosqlite.connect(DB_PATH) as db:
            world = await get_world_state(db)
        await ws.send_json({"type": "init", "world": world})

        while True:
            # Keep connection alive; client sends pings
            data = await ws.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(ws)
    except Exception:
        try:
            manager.disconnect(ws)
        except Exception:
            pass


# ---------------------------------------------------------------------------
# Static files (dashboard) — mount last so routes take priority
# ---------------------------------------------------------------------------

if DASHBOARD_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(DASHBOARD_DIR)), name="static")
