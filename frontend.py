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
                        surface: {
                            base: '#09090b',
                            card: '#111113',
                            raised: '#18181b',
                            border: '#27272a',
                            muted: '#3f3f46',
                        },
                        accent: {
                            cyan:  '#22d3ee',   // sky-400
                            green: '#4ade80',   // green-400
                            red:   '#f87171',   // red-400
                            amber: '#fbbf24',   // amber-400
                            blue:  '#60a5fa',   // blue-400
                            purple:'#c084fc',   // purple-400
                            pink:  '#f472b6',   // pink-400
                        }
                    },
                    fontFamily: {
                        sans: ['Inter', 'sans-serif'],
                        mono: ['JetBrains Mono', 'monospace'],
                    }
                }
            }
        }
    </script>
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,300;0,14..32,400;0,14..32,500;0,14..32,600;0,14..32,700;0,14..32,800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { box-sizing: border-box; }
        body {
            font-family: 'Inter', sans-serif;
            background-color: #09090b;
            -webkit-font-smoothing: antialiased;
        }
        .mono { font-family: 'JetBrains Mono', monospace; }

        /* Thin accent scrollbars */
        ::-webkit-scrollbar { width: 5px; height: 5px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #3f3f46; border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: #52525b; }
        .scrollbar-none::-webkit-scrollbar { display: none; }
        .scrollbar-none { -ms-overflow-style: none; scrollbar-width: none; }

        /* Thinking pulse — subtle glow */
        @keyframes thinking-pulse {
            0%, 100% { box-shadow: 0 0 0px rgba(34,211,238,0); border-color: #3f3f46; }
            50% { box-shadow: 0 0 14px rgba(34,211,238,0.12); border-color: rgba(34,211,238,0.35); }
        }
        .thinking-card { animation: thinking-pulse 2.4s ease-in-out infinite; }

        /* Nav tab active indicator */
        .tab-active {
            background: linear-gradient(135deg, rgba(34,211,238,0.12), rgba(34,211,238,0.04));
            border-color: rgba(34,211,238,0.3);
            color: #e4e4e7;
        }
        .tab-inactive {
            background: transparent;
            border-color: transparent;
            color: #71717a;
        }
        .tab-inactive:hover { color: #a1a1aa; background: rgba(255,255,255,0.03); }

        /* Prose overrides for markdown */
        .prose h1, .prose h2, .prose h3 { color: #f4f4f5; font-weight: 700; }
        .prose h1 { font-size: 1.15rem; border-bottom: 1px solid #27272a; padding-bottom: 0.5rem; margin-bottom: 1rem; }
        .prose h2 { font-size: 1rem; margin-top: 1.4rem; color: #e4e4e7; }
        .prose h3 { font-size: 0.875rem; color: #a1a1aa; }
        .prose p { color: #d4d4d8; line-height: 1.7; font-size: 0.875rem; }
        .prose ul { color: #d4d4d8; }
        .prose li { margin-bottom: 0.25rem; font-size: 0.875rem; }
        .prose strong { color: #f4f4f5; font-weight: 600; }
        .prose code { color: #22d3ee; background: rgba(34,211,238,0.08); padding: 0.1em 0.4em; border-radius: 4px; font-size: 0.8em; }
        .prose hr { border-color: #27272a; }
        .prose blockquote { border-left-color: #22d3ee; color: #a1a1aa; font-style: italic; }
    </style>
    <!-- React & Babel CDNs -->
    <script src="https://unpkg.com/react@18/umd/react.production.min.js" crossorigin></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js" crossorigin></script>
    <script src="https://unpkg.com/@babel/standalone@7.15.0/babel.min.js"></script>
    <!-- Marked.js -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/marked/4.3.0/marked.min.js"></script>
    <!-- html2pdf.js -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
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

        // DownloadIcon
        function DownloadIcon({ className = "w-5 h-5 text-bloomberg-cyan" }) {
            return (
                <svg xmlns="http://www.w3.org/2000/svg" class={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                    <polyline points="7 10 12 15 17 10"/>
                    <line x1="12" y1="15" x2="12" y2="3"/>
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

            if (type === 'hash') {
                return <HashIcon className={className} />;
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
            const [activeTab, setActiveTab] = useState("setup"); // 'setup', 'logs', 'summary'
            const [apiKey, setApiKey] = useState("");
            const [selectedModel, setSelectedModel] = useState("auto");
            const [averageRuntimes, setAverageRuntimes] = useState({});
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
                technical: 'idle',
                risk: 'idle',
                synthesis: 'idle'
            });

            const exportToPDF = () => {
                const element = document.getElementById('thesis-content');
                if (!element) return;
                const opt = {
                    margin:       0.5,
                    filename:     `${ticker || 'report'}_thesis.pdf`,
                    image:        { type: 'jpeg', quality: 0.98 },
                    html2canvas:  { scale: 2 },
                    jsPDF:        { unit: 'in', format: 'letter', orientation: 'portrait' }
                };
                window.html2pdf().set(opt).from(element).save();
            };

            // Auto-scroll logs
            const logEndRef = useRef(null);
            useEffect(() => {
                logEndRef.current?.scrollIntoView({ behavior: 'smooth' });
            }, [logs]);

            const runAnalysis = () => {
                if (!query.trim()) return;

                // Reset state
                setIsAnalyzing(true);
                setActiveTab("logs");
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

                const url = `/api/stream?query=${encodeURIComponent(query)}&api_key=${encodeURIComponent(apiKey)}&model=${encodeURIComponent(selectedModel)}`;
                const eventSource = new EventSource(url);

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
                                nextStates.technical = 'thinking';
                                nextStates.risk = 'idle';
                            }

                            // Complete individual experts in Phase 1
                            if (agent === 'financial' && revCount === 0) nextStates.financial = 'complete';
                            if (agent === 'tech_product' && revCount === 0) nextStates.tech_product = 'complete';
                            if (agent === 'sentiment' && revCount === 0) nextStates.sentiment = 'complete';
                            if (agent === 'macro' && revCount === 0) nextStates.macro = 'complete';
                            if (agent === 'technical' && revCount === 0) nextStates.technical = 'complete';

                            // Phase 2: Once first 4 are complete, active_agent moves to risk
                            if (active_agent === 'risk') {
                                nextStates.financial = 'complete';
                                nextStates.tech_product = 'complete';
                                nextStates.sentiment = 'complete';
                                nextStates.macro = 'complete';
                                nextStates.technical = 'complete';
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
                                    if (['financial', 'tech_product', 'sentiment', 'macro', 'technical'].includes(tgt)) {
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
                        setActiveTab("summary");
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
                <div class="min-h-screen bg-surface-base flex flex-col">
                    {/* Header */}
                    <header class="shrink-0 border-b border-surface-border bg-surface-card/80 backdrop-blur-md px-5 h-14 flex items-center justify-between gap-4 shadow-xl">
                        {/* Brand */}
                        <div class="flex items-center gap-3 shrink-0">
                            <div class="w-7 h-7 rounded-lg bg-gradient-to-br from-accent-cyan/20 to-accent-blue/20 border border-accent-cyan/25 flex items-center justify-center">
                                <CpuIcon className="w-3.5 h-3.5 text-accent-cyan" />
                            </div>
                            <div>
                                <span class="text-sm font-bold text-zinc-100 tracking-tight">Agentic Stock Analyst</span>
                                <span class="hidden sm:inline text-xs text-zinc-600 ml-2 font-normal">/ Institutional AI Committee</span>
                            </div>
                        </div>

                        {/* Pill Tab Navigation */}
                        <nav class="flex items-center gap-1 bg-surface-raised border border-surface-border rounded-xl p-1">
                            {[['setup','Setup'], ['logs','Agent Logs'], ['summary','Summary']].map(([id, label]) => (
                                <button
                                    key={id}
                                    onClick={() => setActiveTab(id)}
                                    class={`px-3.5 py-1.5 text-xs font-semibold rounded-lg border transition-all duration-200 ${activeTab === id ? 'tab-active' : 'tab-inactive'}`}
                                >
                                    {label}
                                </button>
                            ))}
                        </nav>

                        {/* Status row */}
                        <div class="hidden sm:flex items-center gap-3 text-[11px] font-mono text-zinc-500 shrink-0">
                            {isAnalyzing ? (
                                <span class="flex items-center gap-1.5 text-accent-cyan">
                                    <span class="w-1.5 h-1.5 rounded-full bg-accent-cyan animate-ping"></span>
                                    {elapsedTime.toFixed(1)}s
                                </span>
                            ) : totalDuration ? (
                                <span class="flex items-center gap-1.5 text-accent-green">
                                    <span class="w-1.5 h-1.5 rounded-full bg-accent-green"></span>
                                    Done in {totalDuration}s
                                </span>
                            ) : (
                                <span class="flex items-center gap-1.5">
                                    <span class="w-1.5 h-1.5 rounded-full bg-zinc-700"></span>
                                    READY
                                </span>
                            )}
                            <span class="text-zinc-700">|</span>
                            <span class="text-zinc-600">{getModelDisplayName(selectedModel)}</span>
                        </div>
                    </header>

                    {/* Main Area */}
                    <main class="flex-1 p-5 overflow-hidden flex flex-col items-center gap-5">
                        {/* TAB 1: SETUP */}
                        <div class={activeTab === 'setup' ? "w-full max-w-xl flex flex-col gap-5 pt-12" : "hidden"}>
                            {/* Input Card */}
                            <div class="bg-surface-card border border-surface-border rounded-2xl p-7 shadow-2xl flex flex-col gap-5">
                                <div class="flex items-center gap-3 border-b border-surface-border pb-5">
                                    <div class="w-9 h-9 rounded-xl bg-accent-cyan/10 border border-accent-cyan/20 flex items-center justify-center">
                                        <TerminalIcon className="w-4 h-4 text-accent-cyan" />
                                    </div>
                                    <div>
                                        <h2 class="text-sm font-bold text-zinc-100">Analysis Configuration</h2>
                                        <p class="text-xs text-zinc-500 mt-0.5">Configure your ticker and start the AI committee</p>
                                    </div>
                                </div>

                                <div class="flex flex-col gap-1.5">
                                    <label class="text-[11px] font-semibold text-zinc-400 uppercase tracking-widest">Stock Ticker / Query</label>
                                    <input
                                        type="text"
                                        value={query}
                                        onChange={(e) => setQuery(e.target.value)}
                                        onKeyDown={(e) => e.key === 'Enter' && runAnalysis()}
                                        disabled={isAnalyzing}
                                        placeholder="e.g., AAPL, NVDA, TSLA"
                                        class="w-full bg-surface-base border border-surface-border hover:border-surface-muted focus:border-accent-cyan/50 focus:ring-2 focus:ring-accent-cyan/10 rounded-xl px-4 py-3 text-sm text-zinc-100 placeholder-zinc-600 disabled:opacity-40 transition-all outline-none"
                                    />
                                </div>

                                <div class="flex flex-col gap-1.5">
                                    <div class="flex items-center justify-between">
                                        <label class="text-[11px] font-semibold text-zinc-400 uppercase tracking-widest">OpenRouter API Key</label>
                                        <span class="text-[10px] text-zinc-600">Optional — falls back to ENV</span>
                                    </div>
                                    <input
                                        type="password"
                                        value={apiKey}
                                        onChange={(e) => setApiKey(e.target.value)}
                                        disabled={isAnalyzing}
                                        placeholder="sk-or-v1-..."
                                        class="w-full bg-surface-base border border-surface-border hover:border-surface-muted focus:border-accent-cyan/50 focus:ring-2 focus:ring-accent-cyan/10 rounded-xl px-4 py-3 text-sm text-zinc-100 placeholder-zinc-600 disabled:opacity-40 transition-all outline-none mono"
                                    />
                                </div>

                                <div class="flex flex-col gap-1.5">
                                    <div class="flex items-center justify-between">
                                        <label class="text-[11px] font-semibold text-zinc-400 uppercase tracking-widest">Model Selection</label>
                                        <span class="text-[10px] text-zinc-600">Free OpenRouter Models</span>
                                    </div>
                                    <select
                                        value={selectedModel}
                                        onChange={(e) => setSelectedModel(e.target.value)}
                                        disabled={isAnalyzing}
                                        class="w-full bg-surface-base border border-surface-border hover:border-surface-muted focus:border-accent-cyan/50 focus:ring-2 focus:ring-accent-cyan/10 rounded-xl px-4 py-3 text-sm text-zinc-100 placeholder-zinc-600 disabled:opacity-40 transition-all outline-none cursor-pointer appearance-none"
                                        style={{ backgroundImage: "url('data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%23a1a1aa%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13-5.4H18.4c-5%200-9.3%201.8-12.9%205.4A17.6%2017.6%200%200%200%200%2082.2c0%205%201.8%209.3%205.4%2012.9l128%20127.9c3.6%203.6%207.8%205.4%2012.8%205.4s9.2-1.8%2012.8-5.4L287%2095c3.5-3.5%205.4-7.8%205.4-12.8%200-5-1.9-9.2-5.5-12.8z%22%2F%3E%3C%2Fsvg%3E')", backgroundRepeat: "no-repeat", backgroundPosition: "right 1rem top 50%", backgroundSize: "0.65rem auto" }}
                                    >
                                        <option value="auto">Auto-Fallback (All Free Models) {averageRuntimes["auto"] ? `(Avg. ${averageRuntimes["auto"]}s)` : ""}</option>
                                        <option value="meta-llama/llama-3.3-70b-instruct:free">Llama 3.3 70B {averageRuntimes["meta-llama/llama-3.3-70b-instruct:free"] ? `(Avg. ${averageRuntimes["meta-llama/llama-3.3-70b-instruct:free"]}s)` : ""}</option>
                                        <option value="google/gemma-3-27b-it:free">Gemma 3 27B {averageRuntimes["google/gemma-3-27b-it:free"] ? `(Avg. ${averageRuntimes["google/gemma-3-27b-it:free"]}s)` : ""}</option>
                                        <option value="mistralai/mistral-7b-instruct:free">Mistral 7B {averageRuntimes["mistralai/mistral-7b-instruct:free"] ? `(Avg. ${averageRuntimes["mistralai/mistral-7b-instruct:free"]}s)` : ""}</option>
                                        <option value="microsoft/phi-3-medium-128k-instruct:free">Phi-3 Medium {averageRuntimes["microsoft/phi-3-medium-128k-instruct:free"] ? `(Avg. ${averageRuntimes["microsoft/phi-3-medium-128k-instruct:free"]}s)` : ""}</option>
                                        <option value="google/gemma-4-31b-it:free">Gemma 4 31B {averageRuntimes["google/gemma-4-31b-it:free"] ? `(Avg. ${averageRuntimes["google/gemma-4-31b-it:free"]}s)` : ""}</option>
                                    </select>
                                </div>

                                <button
                                    onClick={runAnalysis}
                                    disabled={isAnalyzing || !query.trim()}
                                    class="w-full mt-1 py-3.5 rounded-xl font-bold text-sm flex items-center justify-center gap-2.5 transition-all duration-300 disabled:opacity-40 disabled:cursor-not-allowed bg-accent-cyan text-zinc-900 hover:brightness-110 shadow-lg shadow-accent-cyan/10"
                                >
                                    {isAnalyzing ? (
                                        <>
                                            <div class="w-4 h-4 border-2 border-zinc-900/60 border-t-zinc-900 rounded-full animate-spin"></div>
                                            <span>Running Analysis...</span>
                                        </>
                                    ) : (
                                        <>
                                            <PlayIcon className="w-4 h-4" />
                                            <span>Run Analysis</span>
                                        </>
                                    )}
                                </button>
                            </div>

                            {/* Feature chips */}
                            <div class="grid grid-cols-3 gap-3">
                                {[['📊', 'Financial Analysis', '5 domain experts'],
                                  ['🔍', 'Real-Time Data', 'yfinance + DDG'],
                                  ['🛡️', 'Risk Auditor', 'Peer review loop']
                                ].map(([icon, title, sub]) => (
                                    <div key={title} class="bg-surface-card border border-surface-border rounded-xl p-3.5 text-center">
                                        <div class="text-lg mb-1.5">{icon}</div>
                                        <p class="text-xs font-semibold text-zinc-300">{title}</p>
                                        <p class="text-[10px] text-zinc-600 mt-0.5">{sub}</p>
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* TAB 2: EXECUTION LOGS */}
                        <div class={activeTab === 'logs' ? "w-full flex-1 min-h-0 grid grid-cols-1 lg:grid-cols-2 gap-4" : "hidden"}>
                            {/* Agent Handoff Timeline */}
                            <div class="bg-surface-card border border-surface-border rounded-2xl p-4 flex flex-col gap-3 flex-1 min-h-0 overflow-y-auto">
                                <div class="flex items-center gap-2 border-b border-surface-border pb-3 shrink-0">
                                    <GitBranchIcon className="w-3.5 h-3.5 text-accent-cyan" />
                                    <h2 class="text-xs font-bold text-zinc-400 uppercase tracking-wider">Committee Handoff Pipeline</h2>
                                </div>

                                <div class="flex flex-col gap-2">
                                    {/* Supervisor */}
                                    <AgentCard
                                        title="Supervisor"
                                        desc="Orchestrates committee, extracts ticker"
                                        status={agentStates.supervisor}
                                        icon="supervisor"
                                        color="cyan"
                                    />
                                    {/* Data Gatherer */}
                                    <AgentCard
                                        title="Data Fetcher"
                                        desc="Parallel pre-fetch: financials, news, macro"
                                        status={agentStates.prefetch}
                                        icon="download-cloud"
                                        color="blue"
                                    />
                                    <div class="grid grid-cols-2 md:grid-cols-3 gap-2">
                                        <AgentCard title="Financial" desc="Fundamentals & valuation" status={agentStates.financial} icon="financial" color="green" compact />
                                        <AgentCard title="Tech Moat" desc="Competitive moat & pipeline" status={agentStates.tech_product} icon="tech_product" color="blue" compact />
                                        <AgentCard title="Sentiment" desc="Media & narrative analysis" status={agentStates.sentiment} icon="sentiment" color="pink" compact />
                                        <AgentCard title="Macro" desc="Sector & macro indices" status={agentStates.macro} icon="macro" color="amber" compact />
                                        <AgentCard title="Technical" desc="Charts & indicators" status={agentStates.technical} icon="hash" color="purple" compact />
                                    </div>
                                    <AgentCard
                                        title="Risk Auditor"
                                        desc="Cross-examines all expert reports"
                                        status={agentStates.risk}
                                        icon="risk"
                                        color="red"
                                    />
                                    <AgentCard
                                        title="Synthesis Compiler"
                                        desc="Generates final investment thesis"
                                        status={agentStates.synthesis}
                                        icon="supervisor"
                                        color="purple"
                                    />
                                </div>
                            </div>

                            {/* Live Console Output */}
                            <div class="bg-surface-card border border-surface-border rounded-2xl p-4 flex flex-col gap-3 h-full min-h-0 overflow-hidden">
                                <div class="flex items-center justify-between border-b border-surface-border pb-3 shrink-0">
                                    <div class="flex items-center gap-2">
                                        <TerminalIcon className="w-3.5 h-3.5 text-accent-cyan" />
                                        <h2 class="text-xs font-bold text-zinc-400 uppercase tracking-wider">Graph Console</h2>
                                    </div>
                                    <span class="text-[10px] mono text-zinc-600">{logs.length} events</span>
                                </div>
                                <div class="flex-1 bg-surface-base/80 rounded-xl p-3 overflow-y-auto mono text-[11px] flex flex-col gap-1 border border-surface-border/60">
                                    {logs.length === 0 ? (
                                        <span class="text-zinc-600 italic">Waiting for analysis trigger...</span>
                                    ) : (
                                        logs.map((log, idx) => {
                                            const typeStyles = {
                                                system:     'text-zinc-600',
                                                supervisor: 'text-accent-cyan',
                                                backend:    'text-accent-purple',
                                                financial:  'text-accent-green',
                                                tech_product:'text-accent-blue',
                                                sentiment:  'text-accent-pink',
                                                macro:      'text-accent-amber',
                                                risk:       'text-accent-red',
                                                success:    'text-accent-green',
                                                error:      'text-accent-red',
                                                info:       'text-zinc-400',
                                            };
                                            const style = typeStyles[log.type] || 'text-zinc-500';
                                            return (
                                                <div key={idx} class="flex gap-2 items-start leading-relaxed">
                                                    <span class={`${style} font-bold shrink-0 select-none`}>[{(log.type||'sys').toUpperCase()}]</span>
                                                    <span class="text-zinc-300 break-all">{log.message}</span>
                                                </div>
                                            );
                                        })
                                    )}
                                    <div ref={logEndRef}></div>
                                </div>
                            </div>
                        </div>

                        {/* TAB 3: EXECUTIVE SUMMARY */}
                        <div class={activeTab === 'summary' ? "w-full max-w-5xl flex-1 min-h-0 flex flex-col gap-4 overflow-y-auto pr-0.5 pb-10" : "hidden"}>
                            {/* Metric chips */}
                            <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-2.5 shrink-0">
                                <MetricCard title="Ticker" value={ticker || "—"} IconComponent={HashIcon} color="text-accent-cyan bg-accent-cyan/10" />
                                <MetricCard title="Price" value={metrics.price !== "—" ? `$${metrics.price}` : "—"} IconComponent={DollarIcon} color="text-accent-green bg-accent-green/10" />
                                <MetricCard title="P/E Ratio" value={metrics.pe || "—"} IconComponent={PieChartIcon} color="text-accent-amber bg-accent-amber/10" />
                                <MetricCard title="50-Day SMA" value={metrics.sma50 !== "—" ? `$${metrics.sma50}` : "—"} IconComponent={TrendingUpIcon} color="text-accent-blue bg-accent-blue/10" />
                                <MetricCard title="200-Day SMA" value={metrics.sma200 !== "—" ? `$${metrics.sma200}` : "—"} IconComponent={ActivityIcon} color="text-accent-purple bg-accent-purple/10" />
                            </div>

                            {/* Markdown Report Container */}
                            <div class="bg-surface-card border border-surface-border rounded-2xl p-6 shadow-xl flex flex-col shrink-0 min-h-[300px]">
                                <div class="flex justify-between items-center border-b border-bloomberg-border/50 pb-4 mb-4">
                                    <h2 class="font-bold text-zinc-100 text-sm flex items-center gap-2">
                                        <FileTextIcon className="w-4 h-4 text-accent-cyan" />
                                        Investment Committee Thesis
                                    </h2>
                                    <div class="flex items-center gap-2">
                                        <button onClick={exportToPDF} class="flex items-center gap-1.5 px-3 py-1.5 text-[11px] font-medium text-accent-cyan bg-accent-cyan/10 hover:bg-accent-cyan/20 border border-accent-cyan/20 rounded-lg transition-colors" title="Download Report">
                                            <DownloadIcon className="w-3.5 h-3.5" />
                                            Export PDF
                                        </button>
                                        <span class="mono text-[10px] text-zinc-600 bg-surface-base border border-surface-border px-2.5 py-1 rounded-lg">
                                            {ticker || "Pending"}
                                        </span>
                                    </div>
                                </div>
                                
                                <div id="thesis-content"
                                    class="flex-1 prose prose-invert max-w-none text-zinc-300 text-sm leading-relaxed"
                                    dangerouslySetInnerHTML={{ __html: renderMarkdown(report || streamingText.supervisor) }}
                                ></div>
                            </div>

                            {/* TradingView Advanced Chart */}
                            {ticker && (
                                <div class="bg-surface-card border border-surface-border rounded-2xl p-6 shadow-xl flex flex-col shrink-0 h-[500px]">
                                    <div class="border-b border-bloomberg-border/50 pb-4 mb-4">
                                        <h2 class="font-bold text-zinc-100 text-sm flex items-center gap-2">
                                            <ActivityIcon className="w-4 h-4 text-accent-green" />
                                            Technical Price Action
                                        </h2>
                                    </div>
                                    <div class="flex-1 rounded-xl overflow-hidden bg-surface-base">
                                        <TradingViewChart ticker={ticker} />
                                    </div>
                                </div>
                            )}

                            {/* Committee Drill-Down */}
                            <div class="bg-surface-card border border-surface-border rounded-2xl p-5 shadow-xl flex flex-col shrink-0">
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
                                <div class={`rounded-xl p-5 border transition-colors duration-500 ${
                                    activeExpertTab === 'financial' ? 'bg-bloomberg-green/5 border-bloomberg-green/30' :
                                    activeExpertTab === 'tech_product' ? 'bg-blue-500/5 border-blue-500/30' :
                                    activeExpertTab === 'sentiment' ? 'bg-pink-500/5 border-pink-500/30' :
                                    activeExpertTab === 'macro' ? 'bg-yellow-500/5 border-yellow-500/30' :
                                    activeExpertTab === 'risk' ? 'bg-bloomberg-amber/5 border-bloomberg-amber/30' :
                                    'bg-bloomberg-dark/40 border-bloomberg-border/60'
                                }`}>
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
                                                                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-bloomberg-amber" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
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
                                                                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-bloomberg-cyan animate-pulse" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
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
                        </div>
                    </main>
                </div>
            );
        }

        // Subcomponent: Tab Button (Expert Drill-Down)
        function TabButton({ id, label, active, onClick }) {
            const isActive = active === id;
            return (
                <button
                    onClick={() => onClick(id)}
                    class={`px-3.5 py-1.5 font-semibold text-[11px] rounded-lg border transition-all duration-200 ${
                        isActive
                            ? 'bg-surface-raised border-surface-muted text-zinc-200 shadow-sm'
                            : 'bg-transparent border-transparent text-zinc-500 hover:text-zinc-300 hover:bg-surface-raised/60'
                    }`}
                >
                    {label}
                </button>
            );
        }

        // Subcomponent: Agent Card in Handoff Timeline
        function AgentCard({ title, desc, status, icon, color = 'cyan', compact = false }) {
            const colorMap = {
                cyan:   { ring: 'border-accent-cyan/30 bg-accent-cyan/5',   icon: 'border-accent-cyan/25 bg-accent-cyan/10',   text: 'text-accent-cyan',   badge: 'text-accent-cyan bg-accent-cyan/10 border-accent-cyan/25' },
                green:  { ring: 'border-accent-green/30 bg-accent-green/5',  icon: 'border-accent-green/25 bg-accent-green/10',  text: 'text-accent-green',  badge: 'text-accent-green bg-accent-green/10 border-accent-green/25' },
                blue:   { ring: 'border-accent-blue/30 bg-accent-blue/5',    icon: 'border-accent-blue/25 bg-accent-blue/10',    text: 'text-accent-blue',   badge: 'text-accent-blue bg-accent-blue/10 border-accent-blue/25' },
                amber:  { ring: 'border-accent-amber/30 bg-accent-amber/5',  icon: 'border-accent-amber/25 bg-accent-amber/10',  text: 'text-accent-amber',  badge: 'text-accent-amber bg-accent-amber/10 border-accent-amber/25' },
                pink:   { ring: 'border-accent-pink/30 bg-accent-pink/5',    icon: 'border-accent-pink/25 bg-accent-pink/10',    text: 'text-accent-pink',   badge: 'text-accent-pink bg-accent-pink/10 border-accent-pink/25' },
                red:    { ring: 'border-accent-red/30 bg-accent-red/5',      icon: 'border-accent-red/25 bg-accent-red/10',      text: 'text-accent-red',    badge: 'text-accent-red bg-accent-red/10 border-accent-red/25' },
                purple: { ring: 'border-accent-purple/30 bg-accent-purple/5',icon: 'border-accent-purple/25 bg-accent-purple/10',text: 'text-accent-purple', badge: 'text-accent-purple bg-accent-purple/10 border-accent-purple/25' },
            };
            const c = colorMap[color] || colorMap.cyan;

            const borderStyle =
                status === 'complete' ? `border ${c.ring}`
                : status === 'thinking' ? `thinking-card border`
                : 'border border-surface-border bg-surface-raised/30 opacity-50';

            const getBadge = () => {
                if (status === 'complete') return (
                    <span class={`text-[10px] font-bold px-2 py-0.5 rounded-md border flex items-center gap-1 ${c.badge} shrink-0`}>
                        <svg xmlns="http://www.w3.org/2000/svg" class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                        DONE
                    </span>
                );
                if (status === 'thinking') return (
                    <span class={`text-[10px] font-bold px-2 py-0.5 rounded-md border flex items-center gap-1.5 ${c.badge} shrink-0`}>
                        <div class={`w-2 h-2 border border-t-transparent rounded-full animate-spin ${c.text.replace('text','border')}`}></div>
                        WORKING
                    </span>
                );
                return <span class="text-[10px] text-zinc-700 bg-surface-base border border-surface-border px-2 py-0.5 rounded-md shrink-0">IDLE</span>;
            };

            return (
                <div class={`flex items-center gap-3 rounded-xl p-3 transition-all duration-300 ${borderStyle}`}>
                    <div class={`${compact ? 'w-7 h-7' : 'w-8 h-8'} rounded-lg flex items-center justify-center border shrink-0 ${
                        status === 'complete' ? c.icon
                        : status === 'thinking' ? c.icon
                        : 'border-surface-border bg-surface-base'
                    }`}>
                        <AgentIcon type={icon} className={`${compact ? 'w-3.5 h-3.5' : 'w-4 h-4'} ${status !== 'idle' ? c.text : 'text-zinc-600'}`} />
                    </div>
                    <div class="flex-1 min-w-0">
                        <div class="flex items-center justify-between gap-2">
                            <h3 class={`font-semibold ${compact ? 'text-[11px]' : 'text-xs'} text-zinc-200 truncate`}>{title}</h3>
                            {getBadge()}
                        </div>
                        {!compact && <p class="text-[10px] text-zinc-500 mt-0.5 truncate">{desc}</p>}
                    </div>
                </div>
            );
        }

        // Subcomponent: Quick Metric Stat Card
        function MetricCard({ title, value, IconComponent, color }) {
            return (
                <div class="bg-surface-card border border-surface-border rounded-xl p-3 flex items-center gap-3 shadow-lg select-none min-w-0">
                    <div class={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 ${color}`}>
                        <IconComponent className="w-4 h-4" />
                    </div>
                    <div class="min-w-0 flex-1">
                        <p class="text-[9px] uppercase font-bold tracking-widest text-zinc-600 truncate">{title}</p>
                        <p class="mono font-bold text-sm text-zinc-100 truncate">{value}</p>
                    </div>
                </div>
            );
        }

        function TradingViewChart({ ticker }) {
            const container = useRef();
            
            useEffect(() => {
                if (!container.current) return;
                container.current.innerHTML = '';
                const script = document.createElement("script");
                script.src = "https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js";
                script.type = "text/javascript";
                script.async = true;
                script.innerHTML = `
                {
                    "autosize": true,
                    "symbol": "${ticker.toUpperCase()}",
                    "interval": "D",
                    "timezone": "Etc/UTC",
                    "theme": "dark",
                    "style": "1",
                    "locale": "en",
                    "allow_symbol_change": true,
                    "calendar": false,
                    "support_host": "https://www.tradingview.com"
                }`;
                container.current.appendChild(script);
            }, [ticker]);

            return (
                <div class="tradingview-widget-container" ref={container} style={{ height: "100%", width: "100%" }}>
                    <div class="tradingview-widget-container__widget" style={{ height: "calc(100% - 32px)", width: "100%" }}></div>
                </div>
            );
        }

        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<App />);
    </script>
</body>
</html>
"""
