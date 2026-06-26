const PARTIES = [
  { id: "tvk", name: "TVK", leader: "Vijay", color: "bg-yellow-500" },
  { id: "ntk", name: "NTK", leader: "Seeman", color: "bg-red-600" },
  { id: "dmk", name: "DMK", leader: "Stalin", color: "bg-red-500" },
  { id: "admk", name: "ADMK", leader: "Edappadi Palanisamy", color: "bg-green-600" },
  { id: "vck", name: "VCK", leader: "Thirumavalavan", color: "bg-blue-600" },
  { id: "mnm", name: "MNM", leader: "Kamal Haasan", color: "bg-purple-600" },
]

export { PARTIES }

export default function PartySelector({ party, setParty }) {
  return (
    <div className="space-y-2">
      <p className="text-xs text-gray-400 font-medium">SELECT PARTY / LEADER</p>
      <select
        value={party}
        onChange={(e) => setParty(e.target.value)}
        className="w-full bg-gray-800 border border-gray-700 rounded-lg p-3 text-sm text-white focus:outline-none focus:border-orange-400"
      >
        <option value="">-- Choose Party --</option>
        {PARTIES.map((p) => (
          <option key={p.id} value={p.id}>
            {p.name} — {p.leader}
          </option>
        ))}
      </select>

      {/* Selected leader badge */}
      {party && (() => {
        const selected = PARTIES.find((p) => p.id === party)
        return (
          <div className="flex items-center gap-2 bg-gray-800 border border-gray-700 rounded-lg px-3 py-2">
            <span className={`w-2 h-2 rounded-full ${selected.color}`} />
            <span className="text-xs text-gray-300">
              Voice: <span className="text-orange-400 font-medium">{selected.leader}</span>
            </span>
          </div>
        )
      })()}
    </div>
  )
}