import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Navbar from "@/components/Navbar";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
    title: "DocuShield | AI Contract Analysis",
    description: "Secure, reliable contract risk analysis powered by Hybrid AI",
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en" className="dark" suppressHydrationWarning>
            <body className={inter.className} suppressHydrationWarning>
                <Navbar />
                <main className="container mx-auto px-4 pt-24 pb-8 min-h-screen">
                    {children}
                </main>
            </body>
        </html>
    );
}
