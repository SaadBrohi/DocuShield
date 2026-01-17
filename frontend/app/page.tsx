import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ShieldCheck, FileText, Zap, Lock, ArrowRight, CheckCircle2 } from "lucide-react";

export default function Home() {
    return (
        <div className="flex flex-col items-center justify-center space-y-32 py-20 animate-slide-up">

            {/* Hero Section */}
            <section className="text-center space-y-8 max-w-5xl mx-auto px-4 relative">
                {/* Background Glow */}
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-primary/20 rounded-full blur-[120px] -z-10" />

                <div className="inline-flex items-center px-4 py-1.5 rounded-full border border-primary/20 bg-primary/10 text-primary text-sm font-medium mb-8 animate-glow">
                    <ShieldCheck className="w-4 h-4 mr-2" />
                    AI-Powered Contract Security
                </div>

                <h1 className="text-6xl md:text-8xl font-bold tracking-tighter text-white leading-[1.1]">
                    Secure Contracts <br />
                    <span className="text-gradient-amber">
                        Without Compromise
                    </span>
                </h1>

                <p className="text-xl md:text-2xl text-zinc-400 max-w-3xl mx-auto leading-relaxed">
                    Instantly detect risks, loopholes, and compliance failures.
                    The only AI defense layer your legal team needs.
                </p>

                <div className="flex flex-col sm:flex-row items-center justify-center gap-6 pt-8">
                    <Link href="/upload">
                        <Button size="lg" className="bg-primary hover:bg-primary/90 text-black font-bold shadow-lg shadow-primary/25 px-10 h-14 text-lg rounded-full transition-all hover:scale-105">
                            Analyze Document <ArrowRight className="w-5 h-5 ml-2" />
                        </Button>
                    </Link>
                    <Button variant="outline" size="lg" className="glass-button h-14 px-10 text-lg rounded-full">
                        View Live Demo
                    </Button>
                </div>

                {/* Social Proof */}
                <div className="pt-16 opacity-60 grayscale hover:grayscale-0 transition-all duration-500">
                    <p className="text-sm text-zinc-600 mb-4 uppercase tracking-widest font-semibold">Trusted By Security Teams At</p>
                    <div className="flex justify-center gap-12 items-center">
                        {['Acme Corp', 'Globex', 'Soylent', 'Umbrella'].map(c => (
                            <span key={c} className="text-zinc-500 font-bold text-xl">{c}</span>
                        ))}
                    </div>
                </div>
            </section>

            {/* Features Grid - Bento Style */}
            <section className="w-full max-w-7xl px-4">
                <div className="grid md:grid-cols-3 gap-6">
                    {/* Feature 1 */}
                    <div className="glass-panel p-10 rounded-3xl md:col-span-2 relative overflow-hidden group">
                        <div className="absolute top-0 right-0 w-64 h-64 bg-primary/10 rounded-full blur-[80px] -z-10 group-hover:bg-primary/20 transition-all" />
                        <Zap className="w-12 h-12 text-primary mb-6" />
                        <h3 className="text-3xl font-bold text-white mb-4">Instant Risk Scoring</h3>
                        <p className="text-zinc-400 text-lg leading-relaxed max-w-md">
                            Our hybrid engine processes documents in milliseconds, identifying critical risks with 99.9% accuracy before you even sign.
                        </p>
                    </div>

                    {/* Feature 2 */}
                    <div className="glass-panel p-10 rounded-3xl flex flex-col justify-center relative overflow-hidden group">
                        <div className="absolute bottom-0 left-0 w-full h-1 bg-gradient-to-r from-primary to-transparent" />
                        <Lock className="w-12 h-12 text-zinc-200 mb-6" />
                        <h3 className="text-2xl font-bold text-white mb-4">Local-First Privacy</h3>
                        <p className="text-zinc-400">
                            Zero data retention. Optional local-only processing ensures your NDA never leaves your device.
                        </p>
                    </div>

                    {/* Feature 3 */}
                    <div className="glass-panel p-10 rounded-3xl flex flex-col justify-center relative overflow-hidden group">
                        <FileText className="w-12 h-12 text-zinc-200 mb-6" />
                        <h3 className="text-2xl font-bold text-white mb-4">Deep Semantics</h3>
                        <p className="text-zinc-400">
                            Beyond keywords. We understand context, obligations, and indemnities.
                        </p>
                    </div>

                    {/* Feature 4 with List */}
                    <div className="glass-panel p-10 rounded-3xl md:col-span-2">
                        <div className="flex flex-col md:flex-row gap-8 items-start">
                            <div className="flex-1">
                                <h3 className="text-3xl font-bold text-white mb-6">Why DocuShield?</h3>
                                <ul className="space-y-4">
                                    {[
                                        "Bank-grade encryption (AES-256)",
                                        "GDPR & CCPA Compliant",
                                        "Real-time Clause Analysis",
                                        "Export to PDF & JSON"
                                    ].map((item, i) => (
                                        <li key={i} className="flex items-center text-zinc-300">
                                            <CheckCircle2 className="w-5 h-5 text-primary mr-3" />
                                            {item}
                                        </li>
                                    ))}
                                </ul>
                            </div>
                            {/* Visual Placeholder */}
                            <div className="w-full md:w-1/3 bg-zinc-950/50 rounded-xl border border-white/5 h-48 flex items-center justify-center text-zinc-700 font-mono text-sm">
                                [Analysisgraph]
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Footer */}
            <footer className="w-full border-t border-white/5 py-12 text-center text-zinc-600">
                <p>&copy; 2026 DocuShield Inc. All rights reserved.</p>
            </footer>

        </div>
    );
}
