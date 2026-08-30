import { useState } from "react"
import { Copy, Check } from "lucide-react"
import "./HashDisplay.css"

function truncateHash(hash: string, edge = 5): string {
  if (!hash || hash.length <= edge * 2 + 1) return hash
  return `${hash.slice(0, edge)}…${hash.slice(-edge)}`
}

interface HashDisplayProps {
  value: string | undefined | null
}

function HashDisplay({ value }: HashDisplayProps) {
  const [copied, setCopied] = useState(false)

  if (!value) return <p className="mono">—</p>

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(value)
      setCopied(true)
      setTimeout(() => setCopied(false), 1500)
    } catch (err) {
      console.error("Failed to copy hash:", err)
    }
  }

  return (
    <button
      type="button"
      className={`hash-display mono${copied ? " copied" : ""}`}
      data-tooltip={copied ? "Copied!" : value}
      onClick={handleCopy}
      aria-label={copied ? "Copied to clipboard" : `Copy full hash ${value}`}
    >
      <span>{truncateHash(value)}</span>
      {copied ? <Check size={12} /> : <Copy size={12} />}
    </button>
  )
}

export default HashDisplay
