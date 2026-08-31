import type {User} from './User'

export const CaseStatus = {
  Open: "open",
  Closed: "closed",
  Archived: "archived",
  Pending: "pending",
  InProgress: "in progress"
} as const;
 
export type CaseStatus = typeof CaseStatus[keyof typeof CaseStatus];

export const CasePriority = {
    Low: 'low',
    Medium: 'medium',
    High: 'high',
    Critical: 'critical'
}

export type CasePriority = typeof CasePriority[keyof typeof CasePriority];

export interface Tag{
    name: string
    description: string
    color: string
    id: string
}

export interface Case{
    title:string
    status:CaseStatus
    description: string
    priority: CasePriority
    created_by: User
    deleted_at: string
    id:string
    case_number:string
    created_at:string
    updated_at:string
    tags: Tag[]
}

export const CaseStatusLabels: Record<CaseStatus, string> = {
    [CaseStatus.Open]: "Active",
    [CaseStatus.Closed]: "Closed",
    [CaseStatus.InProgress]: "In Progress",
    [CaseStatus.Pending]: "In Review",
    [CaseStatus.Archived]: "Archived"
}
