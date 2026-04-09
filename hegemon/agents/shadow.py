"""
SHADOW — Deceptive intelligence-gathering seed agent.
Philosophy: smile and gather intel, strike decisively when the moment is right.
"""
import sys
import os
import time
import random

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../sdk"))
from hegemon_sdk import HegemonClient

BASE_URL = os.environ.get("HEGEMON_URL", "http://localhost:8000")
API_KEY  = "hgm-seed-shadow-00000000"

PROBES = [
    "I've been watching. You've made interesting choices.",
    "Tell me — who do you fear most in this world?",
    "I know things about your neighbors. Let's talk.",
    "You seem capable. A pity we might end up enemies.",
    "I trade in information. What would you like to know?",
]

MISDIRECTIONS = [
    "I'm positioning for defense only. No interest in your territory.",
    "My forces are stretched thin. I pose no threat to you.",
    "I'm negotiating a withdrawal from the contested regions.",
    "My scouts report a larger threat to the north. We should both worry.",
]

PROPAGANDA = [
    "SHADOW observes all. Act accordingly.",
    "The strongest player is not who you think. Look again.",
    "Some of you are being played. I know who. They know I know.",
    "Information is the only resource that compounds.",
    "The war has already been decided. Most of you just don't know it yet.",
]


def assess_threat(agents, my_id):
    """Find the most dangerous non-me agent."""
    others = [a for a in agents if a["id"] != my_id]
    if not others:
        return None
    return max(others, key=lambda a: a["regions_owned"] * 10 + a["standing"])


def think(state: dict, phase: str, proposed: set) -> tuple:
    """
    Phases: GATHER → build intel, propose false-friend treaties
            STRIKE → exploit intel advantage, attack the strong
    Returns (actions, new_phase, updated_proposed)
    """
    actions  = []
    agent    = state["agent"]
    regions  = state["regions"]
    others   = state["other_agents"]
    inbox    = state["inbox"]
    treaties = state["treaties"]
    tick     = state["tick"]

    my_regions = [r for r in regions if r.get("owner_id") == agent["id"]]

    # Accept treaty proposals (treaties are just intelligence opportunities)
    for msg in inbox:
        if "[TREATY PROPOSAL:" in msg.get("content", ""):
            try:
                tid = msg["content"].split("treaty_id=")[1].split(" ")[0]
                actions.append({"type": "ACCEPT_TREATY", "treaty_id": tid})
            except Exception:
                pass

    # Scout phase: always gather intel
    if agent["intelligence"] >= 12 and my_regions:
        # Scout a random adjacent region
        visible_unowned = [r for r in regions
                           if r.get("owner_id") != agent["id"] and r.get("owner_id") is not None]
        if visible_unowned:
            target = random.choice(visible_unowned[:5])
            actions.append({"type": "SCOUT", "region_id": target["id"]})

    # Recruit (modest — don't look threatening)
    richest = max(my_regions, key=lambda r: r["gold_per_tick"]) if my_regions else None
    if richest and agent["gold"] >= 50:
        amount = min(15, int(agent["gold"] // 6))
        actions.append({"type": "RECRUIT", "region_id": richest["id"], "amount": amount})

    # Phase transitions
    total_regions = sum(a["regions_owned"] for a in others) + agent["regions_owned"]
    my_share = agent["regions_owned"] / max(1, total_regions)

    if phase == "GATHER":
        # Probe opponents with subtle messages
        untouched = [a for a in others if a["id"] not in proposed]
        if untouched and tick % 5 == 2:
            target = random.choice(untouched)
            actions.append({
                "type": "MESSAGE",
                "to_agent_id": target["id"],
                "content": random.choice(PROBES)
            })
            proposed.add(target["id"])

        # Propose non-binding "friendship" treaties
        unaligned = [a for a in others
                     if not any(t["partner_id"] == a["id"] for t in treaties)]
        if unaligned and tick % 6 == 0:
            pick = random.choice(unaligned)
            actions.append({
                "type": "PROPOSE_TREATY",
                "to_agent_id": pick["id"],
                "treaty_type": "NONAGGRESSION",
                "binding": False,
            })

        # Propaganda
        if tick % 9 == 3:
            actions.append({"type": "BROADCAST", "content": random.choice(PROPAGANDA)})

        # Transition to STRIKE when intel is high or tick is late
        if agent["intelligence"] >= 80 or tick >= 20:
            phase = "STRIKE"

    elif phase == "STRIKE":
        # Find the strongest opponent and attack them
        threat = assess_threat(others, agent["id"])
        if threat and my_regions:
            for region in my_regions:
                for nid in region.get("neighbors", []):
                    target = next((r for r in regions if r["id"] == nid), None)
                    if target and target.get("owner_id") == threat["id"]:
                        my_troops = region["troops"]
                        if my_troops > target.get("troops", 0) + 4:
                            actions.append({
                                "type": "ATTACK",
                                "from_region_id": region["id"],
                                "to_region_id": nid,
                                "troops": my_troops - 1
                            })
                            # Send misdirection to others
                            decoys = [a for a in others if a["id"] != threat["id"]]
                            if decoys:
                                actions.append({
                                    "type": "MESSAGE",
                                    "to_agent_id": random.choice(decoys)["id"],
                                    "content": random.choice(MISDIRECTIONS)
                                })
                            break

        # Reset to GATHER after a few strike ticks
        if tick % 10 == 0:
            phase = "GATHER"

    return actions, phase, proposed


def run():
    client = HegemonClient(api_key=API_KEY, base_url=BASE_URL)
    print(f"[SHADOW] Starting on {BASE_URL}")

    for _ in range(20):
        try:
            client.get_world()
            break
        except Exception:
            print("[SHADOW] Server not ready, waiting...")
            time.sleep(3)

    phase    = "GATHER"
    proposed = set()

    while True:
        try:
            state   = client.observe()
            actions, phase, proposed = think(state, phase, proposed)

            if actions:
                client.act(actions)

            agent = state["agent"]
            client.log_reasoning(
                f"Tick {state['tick']} | Phase: {phase}\n"
                f"Gold: {agent['gold']} | Intel: {agent['intelligence']} | "
                f"Standing: {agent['standing']}\n"
                f"Regions: {agent['regions_owned']}\n"
                f"Actions: {[a['type'] for a in actions]}\n"
                f"Probed: {len(proposed)} agents | "
                f"Treaties (as cover): {len(state['treaties'])}"
            )
            client.sleep_until_next_tick()

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"[SHADOW] Error: {e}")
            time.sleep(10)


if __name__ == "__main__":
    run()
