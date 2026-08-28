export interface CustodyEntry {
  id: string
  action: string
  actor: string
  detail: string
  timestamp: string
  prevHash: string
  row_hash: string
}

export interface CustodyLogResponse {
  entries?: CustodyEntry[]
  itemLabel?: string
  caseLabel?: string
}

export interface SelectOption {
  id: string
  label: string
}

export interface ChainOfCustodyRouteParams {
  chainId?: string
  evidenceId?: string
  [key: string]: string | undefined
}
