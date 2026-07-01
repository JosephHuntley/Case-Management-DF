# Case-Management-DF
An open source case management platform for sorting digital forensics cases.

# Architecture (More Details to be added)
React Front End

Python backend (Fast API)

Job Runner / Task Queue

Embeded Postgres SQL 

# Features

## TODO (More Details to be added)
- ~~Create new cases~~
  - ~~Log new case in audit table~~
  - Assign tags to new cases
- ~~Cleaned Imports adding __init__.py files to services, schemas, and repositories~~
- ~~Added hash chain to audit table.~~
- Create Routes
  - ~~Cases~~
    - ~~Case Tags~~
  - ~~Tags~~
  - ~~Users~~
  - ~~Case Notes~~
  - ~~Chain of Custody~~
  - ~~Evidence Items~~
  - Report
- ~~Store case details in database~~
  - ~~Retrieve old cases~~
- Track changes to data 
  - Update each route to log changes in audit table
    - ~~Case~~
    - ~~Tags~~
    - ~~Users~~
    - ~~Chain of Custody~~
    - ~~Case Notes~~
    - ~~Evidence Items~~
    - ~~Failed logins~~
    - Report
  - Create tests
    - ~~Users~~
    - ~~Cases~~
    - ~~Tags~~ 
    - ~~Audit~~
    - ~~Case Notes~~
    - ~~Evidence Items~~
    - ~~Authenticate User~~
  - Embeded SQL
- Generate reports for common data extractions
- Integrate with other forensic tools (Which tools?)
  - To start, CLI Based tools like TSK and Volatility
- Fix status codes, particularly replace creating endpoints with 201 rather than 200
- Replace repeated user creation with helper function in unit tests
- ~~Add rate limiter on auth login~~
- ~~Log failed logins to the audit table or create new table for failed logins.~~
- ~~CORS~~ ## Note, CORS isn't added to the project because the project is built to operate on a LAN and shouldn't be exposed to the WAN
- Security Headers
- Lockout after x failed logins
- ~~Add check for prod or dev env before seeding the DB~~
- Tests for failed logins added to auth table

# SQL Schema (More Details to be added)
- Audit (Append Only)

## Tables
### NEEDS TO BE UPDATED
---

### users

System users/investigators.

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | Primary key |
| username | VARCHAR(50) UNIQUE | Login username |
| email | VARCHAR(255) UNIQUE | User email |
| password_hash | TEXT | Password hash |
| role | VARCHAR(50) | admin, investigator, auditor |
| is_active | BOOLEAN | Active account flag |
| created_at | TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |
| deleted_at | TIMESTAMP NULL | Soft delete timestamp |

---

### cases

Primary forensic cases.

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | Primary key |
| case_number | VARCHAR(100) UNIQUE | Human-readable case number |
| title | VARCHAR(255) | Case title |
| description | TEXT | Case description |
| status | VARCHAR(50) | open, closed, archived |
| priority | VARCHAR(50) | low, medium, high |
| created_by | UUID FK -> users.id | User who created case |
| assigned_to | UUID FK -> users.id | Assigned investigator |
| opened_at | TIMESTAMP | Case open timestamp |
| closed_at | TIMESTAMP NULL | Case close timestamp |
| created_at | TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |
| deleted_at | TIMESTAMP NULL | Soft delete timestamp |

---

## case_notes

Investigator notes attached to cases.

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | Primary key |
| case_id | UUID FK -> cases.id | Related case |
| author_id | UUID FK -> users.id | Note author |
| note | TEXT | Markdown-supported note |
| created_at | TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |
| is_archived | BOOLEAN | Is the note archived/deleted

---

## evidence_items

Digital evidence associated with a case.

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | Primary key |
| case_id | UUID FK -> cases.id | Related case |
| evidence_tag | VARCHAR(100) | Unique evidence identifier |
| name | VARCHAR(255) | Evidence name |
| description | TEXT | Evidence description |
| evidence_type | VARCHAR(50) | disk, memory, mobile, cloud |
| source_path | TEXT | Original acquisition path |
| acquisition_method | VARCHAR(100) | Acquisition process/tool |
| acquired_by | UUID FK -> users.id | Investigator who acquired evidence |
| acquired_at | TIMESTAMP | Acquisition timestamp |
| sha256 | CHAR(64) | SHA256 hash |
| md5 | CHAR(32) | Optional MD5 hash |
| size_bytes | BIGINT | Evidence size |
| is_verified | BOOLEAN | Hash verification status |
| created_at | TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |

---

## chain_of_custody

Tracks evidence handling and transfers.

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | Primary key |
| evidence_id | UUID FK -> evidence_items.id | Related evidence |
| action | VARCHAR(100) | acquired, transferred, analyzed |
| performed_by | UUID FK -> users.id | User performing action |
| from_person | VARCHAR(255) | Source person/entity |
| to_person | VARCHAR(255) | Destination person/entity |
| notes | TEXT | Additional details |
| created_at | TIMESTAMP | Event timestamp |

---


## tags

Reusable tags for organizing cases.

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | Primary key |
| name | VARCHAR(100) UNIQUE | Tag name |
| description | text | Description of tag |
| color | VARCHAR(7) | Optional UI color hex color | 
| created_at | TIMESTAMP | Creation timestamp |

---

## case_tags

Many-to-many relationship between cases and tags.

| Field | Type | Notes |
|---|---|---|
| case_id | UUID FK -> cases.id | Related case |
| tag_id | UUID FK -> tags.id | Related tag |
| created_at | TIMESTAMP | Creation timestamp |

Composite Primary Key:
- (case_id, tag_id)

---

## reports

Generated forensic reports.

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | Primary key |
| case_id | UUID FK -> cases.id | Related case |
| generated_by | UUID FK -> users.id | Report creator |
| report_type | VARCHAR(100) | Report template/type |
| file_path | TEXT | Report file location |
| created_at | TIMESTAMP | Generation timestamp |

---

## audit_log (Append Only)

Tracks all system modifications.

This table should NEVER allow:
- UPDATE
- DELETE

| Field | Type | Notes |
|---|---|---|
| id | BIGSERIAL PK | Primary key |
| entity_type | VARCHAR(100) | case, evidence, note |
| entity_id | UUID | Related entity ID |
| action | VARCHAR(50) | insert, update, delete |
| changed_by | UUID FK -> users.id | User making change |
| old_values | JSONB | Previous values |
| new_values | JSONB | Updated values |
| previous_hash | varchar(64) | Hash of the previous row |
| row_hash _ varchar(64) | Hash of the row's data |
| created_at | TIMESTAMP | Event timestamp |


**These tables aren't confrimed. Likely will be updated**
---

## artifacts

Parsed forensic findings and extracted artifacts.

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | Primary key |
| case_id | UUID FK -> cases.id | Related case |
| evidence_id | UUID FK -> evidence_items.id | Related evidence |
| tool_job_id | UUID FK -> tool_jobs.id | Generating tool job |
| artifact_type | VARCHAR(100) | file, process, registry, browser_history |
| artifact_key | VARCHAR(255) | Artifact identifier |
| artifact_value | JSONB | Flexible artifact data |
| discovered_at | TIMESTAMP NULL | Original discovery time |
| created_at | TIMESTAMP | Creation timestamp |

---

## forensic_tools

Registered forensic tools available to the platform.

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | Primary key |
| name | VARCHAR(100) | Tool name |
| version | VARCHAR(50) | Tool version |
| executable_path | TEXT | Executable location |
| tool_type | VARCHAR(50) | cli, api |
| created_at | TIMESTAMP | Creation timestamp |

Examples:
- volatility3
- fls
- mmls
- bulk_extractor

---

## tool_jobs

Queued or executed forensic jobs.

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | Primary key |
| case_id | UUID FK -> cases.id | Related case |
| evidence_id | UUID FK -> evidence_items.id | Related evidence |
| tool_id | UUID FK -> forensic_tools.id | Executed tool |
| submitted_by | UUID FK -> users.id | User who started job |
| command_line | TEXT | Full executed command |
| status | VARCHAR(50) | queued, running, failed, completed |
| started_at | TIMESTAMP NULL | Execution start |
| completed_at | TIMESTAMP NULL | Execution completion |
| exit_code | INTEGER NULL | Process exit code |
| stdout_path | TEXT NULL | STDOUT output file |
| stderr_path | TEXT NULL | STDERR output file |
| created_at | TIMESTAMP | Creation timestamp |

---
