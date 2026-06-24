

export default function SourceCards({ sources }) {
  if (!sources || sources.length === 0) return null

  return (
    <div className="w-full max-w-2xl mx-auto px-4 mt-8 animate-fade-up">
      <p className="text-xs font-semibold text-text-muted uppercase tracking-widest mb-4">
        Sources · {sources.length}
      </p>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {sources.map((source, i) => (
          <a
            key={i}
            href={source.url}
            target="_blank"
            rel="noopener noreferrer"
            className="
              group block p-4 rounded-xl
              bg-surface border border-border
              hover:border-cyan hover:bg-elevated
              transition-all duration-200
            "
          >
            
            <div className="flex items-center justify-between mb-2">
              <span className="
                text-xs font-semibold px-2 py-0.5 rounded-full
                bg-cyan/10 text-cyan border border-cyan/20
              ">
                {source.source}
              </span>
              
              <svg
                className="w-4 h-4 text-text-muted opacity-0 group-hover:opacity-100 transition-opacity"
                fill="none" stroke="currentColor" viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                  d="M14 3h7m0 0v7m0-7L10 14M5 5H3a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-2" />
              </svg>
            </div>

           
            <p className="text-sm text-text-secondary group-hover:text-text-primary leading-snug transition-colors line-clamp-3">
              {source.title}
            </p>
          </a>
        ))}
      </div>
    </div>
  )
}