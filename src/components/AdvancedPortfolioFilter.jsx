// src/components/AdvancedPortfolioFilter.jsx
import { useState, useMemo } from 'preact/hooks';

export default function AdvancedPortfolioFilter({ projects }) {
  const [selectedTrack, setSelectedTrack] = useState('All');
  const [selectedSkill, setSelectedSkill] = useState('All');

  const tracks = ['All', 'Global Development', 'Data Engineering & AI', 'Leadership'];

  // 1. Memoize the projects filtered by the selected track
  const projectsInTrack = useMemo(() => {
    if (selectedTrack === 'All') return projects;
    return projects.filter(p => p.data.track === selectedTrack);
  }, [selectedTrack, projects]);

  // 2. Derive the list of relevant skills ONLY from the projects in the current track
  const relevantSkills = useMemo(() => {
    const skills = new Set();
    projectsInTrack.forEach(p => p.data.tags.forEach(tag => skills.add(tag)));
    return ['All', ...skills];
  }, [projectsInTrack]);

  // 3. Get the final list of projects to render
  const finalFilteredProjects = useMemo(() => {
    if (selectedSkill === 'All') return projectsInTrack;
    return projectsInTrack.filter(p => p.data.tags.includes(selectedSkill));
  }, [selectedSkill, projectsInTrack]);
  
  // Handler to reset skill filter when a new track is chosen
  const handleTrackSelect = (track) => {
    setSelectedTrack(track);
    setSelectedSkill('All');
  };

  // ▼▼▼ ADD THIS LINE ▼▼▼
  console.log('Rendering with selectedTrack:', selectedTrack);
  // ▲▲▲ END OF ADDED LINE ▲▲▲

  return (
    <div>
      {/* Primary Filters: Tracks */}
      <div class="flex flex-wrap justify-center gap-4 mb-8">
        {tracks.map((track) => {
          const isActive = selectedTrack === track;
          return (
            <button
              key={track}
              onClick={() => handleTrackSelect(track)}
              class={`px-6 py-3 text-base font-bold rounded-lg transition-transform duration-300 transform hover:scale-105 ${
                isActive
                  ? 'bg-brand-blue text-white shadow-lg'
                  : 'bg-white text-brand-slate shadow-md'
              }`}
            >
              {track}
            </button>
          );
        })}
      </div>

      {/* Secondary Filters: Skills */}
      {selectedTrack !== 'All' && relevantSkills.length > 1 && (
        <div class="flex flex-wrap justify-center gap-2 mb-12 border-t border-gray-200 pt-8" data-animate-on-scroll>
          {relevantSkills.map((skill) => {
            const isSkillActive = selectedSkill === skill;
            return (
              <button
                key={skill}
                onClick={() => setSelectedSkill(skill)}
                class={`px-3 py-1 text-sm font-semibold rounded-full transition-colors duration-200 ${
                  isSkillActive
                    ? 'bg-brand-slate text-white'
                    : 'bg-gray-200 text-brand-slate hover:bg-gray-300'
                }`}
              >
                {skill}
              </button>
            );
          })}
        </div>
      )}

      {/* Project Grid */}
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {finalFilteredProjects.map((project) => (
          <a href={`/portfolio/${project.slug}/`} key={project.slug} class="block bg-white p-6 rounded-lg shadow-md hover:shadow-xl hover:-translate-y-1 transition-all duration-300 border-2 border-transparent hover:border-brand-blue">
            <h3 class="text-xl font-serif font-bold text-brand-slate mb-2">{project.data.title}</h3>
            <p class="text-sm font-semibold text-brand-blue mb-3">{project.data.client} &bull; {project.data.year}</p>
            <div class="flex flex-wrap gap-2">
              {project.data.tags.map((tag) => (
                <span key={tag} class="bg-blue-100 text-brand-blue text-xs font-medium px-2.5 py-0.5 rounded-full">{tag}</span>
              ))}
            </div>
          </a>
        ))}
      </div>
    </div>
  );
}