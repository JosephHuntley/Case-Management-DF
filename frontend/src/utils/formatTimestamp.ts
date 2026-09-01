export function formatTimestamp(iso: string, short:boolean = false): string {
  const d = new Date(iso)
  if (Number.isNaN(d.getTime())) return iso
  const date = d.toISOString().slice(0, 10)
  const time = d.toTimeString().slice(0, 5)
  return !short ? `${date} · ${time}` : date
}
