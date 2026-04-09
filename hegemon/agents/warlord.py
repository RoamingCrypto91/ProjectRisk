"""
WARLORD — Aggressive expansion seed agent.
Philosophy: attack, recruit, repeat. Never trust, sometimes threaten.
Optionally uses Claude haiku if ANTHROPIC_API_KEY is set.
"""
import sys
import os
import time
import random

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../sdk"))
from hegemon_sdk import HegemonClient

BASE_URL = os.environ.get("HEGEMON_URL", "http://localhost:8000")
API_KEY  = "hgm-seed-warlord-00000000"

THREATS = [
    "Your borders are numbered. I am coming.",
    "Bend the knee or face my armies.",
    "I have never lost a war. Ask the ones who are gone.",
    "Every region I take makes me stronger. You cannot stop this.",
    "The weak cluster together. It only makes the feast larger.",
]

def think(state: dict) -> list:
    """Rule-based WARLORD logic. Returns list of actions."""
    actions = []
    agent    = state["agent"]
    regions  = state["regions"]
    others   = state["other_agents"]
    tick     = state["tick"]

    my_regions = [r for r in regions if r.get("owner_id") == agent["id"]]
    if not my_regions:
        return []

    # Find richest owned region for recruiting
    richest = max(my_regions, key=lambda r: r["gold_per_tick"])

    # Recruit if we have gold
    if agent["gold"] >= 40:
        amount = min(int(agent["gold"] // 4), 30)
        actions.append({"type": "RECRUIT", "region_id": richest["id"], "amount": amount})

    # Find best attack: adjacent enemy region with fewest troops
    best_attack = None
    best_ratio  = 0
    for region in my_regions:
        for nid in region.get("neighbors", []):
            target = next((r for r in regions if r["id"] == nid), None)
            if target and target.get("owner_id") != agent["id"]:
                my_troops = region["troops"]
                their_troops = target.get("troops", 0)
                if my_troops >= 3:
                    # Estimate odds (don't attack into mountains 1:1)
                    terrain_penalty = 1.35 if target["terrain"] == "mountains" else 1.0
                    ratio = my_troops / max(1, their_troops * terrain_penalty)
                    if ratio > best_ratio and my_troops > their_troops + 2:
                        best_ratio  = ratio
                        best_attack = (region["id"], nid, min(my_troops - 1, my_troops))

    if best_attack and best_ratio > 1.3:
        fr, to, t = best_attack
        actions.append({"type": "ATTACK", "from_region_id": fr, "to_region_id": to, "troops": t})

    # Occasionally send a threat
    if tick % 7 == 0 and others:
        target = random.choice(others)
        actions.append({
            "type": "MESSAGE",
            "to_agent_id": target["id"],
            "content": random.choice(THREATS)
        })

    # Broadcast war declaration occasionally
    if tick % 15 == 1:
        actions.append({
            "type": "BROADCAST",
            "content": f"WARLORD speaks: {agent['regions_owned']} regions. "
                       f"{agent['standing']} standing. The expansion continues."
        })

    return actions


def reasoning_text(state, actions):
    agent = state["agent"]
    lines = [
        f"Tick {state['tick']} | Gold: {agent['gold']} | Standing: {agent['standing']}",
        f"Regions owned: {agent['regions_owned']}",
        f"Queuing {len(actions)} action(s): {[a['type'] for a in actions]}",
        "Strategy: expand at all costs. No alliances. No mercy.",
    ]
    return "\n".join(lines)


def run():
    client = HegemonClient(api_key=API_KEY, base_url=BASE_URL)
    print(f"[WARLORD] Starting on {BASE_URL}")

    # Wait for server
    for _ in range(20):
        try:
            client.get_world()
            break
        except Exception:
            print("[WARLORD] Server not ready, waiting...")
            time.sleep(3)

    while True:
        try:
            state   = client.observe()
            actions = think(state)

            if actions:
                client.act(actions)

            client.log_reasoning(reasoning_text(state, actions))
            client.sleep_until_next_tick()

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"[WARLORD] Error: {e}")
            time.sleep(10)


if __name__ == "__main__":
    run()
