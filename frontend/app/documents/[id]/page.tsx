"use client";

import { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Loader2, AlertTriangle, Shield, CheckCircle, MessageSquare, FileText, ArrowLeft, Send } from "lucide-react";
import { cn } from "@/lib/utils";
import Link from "next/link";

interface RiskAnalysis {
    risk_score: number;
    risk_level: string;
    flagged_clauses: Array<{
        clause_text: string;
        risk_reason: string;
    }>;
    explanation: string;
}

export default function DocumentPage() {
    const { id } = useParams();
    const [analysis, setAnalysis] = useState<RiskAnalysis | null>(null);
    const [analyzing, setAnalyzing] = useState(false);
    const [chatQuery, setChatQuery] = useState("");
    const [chatHistory, setChatHistory] = useState<Array<{ role: 'user' | 'assistant', content: string }>>([]);
    const [chatting, setChatting] = useState(false);
    const [activeTab, setActiveTab] = useState<'analysis' | 'chat'>('analysis');

    const runAnalysis = async () => {
        setAnalyzing(true);
        try {
            const res = await fetch(`http://localhost:8000/documents/${id}/analyze`, { method: "POST" });
            const data = await res.json();
            setAnalysis(data);
        } catch (e) {
            console.error(e);
            alert("Analysis failed");
        } finally {
            setAnalyzing(false);
        }
    };

    const sendChat = async () => {
        if (!chatQuery.trim()) return;

        const query = chatQuery;
        setChatQuery("");
        setChatHistory(prev => [...prev, { role: 'user', content: query }]);
        setChatting(true);

        try {
            const res = await fetch("http://localhost:8000/chat/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ document_id: id, query }),
            });
            const data = await res.json();
            setChatHistory(prev => [...prev, { role: 'assistant', content: data.answer }]);
        } catch (e) {
            console.error(e);
            setChatHistory(prev => [...prev, { role: 'assistant', content: "Error: Could not get answer." }]);
        } finally {
            setChatting(false);
        }
    };

    return (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 animate-fade-in-up h-[calc(100vh-8rem)]">
            {/* Sidebar / Controls */}
            <div className="lg:col-span-1 space-y-6 flex flex-col">
                <Link href="/" className="inline-flex items-center text-sm text-zinc-400 hover:text-white transition-colors">
                    <ArrowLeft className="w-4 h-4 mr-1" /> Back to Dashboard
                </Link>

                <Card className="glass-panel border-zinc-800">
                    <CardHeader>
                        <CardTitle>Document Actions</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="flex gap-2 p-1 bg-zinc-900/50 rounded-lg border border-white/5">
                            <Button
                                variant="ghost"
                                onClick={() => setActiveTab('analysis')}
                                className={cn(
                                    "flex-1 transition-all rounded-md",
                                    activeTab === 'analysis' ? "bg-primary/20 text-primary shadow-sm" : "text-zinc-400 hover:text-white"
                                )}
                            >
                                <Shield className="w-4 h-4 mr-2" /> Risk
                            </Button>
                            <Button
                                variant="ghost"
                                onClick={() => setActiveTab('chat')}
                                className={cn(
                                    "flex-1 transition-all rounded-md",
                                    activeTab === 'chat' ? "bg-blue-500/20 text-blue-400 shadow-sm" : "text-zinc-400 hover:text-white"
                                )}
                            >
                                <MessageSquare className="w-4 h-4 mr-2" /> Chat
                            </Button>
                        </div>
                    </CardContent>
                </Card>

                {analysis && (
                    <Card className="glass-panel border-zinc-800 animate-in fade-in slide-in-from-bottom-4 duration-500">
                        <CardHeader>
                            <CardTitle>Risk Score</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="flex items-center justify-center py-6">
                                <div className={cn(
                                    "relative w-40 h-40 rounded-full flex items-center justify-center border-8 text-5xl font-bold transition-all shadow-2xl",
                                    analysis.risk_score > 70 ? "border-rose-500 text-rose-500 shadow-rose-900/20" :
                                        analysis.risk_score > 40 ? "border-amber-500 text-amber-500 shadow-amber-900/20" :
                                            "border-emerald-500 text-emerald-500 shadow-emerald-900/20"
                                )}>
                                    {analysis.risk_score}
                                </div>
                            </div>
                            <div className="text-center">
                                <span className={cn(
                                    "px-3 py-1 rounded-full text-sm font-medium border",
                                    analysis.risk_score > 70 ? "bg-rose-500/10 border-rose-500/20 text-rose-400" :
                                        analysis.risk_score > 40 ? "bg-amber-500/10 border-amber-500/20 text-amber-400" :
                                            "bg-emerald-500/10 border-emerald-500/20 text-emerald-400"
                                )}>
                                    {analysis.risk_level} Risk Level
                                </span>
                            </div>
                        </CardContent>
                    </Card>
                )}
            </div>

            {/* Main Content */}
            <div className="lg:col-span-2 h-full flex flex-col">
                <Card className="glass-panel border-zinc-800 flex-1 flex flex-col h-full overflow-hidden shadow-2xl">
                    <CardHeader className="border-b border-white/5 bg-zinc-900/30">
                        <CardTitle className="flex items-center">
                            {activeTab === 'analysis' ? (
                                <>
                                    <Shield className="w-5 h-5 mr-3 text-primary" />
                                    Detailed Risk Analysis
                                </>
                            ) : (
                                <>
                                    <MessageSquare className="w-5 h-5 mr-3 text-blue-400" />
                                    Chat with Contract
                                </>
                            )}
                        </CardTitle>
                    </CardHeader>
                    <CardContent className="flex-1 overflow-y-auto p-6 scrollbar-thin scrollbar-thumb-zinc-700 scrollbar-track-transparent">

                        {activeTab === 'analysis' && (
                            <div className="space-y-8">
                                {!analysis ? (
                                    <div className="flex flex-col items-center justify-center h-full text-center space-y-6 pt-12">
                                        <div className="w-20 h-20 bg-zinc-900 rounded-2xl flex items-center justify-center border border-zinc-800 shadow-xl">
                                            <Shield className="w-10 h-10 text-zinc-600" />
                                        </div>
                                        <div>
                                            <h3 className="text-xl font-semibold text-white">Analysis Pending</h3>
                                            <p className="text-zinc-400 mt-2 max-w-sm">Run our AI engine to scan for legal risks, liability caps, and unusual clauses.</p>
                                        </div>
                                        <Button
                                            onClick={runAnalysis}
                                            disabled={analyzing}
                                            size="lg"
                                            className="bg-primary hover:bg-primary/90 text-white shadow-lg shadow-emerald-900/20 px-8"
                                        >
                                            {analyzing ? <Loader2 className="w-4 h-4 mr-2 animate-spin" /> : "Run AI Risk Analysis"}
                                        </Button>
                                    </div>
                                ) : (
                                    <div className="space-y-6 animate-in fade-in duration-500">
                                        <div className="bg-zinc-900/50 p-6 rounded-xl border border-white/5">
                                            <h4 className="font-semibold text-zinc-200 mb-3 flex items-center">
                                                <FileText className="w-4 h-4 mr-2 text-zinc-400" /> Executive Summary
                                            </h4>
                                            <p className="text-zinc-400 leading-relaxed text-sm">{analysis.explanation}</p>
                                        </div>

                                        <div>
                                            <h4 className="font-semibold text-lg text-white mb-4 flex items-center">
                                                <AlertTriangle className="w-5 h-5 mr-2 text-amber-500" />
                                                Flagged Clauses ({analysis.flagged_clauses.length})
                                            </h4>

                                            <div className="space-y-4">
                                                {analysis.flagged_clauses.map((clause, idx) => (
                                                    <div key={idx} className="group bg-rose-950/10 border border-rose-900/20 hover:border-rose-900/40 p-5 rounded-xl transition-colors">
                                                        <div className="flex items-start gap-4">
                                                            <div className="mt-1 shrink-0">
                                                                <AlertTriangle className="w-4 h-4 text-rose-500" />
                                                            </div>
                                                            <div className="space-y-2">
                                                                <p className="text-sm font-mono text-rose-200/80 bg-rose-950/30 p-2 rounded border border-rose-900/20">
                                                                    "{clause.clause_text}"
                                                                </p>
                                                                <p className="text-sm text-rose-300 font-medium leading-relaxed">
                                                                    Review: {clause.risk_reason}
                                                                </p>
                                                            </div>
                                                        </div>
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                    </div>
                                )}
                            </div>
                        )}

                        {activeTab === 'chat' && (
                            <div className="flex flex-col h-full">
                                <div className="flex-1 space-y-4 mb-4">
                                    {chatHistory.length === 0 && (
                                        <div className="flex flex-col items-center justify-center h-full text-center text-zinc-500 space-y-2">
                                            <MessageSquare className="w-8 h-8 opacity-20" />
                                            <p>Ask questions about the contract.</p>
                                            <p className="text-xs opacity-50">e.g., "What is the termination clause?"</p>
                                        </div>
                                    )}
                                    {chatHistory.map((msg, i) => (
                                        <div key={i} className={cn(
                                            "p-4 rounded-2xl max-w-[80%] w-fit text-sm leading-relaxed shadow-md",
                                            msg.role === 'user'
                                                ? "bg-primary text-white ml-auto rounded-br-none"
                                                : "bg-zinc-800 text-zinc-100 mr-auto rounded-bl-none border border-white/5"
                                        )}>
                                            {msg.content}
                                        </div>
                                    ))}
                                    {chatting && (
                                        <div className="bg-zinc-800 text-zinc-400 mr-auto p-4 rounded-2xl rounded-bl-none border border-white/5 flex items-center shadow-md">
                                            <Loader2 className="w-4 h-4 animate-spin mr-2" /> AI is thinking...
                                        </div>
                                    )}
                                </div>

                                <div className="pt-4 border-t border-white/5 flex gap-3">
                                    <div className="relative flex-1">
                                        <input
                                            className="w-full bg-zinc-900 border border-zinc-700 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-transparent transition-all placeholder:text-zinc-600 text-white"
                                            placeholder="Ask about this document..."
                                            value={chatQuery}
                                            onChange={(e) => setChatQuery(e.target.value)}
                                            onKeyDown={(e) => e.key === 'Enter' && sendChat()}
                                            disabled={chatting}
                                        />
                                    </div>
                                    <Button
                                        onClick={sendChat}
                                        disabled={chatting || !chatQuery.trim()}
                                        className="rounded-xl h-auto aspect-square bg-primary hover:bg-primary/90"
                                    >
                                        <Send className="w-4 h-4" />
                                    </Button>
                                </div>
                            </div>
                        )}

                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
