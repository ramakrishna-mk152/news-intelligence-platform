

import { useState } from 'react'
import HeroSection    from '../components/HeroSection.jsx'
import NewsTickerBar  from '../components/NewsTickerBar.jsx'
import SuggestedChips from '../components/SuggestedChips.jsx'
import SearchBox      from '../components/SearchBox.jsx'
import AnswerPanel    from '../components/AnswerPanel.jsx'
import SourceCards    from '../components/SourceCards.jsx'
import { askQuestion } from '../services/api.js'

export default function HomePage() {
  
  const [question, setQuestion] = useState(null)
  const [answer,   setAnswer]   = useState('')
  const [sources,  setSources]  = useState([])
  const [loading,  setLoading]  = useState(false)
  const [error,    setError]    = useState(null)


  async function handleAsk(q) {
    setQuestion(q)
    setAnswer('')
    setSources([])
    setError(null)
    setLoading(true)

    try {
      const data = await askQuestion(q)
      setAnswer(data.answer)
      setSources(data.sources ?? [])
    } catch (err) {
      setError('Something went wrong. Is the backend running?')
    } finally {
      setLoading(false)
    }
  }

 
  function handleChipSelect(q) {
    handleAsk(q)
  }

  const hasAsked = question !== null

  return (
    <div className="min-h-screen flex flex-col bg-base">


      {!hasAsked && (
        <main className="flex-1 flex flex-col justify-center">
          <HeroSection />
          <NewsTickerBar />

        
          <div className="mt-8 mb-4 space-y-4">
            <SearchBox onSubmit={handleAsk} loading={loading} />
            <SuggestedChips onSelect={handleChipSelect} />
          </div>
        </main>
      )}

      
      {hasAsked && (
        <main className="flex-1 pb-32 pt-12 overflow-y-auto">

          
          {error && (
            <div className="max-w-2xl mx-auto px-4 mb-6">
              <div className="p-4 rounded-xl bg-red-950/40 border border-red-800 text-red-300 text-sm">
                {error}
              </div>
            </div>
          )}

         
          <AnswerPanel question={question} answer={answer} loading={loading} />
          {!loading && <SourceCards sources={sources} />}

          
          <div className="h-8" />
        </main>
      )}

      
      {hasAsked && (
        <footer className="
          fixed bottom-0 inset-x-0 z-10
          bg-base/90 backdrop-blur-md border-t border-border
          py-4
        ">
          <SearchBox onSubmit={handleAsk} loading={loading} />
        </footer>
      )}
    </div>
  )
}