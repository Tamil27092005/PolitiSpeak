const langs = [
  { value: "tamil", label: "தமிழ் Tamil" },
  { value: "hindi", label: "हिंदी Hindi" },
  { value: "english", label: "English" },
]

export default function LanguageSelector({ language, setLanguage }) {
  return (
    <div className="flex gap-2">
      {langs.map((l) => (
        <button key={l.value} onClick={() => setLanguage(l.value)}
          className={`flex-1 py-2 rounded-lg text-sm font-medium transition ${
            language === l.value
              ? "bg-orange-500 text-white"
              : "bg-gray-800 text-gray-400 hover:bg-gray-700"
          }`}
        >
          {l.label}
        </button>
      ))}
    </div>
  )
}