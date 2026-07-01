import { useState } from 'react';
import { Upload, FileJson, Trophy, Activity, Briefcase, ChevronDown } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function App() {
  const [jd, setJd] = useState(`We are looking for a Senior AI Engineer to join our core ML team.
Requirements:
- 5+ years of software engineering experience.
- Deep expertise in Machine Learning, Python, and PyTorch.
- Experience building, fine-tuning, and deploying LLMs (Llama, Mistral) or NLP systems.
- Track record of shipping models to production in a product-focused tech company (not just consulting).`);
  
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState('');
  const [expandedId, setExpandedId] = useState(null);

  const handleRank = async () => {
    if (!file) {
      setError('Please select a JSONL file first.');
      return;
    }
    setError('');
    setLoading(true);

    const formData = new FormData();
    formData.append('candidates_file', file);
    formData.append('job_description', jd);

    try {
      const res = await fetch('http://localhost:8000/api/rank', {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || 'Failed to rank candidates');
      }
      setResults(data.results);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen p-8 max-w-7xl mx-auto flex flex-col gap-8">
      <header className="text-center">
        <h1 className="text-4xl font-bold text-accent mb-2">🚀 Talent Intelligence AI</h1>
        <p className="text-gray-400">Beyond Keywords: 3-Layer Hybrid Ranking Engine</p>
      </header>

      {!results ? (
        <div className="grid md:grid-cols-2 gap-8">
          {/* Left Column: JD */}
          <div className="bg-card border border-border p-6 rounded-2xl shadow-xl backdrop-blur-md">
            <h2 className="text-xl font-semibold mb-4 text-white flex items-center gap-2">
              <Briefcase className="w-5 h-5 text-accent" /> Job Description
            </h2>
            <textarea
              className="w-full h-[400px] bg-[#0d1117] border border-border rounded-xl p-4 text-gray-300 focus:outline-none focus:border-accent transition-colors resize-none"
              value={jd}
              onChange={(e) => setJd(e.target.value)}
            />
          </div>

          {/* Right Column: Upload */}
          <div className="bg-card border border-border p-6 rounded-2xl shadow-xl backdrop-blur-md flex flex-col justify-center items-center gap-6">
            <h2 className="text-xl font-semibold text-white">Upload Candidates</h2>
            
            <label className="flex flex-col items-center justify-center w-full h-64 border-2 border-dashed border-border rounded-xl cursor-pointer hover:bg-white/5 hover:border-accent transition-all">
              <div className="flex flex-col items-center justify-center pt-5 pb-6">
                <FileJson className="w-12 h-12 text-gray-400 mb-4" />
                <p className="mb-2 text-sm text-gray-400">
                  <span className="font-semibold text-accent">Click to upload</span> or drag and drop
                </p>
                <p className="text-xs text-gray-500">JSONL format only</p>
                {file && <p className="mt-4 text-accent font-medium">Selected: {file.name}</p>}
              </div>
              <input type="file" className="hidden" accept=".jsonl,.json" onChange={(e) => setFile(e.target.files[0])} />
            </label>

            {error && <p className="text-red-400 text-sm">{error}</p>}

            <button
              onClick={handleRank}
              disabled={loading}
              className="w-full py-4 bg-accent text-white font-bold rounded-xl hover:bg-blue-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex justify-center items-center gap-2"
            >
              {loading ? (
                <div className="w-6 h-6 border-2 border-white border-t-transparent rounded-full animate-spin" />
              ) : (
                <>✨ Run AI Engine</>
              )}
            </button>
          </div>
        </div>
      ) : (
        <div className="flex flex-col gap-6">
          <div className="flex justify-between items-center bg-card border border-border p-4 rounded-xl">
            <div className="flex gap-8">
              <div><p className="text-sm text-gray-400">Candidates Processed</p><p className="text-2xl font-bold text-white">{results.length}</p></div>
              <div><p className="text-sm text-gray-400">Top Match Score</p><p className="text-2xl font-bold text-accent">{(results[0].score * 100).toFixed(1)}%</p></div>
              <div><p className="text-sm text-gray-400">Execution Time</p><p className="text-2xl font-bold text-green-400">&lt; 2.5s</p></div>
            </div>
            <button onClick={() => setResults(null)} className="px-4 py-2 border border-border rounded-lg hover:bg-white/5 transition-colors">Start Over</button>
          </div>

          <div className="grid gap-4">
            <h2 className="text-2xl font-bold text-white flex items-center gap-2 mb-2">
              <Trophy className="text-yellow-400" /> Top Ranked Candidates
            </h2>
            {results.slice(0, 10).map((r) => (
              <motion.div 
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: r.rank * 0.1 }}
                key={r.candidate_id} 
                className="bg-card border border-border rounded-xl overflow-hidden hover:border-accent transition-colors"
              >
                <div 
                  className="p-6 cursor-pointer flex justify-between items-center"
                  onClick={() => setExpandedId(expandedId === r.candidate_id ? null : r.candidate_id)}
                >
                  <div>
                    <div className="flex items-center gap-3 mb-2">
                      <span className="text-accent font-black text-xl">#{r.rank}</span>
                      <span className="text-white font-bold text-lg">{r.candidate_id}</span>
                    </div>
                    <p className="text-gray-300">💼 {r.title} • ⏳ {r.experience.toFixed(1)} Yrs Exp</p>
                  </div>
                  <div className="flex items-center gap-6">
                    <div className="bg-gradient-to-r from-blue-600 to-green-600 px-4 py-2 rounded-full text-white font-bold shadow-lg">
                      {(r.score * 100).toFixed(1)}% Match
                    </div>
                    <ChevronDown className={`w-5 h-5 text-gray-400 transition-transform ${expandedId === r.candidate_id ? 'rotate-180' : ''}`} />
                  </div>
                </div>

                <AnimatePresence>
                  {expandedId === r.candidate_id && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: 'auto', opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      className="border-t border-border bg-[#0a0d14]"
                    >
                      <div className="p-6">
                        <p className="text-gray-300 leading-relaxed mb-6">
                          <span className="font-bold text-accent">AI Reasoning:</span> {r.reasoning}
                        </p>
                        
                        <div className="grid grid-cols-3 gap-4">
                          <div className="bg-card p-4 rounded-lg border border-border text-center">
                            <p className="text-gray-400 text-sm mb-1">Response Rate</p>
                            <p className="text-xl font-bold text-white flex items-center justify-center gap-2">
                              <Activity className="w-4 h-4 text-green-400" /> {(r.response_rate * 100).toFixed(0)}%
                            </p>
                          </div>
                          <div className="bg-card p-4 rounded-lg border border-border text-center">
                            <p className="text-gray-400 text-sm mb-1">GitHub Score</p>
                            <p className="text-xl font-bold text-white">{r.github_score}</p>
                          </div>
                          <div className="bg-card p-4 rounded-lg border border-border text-center">
                            <p className="text-gray-400 text-sm mb-1">AI Skills Found</p>
                            <p className="text-xl font-bold text-white">{r.ai_skills}</p>
                          </div>
                        </div>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </motion.div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
