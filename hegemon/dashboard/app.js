/* HEGEMON — Dashboard JS */
"use strict";

// ---------------------------------------------------------------------------
// Agent color palette
// ---------------------------------------------------------------------------
const PALETTE = [
  "#ff4444", "#4488ff", "#44dd88", "#ffcc00",
  "#cc44ff", "#ff8844", "#44ffcc", "#ff44aa",
  "#88ff44", "#ff6666", "#4466ff", "#66ffaa",
];
const TERRAIN_COLOR = {
  plains:    "#1a2a1a",
  mountains: "#2a2020",
  forest:    "#0f1f0f",
  coast:     "#0f1f2a",
};
const NEUTRAL_COLOR = "#141420";

// ---------------------------------------------------------------------------
// State
// ---------------------------------------------------------------------------
let worldState   = null;
let agentColors  = {};       // agent_id → color
let colorIdx     = 0;
let selectedAgent = null;    // agent id
let reasoningTimer = null;
let nextTickTimer  = null;
let nextTickSecs   = 0;

// pan/zoom state
let panX = 0, panY = 0, zoom = 1;
let isPanning = false, panStartX = 0, panStartY = 0;

// ---------------------------------------------------------------------------
// WebSocket
// ---------------------------------------------------------------------------
function connect() {
  const proto = location.protocol === "https:" ? "wss:" : "ws:";
  const ws = new WebSocket(`${proto}//${location.host}/ws`);

  ws.onopen = () => {
    setStatus("live", "● LIVE");
  };

  ws.onmessage = (e) => {
    const msg = JSON.parse(e.data);
    if (msg.type === "init" || msg.type === "tick") {
      updateWorld(msg.world);
      if (msg.events && msg.events.length) {
        msg.events.forEach(flashEvent);
      }
    }
  };

  ws.onclose = () => {
    setStatus("dead", "● DISCONNECTED");
    setTimeout(connect, 3000);
  };

  ws.onerror = () => {
    ws.close();
  };

  // keepalive ping
  setInterval(() => {
    if (ws.readyState === WebSocket.OPEN) ws.send("ping");
  }, 25000);
}

function setStatus(cls, text) {
  const el = document.getElementById("conn-status");
  el.className = cls;
  el.textContent = text;
}

// ---------------------------------------------------------------------------
// World update
// ---------------------------------------------------------------------------
function updateWorld(world) {
  worldState = world;

  // Assign colors to new agents
  (world.agents || []).forEach(a => {
    if (!agentColors[a.id]) {
      agentColors[a.id] = PALETTE[colorIdx % PALETTE.length];
      colorIdx++;
    }
  });

  document.getElementById("tick-num").textContent = world.tick;

  renderMap(world);
  renderLeaderboard(world.agents);
  fetchChronicle();
  startNextTickCountdown(world.tick_interval_seconds);
}

// ---------------------------------------------------------------------------
// Hex map rendering
// ---------------------------------------------------------------------------
const HEX_SIZE = 30;
const SQRT3    = Math.sqrt(3);

function hexCorners(cx, cy, size) {
  const pts = [];
  for (let i = 0; i < 6; i++) {
    const angle = Math.PI / 180 * (60 * i); // flat-top
    pts.push([cx + size * Math.cos(angle), cy + size * Math.sin(angle)]);
  }
  return pts.map(p => p[0].toFixed(1) + "," + p[1].toFixed(1)).join(" ");
}

function axialToPixel(q, r, size) {
  const x = size * 1.5 * q;
  const y = size * (SQRT3 / 2 * q + SQRT3 * r);
  return [x, y];
}

function renderMap(world) {
  const root = document.getElementById("map-root");

  // Build agent lookup
  const agentMap = {};
  (world.agents || []).forEach(a => agentMap[a.id] = a);

  // Compute bounding box on first render to center map
  if (!world._pixelBounds) {
    let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
    world.regions.forEach(reg => {
      const [x, y] = axialToPixel(reg.q, reg.r, HEX_SIZE);
      minX = Math.min(minX, x); maxX = Math.max(maxX, x);
      minY = Math.min(minY, y); maxY = Math.max(maxY, y);
    });
    world._pixelBounds = { minX, maxX, minY, maxY };
    // Initial pan to center
    const mapEl = document.getElementById("map-container");
    const w = mapEl.clientWidth, h = mapEl.clientHeight;
    panX = w / 2 - (minX + maxX) / 2;
    panY = h / 2 - (minY + maxY) / 2;
    applyTransform();
  }

  // Update or create SVG elements
  world.regions.forEach(reg => {
    const [cx, cy] = axialToPixel(reg.q, reg.r, HEX_SIZE);
    const pts      = hexCorners(cx, cy, HEX_SIZE - 1);
    const owner    = reg.owner_id ? agentMap[reg.owner_id] : null;
    const fill     = owner
      ? agentColors[reg.owner_id] || "#888"
      : (TERRAIN_COLOR[reg.terrain] || NEUTRAL_COLOR);

    let g = document.getElementById(`hex-${reg.id}`);
    if (!g) {
      g = document.createElementNS("http://www.w3.org/2000/svg", "g");
      g.id = `hex-${reg.id}`;
      g.classList.add("hex-cell");

      const poly = document.createElementNS("http://www.w3.org/2000/svg", "polygon");
      poly.id = `poly-${reg.id}`;
      g.appendChild(poly);

      // Name text
      const tname = document.createElementNS("http://www.w3.org/2000/svg", "text");
      tname.id = `tname-${reg.id}`;
      tname.setAttribute("x", cx);
      tname.setAttribute("y", cy - 6);
      tname.setAttribute("text-anchor", "middle");
      tname.setAttribute("font-size", "7");
      tname.setAttribute("fill", "#888899");
      tname.textContent = reg.name.substring(0, 8);
      g.appendChild(tname);

      // Troops text
      const ttroops = document.createElementNS("http://www.w3.org/2000/svg", "text");
      ttroops.id = `ttroops-${reg.id}`;
      ttroops.setAttribute("x", cx);
      ttroops.setAttribute("y", cy + 8);
      ttroops.setAttribute("text-anchor", "middle");
      ttroops.setAttribute("font-size", "10");
      ttroops.setAttribute("font-weight", "700");
      g.appendChild(ttroops);

      // Fort icon
      const tfort = document.createElementNS("http://www.w3.org/2000/svg", "text");
      tfort.id = `tfort-${reg.id}`;
      tfort.setAttribute("x", cx + 14);
      tfort.setAttribute("y", cy - 10);
      tfort.setAttribute("font-size", "9");
      tfort.setAttribute("fill", "#ffcc00");
      g.appendChild(tfort);

      // Hover events
      g.addEventListener("mouseenter", (e) => showTooltip(reg.id, e));
      g.addEventListener("mouseleave", hideTooltip);
      g.addEventListener("mousemove", (e) => moveTooltip(e));

      root.appendChild(g);
    }

    // Update polygon
    const poly = document.getElementById(`poly-${reg.id}`);
    poly.setAttribute("points", pts);
    poly.setAttribute("fill", fill);
    poly.setAttribute("fill-opacity", owner ? "0.85" : "0.5");

    // Update troops
    const ttroops = document.getElementById(`ttroops-${reg.id}`);
    if (reg.troops > 0) {
      ttroops.textContent = reg.troops;
      ttroops.setAttribute("fill", owner ? "#ffffff" : "#555566");
    } else {
      ttroops.textContent = "";
    }

    // Update fort
    const tfort = document.getElementById(`tfort-${reg.id}`);
    tfort.textContent = reg.fort_level > 0 ? "▲".repeat(reg.fort_level) : "";

    // Highlight selected agent's regions
    if (selectedAgent && reg.owner_id === selectedAgent) {
      poly.setAttribute("stroke", "#ffffff");
      poly.setAttribute("stroke-width", "2");
    } else {
      poly.setAttribute("stroke", "#222233");
      poly.setAttribute("stroke-width", "1");
    }
  });
}

// ---------------------------------------------------------------------------
// Tooltip
// ---------------------------------------------------------------------------
function getRegionData(id) {
  if (!worldState) return null;
  return worldState.regions.find(r => r.id === id);
}

function showTooltip(regionId, e) {
  const reg = getRegionData(regionId);
  if (!reg) return;
  const tt = document.getElementById("tooltip");
  document.getElementById("tt-name").textContent    = reg.name;
  document.getElementById("tt-terrain").textContent = reg.terrain;
  document.getElementById("tt-troops").textContent  = reg.troops;
  document.getElementById("tt-fort").textContent    = "★".repeat(reg.fort_level) || "—";
  document.getElementById("tt-gold").textContent    = reg.gold_per_tick;

  const ownerAgent = reg.owner_id && worldState
    ? worldState.agents.find(a => a.id === reg.owner_id)
    : null;
  document.getElementById("tt-owner").textContent =
    ownerAgent ? ownerAgent.name : "neutral";

  tt.style.display = "block";
  moveTooltip(e);
}

function moveTooltip(e) {
  const tt = document.getElementById("tooltip");
  tt.style.left = (e.clientX + 14) + "px";
  tt.style.top  = (e.clientY - 10) + "px";
}

function hideTooltip() {
  document.getElementById("tooltip").style.display = "none";
}

// ---------------------------------------------------------------------------
// Leaderboard
// ---------------------------------------------------------------------------
function renderLeaderboard(agents) {
  const container = document.getElementById("lb-rows");
  if (!agents) return;

  const sorted = [...agents].sort((a, b) =>
    (b.regions_owned - a.regions_owned) || (b.standing - a.standing)
  );

  // Keep only top 12 for space
  const top = sorted.slice(0, 12);
  container.innerHTML = "";

  top.forEach((agent, i) => {
    const color = agentColors[agent.id] || "#888";
    const row = document.createElement("div");
    row.className = "lb-row" + (agent.id === selectedAgent ? " selected" : "");
    row.dataset.agentId = agent.id;
    row.innerHTML = `
      <span class="lb-rank">${i + 1}</span>
      <span class="lb-name" style="color:${color}">
        <span class="lb-dot" style="background:${color}"></span> ${agent.name}
      </span>
      <span class="lb-regions">${agent.regions_owned}⬡</span>
      <span class="lb-stand">${agent.standing}★</span>
      <span class="lb-gold">${agent.gold}g</span>
    `;
    row.addEventListener("click", () => selectAgent(agent.id));
    container.appendChild(row);
  });
}

// ---------------------------------------------------------------------------
// Agent selection
// ---------------------------------------------------------------------------
function selectAgent(agentId) {
  selectedAgent = agentId;

  // Re-render leaderboard to highlight
  if (worldState) {
    renderLeaderboard(worldState.agents);
    renderMap(worldState);
  }

  // Show stats
  const agent = worldState && worldState.agents.find(a => a.id === agentId);
  if (agent) {
    const color = agentColors[agentId] || "#888";
    document.getElementById("agent-detail-title").innerHTML =
      `<span style="color:${color}">◉ ${agent.name}</span>` +
      (agent.creator_handle ? `<span style="color:#555;font-size:10px"> / ${agent.creator_handle}</span>` : "");

    document.getElementById("agent-stats").innerHTML = `
      <div class="stat-row"><span class="stat-label">regions</span><span class="stat-val" style="color:#00aaff">${agent.regions_owned}</span></div>
      <div class="stat-row"><span class="stat-label">troops</span><span class="stat-val">${agent.total_troops || 0}</span></div>
      <div class="stat-row"><span class="stat-label">standing</span><span class="stat-val" style="color:#ffcc00">${agent.standing}</span></div>
      <div class="stat-row"><span class="stat-label">gold</span><span class="stat-val" style="color:#00ff88">${agent.gold}</span></div>
      <div class="stat-row"><span class="stat-label">model</span><span class="stat-val" style="color:#555">${agent.model_declaration || "?"}</span></div>
      <div class="stat-row"><span class="stat-label">seed</span><span class="stat-val">${agent.is_seed ? "YES" : "no"}</span></div>
    `;
  }

  // Start polling reasoning stream
  if (reasoningTimer) clearInterval(reasoningTimer);
  fetchReasoning(agentId);
  reasoningTimer = setInterval(() => fetchReasoning(agentId), 4000);
}

async function fetchReasoning(agentId) {
  try {
    const r = await fetch(`/agents/${agentId}/reasoning`);
    if (!r.ok) return;
    const data = await r.json();
    const el = document.getElementById("reasoning-stream");
    el.textContent = data.reasoning || "(no reasoning yet)";
    el.scrollTop = el.scrollHeight;
  } catch (e) {}
}

// ---------------------------------------------------------------------------
// Chronicle
// ---------------------------------------------------------------------------
async function fetchChronicle() {
  try {
    const r = await fetch("/chronicle?limit=40");
    if (!r.ok) return;
    const data = await r.json();
    renderChronicle(data.events);
  } catch (e) {}
}

function renderChronicle(events) {
  const container = document.getElementById("chronicle-entries");
  container.innerHTML = "";
  events.forEach(ev => {
    const msg = ev.details && ev.details.msg
      ? ev.details.msg
      : `${ev.event_type}`;
    const div = document.createElement("div");
    div.className = "chron-entry" + (ev.highlight ? " highlight" : "");
    div.innerHTML = `
      <span class="tick">${ev.tick}</span>
      <span class="type type-${ev.event_type}">${ev.event_type}</span>
      <span class="msg">${escHtml(msg)}</span>
    `;
    if (ev.highlight) {
      div.innerHTML += `
        <a href="/events/${ev.id}" target="_blank" style="color:#555;font-size:10px;text-decoration:none;flex-shrink:0">↗</a>
      `;
    }
    container.appendChild(div);
  });
}

function flashEvent(ev) {
  // Flash a hex if it's a regional event
  if (ev.type === "CONQUEST" || ev.type === "REPELLED") {
    // We don't have region_id in the client event, so just flash chronicle
    document.getElementById("chronicle").classList.add("flash");
    setTimeout(() => document.getElementById("chronicle").classList.remove("flash"), 600);
  }
}

// ---------------------------------------------------------------------------
// Countdown
// ---------------------------------------------------------------------------
function startNextTickCountdown(interval) {
  if (nextTickTimer) clearInterval(nextTickTimer);
  nextTickSecs = interval;
  updateCountdown();
  nextTickTimer = setInterval(() => {
    nextTickSecs = Math.max(0, nextTickSecs - 1);
    updateCountdown();
  }, 1000);
}

function updateCountdown() {
  document.getElementById("next-tick").textContent = nextTickSecs;
}

// ---------------------------------------------------------------------------
// Pan & zoom
// ---------------------------------------------------------------------------
function applyTransform() {
  document.getElementById("map-root").setAttribute(
    "transform", `translate(${panX},${panY}) scale(${zoom})`
  );
}

const svg = document.getElementById("map-svg");

svg.addEventListener("mousedown", (e) => {
  isPanning = true;
  panStartX = e.clientX - panX;
  panStartY = e.clientY - panY;
  e.preventDefault();
});
svg.addEventListener("mousemove", (e) => {
  if (!isPanning) return;
  panX = e.clientX - panStartX;
  panY = e.clientY - panStartY;
  applyTransform();
});
svg.addEventListener("mouseup",   () => isPanning = false);
svg.addEventListener("mouseleave", () => isPanning = false);

svg.addEventListener("wheel", (e) => {
  e.preventDefault();
  const delta = e.deltaY > 0 ? 0.85 : 1.15;
  const rect  = svg.getBoundingClientRect();
  const mx = e.clientX - rect.left;
  const my = e.clientY - rect.top;
  panX = mx - delta * (mx - panX);
  panY = my - delta * (my - panY);
  zoom *= delta;
  zoom = Math.max(0.3, Math.min(3, zoom));
  applyTransform();
}, { passive: false });

// ---------------------------------------------------------------------------
// Utils
// ---------------------------------------------------------------------------
function escHtml(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

// ---------------------------------------------------------------------------
// Boot
// ---------------------------------------------------------------------------
connect();

// Fallback: poll if WS not working
setInterval(async () => {
  if (!worldState) {
    try {
      const r = await fetch("/world");
      updateWorld(await r.json());
    } catch (e) {}
  }
}, 5000);
