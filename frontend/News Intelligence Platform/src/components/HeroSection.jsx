
export default function HeroSection() {
  return (
    <div className="relative text-center pt-20 pb-10 px-4 select-none">
      
      <div
        className="absolute inset-0 flex items-center justify-center pointer-events-none"
        aria-hidden="true"
      >
        <div className="w-[600px] h-[300px] bg-indigo opacity-10 blur-[120px] rounded-full" />
      </div>

    
      <p className="relative text-xs font-semibold tracking-[0.2em] uppercase text-indigo mb-4">
        Powered by RAG · Gemini · ChromaDB
      </p>

   
      <h1 className="relative text-5xl sm:text-6xl font-bold text-text-primary leading-tight mb-4">
        News Intelligence
        <span className="block text-transparent bg-clip-text bg-gradient-to-r from-indigo to-cyan">
          Platform
        </span>
      </h1>

      
      <p className="relative text-lg text-text-secondary max-w-xl mx-auto leading-relaxed">
        Ask anything about recent world events. Get synthesised answers
        grounded in live news — with sources.
      </p>
    </div>
  )
}