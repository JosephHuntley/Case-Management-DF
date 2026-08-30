import type { ChainOfCustody } from "./ChainOfCustody";
import type { User } from "./User";

export const EvidenceType = {
  DiskImage: "disk_image",
  MemoryDump: "memory_dump",
  NetworkCapture: "network_capture",
  LogFile: "log_file",
  Document: "document",
  Photograph: "photograph",
  Other: "other",
} as const;
 
export type EvidenceType = typeof EvidenceType[keyof typeof EvidenceType];
 
export const AcquisitionMethod = {
  DD: "dd",
  FTK: "ftk",
  EnCase: "encase",
  Cellebrite: "cellebrite",
  Manual: "manual",
  Other: "other",
} as const;
 
export type AcquisitionMethod = typeof AcquisitionMethod[keyof typeof AcquisitionMethod];


export interface Evidence {
    id: string;
    case_id: string;
    evidence_tag: string;
    case_title: string;
    acquired_by: User;
    name: string;
    description: string;
    evidence_type: EvidenceType;
    acquisition_method: AcquisitionMethod;
    acquired_at: string;
    sha256: string;
    md5: string;
    size_bytes: number;
    is_verified: boolean;
    source_path: string;
    created_at: string;
    updated_at: string;
    chain_of_custody: ChainOfCustody[]
}

export const EvidenceTypeLabels: Record<EvidenceType, string> = {
  [EvidenceType.DiskImage]: "Disk Image",
  [EvidenceType.MemoryDump]: "Memory Dump",
  [EvidenceType.NetworkCapture]: "Network Capture",
  [EvidenceType.LogFile]: "Log File",
  [EvidenceType.Document]: "Document",
  [EvidenceType.Photograph]: "Photograph",
  [EvidenceType.Other]: "Other",
};

export const AcquisitionMethodLabels: Record<AcquisitionMethod, string> = {
  [AcquisitionMethod.DD]: "dd",
  [AcquisitionMethod.FTK]: "FTK Imager",
  [AcquisitionMethod.EnCase]: "EnCase",
  [AcquisitionMethod.Cellebrite]: "Cellebrite",
  [AcquisitionMethod.Manual]: "Manual",
  [AcquisitionMethod.Other]: "Other",
};