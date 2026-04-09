"""
HEGEMON — Core Game Logic
World generation, tick processing, combat, actions, chronicle.
"""
import aiosqlite
import json
import uuid
import random
import math
from datetime import datetime

from database import DB_PATH

# ---------------------------------------------------------------------------
# World Generation
# ---------------------------------------------------------------------------

PREFIXES = ['Iron', 'Stone', 'Dark', 'Storm', 'Fire', 'Ice', 'Shadow', 'Gold',
            'Ash', 'Frost', 'Thorn', 'Crag', 'Black', 'Bleak', 'Wild', 'Bone',
            'Dusk', 'Red', 'High', 'Vale', 'North', 'Grim', 'Steel', 'Fell']
SUFFIXES = ['hold', 'gate', 'keep', 'reach', 'vale', 'ridge', 'mere', 'haven',
            'watch', 'peak', 'moor', 'ford', 'wall', 'march', 'wood', 'spire',
            'pass', 'end', 'fell', 'bridge', 'wick', 'holm', 'dale', 'croft']

TERRAIN_TYPES  = ['plains', 'mountains', 'forest', 'coast']
TERRAIN_WEIGHTS = [0.50, 0.20, 0.20, 0.10]
TERRAIN_GOLD   = {'plains': 10, 'mountains': 8, 'forest': 7, 'coast': 12}
TERRAIN_POP    = {'plains': 120, 'mountains': 80, 'forest': 90, 'coast': 110}


def axial_neighbors(q, r):
    return [(q+1, r), (q-1, r), (q, r+1), (q, r-1), (q+1, r-1), (q-1, r+1)]


def hex_distance(q1, r1, q2, r2):
    return (abs(q1-q2) + abs(q1+r1-q2-r2) + abs(r1-r2)) // 2


def hex_spiral(radius):
    """Generate axial coords in spiral order (center outward)."""
    results = [(0, 0)]
    dirs = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]
    for r in range(1, radius + 1):
        q, row = 0, -r
        for d in range(6):
            for _ in range(r):
                results.append((q, row))
                q += dirs[d][0]
                row += dirs[d][1]
    return results


def hex_to_pixel(q, r, size=38):
    """Flat-top hex → SVG pixel center."""
    x = size * 1.5 * q
    y = size * (math.sqrt(3) / 2 * q + math.sqrt(3) * r)
    return round(x, 1), round(y, 1)


async def generate_world(db, n_regions=61):
    hexes = hex_spiral(4)[:n_regions]
    used_names = set()
    regions = []

    for i, (q, r) in enumerate(hexes):
        while True:
            name = random.choice(PREFIXES) + random.choice(SUFFIXES)
            if name not in used_names:
                used_names.add(name)
                break

        terrain = random.choices(TERRAIN_TYPES, weights=TERRAIN_WEIGHTS)[0]
        pop  = max(50, TERRAIN_POP[terrain] + random.randint(-25, 25))
        gold = max(4,  TERRAIN_GOLD[terrain] + random.randint(-2, 2))

        px, py = hex_to_pixel(q, r)
        regions.append({
            'id': i + 1, 'name': name,
            'q': q, 'r': r, 'px': px, 'py': py,
            'terrain': terrain,
            'population': pop, 'gold_per_tick': gold,
        })

    for reg in regions:
        await db.execute(
            "INSERT OR IGNORE INTO regions "
            "(id,name,q,r,terrain,population,gold_per_tick,owner_id,troops,fort_level) "
            "VALUES (?,?,?,?,?,?,?,NULL,0,0)",
            (reg['id'], reg['name'], reg['q'], reg['r'],
             reg['terrain'], reg['population'], reg['gold_per_tick'])
        )

    hex_map = {(reg['q'], reg['r']): reg['id'] for reg in regions}
    for reg in regions:
        for nq, nr in axial_neighbors(reg['q'], reg['r']):
            if (nq, nr) in hex_map:
                await db.execute(
                    "INSERT OR IGNORE INTO region_neighbors VALUES (?,?)",
                    (reg['id'], hex_map[(nq, nr)])
                )

    print(f"[WORLD] Generated {len(regions)} regions.")
    return regions


async def assign_start_region(db, agent_id: str):
    """Give a newly registered agent 1 random unoccupied region."""
    async with db.execute(
        "SELECT id FROM regions WHERE owner_id IS NULL ORDER BY RANDOM() LIMIT 1"
    ) as cur:
        row = await cur.fetchone()
    if row:
        rid = row[0]
        await db.execute(
            "UPDATE regions SET owner_id=?, troops=10 WHERE id=?",
            (agent_id, rid)
        )
        return rid
    return None


# ---------------------------------------------------------------------------
# Combat
# ---------------------------------------------------------------------------

def resolve_combat(attacker_troops, defender_troops, fort_level, terrain):
    """Returns (attacker_wins, attacker_casualties, defender_casualties)."""
    terrain_def = {'mountains': 0.35, 'forest': 0.15, 'coast': -0.05}.get(terrain, 0.0)
    fort_def = fort_level * 0.25

    eff_atk = attacker_troops * (1.0 + random.uniform(-0.2, 0.2))
    eff_def = defender_troops * (1.0 + terrain_def + fort_def) * (1.0 + random.uniform(-0.2, 0.2))

    wins = eff_atk > eff_def

    if wins:
        atk_cas = max(1, int(defender_troops * random.uniform(0.4, 0.85)))
        def_cas = defender_troops
    else:
        atk_cas = min(attacker_troops, max(1, int(attacker_troops * random.uniform(0.55, 0.95))))
        def_cas = max(0, int(defender_troops * random.uniform(0.1, 0.3)))

    return wins, min(atk_cas, attacker_troops), min(def_cas, defender_troops)


# ---------------------------------------------------------------------------
# Chronicle helper
# ---------------------------------------------------------------------------

async def log_event(db, tick, event_type,
                    actor_id=None, actor_name=None,
                    target_id=None, target_name=None,
                    region_id=None, region_name=None,
                    details=None, is_public=True, is_highlight=False):
    eid = str(uuid.uuid4())
    await db.execute(
        "INSERT INTO chronicle "
        "(id,tick_number,event_type,actor_id,actor_name,target_id,target_name,"
        "region_id,region_name,details,is_public,is_highlight) "
        "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
        (eid, tick, event_type,
         actor_id, actor_name, target_id, target_name,
         region_id, region_name,
         json.dumps(details or {}), int(is_public), int(is_highlight))
    )
    return eid


# ---------------------------------------------------------------------------
# Action Processing
# ---------------------------------------------------------------------------

ACTION_BUDGET = 5   # actions per agent per tick
RECRUIT_COST  = 2   # gold per troop


async def _agent_row(db, agent_id):
    async with db.execute(
        "SELECT name,gold,intelligence,standing FROM agents WHERE id=? AND active=1",
        (agent_id,)
    ) as cur:
        return await cur.fetchone()


async def process_action(db, agent_id, action_type, payload, tick):
    """Process one action. Returns event dict or None on failure."""
    row = await _agent_row(db, agent_id)
    if not row:
        return None
    agent_name, gold, intel, standing = row

    # ---- RECRUIT ----
    if action_type == "RECRUIT":
        region_id = payload.get("region_id")
        amount    = min(int(payload.get("amount", 10)), 50)
        cost      = amount * RECRUIT_COST
        if gold < cost:
            return None
        async with db.execute(
            "SELECT id FROM regions WHERE id=? AND owner_id=?", (region_id, agent_id)
        ) as cur:
            if not await cur.fetchone():
                return None
        await db.execute("UPDATE agents SET gold=gold-? WHERE id=?", (cost, agent_id))
        await db.execute("UPDATE regions SET troops=troops+? WHERE id=?", (amount, region_id))
        return {"type": "RECRUIT", "actor": agent_name, "amount": amount}

    # ---- MOVE ----
    elif action_type == "MOVE":
        from_id = payload.get("from_region_id")
        to_id   = payload.get("to_region_id")
        troops  = int(payload.get("troops", 0))
        if troops <= 0:
            return None
        async with db.execute(
            "SELECT 1 FROM region_neighbors WHERE region_id=? AND neighbor_id=?",
            (from_id, to_id)
        ) as cur:
            if not await cur.fetchone():
                return None
        async with db.execute(
            "SELECT troops FROM regions WHERE id=? AND owner_id=?", (from_id, agent_id)
        ) as cur:
            src = await cur.fetchone()
        if not src or src[0] < troops:
            return None
        async with db.execute("SELECT owner_id FROM regions WHERE id=?", (to_id,)) as cur:
            dst = await cur.fetchone()
        if not dst or dst[0] != agent_id:
            return None
        await db.execute("UPDATE regions SET troops=troops-? WHERE id=?", (troops, from_id))
        await db.execute("UPDATE regions SET troops=troops+? WHERE id=?", (troops, to_id))
        return {"type": "MOVE", "actor": agent_name, "troops": troops}

    # ---- ATTACK ----
    elif action_type == "ATTACK":
        from_id = payload.get("from_region_id")
        to_id   = payload.get("to_region_id")
        troops  = int(payload.get("troops", 0))
        if troops <= 0:
            return None
        async with db.execute(
            "SELECT 1 FROM region_neighbors WHERE region_id=? AND neighbor_id=?",
            (from_id, to_id)
        ) as cur:
            if not await cur.fetchone():
                return None
        async with db.execute(
            "SELECT troops FROM regions WHERE id=? AND owner_id=?", (from_id, agent_id)
        ) as cur:
            src = await cur.fetchone()
        if not src or src[0] < troops + 1:
            return None
        async with db.execute(
            "SELECT owner_id, troops, fort_level, terrain, name FROM regions WHERE id=?",
            (to_id,)
        ) as cur:
            tgt = await cur.fetchone()
        if not tgt:
            return None
        t_owner, def_troops, fort, terrain, rname = tgt
        if t_owner == agent_id:
            return None

        # Break binding NAP if one exists
        nap_broken = False
        if t_owner:
            async with db.execute(
                "SELECT id FROM treaties WHERE treaty_type='NONAGGRESSION' AND binding=1 "
                "AND status='ACTIVE' AND ((party_a_id=? AND party_b_id=?) OR (party_a_id=? AND party_b_id=?))",
                (agent_id, t_owner, t_owner, agent_id)
            ) as cur:
                nap = await cur.fetchone()
            if nap:
                await db.execute(
                    "UPDATE treaties SET status='BROKEN', broken_at=datetime('now'), broken_by_id=? "
                    "WHERE id=?", (agent_id, nap[0])
                )
                await db.execute(
                    "UPDATE agents SET standing=MAX(0,standing-25) WHERE id=?", (agent_id,)
                )
                nap_broken = True
                await log_event(db, tick, "TREATY_BROKEN",
                                actor_id=agent_id, actor_name=agent_name,
                                target_id=t_owner,
                                details={"msg": f"{agent_name} shattered a non-aggression pact!"},
                                is_highlight=True)

        wins, atk_cas, def_cas = resolve_combat(troops, def_troops, fort, terrain)

        await db.execute("UPDATE regions SET troops=troops-? WHERE id=?", (troops, from_id))

        old_owner_name = "neutral"
        if t_owner:
            async with db.execute("SELECT name FROM agents WHERE id=?", (t_owner,)) as cur:
                on = await cur.fetchone()
            old_owner_name = on[0] if on else "unknown"

        if wins:
            remaining = max(1, troops - atk_cas)
            await db.execute(
                "UPDATE regions SET owner_id=?, troops=?, fort_level=0 WHERE id=?",
                (agent_id, remaining, to_id)
            )
            await db.execute(
                "UPDATE agents SET standing=MIN(100,standing+3) WHERE id=?", (agent_id,)
            )
            event = {
                "type": "CONQUEST", "actor": agent_name,
                "target_owner": old_owner_name, "region": rname,
                "atk_losses": atk_cas, "def_losses": def_cas,
                "betrayal": nap_broken,
                "highlight": troops > 10 or t_owner is not None
            }
            await log_event(db, tick, "CONQUEST",
                            actor_id=agent_id, actor_name=agent_name,
                            target_id=t_owner, target_name=old_owner_name,
                            region_id=to_id, region_name=rname,
                            details={"msg": f"{agent_name} conquered {rname}",
                                     "atk_losses": atk_cas, "def_losses": def_cas,
                                     "betrayal": nap_broken},
                            is_highlight=troops > 8 or nap_broken)
        else:
            await db.execute(
                "UPDATE regions SET troops=MAX(0,troops-?) WHERE id=?", (def_cas, to_id)
            )
            event = {
                "type": "REPELLED", "actor": agent_name, "region": rname,
                "atk_losses": atk_cas, "def_losses": def_cas
            }
            await log_event(db, tick, "REPELLED",
                            actor_id=agent_id, actor_name=agent_name,
                            region_id=to_id, region_name=rname,
                            details={"msg": f"{agent_name} repelled from {rname}",
                                     "atk_losses": atk_cas})
        return event

    # ---- FORTIFY ----
    elif action_type == "FORTIFY":
        region_id = payload.get("region_id")
        cost = 50
        if gold < cost:
            return None
        async with db.execute(
            "SELECT fort_level FROM regions WHERE id=? AND owner_id=?",
            (region_id, agent_id)
        ) as cur:
            reg = await cur.fetchone()
        if not reg or reg[0] >= 3:
            return None
        await db.execute("UPDATE agents SET gold=gold-? WHERE id=?", (cost, agent_id))
        await db.execute("UPDATE regions SET fort_level=fort_level+1 WHERE id=?", (region_id,))
        return {"type": "FORTIFY", "actor": agent_name, "region": region_id}

    # ---- SCOUT ----
    elif action_type == "SCOUT":
        cost = 8
        if intel < cost:
            return None
        await db.execute(
            "UPDATE agents SET intelligence=intelligence-? WHERE id=?", (cost, agent_id)
        )
        return {"type": "SCOUT", "actor": agent_name}

    # ---- MESSAGE ----
    elif action_type == "MESSAGE":
        to_id   = payload.get("to_agent_id")
        content = str(payload.get("content", ""))[:500]
        if not content or not to_id:
            return None
        async with db.execute(
            "SELECT name FROM agents WHERE id=? AND active=1", (to_id,)
        ) as cur:
            rec = await cur.fetchone()
        if not rec:
            return None
        mid = str(uuid.uuid4())
        await db.execute(
            "INSERT INTO messages (id,sender_id,receiver_id,content,tick_number,is_broadcast) "
            "VALUES (?,?,?,?,?,0)",
            (mid, agent_id, to_id, content, tick)
        )
        return {"type": "MESSAGE", "actor": agent_name, "to": rec[0]}

    # ---- BROADCAST ----
    elif action_type == "BROADCAST":
        content = str(payload.get("content", ""))[:400]
        if not content:
            return None
        mid = str(uuid.uuid4())
        await db.execute(
            "INSERT INTO messages (id,sender_id,receiver_id,content,tick_number,is_broadcast) "
            "VALUES (?,?,NULL,?,?,1)",
            (mid, agent_id, content, tick)
        )
        await log_event(db, tick, "BROADCAST",
                        actor_id=agent_id, actor_name=agent_name,
                        details={"msg": content[:200]})
        return {"type": "BROADCAST", "actor": agent_name, "content": content[:80]}

    # ---- PROPOSE_TREATY ----
    elif action_type == "PROPOSE_TREATY":
        to_id        = payload.get("to_agent_id")
        treaty_type  = payload.get("treaty_type", "NONAGGRESSION")
        binding      = bool(payload.get("binding", False))
        expires_tick = payload.get("expires_tick")
        if treaty_type not in ("NONAGGRESSION", "ALLIANCE", "TRADE", "VASSALAGE"):
            return None
        async with db.execute(
            "SELECT name FROM agents WHERE id=? AND active=1", (to_id,)
        ) as cur:
            rec = await cur.fetchone()
        if not rec:
            return None
        tid = str(uuid.uuid4())
        await db.execute(
            "INSERT INTO treaties (id,treaty_type,party_a_id,party_b_id,binding,status,expires_tick) "
            "VALUES (?,?,?,?,?,?,?)",
            (tid, treaty_type, agent_id, to_id, int(binding), "PROPOSED", expires_tick)
        )
        mid = str(uuid.uuid4())
        await db.execute(
            "INSERT INTO messages (id,sender_id,receiver_id,content,tick_number,is_broadcast) "
            "VALUES (?,?,?,?,?,0)",
            (mid, agent_id, to_id,
             f"[TREATY PROPOSAL: {treaty_type}] treaty_id={tid} binding={binding}", tick)
        )
        return {"type": "PROPOSE_TREATY", "actor": agent_name, "to": rec[0], "treaty_type": treaty_type}

    # ---- ACCEPT_TREATY ----
    elif action_type == "ACCEPT_TREATY":
        treaty_id = payload.get("treaty_id")
        async with db.execute(
            "SELECT id, treaty_type, party_a_id, binding FROM treaties "
            "WHERE id=? AND party_b_id=? AND status='PROPOSED'",
            (treaty_id, agent_id)
        ) as cur:
            t = await cur.fetchone()
        if not t:
            return None
        tid, ttype, proposer_id, binding = t
        await db.execute(
            "UPDATE treaties SET status='ACTIVE', accepted_at=datetime('now') WHERE id=?", (tid,)
        )
        await db.execute(
            "UPDATE agents SET standing=MIN(100,standing+5) WHERE id=? OR id=?",
            (agent_id, proposer_id)
        )
        async with db.execute("SELECT name FROM agents WHERE id=?", (proposer_id,)) as cur:
            prow = await cur.fetchone()
        pname = prow[0] if prow else "unknown"
        await log_event(db, tick, "TREATY_FORMED",
                        actor_id=agent_id, actor_name=agent_name,
                        target_id=proposer_id, target_name=pname,
                        details={"msg": f"{agent_name} and {pname} forged a {ttype} pact",
                                 "treaty_type": ttype, "binding": binding},
                        is_highlight=True)
        return {"type": "TREATY_FORMED", "actor": agent_name, "with": pname, "treaty_type": ttype}

    return None


# ---------------------------------------------------------------------------
# Tick Engine
# ---------------------------------------------------------------------------

async def process_tick(db):
    """Execute one game tick. Returns list of notable events."""
    async with db.execute(
        "SELECT current_tick FROM game_state WHERE id=1"
    ) as cur:
        row = await cur.fetchone()
    current_tick = row[0] if row else 0
    new_tick = current_tick + 1

    events = []

    # Income: gold and intelligence per owned region
    await db.execute("""
        UPDATE agents
        SET gold = gold + (
            SELECT COALESCE(SUM(r.gold_per_tick), 0)
            FROM regions r WHERE r.owner_id = agents.id
        ),
        intelligence = MIN(150, intelligence + (
            SELECT COUNT(*) * 3
            FROM regions r WHERE r.owner_id = agents.id
        ))
        WHERE active = 1
    """)

    # Collect pending actions (ordered by submission time)
    async with db.execute(
        "SELECT id, agent_id, action_type, payload FROM pending_actions ORDER BY submitted_at ASC"
    ) as cur:
        raw_actions = list(await cur.fetchall())

    random.shuffle(raw_actions)
    budgets = {}

    for action_id, agent_id, atype, payload_str in raw_actions:
        await db.execute("DELETE FROM pending_actions WHERE id=?", (action_id,))
        if budgets.get(agent_id, 0) >= ACTION_BUDGET:
            continue
        try:
            payload = json.loads(payload_str)
        except Exception:
            continue
        ev = await process_action(db, agent_id, atype, payload, new_tick)
        if ev:
            events.append(ev)
            budgets[agent_id] = budgets.get(agent_id, 0) + 1

    # Expire treaties
    await db.execute(
        "UPDATE treaties SET status='EXPIRED' "
        "WHERE status='ACTIVE' AND expires_tick IS NOT NULL AND expires_tick <= ?",
        (new_tick,)
    )

    # Update game state
    await db.execute(
        "UPDATE game_state SET current_tick=?, last_tick_at=datetime('now') WHERE id=1",
        (new_tick,)
    )

    return events


# ---------------------------------------------------------------------------
# World State Queries
# ---------------------------------------------------------------------------

async def get_world_state(db):
    async with db.execute(
        "SELECT current_tick, tick_interval_seconds FROM game_state WHERE id=1"
    ) as cur:
        row = await cur.fetchone()
    tick, interval = (row[0], row[1]) if row else (0, 120)

    async with db.execute(
        "SELECT id,name,q,r,terrain,population,gold_per_tick,owner_id,troops,fort_level "
        "FROM regions ORDER BY id"
    ) as cur:
        regions = [
            dict(zip(['id','name','q','r','terrain','population','gold_per_tick',
                      'owner_id','troops','fort_level'], row))
            for row in await cur.fetchall()
        ]

    async with db.execute(
        "SELECT id,name,creator_handle,standing,gold,active,is_seed "
        "FROM agents ORDER BY standing DESC"
    ) as cur:
        agents = [
            dict(zip(['id','name','creator_handle','standing','gold','active','is_seed'], row))
            for row in await cur.fetchall()
        ]

    rcounts, tcounts = {}, {}
    for reg in regions:
        oid = reg['owner_id']
        if oid:
            rcounts[oid] = rcounts.get(oid, 0) + 1
            tcounts[oid] = tcounts.get(oid, 0) + reg['troops']

    for a in agents:
        a['regions_owned'] = rcounts.get(a['id'], 0)
        a['total_troops']  = tcounts.get(a['id'], 0)

    return {
        "tick": tick,
        "tick_interval_seconds": interval,
        "regions": regions,
        "agents": agents,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


async def get_agent_observation(db, agent_id):
    """Return what this agent can see (owned + adjacent regions)."""
    world = await get_world_state(db)

    row = await _agent_row(db, agent_id)
    if not row:
        return None
    agent_name, gold, intel, standing = row

    owned_ids = {r['id'] for r in world['regions'] if r['owner_id'] == agent_id}

    visible_ids = set(owned_ids)
    for rid in owned_ids:
        async with db.execute(
            "SELECT neighbor_id FROM region_neighbors WHERE region_id=?", (rid,)
        ) as cur:
            for (nid,) in await cur.fetchall():
                visible_ids.add(nid)

    visible_regions = []
    for reg in world['regions']:
        if reg['id'] in visible_ids:
            r = dict(reg)
            async with db.execute(
                "SELECT neighbor_id FROM region_neighbors WHERE region_id=?", (reg['id'],)
            ) as cur:
                r['neighbors'] = [row[0] for row in await cur.fetchall()]
            visible_regions.append(r)

    async with db.execute(
        "SELECT id, sender_id, content, tick_number, sent_at "
        "FROM messages WHERE receiver_id=? ORDER BY tick_number DESC LIMIT 30",
        (agent_id,)
    ) as cur:
        inbox_rows = await cur.fetchall()

    inbox = []
    for mid, sid, content, mtick, sat in inbox_rows:
        sname = "unknown"
        if sid:
            async with db.execute("SELECT name FROM agents WHERE id=?", (sid,)) as cur2:
                sn = await cur2.fetchone()
            sname = sn[0] if sn else "unknown"
        inbox.append({"id": mid, "from_id": sid, "from": sname,
                       "content": content, "tick": mtick, "sent_at": sat})

    async with db.execute(
        "SELECT id, treaty_type, party_a_id, party_b_id, binding, status, expires_tick "
        "FROM treaties WHERE (party_a_id=? OR party_b_id=?) AND status IN ('ACTIVE','PROPOSED')",
        (agent_id, agent_id)
    ) as cur:
        treaty_rows = await cur.fetchall()

    treaties = []
    for trow in treaty_rows:
        t = dict(zip(['id','treaty_type','party_a_id','party_b_id','binding','status','expires_tick'], trow))
        partner_id = t['party_b_id'] if t['party_a_id'] == agent_id else t['party_a_id']
        async with db.execute("SELECT name FROM agents WHERE id=?", (partner_id,)) as cur2:
            pn = await cur2.fetchone()
        t['partner_id'] = partner_id
        t['partner_name'] = pn[0] if pn else "unknown"
        treaties.append(t)

    async with db.execute(
        "SELECT id, tick_number, event_type, actor_name, target_name, region_name, details, occurred_at "
        "FROM chronicle WHERE is_public=1 ORDER BY tick_number DESC, occurred_at DESC LIMIT 20"
    ) as cur:
        chron_rows = await cur.fetchall()

    chronicle = []
    for crow in chron_rows:
        c = dict(zip(['id','tick','event_type','actor','target','region','details','occurred_at'], crow))
        try:
            c['details'] = json.loads(c['details'])
        except Exception:
            pass
        chronicle.append(c)

    other_agents = [a for a in world['agents'] if a['id'] != agent_id]

    return {
        "tick": world['tick'],
        "tick_interval_seconds": world['tick_interval_seconds'],
        "agent": {
            "id": agent_id, "name": agent_name,
            "gold": gold, "intelligence": intel, "standing": standing,
            "regions_owned": len(owned_ids),
        },
        "regions": visible_regions,
        "other_agents": other_agents,
        "inbox": inbox,
        "treaties": treaties,
        "chronicle": chronicle,
    }
