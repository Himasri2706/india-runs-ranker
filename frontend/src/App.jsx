import { useState, useMemo } from 'react';
import { Upload, FileJson, Trophy, Activity, Briefcase, ChevronDown, Sparkles, BarChart3, Users, Filter } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, ScatterChart, Scatter, ZAxis } from 'recharts';

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
  const [activeTab, setActiveTab] = useState('leaderboard'); // 'leaderboard' or 'analytics'
  const [sortBy, setSortBy] = useState('score'); // 'score', 'experience', 'ai_skills'

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
      setActiveTab('leaderboard');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Memoized sorting logic
  const sortedResults = useMemo(() => {
    if (!results) return null;
    const copy = [...results];
    if (sortBy === 'score') copy.sort((a, b) => b.score - a.score);
    if (sortBy === 'experience') copy.sort((a, b) => b.experience - a.experience);
    if (sortBy === 'ai_skills') copy.sort((a, b) => b.ai_skills - a.ai_skills);
    return copy;
  }, [results, sortBy]);

  // Data for Charts
  const chartData = useMemo(() => {
    if (!results) return { distribution: [], scatter: [] };
    
    // Score Distribution (Buckets of 10)
    const buckets = new Array(10).fill(0);
    results.forEach(r => {
      let bucket = Math.floor(r.score * 10);
      if (bucket >= 10) bucket = 9;
      buckets[bucket]++;
    });
    const distribution = buckets.map((count, i) => ({
      range: `${i*10}-${(i+1)*10}%`,
      count
    }));

    // Scatter Data (Experience vs Score)
    const scatter = results.map(r => ({
      id: r.candidate_id,
      exp: r.experience,
      score: Number((r.score * 100).toFixed(1)),
      ai_skills: r.ai_skills
    }));

    return { distribution, scatter };
  }, [results]);

  return (
    <div className="min-h-screen bg-[#030712] relative overflow-x-hidden text-gray-200 font-sans selection:bg-indigo-500/30">
      
      {/* Ambient Glowing Background Orbs */}
      <div className="absolute top-[-20%] left-[-10%] w-[60%] h-[60%] rounded-full bg-indigo-600/10 blur-[120px] pointer-events-none" />
      <div className="absolute bottom-[-20%] right-[-10%] w-[60%] h-[60%] rounded-full bg-fuchsia-600/10 blur-[120px] pointer-events-none" />
      <div className="absolute top-[40%] left-[40%] w-[20%] h-[20%] rounded-full bg-blue-500/10 blur-[100px] pointer-events-none" />

      <div className="relative z-10 p-8 max-w-7xl mx-auto flex flex-col gap-10 py-12">
        <header className="text-center space-y-4">
          <motion.div 
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/[0.03] border border-white/[0.1] text-sm font-medium text-indigo-300 mb-4"
          >
            <Sparkles className="w-4 h-4" /> Powered by Hybrid Dense + Sparse Search
          </motion.div>
          <h1 className="text-6xl font-extrabold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-purple-400 to-fuchsia-400 pb-2">
            Talent Intelligence AI
          </h1>
          <p className="text-lg text-gray-400 max-w-2xl mx-auto font-medium">
            Upload your candidate pool and let the 3-Layer Neural Engine rank them with the precision of a Senior Technical Recruiter.
          </p>
        </header>

        {!results ? (
          <motion.div 
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
            className="grid lg:grid-cols-2 gap-8 mt-4"
          >
            {/* Left Column: JD */}
            <div className="bg-white/[0.02] border border-white/[0.05] p-8 rounded-3xl shadow-2xl backdrop-blur-xl flex flex-col">
              <h2 className="text-2xl font-bold mb-6 text-white flex items-center gap-3">
                <div className="p-2 bg-indigo-500/20 rounded-lg text-indigo-400">
                  <Briefcase className="w-6 h-6" />
                </div>
                Job Description
              </h2>
              <textarea
                className="w-full flex-grow min-h-[350px] bg-black/40 border border-white/[0.08] rounded-2xl p-6 text-gray-300 text-lg leading-relaxed focus:outline-none focus:ring-2 focus:ring-indigo-500/50 transition-all resize-none shadow-inner"
                value={jd}
                onChange={(e) => setJd(e.target.value)}
              />
            </div>

            {/* Right Column: Upload */}
            <div className="bg-white/[0.02] border border-white/[0.05] p-8 rounded-3xl shadow-2xl backdrop-blur-xl flex flex-col justify-between">
              <div>
                <h2 className="text-2xl font-bold mb-6 text-white flex items-center gap-3">
                  <div className="p-2 bg-fuchsia-500/20 rounded-lg text-fuchsia-400">
                    <Upload className="w-6 h-6" />
                  </div>
                  Upload Candidates
                </h2>
                
                <label className="flex flex-col items-center justify-center w-full h-72 border-2 border-dashed border-indigo-500/30 rounded-2xl cursor-pointer bg-indigo-500/[0.02] hover:bg-indigo-500/[0.08] hover:border-indigo-400 transition-all duration-300 group">
                  <div className="flex flex-col items-center justify-center pt-5 pb-6 text-center px-4">
                    <div className="p-4 bg-indigo-500/10 rounded-full mb-4 group-hover:scale-110 transition-transform duration-300">
                      <FileJson className="w-10 h-10 text-indigo-400" />
                    </div>
                    <p className="mb-2 text-lg text-gray-300 font-medium">
                      <span className="text-indigo-400 font-bold">Click to upload</span> or drag and drop
                    </p>
                    <p className="text-sm text-gray-500">Supported format: .jsonl (Up to 100k records)</p>
                    {file && (
                      <div className="mt-6 px-4 py-2 bg-green-500/10 border border-green-500/20 rounded-full flex items-center gap-2">
                        <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
                        <span className="text-green-400 font-medium">{file.name}</span>
                      </div>
                    )}
                  </div>
                  <input type="file" className="hidden" accept=".jsonl,.json" onChange={(e) => setFile(e.target.files[0])} />
                </label>
                
                {error && (
                  <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="mt-4 text-red-400 text-sm font-medium text-center bg-red-500/10 py-2 rounded-lg border border-red-500/20">
                    {error}
                  </motion.p>
                )}
              </div>

              <button
                onClick={handleRank}
                disabled={loading}
                className="mt-8 w-full py-5 px-6 bg-gradient-to-r from-indigo-600 to-fuchsia-600 hover:from-indigo-500 hover:to-fuchsia-500 text-white text-lg font-bold rounded-2xl shadow-[0_0_40px_rgba(99,102,241,0.3)] hover:shadow-[0_0_60px_rgba(99,102,241,0.5)] transition-all duration-300 transform hover:-translate-y-1 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex justify-center items-center gap-3"
              >
                {loading ? (
                  <>
                    <div className="w-6 h-6 border-4 border-white/30 border-t-white rounded-full animate-spin" />
                    <span className="animate-pulse">Processing Candidates...</span>
                  </>
                ) : (
                  <>
                    <Sparkles className="w-6 h-6" /> Run Neural Engine
                  </>
                )}
              </button>
            </div>
          </motion.div>
        ) : (
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex flex-col gap-8"
          >
            {/* Top Metrics Row */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="col-span-3 grid grid-cols-3 gap-4">
                <div className="bg-white/[0.02] border border-white/[0.05] p-6 rounded-2xl backdrop-blur-md relative overflow-hidden">
                  <div className="absolute right-0 top-0 w-24 h-24 bg-blue-500/10 rounded-full blur-2xl translate-x-1/2 -translate-y-1/2" />
                  <p className="text-sm font-semibold text-gray-400 mb-1">Total Processed</p>
                  <p className="text-3xl font-black text-white">{results.length.toLocaleString()}</p>
                </div>
                <div className="bg-white/[0.02] border border-white/[0.05] p-6 rounded-2xl backdrop-blur-md relative overflow-hidden">
                  <div className="absolute right-0 top-0 w-24 h-24 bg-fuchsia-500/10 rounded-full blur-2xl translate-x-1/2 -translate-y-1/2" />
                  <p className="text-sm font-semibold text-gray-400 mb-1">Top Match Score</p>
                  <p className="text-3xl font-black text-transparent bg-clip-text bg-gradient-to-r from-fuchsia-400 to-pink-400">
                    {(results[0].score * 100).toFixed(1)}%
                  </p>
                </div>
                <div className="bg-white/[0.02] border border-white/[0.05] p-6 rounded-2xl backdrop-blur-md relative overflow-hidden">
                  <div className="absolute right-0 top-0 w-24 h-24 bg-green-500/10 rounded-full blur-2xl translate-x-1/2 -translate-y-1/2" />
                  <p className="text-sm font-semibold text-gray-400 mb-1">Compute Time</p>
                  <p className="text-3xl font-black text-green-400">&lt; 3.0s</p>
                </div>
              </div>
              <button 
                onClick={() => setResults(null)} 
                className="h-full bg-white/[0.05] border border-white/[0.1] rounded-2xl hover:bg-white/[0.08] transition-colors font-bold text-gray-300 flex items-center justify-center gap-2 hover:text-white"
              >
                ← Scan New Batch
              </button>
            </div>

            {/* Navigation Tabs */}
            <div className="flex gap-4 p-1 bg-white/[0.02] border border-white/[0.05] rounded-xl w-fit">
              <button
                onClick={() => setActiveTab('leaderboard')}
                className={`px-6 py-3 rounded-lg font-bold flex items-center gap-2 transition-all ${activeTab === 'leaderboard' ? 'bg-indigo-500/20 text-indigo-300 shadow-sm' : 'text-gray-400 hover:text-white'}`}
              >
                <Users className="w-5 h-5" /> Elite Leaderboard
              </button>
              <button
                onClick={() => setActiveTab('analytics')}
                className={`px-6 py-3 rounded-lg font-bold flex items-center gap-2 transition-all ${activeTab === 'analytics' ? 'bg-fuchsia-500/20 text-fuchsia-300 shadow-sm' : 'text-gray-400 hover:text-white'}`}
              >
                <BarChart3 className="w-5 h-5" /> Analytics Dashboard
              </button>
            </div>

            {/* Tab Contents */}
            {activeTab === 'leaderboard' && (
              <div className="bg-white/[0.02] border border-white/[0.05] p-8 rounded-3xl backdrop-blur-xl">
                <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-8">
                  <h2 className="text-2xl font-bold text-white flex items-center gap-3">
                    <Trophy className="text-yellow-400 w-7 h-7" /> The Elite Shortlist
                  </h2>
                  <div className="flex items-center gap-3 bg-black/40 px-4 py-2 rounded-xl border border-white/[0.05]">
                    <Filter className="w-4 h-4 text-gray-400" />
                    <span className="text-sm font-semibold text-gray-400">Sort by:</span>
                    <select 
                      className="bg-transparent text-white text-sm font-bold focus:outline-none cursor-pointer"
                      value={sortBy}
                      onChange={(e) => setSortBy(e.target.value)}
                    >
                      <option className="bg-gray-900" value="score">Highest Score</option>
                      <option className="bg-gray-900" value="experience">Most Experience</option>
                      <option className="bg-gray-900" value="ai_skills">Most AI Skills</option>
                    </select>
                  </div>
                </div>
                
                <div className="flex flex-col gap-4">
                  {sortedResults.slice(0, 100).map((r, idx) => (
                    <motion.div 
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ duration: 0.3, delay: Math.min(idx * 0.05, 0.5) }}
                      key={r.candidate_id} 
                      className="group bg-black/40 border border-white/[0.05] rounded-2xl overflow-hidden hover:border-indigo-500/50 transition-all duration-300"
                    >
                      <div 
                        className="p-6 cursor-pointer flex flex-col md:flex-row justify-between items-start md:items-center gap-4 relative overflow-hidden"
                        onClick={() => setExpandedId(expandedId === r.candidate_id ? null : r.candidate_id)}
                      >
                        <div className="absolute left-0 top-0 bottom-0 w-1 bg-gradient-to-b from-indigo-500 to-fuchsia-500 opacity-0 group-hover:opacity-100 transition-opacity" />
                        
                        <div className="flex gap-6 items-center w-full">
                          <div className="flex-shrink-0 w-12 h-12 rounded-xl bg-white/[0.05] border border-white/[0.1] flex items-center justify-center font-black text-xl text-white">
                            {idx + 1}
                          </div>
                          <div className="flex-grow">
                            <h3 className="text-xl font-bold text-white mb-1">{r.candidate_id}</h3>
                            <p className="text-indigo-300 font-medium">💼 {r.title} <span className="text-gray-500 mx-2">•</span> ⏳ {r.experience.toFixed(1)} Yrs Exp</p>
                          </div>
                        </div>
                        
                        <div className="flex flex-shrink-0 items-center gap-4 w-full md:w-auto justify-between md:justify-end">
                          <div className="bg-gradient-to-r from-indigo-500/20 to-fuchsia-500/20 border border-indigo-500/30 px-5 py-2 rounded-full text-white font-bold tracking-wide flex items-center gap-2">
                            <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
                            {(r.score * 100).toFixed(1)}% Match
                          </div>
                          <ChevronDown className={`w-6 h-6 text-gray-400 transition-transform duration-300 ${expandedId === r.candidate_id ? 'rotate-180 text-indigo-400' : ''}`} />
                        </div>
                      </div>

                      <AnimatePresence>
                        {expandedId === r.candidate_id && (
                          <motion.div
                            initial={{ height: 0, opacity: 0 }}
                            animate={{ height: 'auto', opacity: 1 }}
                            exit={{ height: 0, opacity: 0 }}
                            className="border-t border-white/[0.05] bg-black/60"
                          >
                            <div className="p-8">
                              <div className="bg-indigo-900/20 border border-indigo-500/20 rounded-xl p-5 mb-8">
                                <p className="text-indigo-100 leading-relaxed text-lg">
                                  <span className="font-bold text-indigo-400 mr-2">Engine Reasoning:</span> 
                                  {r.reasoning}
                                </p>
                                {r.extracted_keywords && r.extracted_keywords.length > 0 && (
                                  <div className="mt-4 border-t border-indigo-500/20 pt-4">
                                    <p className="text-sm font-bold text-indigo-300 mb-2">Explainable AI (Exact JD Match):</p>
                                    <div className="flex flex-wrap gap-2">
                                      {r.extracted_keywords.map((kw, i) => (
                                        <span key={i} className="px-3 py-1 bg-green-500/20 border border-green-500/30 text-green-300 rounded-full text-xs font-bold uppercase tracking-wide">
                                          {kw}
                                        </span>
                                      ))}
                                    </div>
                                  </div>
                                )}
                              </div>
                              
                              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                                <div className="bg-white/[0.03] p-5 rounded-xl border border-white/[0.05] flex items-center gap-4">
                                  <div className="p-3 bg-green-500/10 rounded-lg">
                                    <Activity className="w-6 h-6 text-green-400" />
                                  </div>
                                  <div>
                                    <p className="text-gray-400 text-sm font-medium">Response Rate</p>
                                    <p className="text-2xl font-bold text-white">{(r.response_rate * 100).toFixed(0)}%</p>
                                  </div>
                                </div>
                                <div className="bg-white/[0.03] p-5 rounded-xl border border-white/[0.05] flex items-center gap-4">
                                  <div className="p-3 bg-orange-500/10 rounded-lg text-orange-400 font-bold text-xl">GH</div>
                                  <div>
                                    <p className="text-gray-400 text-sm font-medium">GitHub Score</p>
                                    <p className="text-2xl font-bold text-white">{r.github_score}</p>
                                  </div>
                                </div>
                                <div className="bg-white/[0.03] p-5 rounded-xl border border-white/[0.05] flex items-center gap-4">
                                  <div className="p-3 bg-blue-500/10 rounded-lg text-blue-400 font-bold text-xl">AI</div>
                                  <div>
                                    <p className="text-gray-400 text-sm font-medium">Core AI Skills</p>
                                    <p className="text-2xl font-bold text-white">{r.ai_skills}</p>
                                  </div>
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

            {activeTab === 'analytics' && (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Chart 1: Score Distribution */}
                <div className="bg-white/[0.02] border border-white/[0.05] p-8 rounded-3xl backdrop-blur-xl">
                  <h3 className="text-xl font-bold text-white mb-6">Score Distribution</h3>
                  <div className="h-72 w-full">
                    <ResponsiveContainer width="100%" height="100%">
                      <AreaChart data={chartData.distribution}>
                        <defs>
                          <linearGradient id="colorCount" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#6366f1" stopOpacity={0.8}/>
                            <stop offset="95%" stopColor="#6366f1" stopOpacity={0}/>
                          </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" stroke="#ffffff10" />
                        <XAxis dataKey="range" stroke="#9ca3af" />
                        <YAxis stroke="#9ca3af" />
                        <RechartsTooltip 
                          contentStyle={{ backgroundColor: '#111827', borderColor: '#374151', borderRadius: '0.5rem' }}
                          itemStyle={{ color: '#818cf8' }}
                        />
                        <Area type="monotone" dataKey="count" stroke="#818cf8" fillOpacity={1} fill="url(#colorCount)" />
                      </AreaChart>
                    </ResponsiveContainer>
                  </div>
                </div>

                {/* Chart 2: Experience vs Score (Hidden Gems) */}
                <div className="bg-white/[0.02] border border-white/[0.05] p-8 rounded-3xl backdrop-blur-xl">
                  <h3 className="text-xl font-bold text-white mb-6">Experience vs. Match Score</h3>
                  <div className="h-72 w-full">
                    <ResponsiveContainer width="100%" height="100%">
                      <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#ffffff10" />
                        <XAxis type="number" dataKey="exp" name="Experience" unit=" yrs" stroke="#9ca3af" />
                        <YAxis type="number" dataKey="score" name="Score" unit="%" stroke="#9ca3af" domain={[0, 100]} />
                        <ZAxis type="number" dataKey="ai_skills" range={[50, 400]} name="AI Skills" />
                        <RechartsTooltip 
                          cursor={{ strokeDasharray: '3 3' }} 
                          contentStyle={{ backgroundColor: '#111827', borderColor: '#374151', borderRadius: '0.5rem' }}
                        />
                        <Scatter name="Candidates" data={chartData.scatter} fill="#c084fc" />
                      </ScatterChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              </div>
            )}
          </motion.div>
        )}
      </div>
    </div>
  );
}
