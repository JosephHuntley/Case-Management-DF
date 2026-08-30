const UNITS = ["bytes", "KB", "MB", "GB", "TB"] as const

export function formatBytes(bytes: number, decimals = 1): string {
  if (!Number.isFinite(bytes) || bytes < 0) return "—"
  if (bytes === 0) return "0 bytes"

  const exponent = Math.min(
    Math.floor(Math.log(bytes) / Math.log(1024)),
    UNITS.length - 1
  )
  const value = bytes / Math.pow(1024, exponent)

  return exponent === 0
    ? `${value} ${UNITS[exponent]}`
    : `${value.toFixed(decimals)} ${UNITS[exponent]}`
}
