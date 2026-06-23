HTML_FRONTEND_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agentic Stock Analyst - Bloomberg Terminal meets SaaS</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        bloomberg: {
                            dark: '#0a0d14',
                            card: '#121620',
                            border: '#1e2433',
                            cyan: '#00e1ff',
                            green: '#00ff66',
                            red: '#ff3366',
                            amber: '#ffb300'
                        }
                    }
                }
            }
        }
    </script>
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Outfit', sans-serif;
            background-color: #0a0d14;
        }
        .mono {
            font-family: 'JetBrains Mono', monospace;
        }
        /* Custom scrollbars */
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        ::-webkit-scrollbar-track {
            background: #0a0d14;
        }
        ::-webkit-scrollbar-thumb {
            background: #1e2433;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #00e1ff;
        }
        /* Pulsing animations */
        @keyframes pulse-cyan {
            0%, 100% { box-shadow: 0 0 5px rgba(0, 225, 255, 0.4); border-color: rgba(0, 225, 255, 0.4); }
            50% { box-shadow: 0 0 20px rgba(0, 225, 255, 0.8); border-color: #00e1ff; }
        }
        .thinking-card {
            animation: pulse-cyan 2s infinite;
        }
        /* Hide scrollbars for slick scrolling metrics */
        .scrollbar-none::-webkit-scrollbar {
            display: none;
        }
        .scrollbar-none {
            -ms-overflow-style: none;
            scrollbar-width: none;
        }
    </style>
    <!-- React & Babel CDNs -->
    <script src="https://unpkg.com/react@18/umd/react.production.min.js" crossorigin></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js" crossorigin></script>
    <script src="https://unpkg.com/@babel/standalone@7.15.0/babel.min.js"></script>
    <!-- Marked.js -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/marked/4.3.0/marked.min.js"></script>
</head>
<body class="text-zinc-100">
    <div id="root"></div>

    <script type="text/babel">
        const { useState, useEffect, useRef } = React;

        // Custom Inline SVG Icon Components to avoid DOM manipulation mismatch crashes with Lucide
        function CpuIcon({ className = "w-5 h-5 text-bloomberg-cyan" }) {
            return (
                <svg xmlns="http://www.w3.org/2000/svg" class={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect width="16" height="16" x="4" y="4" rx="2"/>
                    <rect width="6" height="6" x="9" y="9" rx="1"/>
                    <path d="M9 1v3M15 1v3M9 20v3M15 20v3M20 9h3M20 15h3M1 9h3M1 15h3"/>
                </svg>
            );
        }

        // TerminalIcon
        function TerminalIcon({ className = "w-4 h-4 text-bloomberg-cyan" }) {
            return (
                <svg xmlns="http://www.w3.org/2000/svg" class={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="4 17 10 11 4 5"/>
                    <line x1="12" y1="19" x2="20" y2="19"/>
                </svg>
            );
        }

        // PlayIcon
        function PlayIcon({ className = "w-4 h-4" }) {
            return (
                <svg xmlns="http://www.w3.org/2000/svg" class={className} viewBox="0 0 24 24" fill="currentColor">
                    <polygon points="6 3 20 12 6 21 6 3"/>
                </svg>
            );
        }

        // GitBranchIcon
        function GitBranchIcon({ className = "w-4 h-4 text-bloomberg-cyan" }) {
            return (
                <svg xmlns="http://www.w3.org/2000/svg" class={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="6" y1="3" x2="6" y2="15"/>
                    <circle cx="18" cy="6" r="3"/>
                    <circle cx="6" cy="18" r="3"/>
                    <path d="M18 9a9 9 0 0 1-9 9"/>
                </svg>
            );
        }

        // FileTextIcon
        function FileTextIcon({ className = "w-5 h-5 text-bloomberg-cyan" }) {
            return (
                <svg xmlns="http://www.w3.org/2000/svg" class={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/>
                    <path d="M14 2v4a2 2 0 0 0 2 2h4"/>
                    <path d="M10 9H8M16 13H8M16 17H8"/>
                </svg>
            );
        }

        // HashIcon
        function HashIcon({ className = "w-5 h-5" }) {
            return (
                <svg xmlns="http://www.w3.org/2000/svg" class={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="4" y1="9" x2="20" y2="9"/>
                    <line x1="4" y1="15" x2="20" y2="15"/>
                    <line x1="10" y1="3" x2="8" y2="21"/>
                    <line x1="16" y1="3" x2="14" y2="21"/>
                </svg>
            );
        }

        // DollarIcon
        function DollarIcon({ className = "w-5 h-5" }) {
            return (
                <svg xmlns="http://www.w3.org/2000/svg" class={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="12" y1="1" x2="12" y2="23"/>
                    <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
                </svg>
            );
        }

        // PieChartIcon
        function PieChartIcon({ className = "w-5 h-5" }) {
            return (
                <svg xmlns="http://www.w3.org/2000/svg" class={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21.21 15.89A10 10 0 1 1 8 2.83"/>
                    <path d="M22 12A10 10 0 0 0 12 2v10z"/>
                </svg>
            );
        }

        // TrendingUpIcon
        function TrendingUpIcon({ className = "w-5 h-5" }) {
            return (
                <svg xmlns="http://www.w3.org/2000/svg" class={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/>
                    <polyline points="16 7 22 7 22 13"/>
                </svg>
            );
        }

        // ActivityIcon
        function ActivityIcon({ className = "w-5 h-5" }) {
            return (
                <svg xmlns="http://www.w3.org/2000/svg" class={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
                </svg>
            );
        }

        // AgentIcon
        function AgentIcon({ type, className = "w-5 h-5" }) {
            if (type === 'supervisor') {
                return (
                    <svg xmlns="http://www.w3.org/2000/svg" class={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                    </svg>
                );
            }
            if (type === 'download-cloud') {
                return (
                    <svg xmlns="http://www.w3.org/2000/svg" class={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M4 14.899A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 2.5 8.242"/>
                        <path d="M12 12v6"/>
                        <path d="m8 14 4 4 4-4"/>
                    </svg>
                );
            }
            if (type === 'financial') {
                return (
                    <svg xmlns="http://www.w3.org/2000/svg" class={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <line x1="18" y1="20" x2="18" y2="10"/>
                        <line x1="12" y1="20" x2="12" y2="4"/>
                        <line x1="6" y1="20" x2="6" y2="14"/>
                    </svg>
                );
            }
            if (type === 'tech_product') {
                return (
                    <svg xmlns="http://www.w3.org/2000/svg" class={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <rect x="2" y="2" width="20" height="8" rx="2" ry="2"/>
                        <rect x="2" y="14" width="20" height="8" rx="2" ry="2"/>
                        <line x1="6" y1="6" x2="6.01" y2="6"/>
                        <line x1="6" y1="18" x2="6.01" y2="18"/>
                    </svg>
                );
            }
            if (type === 'sentiment') {
                return (
                    <svg xmlns="http://www.w3.org/2000/svg" class={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                    </svg>
                );
            }
            if (type === 'macro') {
                return (
                    <svg xmlns="http://www.w3.org/2000/svg" class={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="10"/>
                        <line x1="2" y1="12" x2="22" y2="12"/>
                        <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
                    </svg>
                );
            }
            if (type === 'risk') {
                return (
                    <svg xmlns="http://www.w3.org/2000/svg" class={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/>
                        <line x1="12" y1="9" x2="12" y2="13"/>
                        <line x1="12" y1="17" x2="12.01" y2="17"/>
                    </svg>
                );
            }
            return (
                <svg xmlns="http://www.w3.org/2000/svg" class={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                    <polyline points="9 11 12 14 22 4"/>
                </svg>
            );
        }

        function App() {
            const [query, setQuery] = useState("");
            const [isAnalyzing, setIsAnalyzing] = useState(false);
            const [logs, setLogs] = useState([]);
            const [ticker, setTicker] = useState("");
            const [metrics, setMetrics] = useState({
                price: "—",
                pe: "—",
                sma50: "—",
                sma200: "—",
                market_cap: "—"
            });
            const [report, setReport] = useState("");
            const [expertReports, setExpertReports] = useState({});
            const [streamingText, setStreamingText] = useState({});
            const [activeExpertTab, setActiveExpertTab] = useState("financial");
            const [agentExecutionLogs, setAgentExecutionLogs] = useState([]);
            const [elapsedTime, setElapsedTime] = useState(0);
            const [totalDuration, setTotalDuration] = useState(null);
            const timerRef = useRef(null);
            const startTimeRef = useRef(null);

            useEffect(() => {
                return () => {
                    if (timerRef.current) clearInterval(timerRef.current);
                };
            }, []);
            
            const fetchAgentLogs = () => {
                fetch('/api/logs')
                    .then(res => res.json())
                    .then(data => {
                        if (Array.isArray(data)) {
                            setAgentExecutionLogs(data);
                        }
                    })
                    .catch(err => console.error("Error fetching agent logs:", err));
            };
            
            // Agent states: 'idle', 'thinking', 'complete'
            const [agentStates, setAgentStates] = useState({
                supervisor: 'idle',
                prefetch: 'idle',
                financial: 'idle',
                tech_product: 'idle',
                sentiment: 'idle',
                macro: 'idle',
                risk: 'idle',
                synthesis: 'idle'
            });

            // Auto-scroll logs
            const logEndRef = useRef(null);
            useEffect(() => {
                logEndRef.current?.scrollIntoView({ behavior: 'smooth' });
            }, [logs]);

            const runAnalysis = () => {
                if (!query.trim()) return;

                // Reset state
                setIsAnalyzing(true);
                setLogs([{ type: 'info', message: 'Connecting to state machine...' }]);
                setTicker("");
                setMetrics({ price: "—", pe: "—", sma50: "—", sma200: "—", market_cap: "—" });
                setReport("");
                setExpertReports({});
                setStreamingText({});
                setAgentExecutionLogs([]);
                setElapsedTime(0);
                setTotalDuration(null);
                setAgentStates({
                    supervisor: 'thinking',
                    prefetch: 'idle',
                    financial: 'idle',
                    tech_product: 'idle',
                    sentiment: 'idle',
                    macro: 'idle',
                    risk: 'idle',
                    synthesis: 'idle'
                });

                startTimeRef.current = Date.now();
                if (timerRef.current) clearInterval(timerRef.current);
                timerRef.current = setInterval(() => {
                    const elapsed = (Date.now() - startTimeRef.current) / 1000;
                    setElapsedTime(elapsed);
                }, 100);

                const eventSource = new EventSource(`/api/stream?query=${encodeURIComponent(query)}`);

                eventSource.onmessage = (event) => {
                    const data = JSON.parse(event.data);
                    
                    if (data.event === 'start') {
                        setLogs(prev => [...prev, { type: 'system', message: data.message }]);
                        fetchAgentLogs();
                    } else if (data.event === 'token') {
                        const { agent, text } = data;
                        setStreamingText(prev => ({
                            ...prev,
                            [agent]: (prev[agent] || "") + text
                        }));
                    } else if (data.event === 'update') {
                        const { agent, active_agent, message, ticker: extractedTicker, metrics: newMetrics, expert_reports: reports } = data;
                        
                        // Append log
                        setLogs(prev => [...prev, { type: agent, message }]);
                        
                        if (extractedTicker && typeof extractedTicker === 'string') {
                            setTicker(extractedTicker.toUpperCase());
                        }
                        if (newMetrics && typeof newMetrics === 'object' && Object.keys(newMetrics).length > 0) {
                            setMetrics(prev => ({ ...prev, ...newMetrics }));
                        }
                        if (reports && typeof reports === 'object' && Object.keys(reports).length > 0) {
                            setExpertReports(prev => ({ ...prev, ...reports }));
                        }

                        // Dynamic real-time fetch of raw LLM input/output logs
                        fetchAgentLogs();

                        // Update Agent Timeline States
                        setAgentStates(prev => {
                            const nextStates = { ...prev };
                            const revCount = data.revision_count || 0;
                            
                            if (active_agent === 'pre_fetch') {
                                nextStates.supervisor = 'complete';
                                nextStates.prefetch = 'thinking';
                            } else if (active_agent === 'financial' && revCount === 0) {
                                // Phase 1: Fork to parallel experts (excluding risk)
                                nextStates.prefetch = 'complete';
                                nextStates.financial = 'thinking';
                                nextStates.tech_product = 'thinking';
                                nextStates.sentiment = 'thinking';
                                nextStates.macro = 'thinking';
                                nextStates.risk = 'idle';
                            }

                            // Complete individual experts in Phase 1
                            if (agent === 'financial' && revCount === 0) nextStates.financial = 'complete';
                            if (agent === 'tech_product' && revCount === 0) nextStates.tech_product = 'complete';
                            if (agent === 'sentiment' && revCount === 0) nextStates.sentiment = 'complete';
                            if (agent === 'macro' && revCount === 0) nextStates.macro = 'complete';

                            // Phase 2: Once first 4 are complete, active_agent moves to risk
                            if (active_agent === 'risk') {
                                nextStates.financial = 'complete';
                                nextStates.tech_product = 'complete';
                                nextStates.sentiment = 'complete';
                                nextStates.macro = 'complete';
                                nextStates.risk = 'thinking';
                            }

                            // Risk audit completes
                            if (agent === 'risk') {
                                nextStates.risk = 'complete';
                            }

                            // Phase 3: Revision loop back to flagged expert(s)
                            if (agent === 'risk' && revCount > 0 && active_agent) {
                                const flaggedList = active_agent.split(',');
                                flaggedList.forEach(tgt => {
                                    if (['financial', 'tech_product', 'sentiment', 'macro'].includes(tgt)) {
                                        nextStates[tgt] = 'thinking';
                                    }
                                });
                            }
                            
                            // Complete revision
                            if (revCount > 0 && agent && ['financial', 'tech_product', 'sentiment', 'macro'].includes(agent)) {
                                nextStates[agent] = 'complete';
                            }

                            // Phase 4: Joint synthesis compiler transition
                            if (active_agent === 'synthesis') {
                                nextStates.financial = 'complete';
                                nextStates.tech_product = 'complete';
                                nextStates.sentiment = 'complete';
                                nextStates.macro = 'complete';
                                nextStates.risk = 'complete';
                                nextStates.synthesis = 'thinking';
                            } else if (active_agent === 'finish') {
                                nextStates.financial = 'complete';
                                nextStates.tech_product = 'complete';
                                nextStates.sentiment = 'complete';
                                nextStates.macro = 'complete';
                                nextStates.risk = 'complete';
                                nextStates.synthesis = 'complete';
                            }
                            
                            return nextStates;
                        });

                        // If supervisor has finished and outputs the final report
                        if (agent === 'supervisor' && active_agent === 'finish') {
                            setReport(message);
                        }
                    } else if (data.event === 'complete') {
                        if (timerRef.current) clearInterval(timerRef.current);
                        const finalDuration = ((Date.now() - startTimeRef.current) / 1000).toFixed(2);
                        setTotalDuration(finalDuration);
                        setLogs(prev => [...prev, { type: 'success', message: data.message }]);
                        setIsAnalyzing(false);
                        fetchAgentLogs();
                        eventSource.close();
                    } else if (data.event === 'error') {
                        if (timerRef.current) clearInterval(timerRef.current);
                        const finalDuration = ((Date.now() - startTimeRef.current) / 1000).toFixed(2);
                        setTotalDuration(finalDuration);
                        setLogs(prev => [...prev, { type: 'error', message: `Execution failed: ${data.message}` }]);
                        setIsAnalyzing(false);
                        fetchAgentLogs();
                        eventSource.close();
                    }
                };

                eventSource.onerror = (err) => {
                    if (timerRef.current) clearInterval(timerRef.current);
                    const finalDuration = ((Date.now() - startTimeRef.current) / 1000).toFixed(2);
                    setTotalDuration(finalDuration);
                    setLogs(prev => [...prev, { type: 'error', message: 'Stream connection lost.' }]);
                    setIsAnalyzing(false);
                    eventSource.close();
                };
            };

            const renderMarkdown = (text) => {
                if (!text || typeof text !== 'string') {
                    return '<p class="text-zinc-500 italic">Analyst report is pending...</p>';
                }
                try {
                    if (window.marked && typeof window.marked.parse === 'function') {
                        return window.marked.parse(text);
                    } else if (typeof window.marked === 'function') {
                        return window.marked(text);
                    }
                    return `<p class="whitespace-pre-wrap">${text}</p>`;
                } catch (e) {
                    console.error("Markdown parsing failed, falling back to raw text:", e);
                    return `<p class="whitespace-pre-wrap">${text}</p>`;
                }
            };

            const activeExpertData = expertReports[activeExpertTab];

            return (
                <div class="min-h-screen bg-bloomberg-dark flex flex-col">
                    {/* Header */}
                    <header class="border-b border-bloomberg-border bg-bloomberg-card/50 backdrop-blur px-6 py-4 flex items-center justify-between shadow-lg">
                        <div class="flex items-center gap-3">
                            <div class="w-8 h-8 rounded bg-gradient-to-tr from-bloomberg-cyan to-indigo-600 flex items-center justify-center shadow-[0_0_15px_rgba(0,225,255,0.4)]">
                                <CpuIcon />
                            </div>
                            <div>
                                <h1 class="text-lg font-extrabold tracking-tight text-white flex items-center gap-2">
                                    Agentic Stock Analyst
                                    <span class="text-xs bg-bloomberg-cyan/10 border border-bloomberg-cyan/30 text-bloomberg-cyan px-2 py-0.5 rounded font-mono font-normal">v3.0 COMMITTEE</span>
                                </h1>
                                <p class="text-xs text-zinc-400">Bloomberg-grade institutional investment committee</p>
                            </div>
                        </div>
                        <div class="flex items-center gap-4 text-xs font-mono text-zinc-400">
                            <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-bloomberg-green animate-ping"></span> API CONNECTED</span>
                            <span class="border-l border-bloomberg-border pl-4">MODEL: {model_name}</span>
                        </div>
                    </header>

                    {/* Main Area */}
                    <main class="flex-1 p-6 grid grid-cols-1 lg:grid-cols-12 gap-6 overflow-hidden">
                        {/* Left Column: Command Center */}
                        <section class="lg:col-span-5 flex flex-col gap-6 h-full max-h-[calc(100vh-140px)]">
                            {/* Input Form */}
                            <div class="bg-bloomberg-card border border-bloomberg-border rounded-xl p-5 shadow-2xl flex flex-col gap-4">
                                <h2 class="text-sm font-bold tracking-wider text-zinc-300 uppercase flex items-center gap-2">
                                    <TerminalIcon />
                                    Command Center
                                </h2>
                                <div class="flex gap-2">
                                    <input 
                                        type="text"
                                        value={query}
                                        onChange={(e) => setQuery(e.target.value)}
                                        onKeyDown={(e) => e.key === 'Enter' && runAnalysis()}
                                        disabled={isAnalyzing}
                                        placeholder="e.g., Analyze Apple (AAPL) and recent headlines."
                                        class="flex-1 bg-bloomberg-dark/80 border border-bloomberg-border rounded-lg px-4 py-3 text-sm focus:outline-none focus:ring-1 focus:ring-bloomberg-cyan text-white placeholder-zinc-500 disabled:opacity-50"
                                    />
                                    <button 
                                        onClick={runAnalysis}
                                        disabled={isAnalyzing}
                                        class="bg-gradient-to-tr from-bloomberg-cyan to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 text-bloomberg-dark font-extrabold text-sm px-6 py-3 rounded-lg flex items-center gap-2 shadow-[0_0_15px_rgba(0,225,255,0.2)] disabled:opacity-50 transition-all duration-300"
                                    >
                                        {isAnalyzing ? (
                                            <>
                                                <div class="w-4 h-4 border-2 border-bloomberg-dark border-t-transparent rounded-full animate-spin"></div>
                                                Analyzing
                                            </>
                                        ) : (
                                            <>
                                                <PlayIcon className="w-4 h-4 fill-bloomberg-dark text-bloomberg-dark" />
                                                Analyze
                                            </>
                                        )}
                                    </button>
                                </div>
                                <div class="flex items-center justify-between border-t border-bloomberg-border/50 pt-3 text-xs font-mono">
                                    <span class="text-zinc-500 uppercase tracking-wider flex items-center gap-1.5">
                                        <svg xmlns="http://www.w3.org/2000/svg" class="w-3.5 h-3.5 text-zinc-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                            <circle cx="12" cy="12" r="10"/>
                                            <polyline points="12 6 12 12 16 14"/>
                                        </svg>
                                        EXECUTION TIME
                                    </span>
                                    {isAnalyzing ? (
                                        <span class="text-bloomberg-cyan font-bold animate-pulse flex items-center gap-1.5">
                                            <span class="w-1.5 h-1.5 rounded-full bg-bloomberg-cyan animate-ping"></span>
                                            RUNNING: {elapsedTime.toFixed(1)}s
                                        </span>
                                    ) : totalDuration ? (
                                        <span class="text-bloomberg-green font-bold flex items-center gap-1">
                                            <svg xmlns="http://www.w3.org/2000/svg" class="w-3.5 h-3.5 text-bloomberg-green" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                                                <polyline points="20 6 9 17 4 12"/>
                                            </svg>
                                            COMPLETED IN: {totalDuration}s
                                        </span>
                                    ) : (
                                        <span class="text-zinc-500">⏱️ READY</span>
                                    )}
                                </div>
                            </div>

                            {/* Agent Handoff Timeline */}
                            <div class="bg-bloomberg-card border border-bloomberg-border rounded-xl p-5 shadow-2xl flex flex-col gap-4 flex-1 overflow-y-auto font-mono">
                                <h2 class="text-sm font-bold tracking-wider text-zinc-300 uppercase flex items-center gap-2">
                                    <GitBranchIcon />
                                    Investment Committee Handoff
                                </h2>
                                
                                <div class="flex flex-col gap-3 relative before:absolute before:left-6 before:top-2 before:bottom-2 before:w-[1px] before:bg-bloomberg-border">
                                    {/* Supervisor */}
                                    <AgentCard 
                                        title="Supervisor Agent" 
                                        desc="Orchestrates committee, parses prompt and extracts ticker symbol"
                                        status={agentStates.supervisor}
                                        icon="supervisor"
                                    />
                                    {/* Data Gatherer */}
                                    <AgentCard 
                                        title="Parallel Data Fetcher" 
                                        desc="Fires parallel threads on backend to pre-fetch 5 rich metric blocks"
                                        status={agentStates.prefetch}
                                        icon="download-cloud"
                                    />
                                    {/* Financial Expert */}
                                    <AgentCard 
                                        title="Financial Expert (Phase 1/3)" 
                                        desc="Analyzes fundamentals, valuation, and balance sheet metrics. Responds to Risk critiques."
                                        status={agentStates.financial}
                                        icon="financial"
                                    />
                                    {/* Tech Moat Expert */}
                                    <AgentCard 
                                        title="Tech & Product Expert (Phase 1/3)" 
                                        desc="Assesses company competitive moat, business scale, and product pipelines. Responds to Risk critiques."
                                        status={agentStates.tech_product}
                                        icon="tech_product"
                                    />
                                    {/* Sentiment Expert */}
                                    <AgentCard 
                                        title="Media & Sentiment Expert (Phase 1/3)" 
                                        desc="Gauges media coverage and narrative sentiment. Responds to Risk critiques."
                                        status={agentStates.sentiment}
                                        icon="sentiment"
                                    />
                                    {/* Macro Expert */}
                                    <AgentCard 
                                        title="Macro & Industry Expert (Phase 1/3)" 
                                        desc="Contextualizes market tailwinds and broader sector indices. Responds to Risk critiques."
                                        status={agentStates.macro}
                                        icon="macro"
                                    />
                                    {/* Risk Expert */}
                                    <AgentCard 
                                        title="Risk Expert & Internal Auditor (Phase 2)" 
                                        desc="Performs independent risk checks and cross-examines peer reports."
                                        status={agentStates.risk}
                                        icon="risk"
                                    />
                                    {/* Committee Compiler */}
                                    <AgentCard 
                                        title="Supervisor Compiler (Phase 4)" 
                                        desc="Synthesizes all expert reports and critiques into the final thesis"
                                        status={agentStates.synthesis}
                                        icon="supervisor"
                                    />
                                </div>
                            </div>

                            {/* Live Console Output */}
                            <div class="bg-bloomberg-card border border-bloomberg-border rounded-xl p-5 shadow-2xl flex flex-col gap-3 h-48">
                                <h2 class="text-xs font-bold tracking-wider text-zinc-400 uppercase flex items-center gap-2">
                                    <TerminalIcon className="w-3.5 h-3.5 text-bloomberg-cyan" />
                                    Graph Console Output
                                </h2>
                                <div class="flex-1 bg-bloomberg-dark/60 rounded-lg p-3 overflow-y-auto mono text-xs text-zinc-300 flex flex-col gap-1.5 border border-bloomberg-border/50">
                                    {logs.length === 0 ? (
                                        <span class="text-zinc-500 italic">Waiting for analysis trigger...</span>
                                    ) : (
                                        logs.map((log, idx) => (
                                            <div key={idx} class="flex gap-2">
                                                <span class={`font-bold select-none ${
                                                    log.type === 'system' ? 'text-zinc-500' :
                                                    log.type === 'supervisor' ? 'text-bloomberg-cyan' :
                                                    log.type === 'backend' ? 'text-purple-400' :
                                                    log.type === 'financial' ? 'text-bloomberg-green' :
                                                    log.type === 'tech_product' ? 'text-blue-400' :
                                                    log.type === 'sentiment' ? 'text-pink-400' :
                                                    log.type === 'macro' ? 'text-yellow-300' :
                                                    log.type === 'risk' ? 'text-bloomberg-red' :
                                                    log.type === 'success' ? 'text-bloomberg-green' :
                                                    log.type === 'error' ? 'text-bloomberg-red' :
                                                    'text-zinc-400'
                                                }`}>
                                                    [{(log.type || 'system').toUpperCase()}]
                                                </span>
                                                <span class="break-all whitespace-pre-wrap">{log.message}</span>
                                            </div>
                                        ))
                                    )}
                                    <div ref={logEndRef}></div>
                                </div>
                            </div>
                        </section>

                        {/* Right Column: Analysis Dashboard */}
                        <section class="lg:col-span-7 flex flex-col gap-6 h-full max-h-[calc(100vh-140px)] overflow-y-auto pr-1">
                            {/* Metrics Cards */}
                            <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-2.5 sm:gap-4 shrink-0">
                                <MetricCard title="Ticker" value={ticker || "—"} IconComponent={HashIcon} color="text-bloomberg-cyan bg-bloomberg-cyan/5" />
                                <MetricCard title="Current Price" value={metrics.price !== "—" ? `$${metrics.price}` : "—"} IconComponent={DollarIcon} color="text-bloomberg-green bg-bloomberg-green/5" />
                                <MetricCard title="P/E Ratio" value={metrics.pe || "—"} IconComponent={PieChartIcon} color="text-bloomberg-amber bg-bloomberg-amber/5" />
                                <MetricCard title="50 SMA" value={metrics.sma50 !== "—" ? `$${metrics.sma50}` : "—"} IconComponent={TrendingUpIcon} color="text-bloomberg-cyan bg-bloomberg-cyan/5" />
                                <MetricCard title="200 SMA" value={metrics.sma200 !== "—" ? `$${metrics.sma200}` : "—"} IconComponent={ActivityIcon} color="text-purple-400 bg-purple-500/5" />
                            </div>

                            {/* Markdown Report Container */}
                            <div class="bg-bloomberg-card border border-bloomberg-border rounded-xl p-6 shadow-2xl flex flex-col shrink-0 min-h-[350px]">
                                <div class="flex justify-between items-center border-b border-bloomberg-border/50 pb-4 mb-4">
                                    <h2 class="font-extrabold text-white text-base flex items-center gap-2">
                                        <FileTextIcon />
                                        Synthesized Executive Committee Thesis
                                    </h2>
                                    <span class="mono text-xs text-zinc-500 bg-bloomberg-dark/60 border border-bloomberg-border px-2.5 py-1 rounded">
                                        Ticker: {ticker || "None"}
                                    </span>
                                </div>
                                
                                <div 
                                    class="flex-1 prose prose-invert prose-cyan max-w-none text-zinc-300 text-sm leading-relaxed"
                                    dangerouslySetInnerHTML={{ __html: renderMarkdown(report || streamingText.supervisor) }}
                                ></div>
                            </div>

                            {/* New Section: Committee Drill-Down */}
                            <div class="bg-bloomberg-card border border-bloomberg-border rounded-xl p-6 shadow-2xl flex flex-col shrink-0">
                                <div class="border-b border-bloomberg-border/50 pb-4 mb-4">
                                    <h2 class="font-extrabold text-white text-base flex items-center gap-2">
                                        <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-bloomberg-cyan" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                                            <path d="M8 11h8"/>
                                            <path d="M12 7v8"/>
                                        </svg>
                                        Committee Expert Drill-Down
                                    </h2>
                                    <p class="text-xs text-zinc-500 mt-1">Exposing the raw, structured Pydantic report generated by each institutional expert</p>
                                </div>

                                {/* Tabs Row */}
                                <div class="flex flex-wrap gap-2 mb-4 border-b border-bloomberg-border/40 pb-2">
                                    <TabButton id="financial" label="Financials" active={activeExpertTab} onClick={setActiveExpertTab} />
                                    <TabButton id="tech_product" label="Tech Moat" active={activeExpertTab} onClick={setActiveExpertTab} />
                                    <TabButton id="sentiment" label="Sentiment" active={activeExpertTab} onClick={setActiveExpertTab} />
                                    <TabButton id="macro" label="Macro" active={activeExpertTab} onClick={setActiveExpertTab} />
                                    <TabButton id="risk" label="Risk Management" active={activeExpertTab} onClick={setActiveExpertTab} />
                                    <TabButton id="logs" label="Agent Audit Logs" active={activeExpertTab} onClick={setActiveExpertTab} />
                                </div>

                                {/* Tab Contents */}
                                <div class="bg-bloomberg-dark/40 rounded-xl p-5 border border-bloomberg-border/60">
                                     {activeExpertTab === 'logs' ? (
                                         <div class="flex flex-col gap-4">
                                             <div class="flex justify-between items-center border-b border-bloomberg-border/30 pb-2.5">
                                                 <h4 class="text-xs uppercase font-extrabold tracking-wider text-bloomberg-cyan flex items-center gap-1.5 animate-pulse">
                                                     <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-bloomberg-cyan" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                                                         <polyline points="4 17 10 11 4 5"/>
                                                         <line x1="12" y1="19" x2="20" y2="19"/>
                                                     </svg>
                                                     Real-Time Expert Audit Ledger
                                                 </h4>
                                                 <span class="text-[10px] text-zinc-500 font-mono">Total Traces: {agentExecutionLogs.length}</span>
                                             </div>
                                             
                                             {agentExecutionLogs.length === 0 ? (
                                                 <p class="text-zinc-500 italic text-sm">No agent traces logged yet. Start analysis to populate the ledger.</p>
                                             ) : (
                                                 <div class="flex flex-col gap-4 max-h-[600px] overflow-y-auto pr-1 scrollbar-none">
                                                     {agentExecutionLogs.map((log, idx) => (
                                                         <div key={idx} class="bg-bloomberg-card border border-bloomberg-border/80 hover:border-bloomberg-cyan/40 transition-all duration-300 rounded-xl p-4 flex flex-col gap-3">
                                                             <div class="flex flex-wrap items-center justify-between gap-3 border-b border-bloomberg-border/30 pb-2">
                                                                 <div class="flex items-center gap-2">
                                                                     <span class="text-xs font-bold text-white uppercase font-mono">[{idx + 1}]</span>
                                                                     <span class={`text-[10px] font-bold font-mono px-2 py-0.5 rounded border ${
                                                                         log.agent.includes("synthesis") ? "text-purple-400 bg-purple-400/10 border-purple-400/20" :
                                                                         log.agent.includes("ticker") ? "text-bloomberg-cyan bg-bloomberg-cyan/10 border-bloomberg-cyan/20" :
                                                                         log.agent === "financial" ? "text-bloomberg-green bg-bloomberg-green/10 border-bloomberg-green/20" :
                                                                         log.agent === "tech_product" ? "text-blue-400 bg-blue-400/10 border-blue-400/20" :
                                                                         log.agent === "sentiment" ? "text-pink-400 bg-pink-400/10 border-pink-400/20" :
                                                                         log.agent === "macro" ? "text-yellow-300 bg-yellow-300/10 border-yellow-300/20" :
                                                                         "text-bloomberg-red bg-bloomberg-red/10 border-bloomberg-red/20"
                                                                     }`}>
                                                                         {log.agent.replace('_', ' ').toUpperCase()}
                                                                     </span>
                                                                 </div>
                                                                 <span class="text-[10px] text-zinc-500 font-mono">{new Date(log.timestamp).toLocaleTimeString()}</span>
                                                             </div>
                                                             
                                                             <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                                                 <div class="flex flex-col gap-2 bg-bloomberg-dark/60 rounded-xl p-3 border border-bloomberg-border/40 min-w-0">
                                                                     <h5 class="text-[10px] uppercase font-bold tracking-wider text-bloomberg-cyan">Inputs (Prompts & Context)</h5>
                                                                     <div class="flex flex-col gap-2">
                                                                         <div>
                                                                             <span class="text-[9px] uppercase font-bold text-zinc-500 block">System Instruction:</span>
                                                                             <pre class="bg-bloomberg-card/50 rounded p-2 text-[10px] text-zinc-400 font-mono overflow-x-auto whitespace-pre-wrap max-h-32 scrollbar-none border border-bloomberg-border/20">{log.inputs?.system_prompt}</pre>
                                                                         </div>
                                                                         {log.inputs?.user_prompt && (
                                                                             <div>
                                                                                 <span class="text-[9px] uppercase font-bold text-zinc-500 block">Ingested Context:</span>
                                                                                 <pre class="bg-bloomberg-card/50 rounded p-2 text-[10px] text-zinc-400 font-mono overflow-x-auto whitespace-pre-wrap max-h-32 scrollbar-none border border-bloomberg-border/20">{log.inputs?.user_prompt}</pre>
                                                                             </div>
                                                                         )}
                                                                     </div>
                                                                 </div>
                                                                 
                                                                 <div class="flex flex-col gap-2 bg-bloomberg-dark/60 rounded-xl p-3 border border-bloomberg-border/40 min-w-0">
                                                                     <h5 class="text-[10px] uppercase font-bold tracking-wider text-bloomberg-green">Outputs (JSON / Report)</h5>
                                                                     <pre class="bg-bloomberg-card/50 rounded p-2 text-[10px] text-zinc-300 font-mono overflow-auto scrollbar-none border border-bloomberg-border/20 flex-1 max-h-72">
                                                                         {JSON.stringify(log.outputs, null, 2)}
                                                                     </pre>
                                                                 </div>
                                                             </div>
                                                         </div>
                                                     ))}
                                                 </div>
                                             )}
                                         </div>
                                      ) : !activeExpertData ? (
                                          streamingText[activeExpertTab] ? (
                                              <div class="flex flex-col gap-5">
                                                  <div class="flex flex-wrap gap-3 items-center justify-between border-b border-bloomberg-border/30 pb-3">
                                                      <div class="flex items-center gap-2">
                                                          <span class="text-xs font-bold text-zinc-400">DOMAIN RATING:</span>
                                                          <span class="text-xs font-bold font-mono text-bloomberg-cyan bg-bloomberg-cyan/10 border border-bloomberg-cyan/30 px-2.5 py-0.5 rounded animate-pulse">
                                                              STREAMING...
                                                          </span>
                                                      </div>
                                                  </div>
                                                  <div class="prose prose-invert max-w-none text-zinc-300 text-sm leading-relaxed min-h-[200px]">
                                                      <h4 class="text-xs uppercase font-extrabold tracking-wider text-bloomberg-cyan mb-3 flex items-center gap-1.5">
                                                          <span class="w-1.5 h-1.5 rounded-full bg-bloomberg-cyan animate-ping"></span>
                                                          Real-Time Analysis Feed
                                                      </h4>
                                                      <div dangerouslySetInnerHTML={{ __html: renderMarkdown(streamingText[activeExpertTab]) }} />
                                                  </div>
                                              </div>
                                          ) : (
                                              <p class="text-zinc-500 italic text-sm">No report compiled for this domain yet.</p>
                                          )
                                     ) : (
                                        <div class="flex flex-col gap-5">
                                            {/* Sub-Header info */}
                                            <div class="flex flex-wrap gap-3 items-center justify-between border-b border-bloomberg-border/30 pb-3">
                                                <div class="flex items-center gap-2">
                                                    <span class="text-xs font-bold text-zinc-400">DOMAIN RATING:</span>
                                                    <span class={`text-xs font-bold font-mono px-2.5 py-0.5 rounded border ${
                                                        (activeExpertTab === 'risk' ? activeExpertData.risk_recommendation : activeExpertData.recommendation)?.includes("Buy") 
                                                            ? 'text-bloomberg-green bg-bloomberg-green/10 border-bloomberg-green/30' 
                                                            : (activeExpertTab === 'risk' ? activeExpertData.risk_recommendation : activeExpertData.recommendation)?.includes("Sell") 
                                                                ? 'text-bloomberg-red bg-bloomberg-red/10 border-bloomberg-red/30' 
                                                                : 'text-bloomberg-amber bg-bloomberg-amber/10 border-bloomberg-amber/30'
                                                    }`}>
                                                        {((activeExpertTab === 'risk' ? activeExpertData.risk_recommendation : activeExpertData.recommendation) || 'HOLD').toUpperCase()}
                                                    </span>
                                                </div>
                                                {activeExpertTab !== 'risk' && (
                                                    <div class="flex items-center gap-2">
                                                        <span class="text-xs font-bold text-zinc-400">EST. PRICE TARGET:</span>
                                                        <span class="text-xs font-bold font-mono text-bloomberg-cyan bg-bloomberg-cyan/10 border border-bloomberg-cyan/30 px-2.5 py-0.5 rounded">
                                                            {activeExpertData.price_target}
                                                        </span>
                                                    </div>
                                                )}
                                            </div>

                                            {/* Peer Review Challenge / Cross-Talk Banner for Non-Risk Experts */}
                                            {activeExpertTab !== 'risk' && (() => {
                                                const myCritique = expertReports['risk']?.audit_log?.find(c => c.target_expert === activeExpertTab);
                                                const myCrossTalk = expertReports['risk']?.cross_talk_log?.find(c => c.target_expert === activeExpertTab);
                                                if (!myCritique && !myCrossTalk) return null;
                                                return (
                                                    <div class="flex flex-col gap-3">
                                                        {myCritique && (
                                                            <div class="bg-bloomberg-amber/5 border border-bloomberg-amber/30 rounded-xl p-4 flex flex-col gap-2 shrink-0">
                                                                <div class="flex items-center gap-2 text-bloomberg-amber">
                                                                    <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                                                        <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/>
                                                                        <line x1="12" y1="9" x2="12" y2="13"/>
                                                                        <line x1="12" y1="17" x2="12.01" y2="17"/>
                                                                    </svg>
                                                                    <span class="text-xs font-bold uppercase tracking-wider text-bloomberg-amber">Peer-Review Audit Challenge (Severity: {myCritique.severity})</span>
                                                                </div>
                                                                <p class="text-xs text-zinc-300 italic">"{myCritique.critique}"</p>
                                                                <div class="flex items-center gap-1.5 text-[10px] text-bloomberg-green font-bold uppercase mt-1">
                                                                    <svg xmlns="http://www.w3.org/2000/svg" class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                                                                        <polyline points="20 6 9 17 4 12"/>
                                                                    </svg>
                                                                    Addressed in Revised Expert Report
                                                                </div>
                                                            </div>
                                                        )}
                                                        {myCrossTalk && (
                                                            <div class="bg-bloomberg-cyan/5 border border-bloomberg-cyan/30 rounded-xl p-4 flex flex-col gap-2 shrink-0">
                                                                <div class="flex items-center gap-2 text-bloomberg-cyan animate-pulse">
                                                                    <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                                                        <polyline points="16 3 21 8 8 21 3 21 3 16 16 3"/>
                                                                    </svg>
                                                                    <span class="text-xs font-bold uppercase tracking-wider text-bloomberg-cyan">Supervisor Cross-Talk Intervention (Source: {myCrossTalk.source_expert?.toUpperCase()})</span>
                                                                </div>
                                                                <p class="text-xs text-zinc-300 italic">"{myCrossTalk.instruction}"</p>
                                                                <div class="flex items-center gap-1.5 text-[10px] text-bloomberg-cyan font-bold uppercase mt-1">
                                                                    <svg xmlns="http://www.w3.org/2000/svg" class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                                                                        <polyline points="20 6 9 17 4 12"/>
                                                                    </svg>
                                                                    Linked findings ingested successfully
                                                                </div>
                                                            </div>
                                                        )}
                                                    </div>
                                                );
                                            })()}

                                            {/* Core analysis */}
                                            <div>
                                                <h4 class="text-xs uppercase font-extrabold tracking-wider text-bloomberg-cyan mb-2">
                                                    {activeExpertTab === 'risk' ? 'Risk Audit & Standalone Analysis' : 'Core Audit & Findings'}
                                                </h4>
                                                <div 
                                                    class="prose prose-invert max-w-none text-zinc-300 text-xs leading-relaxed"
                                                    dangerouslySetInnerHTML={{ __html: renderMarkdown(activeExpertTab === 'risk' ? activeExpertData.risk_analysis : activeExpertData.core_analysis) }}
                                                ></div>
                                            </div>

                                            {/* Industry Comparison for Macro & Industry Expert */}
                                            {activeExpertTab === 'macro' && activeExpertData.industry_comparison && (
                                                <div class="mt-6 border-t border-bloomberg-border/30 pt-6 flex flex-col gap-4">
                                                    <h4 class="text-xs uppercase font-extrabold tracking-wider text-bloomberg-cyan flex items-center gap-2">
                                                        <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-bloomberg-cyan" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                                            <line x1="18" y1="20" x2="18" y2="10"/>
                                                            <line x1="12" y1="20" x2="12" y2="4"/>
                                                            <line x1="6" y1="20" x2="6" y2="14"/>
                                                        </svg>
                                                        Sector & Industry peer comparison
                                                    </h4>
                                                    <div class="bg-bloomberg-card/85 border border-bloomberg-border/50 hover:border-bloomberg-cyan/50 hover:bg-bloomberg-card transition-all duration-300 rounded-xl p-4">
                                                        <p class="text-xs text-zinc-300 leading-relaxed whitespace-pre-wrap">{activeExpertData.industry_comparison}</p>
                                                    </div>
                                                </div>
                                            )}

                                            {/* Analyst Consensus for Media & Sentiment Expert */}
                                            {activeExpertTab === 'sentiment' && activeExpertData.analyst_consensus && (
                                                <div class="mt-6 border-t border-bloomberg-border/30 pt-6 flex flex-col gap-4">
                                                    <h4 class="text-xs uppercase font-extrabold tracking-wider text-bloomberg-cyan flex items-center gap-2">
                                                        <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-bloomberg-cyan" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                                            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                                                            <circle cx="9" cy="7" r="4"/>
                                                            <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                                                            <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
                                                        </svg>
                                                        Wall Street Consensus Divergence Audit
                                                    </h4>
                                                    <div class="bg-bloomberg-card/85 border border-bloomberg-border/50 hover:border-bloomberg-cyan/50 hover:bg-bloomberg-card transition-all duration-300 rounded-xl p-4">
                                                        <p class="text-xs text-zinc-300 leading-relaxed whitespace-pre-wrap">{activeExpertData.analyst_consensus}</p>
                                                    </div>
                                                </div>
                                            )}

                                            {/* Future Product Roadmap Component for Tech Moat Tab */}
                                            {activeExpertTab === 'tech_product' && (
                                                <div class="mt-6 border-t border-bloomberg-border/30 pt-6 flex flex-col gap-4">
                                                    <h4 class="text-xs uppercase font-extrabold tracking-wider text-bloomberg-cyan flex items-center gap-2">
                                                        <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-bloomberg-cyan animate-pulse" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                                            <path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/>
                                                            <line x1="4" y1="22" x2="4" y2="15"/>
                                                        </svg>
                                                        Future Product Roadmap & R&D Timeline
                                                    </h4>
                                                    
                                                    {(!activeExpertData.product_roadmap || activeExpertData.product_roadmap.length === 0) ? (
                                                        <p class="text-zinc-500 italic text-xs">No specific product roadmap milestones identified for this asset.</p>
                                                    ) : (
                                                        <div class="relative border-l-2 border-bloomberg-border/60 ml-3 pl-6 flex flex-col gap-6 my-2">
                                                            {activeExpertData.product_roadmap.map((item, idx) => {
                                                                const feasibilityColors = {
                                                                    High: 'text-bloomberg-green bg-bloomberg-green/10 border-bloomberg-green/30 shadow-[0_0_10px_rgba(0,255,102,0.1)]',
                                                                    Medium: 'text-bloomberg-amber bg-bloomberg-amber/10 border-bloomberg-amber/30 shadow-[0_0_10px_rgba(245,158,11,0.1)]',
                                                                    Low: 'text-bloomberg-red bg-bloomberg-red/10 border-bloomberg-red/30 shadow-[0_0_10px_rgba(239,68,68,0.1)]'
                                                                };
                                                                const colorClass = feasibilityColors[item.feasibility] || feasibilityColors.Medium;
                                                                
                                                                return (
                                                                    <div key={idx} class="relative group">
                                                                        {/* Marker dot */}
                                                                        <span class="absolute -left-[31px] top-1.5 w-4 h-4 rounded-full border-2 border-bloomberg-cyan bg-bloomberg-dark flex items-center justify-center transition-all duration-300 group-hover:scale-125 group-hover:shadow-[0_0_8px_rgba(0,225,255,0.6)]">
                                                                            <span class="w-1.5 h-1.5 rounded-full bg-bloomberg-cyan"></span>
                                                                        </span>
                                                                        
                                                                        <div class="bg-bloomberg-card/85 border border-bloomberg-border/50 hover:border-bloomberg-cyan/50 hover:bg-bloomberg-card transition-all duration-300 rounded-xl p-4 flex flex-col gap-2 relative">
                                                                            <div class="flex flex-wrap items-center justify-between gap-3 border-b border-bloomberg-border/30 pb-2">
                                                                                <div class="flex items-center gap-2">
                                                                                    <span class="text-xs font-bold text-zinc-100">{item.product_name}</span>
                                                                                </div>
                                                                                <div class="flex items-center gap-2">
                                                                                    <span class="text-[10px] font-bold text-bloomberg-cyan bg-bloomberg-cyan/10 border border-bloomberg-cyan/30 px-2 py-0.5 rounded font-mono">
                                                                                        {item.timeline}
                                                                                    </span>
                                                                                    <span class={`text-[10px] font-bold px-2 py-0.5 rounded font-mono border ${colorClass}`}>
                                                                                        FEASIBILITY: {item.feasibility?.toUpperCase()}
                                                                                    </span>
                                                                                </div>
                                                                            </div>
                                                                            <p class="text-xs text-zinc-300 leading-relaxed whitespace-pre-wrap">{item.description}</p>
                                                                        </div>
                                                                    </div>
                                                                );
                                                            })}
                                                        </div>
                                                    )}

                                                    {/* Innovation Risk section */}
                                                    {activeExpertData.innovation_risk && (
                                                        <div class="mt-4 bg-bloomberg-red/5 border border-bloomberg-red/20 rounded-xl p-4">
                                                            <h5 class="text-xs font-bold text-bloomberg-red mb-2 flex items-center gap-1.5">
                                                                <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-bloomberg-red animate-pulse" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                                                    <circle cx="12" cy="12" r="10"/>
                                                                    <line x1="12" y1="8" x2="12" y2="12"/>
                                                                    <line x1="12" y1="16" x2="12.01" y2="16"/>
                                                                </svg>
                                                                Innovation & Execution Risk Assessment
                                                              </h5>
                                                            <p class="text-xs text-zinc-300 leading-relaxed whitespace-pre-wrap">{activeExpertData.innovation_risk}</p>
                                                        </div>
                                                    )}
                                                </div>
                                            )}

                                            {/* Standalone Audit & Cross-Talk Log in Risk Management Tab */}
                                            {activeExpertTab === 'risk' && (
                                                <div class="flex flex-col gap-5 mt-4">
                                                    {/* Audit Log */}
                                                    {activeExpertData.audit_log && activeExpertData.audit_log.length > 0 && (
                                                        <div class="bg-bloomberg-dark/60 border border-bloomberg-border rounded-xl p-4 flex flex-col gap-3">
                                                            <h4 class="text-xs uppercase font-extrabold tracking-wider text-bloomberg-amber flex items-center gap-1.5">
                                                                <svg xmlns="http://www.w3.org/2000/svg" class="w-4.5 h-4.5 text-bloomberg-amber" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                                                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                                                                    <line x1="12" y1="9" x2="12" y2="13"/>
                                                                    <line x1="12" y1="17" x2="12.01" y2="17"/>
                                                                </svg>
                                                                Peer Review Audit Log (Risk Cross-Examination)
                                                            </h4>
                                                            <div class="flex flex-col gap-3">
                                                                {activeExpertData.audit_log.map((item, idx) => (
                                                                    <div key={idx} class="bg-bloomberg-card border border-bloomberg-border/50 rounded-lg p-3 flex flex-col gap-1.5">
                                                                        <div class="flex items-center justify-between gap-2">
                                                                            <div class="flex items-center gap-2">
                                                                                <span class="text-[10px] font-bold text-zinc-400 font-mono">TARGET EXPERT:</span>
                                                                                <span class="text-xs font-bold text-bloomberg-cyan font-mono uppercase">{item.target_expert.replace('_', ' ')}</span>
                                                                            </div>
                                                                            <span class={`text-[10px] font-bold px-2 py-0.5 rounded font-mono border ${
                                                                                item.severity === 'High' ? 'text-bloomberg-red bg-bloomberg-red/10 border-bloomberg-red/30' :
                                                                                item.severity === 'Medium' ? 'text-bloomberg-amber bg-bloomberg-amber/10 border-bloomberg-amber/30' :
                                                                                'text-zinc-400 bg-zinc-800/50 border-zinc-700'
                                                                            }`}>
                                                                                {item.severity} SEVERITY
                                                                            </span>
                                                                        </div>
                                                                        <p class="text-xs text-zinc-300 italic">"{item.critique}"</p>
                                                                    </div>
                                                                ))}
                                                            </div>
                                                        </div>
                                                    )}

                                                    {/* Cross-Talk Log */}
                                                    {activeExpertData.cross_talk_log && activeExpertData.cross_talk_log.length > 0 && (
                                                        <div class="bg-bloomberg-dark/60 border border-bloomberg-border rounded-xl p-4 flex flex-col gap-3">
                                                            <h4 class="text-xs uppercase font-extrabold tracking-wider text-bloomberg-cyan flex items-center gap-1.5">
                                                                <svg xmlns="http://www.w3.org/2000/svg" class="w-4.5 h-4.5 text-bloomberg-cyan animate-pulse" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                                                    <path d="m22 2-7 20-4-9-9-4Z"/>
                                                                    <path d="M22 2 11 13"/>
                                                                </svg>
                                                                Supervisor Cross-Talk Interventions
                                                            </h4>
                                                            <div class="flex flex-col gap-3">
                                                                {activeExpertData.cross_talk_log.map((item, idx) => (
                                                                    <div key={idx} class="bg-bloomberg-card border border-bloomberg-border/50 rounded-lg p-3 flex flex-col gap-1.5">
                                                                        <div class="flex items-center justify-between gap-2 border-b border-bloomberg-border/30 pb-1.5 mb-1">
                                                                            <div class="flex items-center gap-2">
                                                                                <span class="text-[10px] font-bold text-zinc-400 font-mono font-bold">SOURCE:</span>
                                                                                <span class="text-xs font-bold text-bloomberg-amber font-mono uppercase">{item.source_expert.replace('_', ' ')}</span>
                                                                            </div>
                                                                            <div class="flex items-center gap-2">
                                                                                <svg xmlns="http://www.w3.org/2000/svg" class="w-3 h-3 text-zinc-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                                                                    <polyline points="9 18 15 12 9 6"/>
                                                                                </svg>
                                                                                <span class="text-[10px] font-bold text-zinc-400 font-mono font-bold">TARGET:</span>
                                                                                <span class="text-xs font-bold text-bloomberg-cyan font-mono uppercase">{item.target_expert.replace('_', ' ')}</span>
                                                                            </div>
                                                                        </div>
                                                                        <p class="text-xs text-zinc-300 italic">"{item.instruction}"</p>
                                                                    </div>
                                                                ))}
                                                            </div>
                                                        </div>
                                                    )}
                                                </div>
                                            )}

                                            {/* Bull/Bear Columns for Non-Risk Experts */}
                                            {activeExpertTab !== 'risk' && (
                                                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                                    <div class="bg-bloomberg-green/5 border border-bloomberg-green/20 rounded-xl p-4">
                                                        <h5 class="text-xs font-bold text-bloomberg-green mb-2 flex items-center gap-1.5">
                                                            <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                                                <polyline points="18 15 12 9 6 15"/>
                                                            </svg>
                                                            Bull Case Scenario
                                                        </h5>
                                                        <p class="text-xs text-zinc-300 leading-relaxed whitespace-pre-wrap">{activeExpertData.bull_case}</p>
                                                    </div>
                                                    <div class="bg-bloomberg-red/5 border border-bloomberg-red/20 rounded-xl p-4">
                                                        <h5 class="text-xs font-bold text-bloomberg-red mb-2 flex items-center gap-1.5">
                                                            <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                                                <polyline points="6 9 12 15 18 9"/>
                                                            </svg>
                                                            Bear Case Scenario
                                                        </h5>
                                                        <p class="text-xs text-zinc-300 leading-relaxed whitespace-pre-wrap">{activeExpertData.bear_case}</p>
                                                    </div>
                                                </div>
                                            )}
                                        </div>
                                    )}
                                </div>
                            </div>
                        </section>
                    </main>
                </div>
            );
        }

        // Subcomponent: Tab Button
        function TabButton({ id, label, active, onClick }) {
            const isActive = active === id;
            return (
                <button
                    onClick={() => onClick(id)}
                    class={`px-4 py-2 font-bold text-xs rounded-lg transition-all duration-300 ${
                        isActive 
                            ? 'bg-bloomberg-cyan text-bloomberg-dark shadow-[0_0_12px_rgba(0,225,255,0.3)]' 
                            : 'bg-zinc-900/60 border border-bloomberg-border/50 text-zinc-400 hover:text-zinc-200'
                    }`}
                >
                    {label}
                </button>
            );
        }

        // Subcomponent: Agent Card in Handoff Timeline
        function AgentCard({ title, desc, status, icon }) {
            const getStatusStyle = () => {
                if (status === 'complete') return 'border-bloomberg-green/40 bg-bloomberg-green/5 text-bloomberg-green shadow-[0_0_10px_rgba(0,255,102,0.05)]';
                if (status === 'thinking') return 'thinking-card bg-bloomberg-cyan/5 text-bloomberg-cyan';
                return 'border-bloomberg-border bg-bloomberg-card text-zinc-400 opacity-60';
            };

            const getBadge = () => {
                if (status === 'complete') {
                    return (
                        <span class="text-xs font-bold text-bloomberg-green bg-bloomberg-green/10 border border-bloomberg-green/30 px-2 py-0.5 rounded flex items-center gap-1">
                            <svg xmlns="http://www.w3.org/2000/svg" class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                                <polyline points="20 6 9 17 4 12"/>
                            </svg>
                            COMPLETED
                        </span>
                    );
                }
                if (status === 'thinking') {
                    return (
                        <span class="text-xs font-bold text-bloomberg-cyan bg-bloomberg-cyan/10 border border-bloomberg-cyan/30 px-2 py-0.5 rounded flex items-center gap-1">
                            <div class="w-2.5 h-2.5 border-2 border-bloomberg-cyan border-t-transparent rounded-full animate-spin"></div>
                            THINKING
                        </span>
                    );
                }
                return <span class="text-xs text-zinc-600 bg-zinc-900 border border-zinc-800 px-2 py-0.5 rounded">IDLE</span>;
            };

            return (
                <div class={`flex items-start gap-4 border rounded-xl p-4 transition-all duration-300 ${getStatusStyle()}`}>
                    <div class={`w-10 h-10 rounded-lg flex items-center justify-center border ${
                        status === 'complete' ? 'border-bloomberg-green/30 bg-bloomberg-green/10' :
                        status === 'thinking' ? 'border-bloomberg-cyan/30 bg-bloomberg-cyan/10' :
                        'border-zinc-800 bg-zinc-900'
                    }`}>
                        <AgentIcon type={icon} />
                    </div>
                    <div class="flex-1 min-w-0 font-sans">
                        <div class="flex justify-between items-center gap-2 mb-1">
                            <h3 class="font-bold text-sm text-white truncate">{title}</h3>
                            {getBadge()}
                        </div>
                        <p class="text-xs text-zinc-400 line-clamp-1">{desc}</p>
                    </div>
                </div>
            );
        }

        // Subcomponent: Quick Metric Stat Card
        function MetricCard({ title, value, IconComponent, color }) {
            return (
                <div class="bg-bloomberg-card border border-bloomberg-border rounded-xl p-3 sm:p-4 flex items-center gap-2 sm:gap-3 xl:gap-4 shadow-xl select-none min-w-0">
                    <div class={`w-8 h-8 sm:w-10 sm:h-10 rounded-lg flex items-center justify-center shrink-0 ${color}`}>
                        <IconComponent className="w-4 h-4 sm:w-5 h-5" />
                    </div>
                    <div class="min-w-0 flex-1">
                        <p class="text-[9px] sm:text-[10px] uppercase font-bold tracking-wider text-zinc-500 whitespace-nowrap overflow-hidden text-ellipsis">{title}</p>
                        <p class="mono font-bold text-sm sm:text-base text-white whitespace-nowrap overflow-x-auto scrollbar-none">{value}</p>
                    </div>
                </div>
            );
        }

        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<App />);
    </script>
</body>
</html>
"""
