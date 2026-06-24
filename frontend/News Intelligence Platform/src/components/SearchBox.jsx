

import { useState } from 'react'

export default function SearchBox({ onSubmit, loading, initialValue = '' }) {
  const [value, setValue] = useState(initialValue)

 

  function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      submit()
    }
  }

  function submit() {
    const trimmed = value.trim()
    if (!trimmed || loading) return
    onSubmit(trimmed)
    setValue('')   
  }

  return (
    <div className="w-full max-w-2xl mx-auto px-4">
      <div className="
        flex items-center gap-3
        bg-elevated border border-border rounded-2xl
        px-4 py-3
        focus-within:border-indigo focus-within:ring-1 focus-within:ring-indigo
        transition-all duration-200
      ">
       
        <svg
          className="w-5 h-5 text-text-muted flex-shrink-0"
          fill="none" stroke="currentColor" viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
            d="M21 21l-4.35-4.35M17 11A6 6 0 1 1 5 11a6 6 0 0 1 12 0z" />
        </svg>

       
        <input
          type="text"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask anything about recent news…"
          disabled={loading}
          className="
            flex-1 bg-transparent text-text-primary placeholder-text-muted
            text-base outline-none
            disabled:opacity-50
          "
          autoFocus
        />

       
        <button
          onClick={submit}
          disabled={!value.trim() || loading}
          className="
            flex-shrink-0 px-4 py-1.5 rounded-xl
            bg-indigo text-white text-sm font-semibold
            hover:bg-indigo-dim disabled:opacity-40 disabled:cursor-not-allowed
            transition-colors duration-150
          "
        >
          {loading ? (
            <span className="flex items-center gap-2">
              <svg className="animate-spin w-4 h-4" viewBox="0 0 24 24" fill="none">
                <circle className="opacity-25" cx="12" cy="12" r="10"
                  stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor"
                  d="M4 12a8 8 0 018-8v8H4z" />
              </svg>
              Thinking
            </span>
          ) : 'Ask'}
        </button>
      </div>
    </div>
  )
}