import { useState } from "react"
import TextInput from "./components/TextInput"
import ImageUpload from "./components/ImageUpload"
import LanguageSelector from "./components/LanguageSelector"
import PartySelector from "./components/PartySelector"
import OutputPanel from "./components/OutputPanel"
import { summarizeText } from "./utils/summarize"
import { PARTIES } from "./components/PartySelector"
import { cleanText } from "./utils/cleanText"

export default function App() {
  const [text, setText] = useState("")
  const [language, setLanguage] = useState("tamil")
  const [party, setParty] = useState("")
  const [output, setOutput] = useState(null)
  const [loading, setLoading] = useState(false)

  const wordCount = text.trim() === "" ? 0 : text.trim().split(/\s+/).length
  const needsSummary = wordCount > 500

  const handleSummarize = async () => {
    setLoading(true)
    setOutput(null)
    const summary = await summarizeText(text, language)
    setOutput({ type: "summary", text: summary })
    setLoading(false)
  }

  const handleGenerateAudio = async () => {
  const rawText = output?.type === "summary" ? output.text : text
  if (!rawText.trim()) return alert("Paste or upload some text first!")

  const finalText = cleanText(rawText)
  const selectedParty = PARTIES.find((p) => p.id === party)

  setLoading(true)

  try {
    const response = await fetch("https://tamilselvan0709-politispeak.hf.space/generate-audio", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        text: finalText,
        party,
        language,
      }),
    })

    if (!response.ok) throw new Error("Backend error")

    const blob = await response.blob()
    const audioUrl = URL.createObjectURL(blob)

    setOutput({
      type: "audio",
      text: finalText,
      party,
      partyLabel: selectedParty?.leader || "",
      language,
      audioUrl,
    })

  } catch (err) {
    alert("Audio generation failed. Is backend running?")
    console.error(err)
  } finally {
    setLoading(false)
  }
}

  return (
    <div className="min-h-screen bg-gray-950 text-white p-6">
      <h1 className="text-3xl font-bold text-center mb-2 text-orange-400">
        🎙️ PolitiSpeak
      </h1>
      <p className="text-center text-gray-400 mb-8 text-sm">
        Paste post · Upload image · Hear it in their voice
      </p>

      <div className="max-w-2xl mx-auto space-y-5">
        <LanguageSelector language={language} setLanguage={setLanguage} />
        <PartySelector party={party} setParty={setParty} />
        <TextInput text={text} setText={setText} />
        <ImageUpload setText={setText} />

        {wordCount > 0 && (
          <p className="text-xs text-gray-500 text-right">
            {wordCount} words
            {needsSummary && (
              <span className="ml-2 text-orange-400 font-medium">
                · Long post detected
              </span>
            )}
          </p>
        )}

        <div className="flex gap-3">
          {needsSummary && (
            <button
              onClick={handleSummarize}
              disabled={loading}
              className="flex-1 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 py-2 rounded-lg font-semibold transition"
            >
              {loading ? "Summarizing..." : "📝 Summarize"}
            </button>
          )}

          <button
            onClick={handleGenerateAudio}
            disabled={!party || loading}
            className="flex-1 bg-orange-500 hover:bg-orange-600 disabled:opacity-50 disabled:cursor-not-allowed py-2 rounded-lg font-semibold transition"
          >
            🔊 Generate Audio
          </button>
        </div>

        {!party && (
          <p className="text-xs text-center text-gray-600">
            Select a party above to enable audio generation
          </p>
        )}

        <OutputPanel output={output} />
      </div>
    </div>
  )
}