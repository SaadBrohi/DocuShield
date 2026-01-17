"use client";

import { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Loader2, AlertTriangle, Shield, CheckCircle, MessageSquare, FileText } from "lucide-react";
import { cn } from "@/lib/utils";

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
            <div className="lg:col-span-1 space-y-6">
                <Card className="glass-panel border-zinc-800">
                    <CardHeader>
                        <CardTitle>Document Actions</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="flex space-x-2">
                            <Button
                                variant={activeTab === 'analysis' ? 'default' : 'outline'}
                                onClick={() => setActiveTab('analysis')}
                                className="flex-1"
                            >
                                <Shield className="w-4 h-4 mr-2" /> Risk
                            </Button>
                            <Button
                                variant={activeTab === 'chat' ? 'default' : 'outline'}
                                onClick={() => setActiveTab('chat')}
                                className="flex-1"
                            >
                                <MessageSquare className="w-4 h-4 mr-2" /> Chat
                            </Button>
                        </div>
                    </CardContent>
                </Card>

                {analysis && (
                    <Card className="glass-panel border-zinc-800">
                        <CardHeader>
                            <CardTitle>Risk Score</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="flex items-center justify-center py-4">
                                <div className={cn(
                                    "relative w-32 h-32 rounded-full flex items-center justify-center border-4 text-4xl font-bold",
                                    analysis.risk_score > 70 ? "border-red-500 text-red-500" :
                                        analysis.risk_score > 40 ? "border-yellow-500 text-yellow-500" :
                                            "border-green-500 text-green-500"
                                )}>
                                    {analysis.risk_score}
                                </div>
                            </div>
                            <div className="text-center font-medium text-lg mt-2">
                                {analysis.risk_level} Risk
                            </div>
                        </CardContent>
                    </Card>
                )}
            </div>

            {/* Main Content */}
            <div className="lg:col-span-2 h-full flex flex-col">
                <Card className="glass-panel border-zinc-800 flex-1 flex flex-col h-full overflow-hidden">
                    <CardHeader>
                        <CardTitle>
                            {activeTab === 'analysis' ? 'Detailed Risk Analysis' : 'Chat with Contract'}
                        </CardTitle>
                    </CardHeader>
                    <CardContent className="flex-1 overflow-y-auto">

                        {activeTab === 'analysis' && (
                            <div className="space-y-6">
                                {!analysis ? (
                                    <div className="flex flex-col items-center justify-center h-64 text-center">
                                        <Shield className="w-16 h-16 text-muted-foreground mb-4" />
                                        <h3 className="text-xl font-medium">No Analysis Yet</h3>
                                        <p className="text-muted-foreground mb-6">Run AI analysis to detect risks.</p>
                                        <Button onClick={runAnalysis} disabled={analyzing} size="lg">
                                            {analyzing ? <Loader2 className="w-4 h-4 mr-2 animate-spin" /> : "Run Risk Analysis"}
                                        </Button>
                                    </div>
                                ) : (
                                    <div className="space-y-6">
                                        <div className="bg-zinc-900/50 p-4 rounded-lg border border-white/5">
                                            <h4 className="font-semibold mb-2">Summary</h4>
                                            <p className="text-sm text-gray-300 leading-relaxed">{analysis.explanation}</p>
                                        </div>

                                        <h4 className="font-semibold text-lg flex items-center">
                                            <AlertTriangle className="w-5 h-5 mr-2 text-yellow-500" /> Flagged Clauses
                                        </h4>

                                        {analysis.flagged_clauses.map((clause, idx) => (
                                            <div key={idx} className="bg-red-950/20 border border-red-900/50 p-4 rounded-lg">
                                                <p className="text-sm font-mono text-red-200 mb-2">"{clause.clause_text}"</p>
                                                <div className="text-xs text-red-400 font-medium flex items-start">
                                                    <AlertTriangle className="w-3 h-3 mr-1 mt-0.5 shrink-0" />
                                                    {clause.risk_reason}
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>
                        )}

                        {activeTab === 'chat' && (
                            <div className="flex flex-col h-full">
                                <div className="flex-1 space-y-4 mb-4">
                                    {chatHistory.length === 0 && (
                                        <div className="text-center text-muted-foreground py-10">
                                            Ask questions about the contract (e.g., "What is the termination clause?")
                                        </div>
                                    )}
                                    {chatHistory.map((msg, i) => (
                                        <div key={i} className={cn(
                                            "p-3 rounded-lg max-w-[80%] text-sm",
                                            msg.role === 'user'
                                                ? "bg-primary text-primary-foreground ml-auto"
                                                : "bg-zinc-800 text-zinc-100 mr-auto"
                                        )}>
                                            {msg.content}
                                        </div>
                                    ))}
                                    {chatting && (
                                        <div className="bg-zinc-800 text-zinc-100 mr-auto p-3 rounded-lg max-w-[80%] flex items-center">
                                            <Loader2 className="w-4 h-4 animate-spin mr-2" /> Thinking...
                                        </div>
                                    )}
                                </div>

                                <div className="pt-4 border-t border-white/10 flex gap-2">
                                    <input
                                        className="flex-1 bg-zinc-900 border border-zinc-700 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary"
                                        placeholder="Ask something..."
                                        value={chatQuery}
                                        onChange={(e) => setChatQuery(e.target.value)}
                                        onKeyDown={(e) => e.key === 'Enter' && sendChat()}
                                        disabled={chatting}
                                    />
                                    <Button onClick={sendChat} disabled={chatting || !chatQuery.trim()}>Send</Button>
                                </div>
                            </div>
                        )}

                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
