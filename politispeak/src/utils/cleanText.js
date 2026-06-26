export function cleanText(text) {
  return text
    // Remove @mentions
    .replace(/@[\w\u0B80-\u0BFF]+/g, "")
    // Remove #hashtags
    .replace(/#[\w\u0B80-\u0BFF]+/g, "")
    // Remove URLs
    .replace(/https?:\/\/\S+/g, "")
    // Remove www links
    .replace(/www\.\S+/g, "")
    // Remove emojis
    .replace(/[\u{1F000}-\u{1FFFF}]/gu, "")
    // Remove special Twitter symbols like · • | /
    .replace(/[|•·\/\\]+/g, " ")
    // Remove extra symbols
    .replace(/[<>{}[\]^~`]/g, "")
    // Collapse multiple spaces/newlines
    .replace(/\n{3,}/g, "\n\n")
    .replace(/ {2,}/g, " ")
    .trim()
}