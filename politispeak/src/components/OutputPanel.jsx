import { useState, useEffect, useRef } from "react"

export default function OutputPanel({ output }) {
  const [speaking, setSpeaking] = useState(false)
  const [paused, setPaused] = useState(false)
  const utteranceRef = useRef(null)

  // Stop speech when output changes
  useEffect(() => {
    window.speechSynthesis.cancel()
    setSpeaking(false)
    setPaused(false)
  }, [output])

  const getVoiceLang = (language) => {
    const map = {
      tamil: "ta-IN",
      hindi: "hi-IN",
      english: "en-IN",
    }
    return map[language] || "ta-IN"
  }

  const handlePlay = () => {
    if (!output?.text) return

    if (paused) {
      window.speechSynthesis.resume()
      setPaused(false)
      setSpeaking(true)
      return
    }

    window.speechSynthesis.cancel()

    const utterance = new SpeechSynthesisUtterance(output.text)
    utterance.lang = getVoiceLang(output.language)
    utterance.rate = 0.9
    utterance.pitch = 1

    // Pick best available voice for language
    const voices = window.speechSynthesis.getVoices()
    const match = voices.find((v) => v.lang === utterance.lang)
    if (match) utterance.voice = match

    utterance.onstart = () => setSpeaking(true)
    utterance.onend = () => { setSpeaking(false); setPaused(false) }
    utterance.onerror = () => { setSpeaking(false); setPaused(false) }

    utteranceRef.current = utterance
    window.speechSynthesis.speak(utterance)
  }

  const handlePause = () => {
    window.speechSynthesis.pause()
    setPaused(true)
    setSpeaking(false)
  }

  const handleStop = () => {
    window.speechSynthesis.cancel()
    setSpeaking(false)
    setPaused(false)
  }

  if (!output) return null

  return (
    <div className="bg-gray-800 rounded-lg p-4 text-sm text-gray-300 border border-gray-700 space-y-3">

      {/* Summary output */}
      {output.type === "summary" && (
        <>
          <p className="text-blue-400 font-semibold">📝 Summary</p>
          <p className="leading-relaxed">{output.text}</p>
          <p className="text-xs text-gray-500">
            ✅ Now click <span className="text-orange-400">Generate Audio</span> to hear this
          </p>
        </>
      )}

      {/* Audio output */}
      {output.type === "audio" && (
  <>
    <p className="text-orange-400 font-semibold">🔊 Audio — {output.partyLabel}</p>
    <p className="text-xs text-gray-500 leading-relaxed line-clamp-3">
      {output.text}
    </p>

    {output.audioUrl && (
      <audio
        controls
        autoPlay
        src={output.audioUrl}
        className="w-full mt-2 rounded-lg"
      />
    )}

    <p className="text-xs text-gray-600 text-center mt-1">
      ⚠️ Generic voice — cloned voice coming in Module 5
    </p>
  </>
)}
    </div>
  )
}