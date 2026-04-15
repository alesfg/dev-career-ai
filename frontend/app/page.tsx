"use client";

import { useState } from "react";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [jobText, setJobText] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [tab, setTab] = useState("analysis");

  const handleSubmit = async () => {
    if (!file || !jobText) return;

    const formData = new FormData();
    formData.append("file", file);
    formData.append("job_text", jobText);

    setLoading(true);

    const res = await fetch("http://127.0.0.1:8000/api/analyze-pdf", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    setResult(data);
    setLoading(false);
  };

  return (
    <main className="min-h-screen bg-gradient-to-b from-black to-gray-900 text-white px-6 py-12">
      
      {/* HERO */}
      <div className="max-w-4xl mx-auto text-center mb-12">
        <h1 className="text-5xl font-bold mb-4">
          Dev Career AI 🚀
        </h1>
        <p className="text-gray-400">
          Optimize your CV for any job using AI
        </p>
      </div>

      {/* INPUT CARD */}
      <div className="max-w-xl mx-auto bg-white/5 backdrop-blur p-6 rounded-2xl border border-white/10 space-y-4 shadow-xl">
        
        <input
          type="file"
          accept="application/pdf"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
          className="w-full text-sm"
        />

        <textarea
          placeholder="Paste job description or LinkedIn link..."
          value={jobText}
          onChange={(e) => setJobText(e.target.value)}
          className="w-full p-3 rounded-lg bg-black/50 border border-white/10"
        />

        <button
          onClick={handleSubmit}
          className="w-full bg-blue-600 hover:bg-blue-500 transition p-3 rounded-xl font-semibold"
        >
          {loading ? "Analyzing..." : "Analyze"}
        </button>
      </div>

      {/* RESULTS */}
      {result && (
        <div className="max-w-4xl mx-auto mt-12">

          {/* TABS */}
          <div className="flex gap-4 mb-6">
            {["analysis", "rewrite", "roadmap"].map((t) => (
              <button
                key={t}
                onClick={() => setTab(t)}
                className={`px-4 py-2 rounded-lg ${
                  tab === t ? "bg-blue-600" : "bg-white/10"
                }`}
              >
                {t}
              </button>
            ))}
          </div>

          <div className="bg-white/5 p-6 rounded-2xl border border-white/10">

            {/* ANALYSIS */}
            {tab === "analysis" && (
              <>
                <h2 className="text-2xl mb-4">Match Score</h2>
                <p className="text-4xl font-bold mb-6">
                  {result.analysis?.match_score}
                </p>

                <h3 className="text-xl mb-2">Missing Skills</h3>
                <ul className="text-gray-300">
                  {result.analysis?.missing_skills?.map((s: string, i: number) => (
                    <li key={i}>• {s}</li>
                  ))}
                </ul>
              </>
            )}

            {/* REWRITE */}
            {tab === "rewrite" && (
              <>
                <h2 className="text-2xl mb-4">Rewritten CV</h2>
                <pre className="whitespace-pre-wrap text-sm text-gray-300">
                  {result.rewritten_cv?.rewritten_cv}
                </pre>
              </>
            )}

            {/* ROADMAP */}
            {tab === "roadmap" && (
              <>
                <h2 className="text-2xl mb-4">Roadmap</h2>
                {result.roadmap?.roadmap?.map((week: any, i: number) => (
                  <div key={i} className="mb-4">
                    <p className="font-semibold">
                      Week {week.week}: {week.focus}
                    </p>
                    <ul className="text-gray-400 ml-4">
                      {week.actions.map((a: string, j: number) => (
                        <li key={j}>- {a}</li>
                      ))}
                    </ul>
                  </div>
                ))}
              </>
            )}

          </div>
        </div>
      )}
    </main>
  );
}