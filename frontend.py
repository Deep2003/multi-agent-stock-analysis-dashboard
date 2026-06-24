HTML_FRONTEND_CONTENT = """<!DOCTYPE html>
<html class="dark" lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>StockGraph AI | Institutional Analysis</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600;700;800&display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>
<!-- React & Babel CDNs -->
<script src="https://unpkg.com/react@18/umd/react.production.min.js" crossorigin></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js" crossorigin></script>
<script src="https://unpkg.com/@babel/standalone@7.15.0/babel.min.js"></script>
<!-- Marked.js -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/marked/4.3.0/marked.min.js"></script>
<!-- html2pdf.js -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
<script id="tailwind-config">
  tailwind.config = {
    darkMode: "class",
    theme: {
      extend: {
        colors: {
          "on-primary": "#283330",
          "outline": "#8d9290",
          "secondary-fixed": "#ffe088",
          "surface-container-low": "#181c1c",
          "on-surface": "#e0e3e2",
          "primary-container": "#040d0b",
          "outline-variant": "#434846",
          "background": "#101414",
          "surface-dim": "#101414",
          "tertiary": "#69dbad",
          "surface-container-high": "#272b2a",
          "on-background": "#e0e3e2",
          "surface-container": "#1c2020",
          "tertiary-fixed": "#86f8c8",
          "surface-container-highest": "#313635",
          "on-secondary": "#3c2f00",
          "primary": "#bdc9c5",
          "surface": "#101414",
          "inverse-surface": "#e0e3e2",
          "tertiary-container": "#000e07",
          "secondary-fixed-dim": "#e9c349",
          "surface-bright": "#363a3a",
          "error-container": "#93000a",
          "surface-container-lowest": "#0b0f0f",
          "on-surface-variant": "#c3c8c5",
          "surface-variant": "#313635",
          "on-secondary-fixed": "#241a00",
          "error": "#ffb4ab",
          "secondary": "#e9c349"
        },
        spacing: {
          "container-max": "1280px",
          "gutter": "24px",
          "margin-desktop": "64px",
          "margin-mobile": "20px",
        },
        fontFamily: {
          sans: ["Hanken Grotesk", "sans-serif"],
        },
        fontSize: {
          "body-md": ["16px", { lineHeight: "24px", fontWeight: "400" }],
          "label-md": ["14px", { lineHeight: "20px", letterSpacing: "0.05em", fontWeight: "600" }],
          "display-lg": ["48px", { lineHeight: "56px", letterSpacing: "-0.02em", fontWeight: "700" }],
          "body-lg": ["18px", { lineHeight: "28px", fontWeight: "400" }],
          "display-lg-mobile": ["32px", { lineHeight: "40px", letterSpacing: "-0.02em", fontWeight: "700" }],
          "label-sm": ["12px", { lineHeight: "16px", letterSpacing: "0.02em", fontWeight: "500" }],
          "headline-md": ["32px", { lineHeight: "40px", letterSpacing: "-0.01em", fontWeight: "600" }],
          "headline-sm": ["24px", { lineHeight: "32px", fontWeight: "600" }]
        }
      },
    },
  }
</script>
<style>
  body {
    font-family: 'Hanken Grotesk', sans-serif;
    background-color: #101414;
    color: #e0e3e2;
    -webkit-font-smoothing: antialiased;
  }
  .material-symbols-outlined {
    font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
    line-height: 1;
    font-size: 20px;
  }
  .material-symbols-filled {
    font-variation-settings: 'FILL' 1, 'wght' 400, 'GRAD' 0, 'opsz' 24;
  }
  .glass-panel {
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.4);
  }
  .glass-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(233, 195, 73, 0.15);
  }
  .glow-gold { border-top: 1px solid rgba(233, 195, 73, 0.15); }
  .gold-glow { box-shadow: 0 0 15px rgba(233, 195, 73, 0.2); }
  .emerald-gradient {
    background: linear-gradient(180deg, rgba(105, 219, 173, 0.05) 0%, rgba(16, 20, 20, 0) 100%);
  }
  .grid-pattern {
    background-image: radial-gradient(circle, rgba(233, 195, 73, 0.04) 1px, transparent 1px);
    background-size: 32px 32px;
  }
  /* Scrollbar */
  ::-webkit-scrollbar { width: 4px; height: 4px; }
  ::-webkit-scrollbar-track { background: transparent; }
  ::-webkit-scrollbar-thumb { background: #434846; border-radius: 10px; }
  .scrollbar-hide::-webkit-scrollbar { display: none; }
  .scrollbar-hide { -ms-overflow-style: none; scrollbar-width: none; }
  /* Glass card hover lift */
  .glass-panel, .glass-card {
    transition: transform 0.3s cubic-bezier(0.2, 0, 0, 1), box-shadow 0.3s ease;
  }
  .glass-panel:hover, .glass-card:hover {
    transform: translateY(-2px);
  }
  /* Prose overrides */
  .prose h1, .prose h2, .prose h3 { color: #e0e3e2; font-weight: 700; }
  .prose h1 { font-size: 1.1rem; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 0.5rem; margin-bottom: 1rem; }
  .prose h2 { font-size: 0.95rem; margin-top: 1.4rem; color: #c3c8c5; }
  .prose h3 { font-size: 0.875rem; color: #8d9290; }
  .prose p { color: #c3c8c5; line-height: 1.7; font-size: 0.875rem; }
  .prose ul { color: #c3c8c5; }
  .prose li { margin-bottom: 0.25rem; font-size: 0.875rem; }
  .prose strong { color: #e0e3e2; font-weight: 600; }
  .prose code { color: #69dbad; background: rgba(105,219,173,0.08); padding: 0.1em 0.4em; border-radius: 4px; font-size: 0.8em; }
  .prose hr { border-color: rgba(255,255,255,0.08); }
  .prose blockquote { border-left-color: #e9c349; color: #8d9290; font-style: italic; }
  /* Animate-in slide */
  @keyframes slideIn {
    from { opacity: 0; transform: translateY(6px); }
    to { opacity: 1; transform: translateY(0); }
  }
  .animate-slide-in { animation: slideIn 0.4s ease forwards; }
  input, select {
    background-color: rgba(255,255,255,0.04) !important;
  }
  select option { background-color: #1c2020; color: #e0e3e2; }
</style>
</head>
<body class="min-h-screen flex flex-col grid-pattern">
<div id="root"></div>

<script type="text/babel">
  const { useState, useEffect, useRef, useCallback } = React;

  // ─── Helpers ──────────────────────────────────────────────────────────────

  function Icon({ name, className = "", filled = false }) {
    return (
      <span
        className={`material-symbols-outlined ${filled ? "material-symbols-filled" : ""} ${className}`}
        aria-hidden="true"
      >{name}</span>
    );
  }

  function renderMarkdown(text) {
    if (!text || typeof text !== "string") return '<p class="text-outline italic text-sm">Report pending...</p>';
    try {
      if (window.marked && typeof window.marked.parse === "function") return window.marked.parse(text);
      if (typeof window.marked === "function") return window.marked(text);
      return `<p class="whitespace-pre-wrap">${text}</p>`;
    } catch (e) {
      return `<p class="whitespace-pre-wrap">${text}</p>`;
    }
  }

  const MODEL_NAMES = {
    "auto": "Auto-Fallback",
    "meta-llama/llama-3.3-70b-instruct:free": "LLaMA 3.3 70B",
    "google/gemma-4-31b-it:free": "Gemma 4 31B",
    "qwen/qwen3-next-80b-a3b-instruct:free": "Qwen3 Next 80B",
    "google/gemma-4-26b-a4b-it:free": "Gemma 4 26B",
    "qwen/qwen3-coder:free": "Qwen3 Coder",
    "openai/gpt-oss-120b:free": "GPT-OSS 120B",
    "nousresearch/hermes-3-llama-3.1-405b:free": "Hermes 3 405B",
    "cognitivecomputations/dolphin-mistral-24b-venice-edition:free": "Dolphin Mistral 24B",
    "nvidia/nemotron-3-nano-30b-a3b:free": "Nemotron 3 30B",
    "openrouter/free": "OpenRouter Free Router",
  };

  const AGENT_STATE_COLOR = {
    idle:     { badge: "text-outline border-outline-variant bg-white/5",       dot: "bg-outline" },
    thinking: { badge: "text-tertiary border-tertiary/50 bg-tertiary/10",      dot: "bg-tertiary animate-pulse" },
    complete: { badge: "text-secondary border-secondary/50 bg-secondary/10",   dot: "bg-secondary" },
  };

  const AGENT_ICONS = {
    supervisor:   "shield",
    prefetch:     "cloud_download",
    financial:    "bar_chart",
    tech_product: "memory",
    sentiment:    "chat",
    macro:        "public",
    technical:    "candlestick_chart",
    risk:         "warning",
    synthesis:    "verified",
  };

  const EXPERT_ACCENT = {
    financial:    { text: "text-secondary",    border: "border-secondary/30",    bg: "bg-secondary/5"  },
    tech_product: { text: "text-tertiary",     border: "border-tertiary/30",     bg: "bg-tertiary/5"   },
    sentiment:    { text: "text-[#c084fc]",    border: "border-purple-500/30",   bg: "bg-purple-500/5" },
    macro:        { text: "text-secondary-fixed-dim", border: "border-amber-400/30", bg: "bg-amber-400/5" },
    risk:         { text: "text-error",        border: "border-error/30",        bg: "bg-error/5"      },
    logs:         { text: "text-on-surface-variant", border: "border-outline-variant", bg: "bg-white/3" },
  };

  // ─── Reusable Components ──────────────────────────────────────────────────

  function AgentRow({ title, desc, status, icon, compact = false }) {
    const s = AGENT_STATE_COLOR[status] || AGENT_STATE_COLOR.idle;
    const statusLabel = status === "thinking" ? "WORKING" : status === "complete" ? "DONE" : "IDLE";
    if (compact) {
      return (
        <div className={`flex items-center justify-between p-3 rounded-lg border ${status === "thinking" ? "border-tertiary/30 bg-tertiary/5" : "border-secondary/20 bg-white/5"} transition-all duration-500`}>
          <div className="flex items-center gap-3">
            <Icon name={icon || AGENT_ICONS[title.toLowerCase()] || "smart_toy"} className={status === "thinking" ? "text-tertiary text-[18px]" : "text-secondary text-[18px]"} />
            <span className="font-label-md text-label-md text-on-surface">{title}</span>
          </div>
          <span className={`font-label-sm text-label-sm flex items-center gap-1 ${status === "thinking" ? "text-tertiary animate-pulse" : status === "complete" ? "text-secondary" : "text-outline"}`}>
            <Icon name={status === "thinking" ? "sync" : status === "complete" ? "check" : "radio_button_unchecked"} className="text-[14px]" />
            {statusLabel}
          </span>
        </div>
      );
    }
    return (
      <div className={`flex items-center justify-between p-4 rounded-lg border ${status === "thinking" ? "border-tertiary/40 bg-tertiary/5" : "border-secondary/30 bg-white/5"} transition-all duration-500`}>
        <div className="flex items-center gap-4">
          <div className={`w-10 h-10 rounded-lg border flex items-center justify-center ${status === "thinking" ? "border-tertiary/50 text-tertiary" : "border-secondary/50 text-secondary"}`}>
            <Icon name={icon || AGENT_ICONS[title.toLowerCase().replace(" ","_")] || "smart_toy"} />
          </div>
          <div>
            <p className={`font-label-md text-label-md ${status === "thinking" ? "text-tertiary" : "text-secondary"}`}>{title}</p>
            <p className="font-label-sm text-label-sm text-outline">{desc}</p>
          </div>
        </div>
        <div className={`flex items-center gap-2 px-3 py-1 rounded-full border font-label-sm text-label-sm ${s.badge} ${status === "thinking" ? "animate-pulse" : ""}`}>
          <Icon name={status === "thinking" ? "sync" : status === "complete" ? "check" : "radio_button_unchecked"} className="text-[14px]" />
          {statusLabel}
        </div>
      </div>
    );
  }

  function MetricCard({ label, value, icon, accent = "secondary" }) {
    const colorMap = {
      secondary: "text-secondary",
      tertiary:  "text-tertiary",
      outline:   "text-outline",
    };
    return (
      <div className="glass-panel p-5 rounded-xl glow-gold flex flex-col gap-3">
        <div className="flex justify-between items-start">
          <span className="font-label-sm text-label-sm text-secondary uppercase tracking-wider">{label}</span>
          <Icon name={icon} className="text-outline text-[20px]" />
        </div>
        <div className={`font-headline-sm text-headline-sm ${colorMap[accent] || colorMap.secondary}`}>{value}</div>
      </div>
    );
  }

  function ExpertTabBtn({ id, label, active, onClick }) {
    const acc = EXPERT_ACCENT[id] || EXPERT_ACCENT.logs;
    const isActive = active === id;
    return (
      <button
        onClick={() => onClick(id)}
        className={`px-4 py-2 rounded-lg font-label-sm text-label-sm uppercase tracking-wider border transition-all duration-200 ${isActive ? `${acc.text} ${acc.border} ${acc.bg}` : "border-transparent text-outline hover:text-on-surface hover:bg-white/5"}`}
      >
        {label}
      </button>
    );
  }

  function TradingViewChart({ ticker }) {
    const ref = useRef(null);
    useEffect(() => {
      if (!ref.current || !ticker) return;
      ref.current.innerHTML = "";
      const s = document.createElement("script");
      s.src = "https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js";
      s.type = "text/javascript";
      s.async = true;
      s.innerHTML = JSON.stringify({
        autosize: true,
        symbol: ticker,
        interval: "D",
        timezone: "Etc/UTC",
        theme: "dark",
        style: "1",
        locale: "en",
        backgroundColor: "rgba(16,20,20,1)",
        gridColor: "rgba(255,255,255,0.05)",
        hide_top_toolbar: false,
        hide_legend: false,
        save_image: false,
        support_host: "https://www.tradingview.com",
      });
      ref.current.appendChild(s);
    }, [ticker]);
    return (
      <div className="tradingview-widget-container h-full w-full" ref={ref}>
        <div className="tradingview-widget-container__widget h-full w-full"></div>
      </div>
    );
  }

  // ─── Main App ──────────────────────────────────────────────────────────────
  function App() {
    const [activeTab, setActiveTab] = useState("setup");
    const [apiKey, setApiKey] = useState("");
    const [selectedModel, setSelectedModel] = useState("auto");
    const [averageRuntimes, setAverageRuntimes] = useState({});
    const [query, setQuery] = useState("");
    const [isAnalyzing, setIsAnalyzing] = useState(false);
    const [logs, setLogs] = useState([]);
    const [ticker, setTicker] = useState("");
    const [metrics, setMetrics] = useState({ price: "—", pe: "—", sma50: "—", sma200: "—", market_cap: "—" });
    const [report, setReport] = useState("");
    const [expertReports, setExpertReports] = useState({});
    const [streamingText, setStreamingText] = useState({});
    const [activeExpertTab, setActiveExpertTab] = useState("financial");
    const [agentExecutionLogs, setAgentExecutionLogs] = useState([]);
    const [newsArticles, setNewsArticles] = useState([]);
    const [elapsedTime, setElapsedTime] = useState(0);
    const [totalDuration, setTotalDuration] = useState(null);
    const timerRef = useRef(null);
    const startTimeRef = useRef(null);
    const logEndRef = useRef(null);
    const [agentStates, setAgentStates] = useState({
      supervisor: "idle", prefetch: "idle", financial: "idle",
      tech_product: "idle", sentiment: "idle", macro: "idle",
      technical: "idle", risk: "idle", synthesis: "idle",
    });

    useEffect(() => { return () => { if (timerRef.current) clearInterval(timerRef.current); }; }, []);
    useEffect(() => { logEndRef.current?.scrollIntoView({ behavior: "smooth" }); }, [logs]);

    // Fetch real runtimes on mount
    useEffect(() => {
      fetch("/api/runtimes")
        .then(r => r.json())
        .then(d => { if (d?.averages) setAverageRuntimes(d.averages); })
        .catch(() => {});
    }, []);

    const fetchAgentLogs = () => {
      fetch("/api/logs").then(r => r.json()).then(d => { if (Array.isArray(d)) setAgentExecutionLogs(d); }).catch(() => {});
    };

    const exportToPDF = () => {
      const el = document.getElementById("thesis-content");
      if (!el) return;
      window.html2pdf().set({
        margin: 0.5, filename: `${ticker || "report"}_thesis.pdf`,
        image: { type: "jpeg", quality: 0.98 }, html2canvas: { scale: 2 },
        jsPDF: { unit: "in", format: "letter", orientation: "portrait" },
      }).from(el).save();
    };

    const runAnalysis = () => {
      if (!query.trim()) return;
      setIsAnalyzing(true);
      setActiveTab("console");
      setLogs([{ type: "system", message: "Connecting to state machine..." }]);
      setTicker(""); setMetrics({ price: "—", pe: "—", sma50: "—", sma200: "—", market_cap: "—" });
      setReport(""); setExpertReports({}); setStreamingText({}); setAgentExecutionLogs([]); setNewsArticles([]);
      setElapsedTime(0); setTotalDuration(null);
      setAgentStates({ supervisor: "thinking", prefetch: "idle", financial: "idle", tech_product: "idle", sentiment: "idle", macro: "idle", technical: "idle", risk: "idle", synthesis: "idle" });

      startTimeRef.current = Date.now();
      if (timerRef.current) clearInterval(timerRef.current);
      timerRef.current = setInterval(() => setElapsedTime((Date.now() - startTimeRef.current) / 1000), 100);

      const url = `/api/stream?query=${encodeURIComponent(query)}&api_key=${encodeURIComponent(apiKey)}&model=${encodeURIComponent(selectedModel)}`;
      const es = new EventSource(url);

      es.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.event === "start") {
          setLogs(prev => [...prev, { type: "system", message: data.message }]);
          fetchAgentLogs();
        } else if (data.event === "token") {
          const { agent, text } = data;
          setStreamingText(prev => ({ ...prev, [agent]: (prev[agent] || "") + text }));
        } else if (data.event === "update") {
          const { agent, active_agent, message, ticker: t, metrics: m, expert_reports: rpts, news_articles: na } = data;
          setLogs(prev => [...prev, { type: agent, message }]);
          if (t && typeof t === "string") setTicker(t.toUpperCase());
          if (m && Object.keys(m).length) setMetrics(prev => ({ ...prev, ...m }));
          if (rpts && Object.keys(rpts).length) setExpertReports(prev => ({ ...prev, ...rpts }));
          if (na && na.length > 0) setNewsArticles(na);
          fetchAgentLogs();
          setAgentStates(prev => {
            const n = { ...prev };
            const rev = data.revision_count || 0;
            if (active_agent === "pre_fetch") { n.supervisor = "complete"; n.prefetch = "thinking"; }
            else if (active_agent === "financial" && rev === 0) {
              n.prefetch = "complete";
              ["financial","tech_product","sentiment","macro","technical"].forEach(k => n[k] = "thinking");
              n.risk = "idle";
            }
            if (agent === "financial" && rev === 0) n.financial = "complete";
            if (agent === "tech_product" && rev === 0) n.tech_product = "complete";
            if (agent === "sentiment" && rev === 0) n.sentiment = "complete";
            if (agent === "macro" && rev === 0) n.macro = "complete";
            if (agent === "technical" && rev === 0) n.technical = "complete";
            if (active_agent === "risk") {
              ["financial","tech_product","sentiment","macro","technical"].forEach(k => n[k] = "complete");
              n.risk = "thinking";
            }
            if (agent === "risk") n.risk = "complete";
            if (agent === "risk" && rev > 0 && active_agent) {
              active_agent.split(",").forEach(t2 => {
                if (["financial","tech_product","sentiment","macro","technical"].includes(t2)) n[t2] = "thinking";
              });
            }
            if (rev > 0 && ["financial","tech_product","sentiment","macro","technical"].includes(agent)) n[agent] = "complete";
            if (active_agent === "synthesis") {
              ["financial","tech_product","sentiment","macro","technical","risk"].forEach(k => n[k] = "complete");
              n.synthesis = "thinking";
            } else if (active_agent === "finish") {
              ["financial","tech_product","sentiment","macro","technical","risk","synthesis"].forEach(k => n[k] = "complete");
            }
            return n;
          });
          if (agent === "supervisor" && active_agent === "finish") setReport(message);
        } else if (data.event === "complete") {
          clearInterval(timerRef.current);
          setTotalDuration(((Date.now() - startTimeRef.current) / 1000).toFixed(2));
          setLogs(prev => [...prev, { type: "success", message: data.message }]);
          setIsAnalyzing(false); setActiveTab("summary"); fetchAgentLogs(); es.close();
        } else if (data.event === "error") {
          clearInterval(timerRef.current);
          setTotalDuration(((Date.now() - startTimeRef.current) / 1000).toFixed(2));
          setLogs(prev => [...prev, { type: "error", message: `Execution failed: ${data.message}` }]);
          setIsAnalyzing(false); fetchAgentLogs(); es.close();
        }
      };

      es.onerror = () => {
        clearInterval(timerRef.current);
        setTotalDuration(((Date.now() - startTimeRef.current) / 1000).toFixed(2));
        setLogs(prev => [...prev, { type: "error", message: "Stream connection lost." }]);
        setIsAnalyzing(false); es.close();
      };
    };

    const LOG_COLORS = {
      system: "border-outline", supervisor: "border-secondary", backend: "border-tertiary",
      financial: "border-secondary", tech_product: "border-tertiary",
      sentiment: "border-[#c084fc]", macro: "border-amber-400",
      risk: "border-error", success: "border-tertiary", error: "border-error", info: "border-outline",
    };
    const LOG_TEXT = {
      system: "text-outline", supervisor: "text-secondary", financial: "text-secondary",
      tech_product: "text-tertiary", sentiment: "text-[#c084fc]", macro: "text-amber-400",
      risk: "text-error", success: "text-tertiary", error: "text-error", info: "text-on-surface-variant",
    };

    const activeExpertData = expertReports[activeExpertTab];

    // ── Render ───────────────────────────────────────────────────────────────
    return (
      <div className="min-h-screen flex flex-col">
        {/* ── HEADER ── */}
        <header className="w-full sticky top-0 z-50 bg-background/80 backdrop-blur-xl border-b border-white/10">
          <div className="flex justify-between items-center h-16 px-margin-mobile md:px-margin-desktop max-w-container-max mx-auto">
            {/* Brand */}
            <div className="font-headline-sm text-headline-sm font-bold tracking-tight text-secondary">
              StockGraph AI
            </div>
            {/* Nav */}
            <nav className="hidden md:flex items-center gap-6">
              {[["setup","Setup"],["console","Agent Console"],["summary","Executive Summary"]].map(([id,label]) => (
                <button key={id} onClick={() => setActiveTab(id)}
                  className={`font-body-md text-body-md px-3 py-1 rounded transition-all ${activeTab === id ? "text-secondary border-b-2 border-secondary pb-0" : "text-on-surface-variant hover:text-primary hover:bg-white/5"}`}>
                  {label}
                </button>
              ))}
            </nav>
            {/* Status */}
            <div className="flex items-center gap-4 text-secondary">
              {isAnalyzing ? (
                <span className="flex items-center gap-2 font-label-sm text-label-sm text-tertiary">
                  <span className="w-2 h-2 rounded-full bg-tertiary animate-pulse"></span>
                  {elapsedTime.toFixed(1)}s
                </span>
              ) : totalDuration ? (
                <span className="flex items-center gap-2 font-label-sm text-label-sm text-tertiary">
                  <span className="w-2 h-2 rounded-full bg-tertiary"></span>
                  Done in {totalDuration}s
                </span>
              ) : (
                <span className="font-label-sm text-label-sm text-outline uppercase tracking-widest">READY</span>
              )}
              <span className="text-outline font-label-sm text-label-sm">|</span>
              <span className="font-label-sm text-label-sm text-secondary-fixed-dim">{MODEL_NAMES[selectedModel] || selectedModel}</span>
            </div>
          </div>
        </header>

        {/* ══════════════════════════════════════════════════════════════════════
            TAB 1: SETUP
        ══════════════════════════════════════════════════════════════════════ */}
        <main className={`flex-grow w-full max-w-container-max mx-auto px-margin-mobile md:px-margin-desktop py-12 ${activeTab === "setup" ? "block" : "hidden"}`}>
          {/* Hero */}
          <section className="mb-12">
            <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
              <div>
                <span className="font-label-sm text-label-sm uppercase tracking-widest text-secondary mb-2 block">Institutional Grade Analysis</span>
                <h1 className="font-display-lg-mobile md:font-display-lg text-display-lg-mobile md:text-display-lg">
                  AI Investment <span className="text-secondary">Committee</span>
                </h1>
                <div className="w-32 h-1 bg-secondary mt-4 shadow-[0_0_15px_rgba(233,195,73,0.3)]"></div>
                <p className="mt-4 text-on-surface-variant font-body-md text-body-md max-w-xl">
                  A multi-agent LangGraph pipeline with 5 domain experts, a Risk Auditor, and a Synthesis Compiler — delivering institutional-grade equity analysis.
                </p>
              </div>
            </div>
          </section>

          {/* Feature Cards + Form */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-gutter items-start">
            {/* Form */}
            <div className="lg:col-span-5 flex flex-col gap-4">
              <div className="glass-card p-8 rounded-xl flex flex-col gap-6">
                <h2 className="font-headline-sm text-headline-sm text-secondary flex items-center gap-2">
                  <Icon name="settings" /> Configuration
                </h2>

                {/* Ticker */}
                <div className="flex flex-col gap-2">
                  <label className="font-label-sm text-label-sm text-secondary uppercase tracking-widest">Stock Ticker / Query</label>
                  <input
                    type="text" value={query} onChange={e => setQuery(e.target.value)}
                    onKeyDown={e => e.key === "Enter" && runAnalysis()}
                    disabled={isAnalyzing} placeholder="e.g., AAPL, NVDA, TSLA"
                    className="w-full border border-outline-variant focus:border-secondary/60 focus:ring-1 focus:ring-secondary/20 rounded-lg px-4 py-3 font-body-md text-body-md text-on-surface placeholder-outline disabled:opacity-40 transition-all outline-none"
                  />
                </div>

                {/* API Key */}
                <div className="flex flex-col gap-2">
                  <div className="flex justify-between items-center">
                    <label className="font-label-sm text-label-sm text-secondary uppercase tracking-widest">OpenRouter API Key</label>
                    <span className="font-label-sm text-label-sm text-outline">Optional — falls back to ENV</span>
                  </div>
                  <input
                    type="password" value={apiKey} onChange={e => setApiKey(e.target.value)}
                    disabled={isAnalyzing} placeholder="sk-or-v1-..."
                    className="w-full border border-outline-variant focus:border-secondary/60 focus:ring-1 focus:ring-secondary/20 rounded-lg px-4 py-3 font-body-md text-body-md text-on-surface placeholder-outline disabled:opacity-40 transition-all outline-none font-mono"
                  />
                </div>

                {/* Model */}
                <div className="flex flex-col gap-2">
                  <div className="flex justify-between items-center">
                    <label className="font-label-sm text-label-sm text-secondary uppercase tracking-widest">Model Selection</label>
                    <span className="font-label-sm text-label-sm text-outline">Free Tier</span>
                  </div>
                  <select
                    value={selectedModel} onChange={e => setSelectedModel(e.target.value)}
                    disabled={isAnalyzing}
                    className="w-full border border-outline-variant focus:border-secondary/60 rounded-lg px-4 py-3 font-body-md text-body-md text-on-surface disabled:opacity-40 transition-all outline-none cursor-pointer"
                  >
                    <option value="auto">Auto-Fallback {averageRuntimes["auto"] ? `· Avg ${averageRuntimes["auto"]}s` : ""}</option>
                    <option value="meta-llama/llama-3.3-70b-instruct:free">LLaMA 3.3 70B {averageRuntimes["meta-llama/llama-3.3-70b-instruct:free"] ? `· Avg ${averageRuntimes["meta-llama/llama-3.3-70b-instruct:free"]}s` : ""}</option>
                    <option value="google/gemma-4-31b-it:free">Gemma 4 31B {averageRuntimes["google/gemma-4-31b-it:free"] ? `· Avg ${averageRuntimes["google/gemma-4-31b-it:free"]}s` : ""}</option>
                    <option value="qwen/qwen3-next-80b-a3b-instruct:free">Qwen3 Next 80B {averageRuntimes["qwen/qwen3-next-80b-a3b-instruct:free"] ? `· Avg ${averageRuntimes["qwen/qwen3-next-80b-a3b-instruct:free"]}s` : ""}</option>
                    <option value="google/gemma-4-26b-a4b-it:free">Gemma 4 26B {averageRuntimes["google/gemma-4-26b-a4b-it:free"] ? `· Avg ${averageRuntimes["google/gemma-4-26b-a4b-it:free"]}s` : ""}</option>
                    <option value="qwen/qwen3-coder:free">Qwen3 Coder {averageRuntimes["qwen/qwen3-coder:free"] ? `· Avg ${averageRuntimes["qwen/qwen3-coder:free"]}s` : ""}</option>
                    <option value="openai/gpt-oss-120b:free">GPT-OSS 120B {averageRuntimes["openai/gpt-oss-120b:free"] ? `· Avg ${averageRuntimes["openai/gpt-oss-120b:free"]}s` : ""}</option>
                    <option value="nousresearch/hermes-3-llama-3.1-405b:free">Hermes 3 405B {averageRuntimes["nousresearch/hermes-3-llama-3.1-405b:free"] ? `· Avg ${averageRuntimes["nousresearch/hermes-3-llama-3.1-405b:free"]}s` : ""}</option>
                    <option value="cognitivecomputations/dolphin-mistral-24b-venice-edition:free">Dolphin Mistral 24B {averageRuntimes["cognitivecomputations/dolphin-mistral-24b-venice-edition:free"] ? `· Avg ${averageRuntimes["cognitivecomputations/dolphin-mistral-24b-venice-edition:free"]}s` : ""}</option>
                    <option value="nvidia/nemotron-3-nano-30b-a3b:free">Nemotron 3 30B {averageRuntimes["nvidia/nemotron-3-nano-30b-a3b:free"] ? `· Avg ${averageRuntimes["nvidia/nemotron-3-nano-30b-a3b:free"]}s` : ""}</option>
                    <option value="openrouter/free">OpenRouter Free Router {averageRuntimes["openrouter/free"] ? `· Avg ${averageRuntimes["openrouter/free"]}s` : ""}</option>
                  </select>
                </div>

                {/* Run Button */}
                <button
                  onClick={runAnalysis} disabled={isAnalyzing || !query.trim()}
                  className="w-full bg-secondary text-on-primary py-3.5 rounded-xl font-label-md text-label-md flex items-center justify-center gap-2.5 transition-all active:scale-[0.98] disabled:opacity-40 disabled:cursor-not-allowed hover:brightness-110 shadow-lg shadow-secondary/20"
                >
                  {isAnalyzing ? (
                    <><div className="w-4 h-4 border-2 border-on-primary/40 border-t-on-primary rounded-full animate-spin"></div><span>Running Analysis...</span></>
                  ) : (
                    <><Icon name="play_arrow" /><span>RUN ANALYSIS</span></>
                  )}
                </button>
              </div>
            </div>

            {/* Feature Cards */}
            <div className="lg:col-span-7 grid grid-cols-1 md:grid-cols-2 gap-gutter">
              {[
                { icon: "bar_chart",    title: "Financial Expert",    desc: "DCF valuation, earnings quality, balance sheet forensics, P/E multiples.",        accent: "secondary" },
                { icon: "memory",       title: "Tech Moat Expert",    desc: "Competitive positioning, product roadmap & R&D pipeline analysis.",     accent: "tertiary" },
                { icon: "chat",         title: "Sentiment Expert",    desc: "News NLP, analyst consensus divergence, social media sentiment aggregation.",       accent: "secondary" },
                { icon: "public",       title: "Macro Expert",        desc: "Interest rate cycles, sector rotation, geopolitical risk, Treasury yields.",        accent: "tertiary" },
                { icon: "candlestick_chart", title: "Technical Expert",  desc: "RSI, MACD, Bollinger Bands, support/resistance, chart pattern recognition.",   accent: "secondary" },
                { icon: "warning",      title: "Risk Auditor",        desc: "Peer-review loop — cross-examines all expert reports for logical inconsistencies.", accent: "tertiary" },
              ].map(({ icon, title, desc, accent }) => (
                <div key={title} className={`glass-panel p-5 rounded-xl glow-gold flex flex-col gap-3`}>
                  <div className="flex justify-between items-start">
                    <Icon name={icon} className={`text-[24px] ${accent === "tertiary" ? "text-tertiary" : "text-secondary"}`} />
                  </div>
                  <div>
                    <p className={`font-label-md text-label-md uppercase tracking-wider ${accent === "tertiary" ? "text-tertiary" : "text-secondary"}`}>{title}</p>
                    <p className="font-body-md text-body-md text-on-surface-variant mt-1">{desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </main>

        {/* ══════════════════════════════════════════════════════════════════════
            TAB 2: AGENT CONSOLE
        ══════════════════════════════════════════════════════════════════════ */}
        <main className={`flex-grow w-full max-w-container-max mx-auto px-margin-mobile md:px-margin-desktop py-8 flex flex-col gap-8 ${activeTab === "console" ? "flex" : "hidden"}`}>
          {/* Pipeline Tracker */}
          <section className="glass-panel rounded-xl p-6 relative overflow-hidden">
            <div className="absolute inset-0 emerald-gradient opacity-50 pointer-events-none"></div>
            <div className="relative z-10">
              <div className="flex justify-between items-center mb-8">
                <h2 className="font-headline-sm text-headline-sm text-secondary flex items-center gap-2">
                  <Icon name="account_tree" /> Committee Handoff Pipeline
                </h2>
                <span className="font-label-sm text-label-sm px-3 py-1 bg-secondary/10 text-secondary border border-secondary/20 rounded-full uppercase tracking-widest">
                  {isAnalyzing ? "LIVE" : "COMPLETE"}
                </span>
              </div>
              <div className="flex flex-col gap-4">
                <AgentRow title="Supervisor" desc="Orchestrates committee, extracts ticker" status={agentStates.supervisor} icon="shield" />
                <AgentRow title="Data Fetcher" desc="Parallel pre-fetch: financials, news, macro" status={agentStates.prefetch} icon="cloud_download" />
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <AgentRow title="Financial" desc="" status={agentStates.financial} icon="bar_chart" compact />
                  <AgentRow title="Tech Moat" desc="" status={agentStates.tech_product} icon="memory" compact />
                  <AgentRow title="Sentiment" desc="" status={agentStates.sentiment} icon="chat" compact />
                  <AgentRow title="Macro" desc="" status={agentStates.macro} icon="public" compact />
                  <AgentRow title="Technical" desc="" status={agentStates.technical} icon="candlestick_chart" compact />
                </div>
                <AgentRow title="Risk Auditor" desc="Cross-examines all expert reports" status={agentStates.risk} icon="warning" />
                <AgentRow title="Synthesis Compiler" desc="Generates final investment thesis" status={agentStates.synthesis} icon="verified" />
              </div>
            </div>
          </section>

          {/* Log Stream + Sidebar */}
          <div className="grid grid-cols-12 gap-gutter flex-grow">
            {/* Live Activity Stream */}
            <div className="col-span-12 lg:col-span-8 flex flex-col gap-6">
              <div className="glass-panel rounded-xl flex-grow flex flex-col overflow-hidden">
                <div className="p-5 border-b border-white/5 flex justify-between items-center">
                  <h3 className="font-headline-sm text-headline-sm text-secondary" style={{fontSize:"20px"}}>Live Activity Stream</h3>
                  <div className="flex items-center gap-2">
                    <span className="w-2.5 h-2.5 rounded-full bg-tertiary animate-pulse"></span>
                    <span className="font-label-sm text-label-sm text-tertiary">{logs.length} events</span>
                  </div>
                </div>
                <div className="p-5 flex-grow overflow-y-auto space-y-3 max-h-[500px] scrollbar-hide">
                  {logs.length === 0 ? (
                    <p className="text-outline font-body-md italic">Waiting for analysis trigger...</p>
                  ) : logs.map((log, idx) => (
                    <div key={idx} className={`flex items-start gap-4 p-4 rounded-lg bg-white/5 border-l-4 ${LOG_COLORS[log.type] || "border-outline"} hover:bg-white/10 transition-colors animate-slide-in`}>
                      <div className="flex-grow">
                        <div className="flex justify-between">
                          <span className={`font-label-md text-label-md ${LOG_TEXT[log.type] || "text-on-surface-variant"}`}>
                            [{(log.type || "sys").toUpperCase()}]
                          </span>
                          <span className="font-label-sm text-label-sm text-outline">{new Date().toLocaleTimeString()}</span>
                        </div>
                        <p className="font-body-md text-body-md mt-1 text-on-surface">{log.message}</p>
                      </div>
                    </div>
                  ))}
                  <div ref={logEndRef} />
                </div>
              </div>
            </div>

            {/* Sidebar */}
            <aside className="col-span-12 lg:col-span-4 flex flex-col gap-6">
              {/* Agent Progress */}
              <div className="glass-panel rounded-xl p-6">
                <h3 className="font-label-md text-label-md uppercase tracking-wider text-outline mb-6">Agent Progress</h3>
                <div className="space-y-5">
                  {[
                    ["Supervisor",  agentStates.supervisor],
                    ["Data Fetch",  agentStates.prefetch],
                    ["Specialists", Object.values({f:agentStates.financial,t:agentStates.tech_product,s:agentStates.sentiment,m:agentStates.macro,tc:agentStates.technical}).filter(v=>v==="complete").length === 5 ? "complete" : Object.values({f:agentStates.financial,t:agentStates.tech_product,s:agentStates.sentiment,m:agentStates.macro,tc:agentStates.technical}).some(v=>v==="thinking") ? "thinking" : "idle"],
                    ["Risk Audit",  agentStates.risk],
                    ["Synthesis",   agentStates.synthesis],
                  ].map(([name, st]) => {
                    const pct = st === "complete" ? 100 : st === "thinking" ? 60 : 0;
                    return (
                      <div key={name} className="space-y-2">
                        <div className="flex justify-between">
                          <span className="font-body-md text-body-md text-on-surface">{name}</span>
                          <span className="font-label-sm text-label-sm text-secondary">{pct}%</span>
                        </div>
                        <div className="w-full h-1.5 bg-white/10 rounded-full overflow-hidden">
                          <div
                            className={`h-full rounded-full transition-all duration-700 ${st === "complete" ? "bg-secondary gold-glow" : st === "thinking" ? "bg-tertiary animate-pulse" : "bg-white/10"}`}
                            style={{ width: `${pct}%` }}
                          ></div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Metrics Preview (once available) */}
              {ticker && (
                <div className="glass-panel rounded-xl p-6">
                  <h3 className="font-label-md text-label-md uppercase tracking-wider text-outline mb-4">{ticker} Metrics</h3>
                  <div className="space-y-3">
                    {[
                      ["Price", metrics.price !== "—" ? `$${metrics.price}` : "—", "trending_up"],
                      ["P/E Ratio", metrics.pe, "analytics"],
                      ["50-Day SMA", metrics.sma50 !== "—" ? `$${metrics.sma50}` : "—", "show_chart"],
                      ["200-Day SMA", metrics.sma200 !== "—" ? `$${metrics.sma200}` : "—", "show_chart"],
                    ].map(([label, val, icon]) => (
                      <div key={label} className="flex items-center justify-between p-3 rounded-lg bg-white/5 hover:bg-white/10 transition-all border border-white/5">
                        <span className="font-body-md text-body-md text-on-surface">{label}</span>
                        <span className="font-label-md text-label-md text-secondary">{val}</span>
                      </div>
                    ))}
                  </div>
                  <button onClick={() => setActiveTab("summary")} className="w-full mt-4 py-2.5 border border-secondary/30 text-secondary rounded-lg font-label-md text-label-md hover:bg-secondary/5 transition-all active:scale-[0.98]">
                    VIEW FULL REPORT
                  </button>
                </div>
              )}
            </aside>
          </div>
        </main>

        {/* ══════════════════════════════════════════════════════════════════════
            TAB 3: EXECUTIVE SUMMARY
        ══════════════════════════════════════════════════════════════════════ */}
        <main className={`flex-grow w-full max-w-container-max mx-auto px-margin-mobile md:px-margin-desktop py-12 ${activeTab === "summary" ? "block" : "hidden"}`}>
          {/* Hero */}
          <section className="mb-12 relative">
            <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
              <div>
                <span className="font-label-sm text-label-sm uppercase tracking-widest text-secondary mb-2 block">Institutional Grade Report</span>
                <h1 className="font-display-lg-mobile md:font-display-lg text-display-lg-mobile md:text-display-lg">
                  Executive Summary: <span className="text-secondary">{ticker || "—"}</span>
                </h1>
                <div className="w-32 h-1 bg-secondary mt-4 shadow-[0_0_15px_rgba(233,195,73,0.3)]"></div>
              </div>
              <div className="flex gap-3">
                <button onClick={exportToPDF} className="bg-secondary text-on-primary px-6 py-2 font-label-md text-label-md rounded-lg active:scale-95 transition-all hover:brightness-110">
                  GENERATE PDF
                </button>
                <button onClick={() => setActiveTab("console")} className="border border-outline-variant text-on-surface px-6 py-2 font-label-md text-label-md rounded-lg hover:bg-white/5 transition-all">
                  AGENT CONSOLE
                </button>
              </div>
            </div>
          </section>

          {/* Metrics Grid - 5 cards in a row */}
          <section className="grid grid-cols-2 md:grid-cols-5 gap-gutter mb-12">
            <MetricCard label="Market Price" value={metrics.price !== "—" ? `$${metrics.price}` : "—"} icon="trending_up" accent="secondary" />
            <MetricCard label="P/E Ratio" value={metrics.pe || "—"} icon="analytics" accent="secondary" />
            <MetricCard label="Market Cap" value={metrics.market_cap || "—"} icon="account_balance" accent="secondary" />
            <MetricCard label="50-Day SMA" value={metrics.sma50 !== "—" ? `$${metrics.sma50}` : "—"} icon="show_chart" accent="tertiary" />
            <MetricCard label="200-Day SMA" value={metrics.sma200 !== "—" ? `$${metrics.sma200}` : "—"} icon="show_chart" accent="tertiary" />
          </section>

          {/* Main Content */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-gutter items-start">
            {/* Left: Thesis + Chart + Committee Drill-Down */}
            <div className="lg:col-span-8 flex flex-col gap-8">
              {/* Investment Thesis */}
              <div className="glass-panel p-8 rounded-xl relative overflow-hidden" id="thesis-content">
                <div className="absolute top-0 right-0 p-8 opacity-5">
                  <Icon name="account_balance" className="text-[120px] text-on-surface" />
                </div>
                <h2 className="font-headline-sm text-headline-sm text-secondary mb-6 flex items-center gap-2" style={{fontSize:"20px"}}>
                  <Icon name="menu_book" /> Investment Thesis
                </h2>
                <div
                  className="font-body-lg text-body-lg text-on-surface leading-relaxed prose prose-invert max-w-none"
                  dangerouslySetInnerHTML={{ __html: renderMarkdown(report || streamingText.supervisor || "") }}
                />
                {!report && !streamingText.supervisor && (
                  <p className="text-outline italic font-body-md">Analysis pending. Run a query to generate the investment thesis.</p>
                )}
              </div>

              {/* Committee Drill-Down comes before chart */}
              <div className="glass-panel p-8 rounded-xl">
                <h2 className="font-headline-sm text-headline-sm text-secondary mb-2 flex items-center gap-2" style={{fontSize:"20px"}}>
                  <Icon name="groups" /> Committee Expert Drill-Down
                </h2>
                <p className="font-label-sm text-label-sm text-outline mb-6">Structured reports from each institutional expert on the committee</p>

                {/* Tabs */}
                <div className="flex flex-wrap gap-2 mb-6 border-b border-white/5 pb-4">
                  <ExpertTabBtn id="financial"   label="Financials"      active={activeExpertTab} onClick={setActiveExpertTab} />
                  <ExpertTabBtn id="tech_product" label="Tech Moat"       active={activeExpertTab} onClick={setActiveExpertTab} />
                  <ExpertTabBtn id="sentiment"    label="Sentiment"       active={activeExpertTab} onClick={setActiveExpertTab} />
                  <ExpertTabBtn id="macro"        label="Macro"           active={activeExpertTab} onClick={setActiveExpertTab} />
                  <ExpertTabBtn id="risk"         label="Risk Mgmt"       active={activeExpertTab} onClick={setActiveExpertTab} />
                  <ExpertTabBtn id="logs"         label="Audit Ledger"    active={activeExpertTab} onClick={setActiveExpertTab} />
                </div>

                {/* Tab Content */}
                {activeExpertTab === "logs" ? (
                  <div className="flex flex-col gap-4">
                    <div className="flex justify-between items-center mb-2">
                      <h4 className="font-label-md text-label-md text-secondary uppercase tracking-widest flex items-center gap-2">
                        <Icon name="terminal" /> Real-Time Expert Audit Ledger
                      </h4>
                      <span className="font-label-sm text-label-sm text-outline">Traces: {agentExecutionLogs.length}</span>
                    </div>
                    {agentExecutionLogs.length === 0 ? (
                      <p className="text-outline italic font-body-md">No traces yet.</p>
                    ) : (
                      <div className="flex flex-col gap-4 max-h-[600px] overflow-y-auto scrollbar-hide">
                        {agentExecutionLogs.map((log, idx) => (
                          <div key={idx} className="glass-card rounded-xl p-5 flex flex-col gap-3">
                            <div className="flex flex-wrap items-center justify-between gap-2 border-b border-white/5 pb-3">
                              <div className="flex items-center gap-2">
                                <span className="font-label-sm text-label-sm text-outline font-mono">[{idx+1}]</span>
                                <span className="font-label-md text-label-md text-secondary uppercase">{log.agent?.replace("_"," ")}</span>
                              </div>
                              <span className="font-label-sm text-label-sm text-outline">{new Date(log.timestamp).toLocaleTimeString()}</span>
                            </div>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                              <div>
                                <p className="font-label-sm text-label-sm text-tertiary uppercase tracking-widest mb-2">System Instruction</p>
                                <pre className="bg-surface-container-lowest rounded-lg p-3 font-label-sm text-label-sm text-on-surface-variant overflow-auto max-h-32 scrollbar-hide whitespace-pre-wrap border border-white/5">{log.inputs?.system_prompt}</pre>
                              </div>
                              <div>
                                <p className="font-label-sm text-label-sm text-secondary uppercase tracking-widest mb-2">Output (JSON)</p>
                                <pre className="bg-surface-container-lowest rounded-lg p-3 font-label-sm text-label-sm text-on-surface-variant overflow-auto max-h-32 scrollbar-hide border border-white/5">{JSON.stringify(log.outputs, null, 2)}</pre>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                ) : !activeExpertData ? (
                  streamingText[activeExpertTab] ? (
                    <div>
                      <div className="flex items-center gap-2 mb-4">
                        <span className="w-2 h-2 rounded-full bg-tertiary animate-ping"></span>
                        <span className="font-label-md text-label-md text-tertiary uppercase">Streaming...</span>
                      </div>
                      <div className="prose prose-invert max-w-none" dangerouslySetInnerHTML={{ __html: renderMarkdown(streamingText[activeExpertTab]) }} />
                    </div>
                  ) : (
                    <p className="text-outline italic font-body-md">No report compiled for this domain yet.</p>
                  )
                ) : (
                  <div className="flex flex-col gap-6">
                    {/* Rating row */}
                    <div className="flex flex-wrap gap-3 items-center justify-between border-b border-white/5 pb-4">
                      <div className="flex items-center gap-3">
                        <span className="font-label-sm text-label-sm text-outline uppercase">Domain Rating:</span>
                        <span className={`font-label-md text-label-md px-3 py-1 rounded-full border ${
                          (activeExpertTab === "risk" ? activeExpertData.risk_recommendation : activeExpertData.recommendation)?.includes("Buy")
                            ? "text-tertiary border-tertiary/50 bg-tertiary/10"
                            : (activeExpertTab === "risk" ? activeExpertData.risk_recommendation : activeExpertData.recommendation)?.includes("Sell")
                            ? "text-error border-error/50 bg-error/10"
                            : "text-secondary border-secondary/50 bg-secondary/10"
                        }`}>
                          {((activeExpertTab === "risk" ? activeExpertData.risk_recommendation : activeExpertData.recommendation) || "HOLD").toUpperCase()}
                        </span>
                      </div>
                      {activeExpertTab !== "risk" && activeExpertData.price_target && (
                        <div className="flex items-center gap-2">
                          <span className="font-label-sm text-label-sm text-outline uppercase">Price Target:</span>
                          <span className="font-label-md text-label-md text-secondary px-3 py-1 rounded-full border border-secondary/50 bg-secondary/10">
                            {activeExpertData.price_target}
                          </span>
                        </div>
                      )}
                    </div>

                    {/* Risk Audit banners */}
                    {activeExpertTab !== "risk" && (() => {
                      const critique  = expertReports["risk"]?.audit_log?.find(c => c.target_expert === activeExpertTab);
                      const crosstalk = expertReports["risk"]?.cross_talk_log?.find(c => c.target_expert === activeExpertTab);
                      if (!critique && !crosstalk) return null;
                      return (
                        <div className="flex flex-col gap-3">
                          {critique && (
                            <div className="p-4 border-l-2 border-secondary bg-secondary/5 rounded-r-xl">
                              <div className="flex items-center gap-2 mb-2">
                                <Icon name="warning" className="text-secondary text-[16px]" />
                                <span className="font-label-md text-label-md text-secondary uppercase">Peer-Review Challenge · {critique.severity}</span>
                              </div>
                              <p className="font-body-md text-body-md text-on-surface-variant italic">"{critique.critique}"</p>
                            </div>
                          )}
                          {crosstalk && (
                            <div className="p-4 border-l-2 border-tertiary bg-tertiary/5 rounded-r-xl">
                              <div className="flex items-center gap-2 mb-2">
                                <Icon name="send" className="text-tertiary text-[16px]" />
                                <span className="font-label-md text-label-md text-tertiary uppercase">Cross-Talk from {crosstalk.source_expert?.toUpperCase()}</span>
                              </div>
                              <p className="font-body-md text-body-md text-on-surface-variant italic">"{crosstalk.instruction}"</p>
                            </div>
                          )}
                        </div>
                      );
                    })()}

                    {/* Core Analysis */}
                    <div>
                      <h4 className="font-label-md text-label-md text-secondary uppercase tracking-widest mb-3">
                        {activeExpertTab === "risk" ? "Risk Audit & Findings" : "Core Audit & Findings"}
                      </h4>
                      <div className="prose prose-invert max-w-none"
                        dangerouslySetInnerHTML={{ __html: renderMarkdown(activeExpertTab === "risk" ? activeExpertData.risk_analysis : activeExpertData.core_analysis) }}
                      />
                    </div>

                    {/* Macro: Industry Comparison */}
                    {activeExpertTab === "macro" && activeExpertData.industry_comparison && (
                      <div className="border-t border-white/5 pt-6">
                        <h4 className="font-label-md text-label-md text-secondary uppercase tracking-widest mb-3 flex items-center gap-2">
                          <Icon name="bar_chart" className="text-[18px]" /> Sector Peer Comparison
                        </h4>
                        <div className="glass-card rounded-xl p-4">
                          <p className="font-body-md text-body-md text-on-surface-variant whitespace-pre-wrap">{activeExpertData.industry_comparison}</p>
                        </div>
                      </div>
                    )}

                    {/* Sentiment: Analyst Consensus */}
                    {activeExpertTab === "sentiment" && activeExpertData.analyst_consensus && (
                      <div className="border-t border-white/5 pt-6">
                        <h4 className="font-label-md text-label-md text-secondary uppercase tracking-widest mb-3 flex items-center gap-2">
                          <Icon name="groups" className="text-[18px]" /> Wall Street Consensus Divergence
                        </h4>
                        <div className="glass-card rounded-xl p-4">
                          <p className="font-body-md text-body-md text-on-surface-variant whitespace-pre-wrap">{activeExpertData.analyst_consensus}</p>
                        </div>
                      </div>
                    )}

                    {/* Tech: Product Roadmap */}
                    {activeExpertTab === "tech_product" && (
                      <div className="border-t border-white/5 pt-6">
                        <h4 className="font-label-md text-label-md text-secondary uppercase tracking-widest mb-3 flex items-center gap-2">
                          <Icon name="flag" className="text-[18px] animate-pulse" /> Product Roadmap & R&D Timeline
                        </h4>
                        {(!activeExpertData.product_roadmap || activeExpertData.product_roadmap.length === 0) ? (
                          <p className="text-outline italic font-body-md">No roadmap milestones identified.</p>
                        ) : (
                          <div className="relative border-l-2 border-outline-variant ml-4 pl-6 flex flex-col gap-5">
                            {activeExpertData.product_roadmap.map((item, i) => (
                              <div key={i} className="relative">
                                <span className="absolute -left-[31px] top-2 w-4 h-4 rounded-full border-2 border-secondary bg-background flex items-center justify-center">
                                  <span className="w-1.5 h-1.5 rounded-full bg-secondary"></span>
                                </span>
                                <div className="glass-card rounded-xl p-4">
                                  <div className="flex flex-wrap justify-between items-center gap-2 mb-2">
                                    <span className="font-label-md text-label-md text-on-surface">{item.product_name}</span>
                                    <div className="flex items-center gap-2">
                                      <span className="font-label-sm text-label-sm text-secondary border border-secondary/30 bg-secondary/10 px-2 py-0.5 rounded">{item.timeline}</span>
                                      <span className={`font-label-sm text-label-sm px-2 py-0.5 rounded border ${item.feasibility === "High" ? "text-tertiary border-tertiary/30 bg-tertiary/10" : item.feasibility === "Low" ? "text-error border-error/30 bg-error/10" : "text-secondary border-secondary/30 bg-secondary/10"}`}>
                                        {item.feasibility?.toUpperCase()}
                                      </span>
                                    </div>
                                  </div>
                                  <p className="font-body-md text-body-md text-on-surface-variant">{item.description}</p>
                                </div>
                              </div>
                            ))}
                          </div>
                        )}
                        {activeExpertData.innovation_risk && (
                          <div className="mt-4 p-4 border-l-2 border-error bg-error/5 rounded-r-xl">
                            <h5 className="font-label-md text-label-md text-error mb-2">Innovation & Execution Risk</h5>
                            <p className="font-body-md text-body-md text-on-surface-variant">{activeExpertData.innovation_risk}</p>
                          </div>
                        )}
                      </div>
                    )}

                    {/* Risk: Audit Log + Cross-Talk */}
                    {activeExpertTab === "risk" && (
                      <div className="flex flex-col gap-5">
                        {activeExpertData.audit_log?.length > 0 && (
                          <div>
                            <h4 className="font-label-md text-label-md text-secondary uppercase tracking-widest mb-3 flex items-center gap-2">
                              <Icon name="shield" className="text-[18px]" /> Peer Review Audit Log
                            </h4>
                            <div className="flex flex-col gap-3">
                              {activeExpertData.audit_log.map((item, i) => (
                                <div key={i} className="glass-card rounded-xl p-4">
                                  <div className="flex items-center justify-between mb-2">
                                    <span className="font-label-md text-label-md text-tertiary uppercase">{item.target_expert?.replace("_"," ")}</span>
                                    <span className={`font-label-sm text-label-sm px-2 py-0.5 rounded border ${item.severity === "High" ? "text-error border-error/30 bg-error/10" : item.severity === "Medium" ? "text-secondary border-secondary/30 bg-secondary/10" : "text-outline border-outline-variant"}`}>
                                      {item.severity} SEVERITY
                                    </span>
                                  </div>
                                  <p className="font-body-md text-body-md text-on-surface-variant italic">"{item.critique}"</p>
                                </div>
                              ))}
                            </div>
                          </div>
                        )}
                        {activeExpertData.cross_talk_log?.length > 0 && (
                          <div>
                            <h4 className="font-label-md text-label-md text-tertiary uppercase tracking-widest mb-3 flex items-center gap-2">
                              <Icon name="send" className="text-[18px] animate-pulse" /> Supervisor Cross-Talk Interventions
                            </h4>
                            <div className="flex flex-col gap-3">
                              {activeExpertData.cross_talk_log.map((item, i) => (
                                <div key={i} className="glass-card rounded-xl p-4">
                                  <div className="flex items-center justify-between mb-2">
                                    <span className="font-label-md text-label-md text-secondary uppercase">{item.source_expert?.replace("_"," ")} → {item.target_expert?.replace("_"," ")}</span>
                                  </div>
                                  <p className="font-body-md text-body-md text-on-surface-variant italic">"{item.instruction}"</p>
                                </div>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                )}
              </div>

              {/* TradingView Chart moved to the bottom */}
              {ticker && (
                <div className="glass-panel p-8 rounded-xl h-96 flex flex-col">
                  <h2 className="font-headline-sm text-headline-sm text-secondary mb-4" style={{fontSize:"20px"}}>Price Action Chart</h2>
                  <div className="flex-grow rounded-xl overflow-hidden">
                    <TradingViewChart ticker={ticker} />
                  </div>
                </div>
              )}
            </div>

            {/* Right Sidebar */}
            <aside className="lg:col-span-4 flex flex-col gap-6">
              {/* Top News Panel */}
              <div className="bg-surface-container-high p-6 rounded-xl border border-white/10 relative overflow-hidden">
                <div className="flex items-center gap-2 mb-5">
                  <Icon name="newspaper" className="text-secondary" />
                  <h3 className="font-label-md text-label-md text-on-surface uppercase tracking-widest">Top News · {ticker || "—"}</h3>
                </div>
                {newsArticles.length === 0 ? (
                  <p className="font-body-md text-body-md text-outline italic">News articles will appear after analysis completes.</p>
                ) : (
                  <ul className="flex flex-col gap-3">
                    {newsArticles.map((article, i) => (
                      <li key={i} className="flex flex-col gap-1 p-3 rounded-lg bg-white/5 border border-white/5 hover:bg-white/10 transition-colors">
                        <p className="font-body-md text-body-md text-on-surface leading-snug">{article.title}</p>
                        <div className="flex items-center gap-2 flex-wrap">
                          {article.source && (
                            <span className="font-label-sm text-label-sm text-secondary border border-secondary/30 bg-secondary/5 px-2 py-0.5 rounded">{article.source}</span>
                          )}
                          {article.date && (
                            <span className="font-label-sm text-label-sm text-outline">{article.date}</span>
                          )}
                        </div>
                      </li>
                    ))}
                  </ul>
                )}
                <div className="mt-5 pt-5 border-t border-white/5">
                  <button onClick={runAnalysis} disabled={isAnalyzing || !query.trim()} className="w-full bg-white/5 hover:bg-white/10 text-on-surface py-3 rounded-lg font-label-md text-label-md transition-all active:scale-95 disabled:opacity-40">
                    RE-RUN ANALYSIS
                  </button>
                </div>
              </div>

              {/* Technical Signals from Report */}
              {expertReports.technical && (
                <div className="glass-panel p-6 rounded-xl">
                  <h3 className="font-label-md text-label-md text-outline uppercase tracking-widest mb-5">Technical Signal Hub</h3>
                  <div className="prose prose-invert max-w-none">
                    <div dangerouslySetInnerHTML={{ __html: renderMarkdown(expertReports.technical?.core_analysis || "") }} />
                  </div>
                </div>
              )}

              {/* 200-Day SMA metric card */}
              <div className="glass-panel p-6 rounded-xl glow-gold">
                <div className="flex justify-between items-start mb-4">
                  <span className="font-label-sm text-label-sm text-secondary uppercase tracking-wider">200-Day SMA</span>
                  <Icon name="candlestick_chart" className="text-outline text-[20px]" />
                </div>
                <div className="font-headline-sm text-headline-sm text-on-surface">{metrics.sma200 !== "—" ? `$${metrics.sma200}` : "—"}</div>
                <p className="font-label-sm text-label-sm text-outline-variant mt-2">Long-term trend indicator · {ticker || "—"}</p>
              </div>
            </aside>
          </div>
        </main>

        {/* ── FOOTER ── */}
        <footer className="w-full py-10 mt-auto bg-surface-container-lowest border-t border-white/5">
          <div className="flex flex-col md:flex-row justify-between items-center px-margin-mobile md:px-margin-desktop max-w-container-max mx-auto gap-gutter">
            <div className="font-headline-sm text-secondary" style={{fontSize:"20px"}}>StockGraph AI</div>
            <div className="font-label-sm text-label-sm uppercase tracking-wider text-tertiary text-center">
              © 2024 StockGraph AI. Institutional Grade Analysis.
            </div>
            <div className="flex gap-8">
              {["Privacy","Terms","API Docs"].map(l => (
                <a key={l} className="font-label-sm text-label-sm uppercase tracking-wider text-outline hover:text-on-surface transition-colors cursor-pointer hover:underline decoration-secondary underline-offset-4">{l}</a>
              ))}
            </div>
          </div>
        </footer>
      </div>
    );
  }

  ReactDOM.render(<App />, document.getElementById("root"));
</script>
</body>
</html>"""


def get_frontend_html():
    return HTML_FRONTEND_CONTENT
