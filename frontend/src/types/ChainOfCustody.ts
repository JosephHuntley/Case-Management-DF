import type { User } from "./User"

export type CustodyAction =
  | "collected"
  | "transferred"
  | "checked_out"
  | "returned"
  | "archived"

export const CustodyActionLabels: Record<CustodyAction, string> = {
  collected: "Collected",
  transferred: "Transferred",
  checked_out: "Checked Out",
  returned: "Returned",
  archived: "Archived",
}

export interface ChainOfCustody {
  id: string
  evidence_id: string
  action: CustodyAction
  from_person: User | null
  to_person: User | null
  notes: string | null
  performed_by: User
  created_at: string
  previous_hash: string | null
  row_hash: string
}