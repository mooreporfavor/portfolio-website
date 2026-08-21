// src/components/AdvancedPortfolioFilter.jsx
import { useState, useMemo } from 'preact/hooks';

export default function AdvancedPortfolioFilter({ projects }) {
  const [selectedTrack, setSelectedTrack] = useState('All');
  const [selectedSkill, setSelectedSkill] = useState('All');
  const [searchQuery, setSearchQuery] = useState('');

  const tracks = ['All', 'Global Development', 'Data Engineering & AI', 'Leadership'];

  // Count projects per track
  const trackCounts = useMemo(() => {
    const counts = { All: projects.length };
    tracks.slice(1).forEach(t => {
      counts[t] = projects.filter(p => p.data.track === t).length;
    });
    return counts;
  }, [projects]);

  // Filter projects by track
  const projectsInTrack = useMemo(() => {
    if (selectedTrack === 'All') return projects;
    return projects.filter(p => p.data.track === selectedTrack);
  }, [selectedTrack, projects]);

  // Derive relevant skills in track
  const relevantSkills = useMemo(() => {
    const skills = new Set();
    projectsInTrack.forEach(p => p.data.tags.forEach(tag => skills.add(tag)));
    const sortedSkills = [...skills].sort();
    return ['All', ...sortedSkills];
  }, [projectsInTrack]);

  // Final filtered list with search
  const finalFilteredProjects = useMemo(() => {
    let result = projectsInTrack;
    if (selectedSkill !== 'All') {
      result = result.filter(p => p.data.tags.includes(selectedSkill));
    }
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      result = result.filter(p => 
        p.data.title.toLowerCase().includes(q) ||
        p.data.client.toLowerCase().includes(q) ||
        p.data.tags.some(t => t.toLowerCase().includes(q)) ||
        (p.body && p.body.toLowerCase().includes(q))
      );
    }
    return result;
  }, [selectedSkill, projectsInTrack, searchQuery]);
  
  const handleTrackSelect = (track) => {
    setSelectedTrack(track);
    setSelectedSkill('All');
  };

  const getTrackBadgeClass = (track) => {
    switch(track) {
      case 'Global Development':
        return 'bg-emerald-50 text-emerald-800 border-emerald-200';
      case 'Data Engineering & AI':
        return 'bg-blue-50 text-brand-blue border-blue-200';
      case 'Leadership':
        return 'bg-amber-50 text-amber-800 border-amber-200';
      default:
        return 'bg-slate-100 text-slate-700 border-slate-200';
    }
  };

  return (
    <div class="space-y-10">
      
      {/* Filter Control Bar */}
      <div class="glass-panel p-6 rounded-3xl border border-slate-200 shadow-lg space-y-6">
        
        {/* Search and Track Header */}
        <div class="flex flex-col md:flex-row items-center justify-between gap-4">
          
          {/* Search Input */}
          <div class="relative w-full md:w-80">
            <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <input
              type="text"
              placeholder="Search projects, skills, tools..."
              value={searchQuery}
              onInput={(e) => setSearchQuery(e.target.value)}
              class="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm font-medium text-brand-slate placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-brand-accent focus:bg-white transition-all"
            />
            {searchQuery && (
              <button 
                onClick={() => setSearchQuery('')}
                class="absolute inset-y-0 right-0 pr-3 flex items-center text-xs text-slate-400 hover:text-slate-600"
              >
                Clear
              </button>
            )}
          </div>

          {/* Project Result Count */}
          <div class="text-xs font-semibold text-slate-500 uppercase tracking-wider">
            Showing <span class="text-brand-blue font-bold">{finalFilteredProjects.length}</span> of {projects.length} Case Studies
          </div>

        </div>

        {/* Track Tabs */}
        <div class="flex flex-wrap items-center gap-2 pt-2 border-t border-slate-100">
          {tracks.map((track) => {
            const isActive = selectedTrack === track;
            const count = trackCounts[track] || 0;
            return (
              <button
                key={track}
                onClick={() => handleTrackSelect(track)}
                class={`px-4 py-2 text-sm font-semibold rounded-full transition-all duration-200 flex items-center gap-2 ${
                  isActive
                    ? 'bg-brand-blue text-white shadow-md shadow-blue-900/20 ring-1 ring-brand-blue scale-102'
                    : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                }`}
              >
                <span>{track}</span>
                <span class={`text-xs px-1.5 py-0.2 rounded-full font-mono ${
                  isActive ? 'bg-blue-800 text-white' : 'bg-white text-slate-600'
                }`}>
                  {count}
                </span>
              </button>
            );
          })}
        </div>

        {/* Secondary Skill Pills (if specific track selected) */}
        {relevantSkills.length > 2 && (
          <div class="pt-4 border-t border-slate-100 flex flex-wrap items-center gap-1.5">
            <span class="text-xs font-bold text-slate-400 mr-2 uppercase tracking-wide">Filter by tag:</span>
            {relevantSkills.map((skill) => {
              const isSkillActive = selectedSkill === skill;
              return (
                <button
                  key={skill}
                  onClick={() => setSelectedSkill(skill)}
                  class={`px-3 py-1 text-xs font-semibold rounded-lg transition-all ${
                    isSkillActive
                      ? 'bg-brand-slate text-white shadow-xs'
                      : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                  }`}
                >
                  {skill}
                </button>
              );
            })}
          </div>
        )}

      </div>

      {/* Projects Grid */}
      {finalFilteredProjects.length === 0 ? (
        <div class="text-center py-16 bg-white rounded-3xl border border-slate-200 p-8">
          <p class="text-lg font-serif font-bold text-slate-700 mb-2">No matching case studies found</p>
          <p class="text-sm text-slate-500 mb-6">Try searching with a different keyword or reset your track filter.</p>
          <button 
            onClick={() => { setSelectedTrack('All'); setSelectedSkill('All'); setSearchQuery(''); }}
            class="px-5 py-2 rounded-full bg-brand-blue text-white text-xs font-semibold"
          >
            Reset Filters
          </button>
        </div>
      ) : (
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {finalFilteredProjects.map((project) => (
            <a 
              href={`/portfolio/${project.slug}/`} 
              key={project.slug} 
              class="group relative bg-white rounded-2xl p-7 border border-slate-200/80 shadow-card hover:shadow-card-hover transition-all duration-300 hover:-translate-y-1.5 flex flex-col justify-between"
            >
              <div>
                {/* Card Header Badges */}
                <div class="flex items-center justify-between gap-2 mb-4">
                  <span class={`text-xs font-semibold px-2.5 py-0.5 rounded-full border ${getTrackBadgeClass(project.data.track)}`}>
                    {project.data.track}
                  </span>
                  <span class="text-xs font-mono font-medium text-slate-400">
                    {project.data.year}
                  </span>
                </div>

                {/* Title */}
                <h3 class="text-xl font-serif font-bold text-brand-slate mb-2 group-hover:text-brand-accent transition-colors line-clamp-2 leading-snug">
                  {project.data.title}
                </h3>

                {/* Client */}
                <p class="text-xs font-bold text-brand-blue uppercase tracking-wide mb-4">
                  {project.data.client}
                </p>

                {/* Excerpt or Summary */}
                {project.body && (
                  <p class="text-xs text-slate-600 leading-relaxed line-clamp-3 mb-6">
                    {project.body.replace(/<[^>]*>?/gm, '').replace(/[#*`[\]()]/g, '').slice(0, 140)}...
                  </p>
                )}
              </div>

              {/* Card Footer: Tag Chips & CTA */}
              <div class="pt-4 border-t border-slate-100 flex items-center justify-between gap-2">
                <div class="flex flex-wrap gap-1 max-w-[70%]">
                  {project.data.tags.slice(0, 2).map((tag) => (
                    <span key={tag} class="bg-slate-100 text-slate-600 text-[11px] font-medium px-2 py-0.5 rounded-md">
                      {tag}
                    </span>
                  ))}
                  {project.data.tags.length > 2 && (
                    <span class="text-[10px] text-slate-400 font-medium py-0.5">+{project.data.tags.length - 2}</span>
                  )}
                </div>

                <span class="text-xs font-bold text-brand-blue group-hover:underline flex items-center gap-0.5">
                  Explore &rarr;
                </span>
              </div>

            </a>
          ))}
        </div>
      )}

    </div>
  );
}
