

import { useEffect, useState } from 'react'
import { fetchArticles } from '../services/api.js'


function formatDate(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}


function TickerCard({ article }) {
  return (
    <a
      href={article.url}
      target="_blank"
      rel="noopener noreferrer"
      className="
        flex-shrink-0 w-64 mx-2 p-4 rounded-xl
        bg-surface border border-border
        hover:border-indigo hover:bg-elevated
        transition-colors duration-200 group
      "
    >
      
      <div className="flex items-center justify-between mb-2">
        <span className="text-xs font-semibold text-indigo uppercase tracking-wide">
          {article.source}
        </span>
        <span className="text-xs text-text-muted">
          {formatDate(article.published_at)}
        </span>
      </div>

      
      <p className="text-sm text-text-primary leading-snug line-clamp-3 group-hover:text-white transition-colors">
        {article.title}
      </p>
    </a>
  )
}

export default function NewsTickerBar() {
  const [articles, setArticles] = useState([])
  const [error, setError]       = useState(false)

  useEffect(() => {
    fetchArticles()
      .then(setArticles)
      .catch(() => setError(true))
  }, [])   

  if (error) {
    return (
      <p className="text-center text-text-muted text-sm py-4">
        Could not load live articles — is the backend running?
      </p>
    )
  }

  if (articles.length === 0) {
    return (
      <div className="flex gap-3 justify-center py-6 px-8 overflow-hidden">
      
        {Array.from({ length: 5 }).map((_, i) => (
          <div
            key={i}
            className="flex-shrink-0 w-64 h-24 rounded-xl bg-surface border border-border animate-pulse"
          />
        ))}
      </div>
    )
  }

  return (
    <div className="py-6">
     
      <p className="text-xs font-semibold text-text-muted uppercase tracking-widest text-center mb-4">
        Live News
      </p>

      
      <div className="overflow-hidden ticker-wrapper">
       
        <div className="flex ticker-track animate-ticker">
          {[...articles, ...articles].map((article, i) => (
            <TickerCard key={`${article.id}-${i}`} article={article} />
          ))}
        </div>
      </div>
    </div>
  )
}