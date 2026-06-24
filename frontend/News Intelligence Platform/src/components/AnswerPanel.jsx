

export default function AnswerPanel({ question, answer, loading }) {
  return (
    <div className="w-full max-w-2xl mx-auto px-4 animate-fade-up">

     
      <div className="mb-6">
        <p className="text-xs font-semibold text-text-muted uppercase tracking-widest mb-2">
          Your question
        </p>
        <h2 className="text-xl font-semibold text-text-primary leading-snug">
          {question}
        </h2>
      </div>

      
      <div className="w-12 h-0.5 bg-indigo mb-6 rounded-full" />

   
      <div>
        <p className="text-xs font-semibold text-text-muted uppercase tracking-widest mb-4">
          Answer
        </p>

        {loading ? (
         
          <div className="space-y-3">
            {[100, 90, 95, 70].map((w, i) => (
              <div
                key={i}
                style={{ width: `${w}%` }}
                className="h-4 rounded bg-elevated animate-pulse"
              />
            ))}
          </div>
        ) : (
          
          <div className="answer-body space-y-4">
            {answer.split('\n').filter(Boolean).map((para, i) => (
              <p key={i}>{para}</p>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}