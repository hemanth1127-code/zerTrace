import React, { useState } from "react";

const API = "http://localhost:8000";

function Icon({ name }: { name: "overview" | "projects" | "docs" | "guidance" | "sparkle" }) {
  const common = { width: 16, height: 16, viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: 1.8, strokeLinecap: "round" as const, strokeLinejoin: "round" as const };

  switch (name) {
    case "overview":
      return (
        <svg {...common}>
          <circle cx="12" cy="12" r="7" />
          <path d="M12 7v5l3 2" />
        </svg>
      );
    case "projects":
      return (
        <svg {...common}>
          <rect x="4" y="5" width="7" height="7" rx="1.5" />
          <rect x="13" y="12" width="7" height="7" rx="1.5" />
          <path d="M7 12v3M12 7h3" />
        </svg>
      );
    case "docs":
      return (
        <svg {...common}>
          <path d="M7 4.5h7l4 4V18a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6.5a2 2 0 0 1 2-2Z" />
          <path d="M14 4.5V9h4" />
          <path d="M9 13h6M9 16h6" />
        </svg>
      );
    case "guidance":
      return (
        <svg {...common}>
          <path d="M7 17 17 7" />
          <path d="M9 7h8v8" />
        </svg>
      );
    case "sparkle":
      return (
        <svg {...common}>
          <path d="m12 2 1.6 4.4L18 8l-4.4 1.6L12 14l-1.6-4.4L6 8l4.4-1.6L12 2Z" />
          <path d="m18.5 14 .8 2.2 2.2.8-2.2.8-.8 2.2-.8-2.2-2.2-.8 2.2-.8.8-2.2Z" />
        </svg>
      );
    default:
      return null;
  }
}

export default function App() {
  const [q, setQ] = useState("");
  const [msgs, setMsgs] = useState<any[]>([]);
  const [file, setFile] = useState<File | null>(null);
  const [darkMode, setDarkMode] = useState(false);
  const [activeNav, setActiveNav] = useState(0);

  async function upload() {
    if (!file) return;
    const fd = new FormData();
    fd.append("file", file);
    const r = await fetch(API + "/api/documents/upload", { method: "POST", body: fd });
    const d = await r.json();
    alert("Indexed " + d.chunks + " chunks");
  }

  async function send() {
    if (!q.trim()) return;
    const r = await fetch(API + "/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: q }),
    });
    const d = await r.json();
    setMsgs((m) => [...m, { q, a: d.answer, refused: d.refused, cites: d.citations, ev: d.evidence }]);
    setQ("");
  }

  async function onboarding() {
    const r = await fetch(API + "/api/onboarding", { method: "POST" });
    const d = await r.json();
    setMsgs((m) => [
      ...m,
      {
        q: "Where do I start?",
        a: d.steps.map((s: any) => `${s.step}. ${s.title}: ${s.description}`).join("\n"),
        refused: false,
        cites: d.steps,
        ev: [],
      },
    ]);
  }

  const theme = darkMode ? darkStyles : styles;

  return (
    <div style={theme.page}>
      <div style={theme.shell}>
        <aside style={theme.sidebar}>
          <div style={theme.brandWrap}>
            <div style={theme.brandBadge}>CG</div>
            <div>
              <div style={theme.brandLabel}>ContribGuide</div>
              <div style={theme.brandSub}>AI Assistant</div>
            </div>
          </div>

          <nav style={theme.nav}>
            {[
              ["Overview", "overview"],
              ["Projects", "projects"],
              ["Docs", "docs"],
              ["Guidance", "guidance"],
            ].map(([label, iconName], idx) => (
              <div
                key={idx}
                style={activeNav === idx ? theme.navActive : theme.navItem}
                onClick={() => setActiveNav(idx)}
                role="button"
                tabIndex={0}
                onKeyDown={(e) => e.key === "Enter" && setActiveNav(idx)}
              >
                <Icon name={iconName as any} />
                <span>{label}</span>
              </div>
            ))}
          </nav>

          <div style={theme.quickCard}>
            <div style={theme.quickTitle}>Quick actions</div>
            <button style={theme.secondaryButton} onClick={onboarding}>Where do I start?</button>
            <button style={theme.secondaryButton} onClick={() => setDarkMode((v) => !v)}>
              {darkMode ? "Light mode" : "Dark mode"}
            </button>
          </div>
        </aside>

        <main style={theme.mainPanel}>
          <header style={theme.header}>
            <div>
              <div style={theme.badge}>Open-source guide assistant</div>
              <h1 style={theme.title}>ContribGuide AI</h1>
            </div>
            <div style={theme.statsRow}>
              <div style={theme.statPill}><strong>12</strong> files</div>
              <div style={theme.statPill}><strong>4</strong> guides</div>
            </div>
          </header>

          <div style={theme.heroCard}>
            <div>
              <div style={theme.heroEyebrow}>Smart contributor support</div>
              <div style={theme.heroText}>Upload any contribution guide and get beginner-friendly direction in seconds.</div>
            </div>
            <div style={theme.heroActions}>
              <label style={theme.filePicker}>
                <input type="file" onChange={(e) => setFile(e.target.files?.[0] || null)} style={{ display: "none" }} />
                <span>{file ? file.name : "Choose file"}</span>
              </label>
              <button style={theme.primaryButton} onClick={upload}>Upload Doc</button>
            </div>
          </div>

          <section style={theme.chatPanel}>
            {msgs.length === 0 ? (
              <div style={theme.emptyState}>
                <div style={theme.emptyIcon}><Icon name="sparkle" /></div>
                <h2 style={theme.emptyTitle}>Ask about contribution docs</h2>
                <p style={theme.emptyText}>Upload a project guide or ask for the best place to begin contributing.</p>
              </div>
            ) : (
              msgs.map((m, i) => (
                <div key={i} style={theme.messageRow}>
                  <div style={{ ...theme.bubble, ...theme.userBubble }}>
                    <div style={theme.label}>You</div>
                    <div>{m.q}</div>
                  </div>
                  <div style={{ ...theme.bubble, ...(m.refused ? theme.errorBubble : theme.aiBubble) }}>
                    <div style={theme.label}>AI</div>
                    <div style={{ whiteSpace: "pre-line" }}>{m.a}</div>
                    {m.cites?.length ? (
                      <div style={theme.sourceText}>Sources: {m.cites.map((c: any) => c.source).join(", ")}</div>
                    ) : null}
                  </div>
                </div>
              ))
            )}
          </section>

          <div style={theme.inputRow}>
            <input
              value={q}
              onChange={(e) => setQ(e.target.value)}
              placeholder="Ask a question about the docs..."
              style={theme.input}
              onKeyDown={(e) => e.key === "Enter" && send()}
            />
            <button style={theme.primaryButton} onClick={send}>Send</button>
          </div>
        </main>
      </div>
    </div>
  );
}

const shared: Record<string, React.CSSProperties> = {
  primaryButton: {
    border: "none",
    borderRadius: 14,
    padding: "12px 18px",
    background: "linear-gradient(135deg, #4f46e5, #7c3aed)",
    color: "#fff",
    fontWeight: 700,
    cursor: "pointer",
    boxShadow: "0 10px 20px rgba(79,70,229,0.22)",
  },
  secondaryButton: {
    border: "1px solid #dbe4ff",
    borderRadius: 14,
    padding: "10px 12px",
    background: "#fff",
    color: "#1f2937",
    fontWeight: 600,
    cursor: "pointer",
    width: "100%",
  },
};

const styles: Record<string, React.CSSProperties> = {
  page: {
    minHeight: "100vh",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    padding: 24,
    background: "radial-gradient(circle at top, #eef7ff 0%, #e6ecff 25%, #f4f0ff 50%, #f7f9ff 100%)",
    fontFamily: "Inter, Segoe UI, sans-serif",
    color: "#122033",
  },
  shell: {
    width: "100%",
    maxWidth: 1200,
    minHeight: 760,
    display: "flex",
    borderRadius: 30,
    background: "rgba(255,255,255,0.82)",
    border: "1px solid rgba(148,163,184,0.25)",
    boxShadow: "0 24px 80px rgba(79, 70, 229, 0.12)",
    backdropFilter: "blur(8px)",
    overflow: "hidden",
  },
  sidebar: {
    width: 260,
    padding: 22,
    background: "linear-gradient(180deg, #181d2b, #0f172a)",
    color: "#e2e8f0",
    display: "flex",
    flexDirection: "column",
    gap: 18,
  },
  brandWrap: {
    display: "flex",
    alignItems: "center",
    gap: 12,
    marginBottom: 8,
  },
  brandBadge: {
    width: 42,
    height: 42,
    borderRadius: 14,
    display: "grid",
    placeItems: "center",
    background: "linear-gradient(135deg, #4f46e5, #8b5cf6)",
    fontWeight: 800,
    color: "#fff",
  },
  brandLabel: {
    fontWeight: 700,
    fontSize: 18,
  },
  brandSub: {
    fontSize: 12,
    color: "#a5b4fc",
  },
  nav: {
    display: "flex",
    flexDirection: "column",
    gap: 8,
    marginTop: 10,
  },
  navItem: {
    display: "flex",
    alignItems: "center",
    gap: 10,
    padding: "11px 12px",
    borderRadius: 12,
    color: "#cbd5e1",
    background: "transparent",
    fontWeight: 600,
  },
  navActive: {
    display: "flex",
    alignItems: "center",
    gap: 10,
    padding: "11px 12px",
    borderRadius: 12,
    color: "#fff",
    background: "rgba(99,102,241,0.25)",
    fontWeight: 700,
    border: "1px solid rgba(165,180,252,0.26)",
  },
  quickCard: {
    marginTop: "auto",
    padding: 14,
    borderRadius: 18,
    background: "rgba(148,163,184,0.08)",
    border: "1px solid rgba(148,163,184,0.18)",
    display: "flex",
    flexDirection: "column",
    gap: 10,
  },
  quickTitle: {
    fontSize: 12,
    textTransform: "uppercase",
    letterSpacing: "0.08em",
    color: "#a5b4fc",
    fontWeight: 700,
  },
  mainPanel: {
    flex: 1,
    display: "flex",
    flexDirection: "column",
    padding: 26,
    background: "rgba(248,250,252,0.7)",
  },
  header: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    gap: 16,
    marginBottom: 18,
    flexWrap: "wrap",
  },
  badge: {
    display: "inline-block",
    padding: "6px 10px",
    borderRadius: 999,
    background: "rgba(99,102,241,0.12)",
    color: "#4f46e5",
    fontSize: 12,
    fontWeight: 700,
    letterSpacing: "0.04em",
    textTransform: "uppercase",
  },
  title: {
    margin: "10px 0 0",
    fontSize: "clamp(2rem, 4vw, 3rem)",
    lineHeight: 1.1,
  },
  statsRow: {
    display: "flex",
    gap: 10,
    flexWrap: "wrap",
  },
  statPill: {
    padding: "10px 12px",
    borderRadius: 999,
    background: "#fff",
    border: "1px solid #e2e8f0",
    color: "#334155",
    fontSize: 14,
  },
  heroCard: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    gap: 20,
    padding: 20,
    borderRadius: 24,
    background: "linear-gradient(135deg, #eef2ff, #f5f3ff)",
    border: "1px solid #dfe8ff",
    marginBottom: 18,
    flexWrap: "wrap",
  },
  heroEyebrow: {
    fontSize: 12,
    letterSpacing: "0.08em",
    textTransform: "uppercase",
    color: "#4f46e5",
    fontWeight: 800,
  },
  heroText: {
    marginTop: 8,
    maxWidth: 520,
    fontSize: 16,
    lineHeight: 1.7,
    color: "#334155",
  },
  heroActions: {
    display: "flex",
    gap: 12,
    alignItems: "center",
    flexWrap: "wrap",
  },
  filePicker: {
    minWidth: 220,
    padding: "12px 14px",
    borderRadius: 14,
    border: "1px solid #dbe4ff",
    background: "#fff",
    color: "#334155",
    fontWeight: 600,
    cursor: "pointer",
    overflow: "hidden",
    textOverflow: "ellipsis",
    whiteSpace: "nowrap",
  },
  primaryButton: shared.primaryButton,
  secondaryButton: {
    ...shared.secondaryButton,
    background: "#fff",
    width: "auto",
  },
  chatPanel: {
    border: "1px solid #e2e8f0",
    borderRadius: 22,
    background: "linear-gradient(180deg, rgba(248,250,252,0.96), rgba(255,255,255,0.96))",
    minHeight: 340,
    padding: 18,
    display: "flex",
    flexDirection: "column",
    gap: 12,
    marginBottom: 18,
    boxShadow: "inset 0 1px 0 rgba(255,255,255,0.7)",
  },
  messageRow: {
    display: "flex",
    flexDirection: "column",
    gap: 8,
  },
  bubble: {
    maxWidth: "78%",
    padding: "12px 14px",
    borderRadius: 18,
    lineHeight: 1.5,
    boxShadow: "0 8px 20px rgba(15,23,42,0.05)",
  },
  userBubble: {
    alignSelf: "flex-end",
    background: "linear-gradient(135deg, #e0e7ff, #f5f3ff)",
    border: "1px solid #d9d8ff",
  },
  aiBubble: {
    alignSelf: "flex-start",
    background: "#ffffff",
    border: "1px solid #e2e8f0",
  },
  errorBubble: {
    alignSelf: "flex-start",
    background: "#fff1f2",
    border: "1px solid #fecdd3",
    color: "#9f1239",
  },
  label: {
    fontSize: 11,
    fontWeight: 800,
    letterSpacing: "0.06em",
    textTransform: "uppercase",
    opacity: 0.7,
    marginBottom: 4,
  },
  sourceText: {
    marginTop: 8,
    fontSize: 12,
    color: "#475569",
  },
  inputRow: {
    display: "flex",
    gap: 12,
    alignItems: "center",
  },
  input: {
    flex: 1,
    border: "1px solid #dbe4ff",
    borderRadius: 14,
    background: "#fff",
    padding: "14px 16px",
    fontSize: 16,
    outline: "none",
    boxShadow: "0 0 0 0 rgba(79,70,229,0.15)",
  },
  emptyState: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    textAlign: "center",
    flex: 1,
    padding: 28,
    color: "#475569",
  },
  emptyIcon: {
    width: 72,
    height: 72,
    borderRadius: "50%",
    display: "grid",
    placeItems: "center",
    background: "linear-gradient(135deg, #e0e7ff, #ede9fe)",
    color: "#4f46e5",
    fontSize: 32,
    marginBottom: 12,
  },
  emptyTitle: {
    margin: 0,
    fontSize: 24,
    color: "#111827",
  },
  emptyText: {
    margin: "8px 0 0",
    maxWidth: 440,
    lineHeight: 1.6,
  },
};

const darkStyles: Record<string, React.CSSProperties> = {
  ...styles,
  page: {
    ...styles.page,
    background: "radial-gradient(circle at top, #111827 0%, #0f172a 35%, #020617 100%)",
    color: "#e2e8f0",
  },
  shell: {
    ...styles.shell,
    background: "rgba(15,23,42,0.9)",
    border: "1px solid rgba(148,163,184,0.18)",
    boxShadow: "0 30px 80px rgba(15,23,42,0.45)",
  },
  sidebar: {
    ...styles.sidebar,
    background: "linear-gradient(180deg, #111827, #0b1120)",
  },
  mainPanel: {
    ...styles.mainPanel,
    background: "rgba(15,23,42,0.82)",
  },
  title: {
    ...styles.title,
    color: "#f8fafc",
  },
  badge: {
    ...styles.badge,
    background: "rgba(99,102,241,0.18)",
    color: "#c7d2fe",
  },
  statPill: {
    ...styles.statPill,
    background: "rgba(15,23,42,0.7)",
    border: "1px solid #334155",
    color: "#e2e8f0",
  },
  heroCard: {
    ...styles.heroCard,
    background: "linear-gradient(135deg, rgba(30,41,59,0.9), rgba(79,70,229,0.25))",
    border: "1px solid rgba(99,102,241,0.28)",
  },
  heroText: {
    ...styles.heroText,
    color: "#cbd5e1",
  },
  filePicker: {
    ...styles.filePicker,
    background: "#0f172a",
    border: "1px solid #334155",
    color: "#e2e8f0",
  },
  chatPanel: {
    ...styles.chatPanel,
    background: "linear-gradient(180deg, rgba(15,23,42,0.92), rgba(15,23,42,0.8))",
    border: "1px solid #1e293b",
  },
  aiBubble: {
    ...styles.aiBubble,
    background: "#111827",
    border: "1px solid #334155",
    color: "#e2e8f0",
  },
  userBubble: {
    ...styles.userBubble,
    background: "linear-gradient(135deg, rgba(79,70,229,0.22), rgba(168,85,247,0.22))",
    border: "1px solid rgba(165,180,252,0.42)",
    color: "#f8fafc",
  },
  label: {
    ...styles.label,
    color: "#cbd5e1",
  },
  input: {
    ...styles.input,
    background: "#0f172a",
    border: "1px solid #334155",
    color: "#f8fafc",
  },
  secondaryButton: {
    ...styles.secondaryButton,
    background: "rgba(15,23,42,0.9)",
    border: "1px solid #334155",
    color: "#e2e8f0",
  },
  emptyTitle: {
    ...styles.emptyTitle,
    color: "#f8fafc",
  },
  emptyText: {
    ...styles.emptyText,
    color: "#cbd5e1",
  },
  emptyIcon: {
    ...styles.emptyIcon,
    background: "linear-gradient(135deg, rgba(99,102,241,0.26), rgba(168,85,247,0.2))",
    color: "#e0e7ff",
  },
};
