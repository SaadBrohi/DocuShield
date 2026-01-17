"use client";

import Link from "next/link";
import { ShieldCheck, FileText, Upload } from "lucide-react";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";

export default function Navbar() {
    const pathname = usePathname();

    const navItems = [
        { name: "Dashboard", href: "/", icon: FileText },
        { name: "Upload", href: "/upload", icon: Upload },
    ];

    return (
        <nav className="fixed top-0 left-0 right-0 z-50 glass-panel border-x-0 border-t-0 rounded-none h-16 flex items-center justify-center">
            <div className="container mx-auto px-4 h-16 flex items-center justify-between">
                <div className="flex items-center space-x-2">
                    <ShieldCheck className="w-8 h-8 text-primary" />
                    <span className="text-xl font-bold text-white tracking-tight">
                        Docu<span className="text-primary">Shield</span>
                    </span>
                </div>

                <div className="flex items-center space-x-6">
                    {navItems.map((item) => {
                        const Icon = item.icon;
                        const isActive = pathname === item.href;
                        return (
                            <Link
                                key={item.href}
                                href={item.href}
                                className={cn(
                                    "flex items-center space-x-2 text-sm font-medium transition-colors hover:text-primary",
                                    isActive ? "text-primary" : "text-muted-foreground"
                                )}
                            >
                                <Icon className="w-4 h-4" />
                                <span>{item.name}</span>
                            </Link>
                        );
                    })}
                </div>
            </div>
        </nav>
    );
}
