

const SUGGESTED_QUESTIONS = [
  'What happened in AI recently?',
  'India-China relations',
  'Latest stock market news',
  'Middle East developments',
  'Major tech funding news',
]

export default function SuggestedChips({ onSelect }) {
  return (
    <div className="flex flex-wrap justify-center gap-2 px-4 py-4 animate-fade-up">
      {SUGGESTED_QUESTIONS.map((q) => (
        <button
          key={q}
          onClick={() => onSelect(q)}
          className="
            px-4 py-2 rounded-full text-sm font-medium
            bg-elevated border border-border text-text-secondary
            hover:border-indigo hover:text-text-primary hover:bg-indigo/10
            transition-all duration-150 cursor-pointer
          "
        >
          {q}
        </button>
      ))}
    </div>
  )
}