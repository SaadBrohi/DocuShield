"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { UploadCloud, CheckCircle, AlertCircle, Loader2 } from "lucide-react";

export default function UploadPage() {
    const [file, setFile] = useState<File | null>(null);
    const [uploading, setUploading] = useState(false);
    const router = useRouter();

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            setFile(e.target.files[0]);
        }
    };

    const handleUpload = async () => {
        if (!file) return;

        setUploading(true);
        const formData = new FormData();
        formData.append("file", file);

        try {
            const res = await fetch("http://localhost:8000/documents/upload", {
                method: "POST",
                body: formData,
            });

            if (!res.ok) throw new Error("Upload failed");

            const data = await res.json();
            router.push(`/documents/${data.id}`);
        } catch (error) {
            console.error(error);
            alert("Error uploading file");
            setUploading(false);
        }
    };

    return (
        <div className="max-w-2xl mx-auto animate-fade-in-up">
            <Card className="glass-panel border-zinc-800">
                <CardHeader>
                    <CardTitle>Upload Contract</CardTitle>
                    <CardDescription>
                        Upload a PDF or DOCX file to start the risk analysis.
                    </CardDescription>
                </CardHeader>
                <CardContent className="space-y-8">
                    <label
                        className="border-2 border-dashed border-zinc-800 rounded-xl p-12 flex flex-col items-center justify-center space-y-4 hover:bg-zinc-900/50 hover:border-primary/50 transition-all duration-300 group cursor-pointer relative overflow-hidden w-full block"
                    >
                        {/* Glow Effect */}
                        <div className="absolute inset-0 bg-primary/5 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none" />

                        <div className="p-5 bg-zinc-900 rounded-full group-hover:scale-110 transition-transform shadow-xl shadow-black/50 border border-zinc-800 group-hover:border-primary/20">
                            <UploadCloud className="w-10 h-10 text-primary group-hover:text-emerald-400 transition-colors" />
                        </div>

                        <div className="text-center z-10">
                            <span className="mt-4 block text-lg font-medium text-white group-hover:text-emerald-300 transition-colors">
                                {file ? file.name : "Click to select contract"}
                            </span>
                            <input
                                id="file-upload"
                                name="file-upload"
                                type="file"
                                className="sr-only"
                                accept=".pdf,.docx"
                                onChange={handleFileChange}
                            />
                            <p className="mt-2 text-sm text-zinc-500">PDF or DOCX up to 10MB</p>
                        </div>
                    </label>

                    <div className="flex justify-end">
                        <Button
                            onClick={handleUpload}
                            disabled={!file || uploading}
                            size="lg"
                            className="w-full sm:w-auto bg-primary hover:bg-primary/90 text-white shadow-lg shadow-emerald-900/20 px-8"
                        >
                            {uploading ? (
                                <>
                                    <Loader2 className="mr-2 h-4 w-4 animate-spin" /> Analyzing...
                                </>
                            ) : (
                                "Start Risk Analysis"
                            )}
                        </Button>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
