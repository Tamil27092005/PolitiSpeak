export async function summarizeText(text, language) {
  const langPrompt = {
    tamil: "Summarize the following in simple Tamil language:",
    hindi: "Summarize the following in simple Hindi language:",
    english: "Summarize the following in simple English:",
  }

  const apiKey = import.meta.env.VITE_GROQ_API_KEY
  if (!apiKey) {
    throw new Error("Missing Groq API key. Add VITE_GROQ_API_KEY to your .env and restart the dev server.")
  }

  const response = await fetch("/api/groq/v1/chat/completions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${apiKey}`,
    },
    body: JSON.stringify({
      model: "llama3-8b-8192",
      messages: [{ role: "user", content: `${langPrompt[language]}\n\n${text}` }],
      max_tokens: 300,
    }),
  })

  const data = await response.json()
  return data.choices[0].message.content
}