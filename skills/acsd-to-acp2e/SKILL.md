---
name: acsd-to-acp2e
description: When invoked with an ACSD issue, create two new ACP2E tickets with values extracted from that ACSD: (1) issue type "Customer Request", (2) issue type "Backport Request". Customer Request gets all fields (Summary, Support Tickets, Customer Names, Project Page, Affects Version/s, customfield_16201, customfield_29601 Business Impact, customfield_15900, customfield_15901); Backport Request gets the same except customfield_18505 (Project Page) is excluded. Fill the Jira Bug Report Template with content from acp2e.md and use that template as the ACP2E description. Also use to read/interpret these fields on any Jira issue.
---

# Jira fields: Support Tickets, Customer Names, Project Page, Affects Version/s

## Source files

- **Template:** **`jira-bug-report-template.md`** . **Always use this template when creating ACP2E**—the ticket description must follow its structure (Summary, Description, Steps to Reproduce, Actual Result, Expected Result, Attachments / References, Technical Details).
- **Content source:** **`acp2e.md`** (workspace root). **Fill the template with content from `acp2e.md` only.** Do not refer any content from ACSD in the ACP2E ticket description (no "Source: ACSD-XXXXX", no link to ACSD, no ACSD narrative). Map sections as follows:
  - `acp2e.md` **ISSUE** → template **Summary** (one-line title) and ACP2E ticket **summary**
  - `acp2e.md` **DESCRIPTION** → template **Description**
  - `acp2e.md` **STEPS** → template **Steps to Reproduce** (numbered list)
  - `acp2e.md` **ACTUAL** → template **Actual Result**
  - `acp2e.md` **EXPECTED** → template **Expected Result**
  - **Attachments / References** and **Technical Details** — fill only from `acp2e.md` if present; otherwise omit these sections. Do not add ACSD link or ACSD-sourced rows.


## When invoked with ACSD: create ACP2E

**When the user provides an ACSD issue key or invokes this skill in the context of an ACSD issue, create a new ticket in project ACP2E** by:

1. Getting the ACSD issue with **`get_jira_issue`** and passing the **`fields`** parameter with the Jira field IDs needed for ACP2E:
   - `issue_id_or_key`: the ACSD key (e.g. `ACSD-70139`)
   - `fields`: `["summary", "customfield_10802", "customfield_10803", "customfield_18505", "versions", "customfield_16201", "customfield_29601", "customfield_15900", "customfield_15901"]`
   (This requests only those fields from the API; see jira_client.get_issue implementation.)
2. Extracting from the response: Summary, Support Tickets, Customer Names, Project Page, Affects Version/s, customfield_16201, customfield_29601 (Business Impact), customfield_15900, customfield_15901 (see field IDs below).
3. Creating **two** ACP2E tickets with **`create_jira_issue`**, using the **same** summary, description, and extracted fields for both. For each ticket:
   - `project_key`: `"ACP2E"`
   - **First ticket:** `issue_type`: `"Customer Request"`
   - **Second ticket:** `issue_type`: `"Backport Request"`
   - `summary`: **Use `acp2e.md` ISSUE** as the ACP2E ticket summary (one-line title). If ISSUE is empty, use a one-line summary derived from DESCRIPTION if available; otherwise leave for the user to fill. Do not use placeholder text (e.g. "See description", "TBD"). Do not use ACSD summary in the ticket content.
   - `description`: **Use the Jira Bug Report Template** (see "Description template" section below). **Fill the template with content from `acp2e.md` only.** Do not refer ACSD in the description (no "Source: ACSD-XXXXX", no ACSD link in Attachments/References, no ACSD-sourced table rows). The final description must follow the template structure.
   - **Include the extracted values as Jira fields** (so they appear as proper fields, not only in the description):
     - **Customer Request:** pass all eight fields: `customfield_10802`, `customfield_10803`, `customfield_18505` (Project Page), `versions`, `customfield_16201`, `customfield_29601`, `customfield_15900`, `customfield_15901`.
     - **Backport Request:** pass the same fields **except** `customfield_18505` — do **not** include Project Page on the Backport Request ticket (seven fields: `customfield_10802`, `customfield_10803`, `versions`, `customfield_16201`, `customfield_29601`, `customfield_15900`, `customfield_15901`).

   Pass the **exact payload** returned by `get_jira_issue` into `create_jira_issue`. For option-type fields (e.g. customfield_16201 when it is a select), use the option object as returned—including the **option id**—so the create payload matches what Jira expects. Do not transform or stringify; pass the same structures. **Create both tickets** (Customer Request and Backport Request); only `issue_type` and the presence of `customfield_18505` differ (Backport Request omits Project Page).

Do not skip creating the ACP2E tickets when the invocation context is ACSD—creating both ACP2E tickets is the primary action.

## Description template (Jira Bug Report Template)

**When creating ACP2E, always use the template** at **`jira-bug-report-template.md`** (in the skill folder). Do the following:

1. **Read the template** to get the exact section headings and layout.
2. **Read `acp2e.md`** and **fill the template** with its content only (do not use any content from ACSD in the description):
   - **Summary** — from `acp2e.md` ISSUE (one line). If ISSUE is empty, omit the Summary section or use one line from DESCRIPTION; do not use placeholder text.
   - **Description** — from `acp2e.md` DESCRIPTION. Do not add "Source: ACSD-XXXXX" or any ACSD reference.
   - **Steps to Reproduce** — from `acp2e.md` STEPS as a numbered list.
   - **Actual Result** — from `acp2e.md` ACTUAL (errors, logs, code blocks as in file).
   - **Expected Result** — from `acp2e.md` EXPECTED.
   - **Attachments / References** and **Technical Details** — fill only from `acp2e.md` if those sections exist there; otherwise omit these sections. Do not add link to ACSD or rows sourced from ACSD.
3. **Output the filled template** as the ACP2E ticket description (use the same headings and tables as in the template; convert to Jira wiki markup as needed). **Omit any section that has no content in `acp2e.md`**; do not include empty sections or placeholder text (e.g. "TBD"). Do not refer or copy content from ACSD into the ACP2E description.

## Field identification

| Field ID            | Display name                 | Type     | Usage |
|---------------------|------------------------------|----------|--------|
| `customfield_10802` | Support Tickets              | Custom   | Support-ticket references or links (e.g. linked cases, related support IDs). |
| `customfield_10803` | Customer Names               | Custom   | Customer name(s) associated with the issue. |
| `customfield_18505` | Project Page                 | Custom   | Project page reference or link. |
| `versions`          | Affects Version/s            | Standard | Version(s) affected by the issue (not a custom field). |
| `customfield_16201` | (custom field 16201)          | Custom   | Copy from ACSD to ACP2E; use raw value from response. |
| `customfield_29601` | Business Impact               | Custom   | Copy from ACSD to ACP2E; use raw value from response. |
| `customfield_15900` | (custom field 15900)          | Custom   | Copy from ACSD to ACP2E; use raw value from response. |
| `customfield_15901` | (custom field 15901)          | Custom   | Copy from ACSD to ACP2E; use raw value from response. |

## How to read

1. **Get the issue** using the Jira MCP tool **`get_jira_issue`**. Pass **`fields`** with the relevant Jira field IDs so the API returns them (e.g. for ACSD→ACP2E use `fields`: `["summary", "customfield_10802", "customfield_10803", "customfield_18505", "versions", "customfield_16201", "customfield_29601", "customfield_15900", "customfield_15901"]`). If `fields` is omitted, all fields are returned.
2. **Locate the value** in the response:
   - **Custom fields:** In the Custom fields section, or in raw JSON: `result["fields"]["customfield_10802"]`, `result["fields"]["customfield_10803"]`, `result["fields"]["customfield_18505"]`, `result["fields"]["customfield_16201"]`, `result["fields"]["customfield_29601"]`, `result["fields"]["customfield_15900"]`, `result["fields"]["customfield_15901"]`.
   - **Affects Version/s:** Use the standard field `versions`; e.g. raw JSON `result["fields"]["versions"]`.

## Values to extract for ACP2E (from ACSD)

When creating ACP2E from ACSD, extract these from the ACSD issue’s `fields`:

| What to extract | Field | How to read |
|-----------------|--------|-------------|
| Summary | `acp2e.md` ISSUE | one-line title — use as ACP2E `summary` (do not use ACSD summary) |
| Support Tickets | `customfield_10802` | string or formatted list |
| Customer Names | `customfield_10803` | string or formatted list |
| Project Page | `customfield_18505` | use raw value from response |
| Affects Version/s | `versions` | each item’s `name` (e.g. `"2.4.7-p8"`) |
| customfield_16201 | `customfield_16201` | use raw value from response |
| Business Impact | `customfield_29601` | use raw value from response |
| customfield_15900 | `customfield_15900` | use raw value from response |
| customfield_15901 | `customfield_15901` | use raw value from response |

**Include summary and fields when creating each ACP2E ticket:** (1) Use **`acp2e.md` ISSUE** as the ACP2E ticket’s `summary` (do not use ACSD summary in ticket content). (2) **Customer Request:** pass all eight fields from ACSD to **`create_jira_issue`**. **Backport Request:** pass the same fields **except** `customfield_18505` (Project Page)—omit Project Page on the Backport Request. (3) **Fill the Jira Bug Report Template with content from `acp2e.md` only** and use that as the ACP2E `description`; do not refer any content from ACSD in the description (no "Source: ACSD", no ACSD link, no ACSD-sourced Attachments/Technical Details). (4) Create **two** tickets: first with `issue_type` **"Customer Request"**, second with `issue_type` **"Backport Request"**—same summary and description; Customer Request gets all eight fields, Backport Request gets seven (no customfield_18505).

## Value shape and formatting

- **Empty:** Omitted or shown as empty (custom fields in the Custom fields section; versions as standard field).
- **Single object:** For option fields, use `value`, `name`, `displayName`, or `key` for the human-readable label.
- **List:** Multiple items; formatted as comma-separated. For `versions`, each item is typically `{"name": "1.0", "id": "12345", ...}`; use `name` for the version label.
- **String/number:** Shown as-is (e.g. Support Tickets or Customer Names when stored as string).

## Quick reference

| Field                        | In code | User-facing name                    |
|-----------------------------|---------|-------------------------------------|
| Summary                     | `acp2e.md` ISSUE (not ACSD)                  | ACP2E ticket summary — from acp2e.md only       |
| Support Tickets             | `issue["fields"].get("customfield_10802")` | Support Tickets |
| Customer Names              | `issue["fields"].get("customfield_10803")` | Customer Names  |
| Project Page                | `issue["fields"].get("customfield_18505")` | Project Page |
| Affects Version/s           | `issue["fields"].get("versions")`          | Affects Version/s |
| customfield_16201 | `issue["fields"].get("customfield_16201")` | customfield_16201 |
| Business Impact | `issue["fields"].get("customfield_29601")` | Business Impact |
| customfield_15900 | `issue["fields"].get("customfield_15900")` | customfield_15900 |
| customfield_15901 | `issue["fields"].get("customfield_15901")` | customfield_15901 |

### get_jira_issue: pass `fields` for ACSD→ACP2E

When calling **get_jira_issue** to fetch an ACSD issue for creating ACP2E, always pass the **fields** parameter with this list of Jira field IDs:

`["summary", "customfield_10802", "customfield_10803", "customfield_18505", "versions", "customfield_16201", "customfield_29601", "customfield_15900", "customfield_15901"]`

Implementation: see `jira_client.get_issue(issue_id_or_key, fields=...)`; the client sends these as the `fields` query parameter to the Jira REST API.

### create_jira_issue: pass extracted fields for ACP2E

When calling **create_jira_issue** for ACP2E, pass the **payload from `get_jira_issue`** as-is for each field. For option/select fields, the object returned includes the **option id** (e.g. `id`, `value`); pass that full object so Jira sets the field correctly on create.

| Parameter             | Source from ACSD response   | Example / shape |
|-----------------------|-----------------------------|------------------|
| `summary`             | `acp2e.md` ISSUE            | string — one-line title from acp2e.md (do not use ACSD summary)     |
| `customfield_10802`   | `fields.customfield_10802`  | string (e.g. `"E-002066354"`) |
| `customfield_10803`   | `fields.customfield_10803`  | string (e.g. `"Asics Corporation"`) |
| `customfield_18505`   | `fields.customfield_18505`  | Project Page — use raw value from ACSD response. **Omit for Backport Request** (include only for Customer Request). |
| `versions`            | `fields.versions`           | array of version objects (e.g. `[{"id": "321926", "name": "2.4.7-p8"}]`) |
| `customfield_16201`   | `fields.customfield_16201`  | pass full payload from get_jira_issue (if option type, include option id) |
| `customfield_29601`   | `fields.customfield_29601`  | Business Impact — pass full payload from get_jira_issue (if option type, include option id) |
| `customfield_15900`   | `fields.customfield_15900`  | pass full payload from get_jira_issue (if option type, include option id) |
| `customfield_15901`   | `fields.customfield_15901`  | pass full payload from get_jira_issue (if option type, include option id) |

When creating ACP2E, use **`acp2e.md` ISSUE** as the ACP2E `summary` (do not refer ACSD content). Use the **exact payload** from `get_jira_issue` for the custom/version fields—including option ids for option-type fields—without transforming or stringifying. **Create two ACP2E tickets:** (1) **Customer Request** — same summary, description, and all eight fields (including `customfield_18505`). (2) **Backport Request** — same summary and description, but **omit `customfield_18505`** (Project Page); pass only the other seven fields. **Use the Jira Bug Report Template when creating ACP2E:** fill the template with content from `acp2e.md` only; do not refer any content from ACSD in the ticket description.
