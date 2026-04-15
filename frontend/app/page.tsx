"use client";

import { useState, useEffect } from "react";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [jobText, setJobText] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [tab, setTab] = useState("analysis");
  const [lang, setLang] = useState("en");

  const text = {
    en: {
      title: "Dev Career AI 🚀",
      subtitle: "Optimize your CV for any job using AI",
      upload: "Drag & drop your CV or click to upload",
      jobLabel: "Paste job link or description",
      jobPlaceholder: "e.g. https://linkedin.com/jobs/... or job description",
      hint: "You can paste a LinkedIn link or job description",
      analyze: "Analyze",
      analyzing: "Analyzing...",
      match: "Match Score",
      missing: "Missing Skills",
      rewrite: "Rewritten CV",
      roadmap: "Roadmap",
    },
    es: {
      title: "Dev Career AI 🚀",
      subtitle: "Optimiza tu CV para cualquier trabajo con IA",
      upload: "Arrastra tu CV o haz clic para subirlo",
      jobLabel: "Pega el enlace de la oferta o descripción",
      jobPlaceholder: "Ej: https://linkedin.com/jobs/... o descripción del trabajo",
      hint: "Puedes pegar un enlace de LinkedIn o copiar la descripción",
      analyze: "Analizar",
      analyzing: "Analizando...",
      match: "Match Score",
      missing: "Habilidades faltantes",
      rewrite: "CV reescrito",
      roadmap: "Plan de mejora",
    },
  };

  useEffect(() => {
    const browserLang = navigator.language;
    if (browserLang.startsWith("es")) {
      setLang("es");
    }
  }, []);

  const handleSubmit = async () => {
    if (!file || !jobText) return;

    const formData = new FormData();
    formData.append("file", file);
    formData.append("job_text", jobText);

    setLoading(true);
    setResult(null);

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
          {text[lang].title}
        </h1>
        <p className="text-gray-400">
          {text[lang].subtitle}
        </p>
      </div>

      {/* CARD */}
      <div className="max-w-xl mx-auto bg-white/5 backdrop-blur-xl p-6 rounded-2xl border border-white/10 shadow-2xl space-y-4">

        {/* DROPZONE */}
        <div
          className="border-2 border-dashed border-white/20 rounded-xl p-6 text-center cursor-pointer hover:border-blue-500 transition"
          onClick={() => document.getElementById("fileInput")?.click()}
        >
          {file ? (
            <p className="text-green-400">
              📄 {file.name}
            </p>
          ) : (
            <p className="text-gray-400">
              {text[lang].upload}
            </p>
          )}

          <input
            id="fileInput"
            type="file"
            accept="application/pdf"
            className="hidden"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
          />
        </div>

        {/* JOB INPUT */}
        <div className="space-y-2">
          <label className="text-sm text-gray-400">
            {text[lang].jobLabel}
          </label>

          <textarea
            placeholder={text[lang].jobPlaceholder}
            value={jobText}
            onChange={(e) => setJobText(e.target.value)}
            className="w-full p-3 rounded-lg bg-black/50 border border-white/10 focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows={4}
          />

          <p className="text-xs text-gray-500">
            {text[lang].hint}
          </p>
        </div>

        {/* BUTTON */}
        <button
          onClick={handleSubmit}
          className="w-full bg-gradient-to-r from-blue-600 to-blue-400 hover:opacity-90 transition p-3 rounded-xl font-semibold shadow-lg"
        >
          {loading ? text[lang].analyzing : text[lang].analyze}
        </button>
      </div>

      {/* LOADING */}
      {loading && (
        <div className="mt-10 max-w-3xl mx-auto animate-pulse">
          <div className="h-6 bg-white/10 rounded w-1/3 mb-4"></div>
          <div className="h-4 bg-white/10 rounded mb-2"></div>
          <div className="h-4 bg-white/10 rounded mb-2"></div>
          <div className="h-4 bg-white/10 rounded w-2/3"></div>
        </div>
      )}

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

          <div className="bg-white/5 backdrop-blur-xl p-6 rounded-2xl border border-white/10 shadow-2xl">

            {/* ANALYSIS */}
            {tab === "analysis" && (
              <>
                <h2 className="text-2xl mb-4">
                  {text[lang].match}
                </h2>
                <p className="text-4xl font-bold mb-6">
                  {result.analysis?.match_score}
                </p>

                <h3 className="text-xl mb-2">
                  {text[lang].missing}
                </h3>
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
                <h2 className="text-2xl mb-4">
                  {text[lang].rewrite}
                </h2>
                <pre className="whitespace-pre-wrap text-sm text-gray-300">
                  {result.rewritten_cv?.rewritten_cv || "—"}
                </pre>
              </>
            )}

            {/* ROADMAP */}
            {tab === "roadmap" && (
              <>
                <h2 className="text-2xl mb-4">
                  {text[lang].roadmap}
                </h2>
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