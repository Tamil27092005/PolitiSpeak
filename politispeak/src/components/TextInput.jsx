export default function TextInput({ text, setText }) {
  return (
    <textarea
      rows={6}
      placeholder="Paste politician's post here..."
      value={text}
      onChange={(e) => setText(e.target.value)}
      className="w-full bg-gray-800 border border-gray-700 rounded-lg p-3 text-sm resize-none focus:outline-none focus:border-orange-400"
    />
  )
}