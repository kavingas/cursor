---
name: investigation-to-response
description: Generates customer-facing investigation responses and Jira panel comments from Adobe Commerce support investigation notes. Use when writing support replies from dyn.md, creating Jira findings, or when the user mentions customer response, Jira comment, or investigation output.
---

# Adobe Commerce Support Investigation Responses

Use this skill when generating support responses or Jira comments from investigation notes in `dyn.md` and findings in `find.md`.

## Input

- **Source files**: `dyn.md` (investigation notes, logs, observations), `find.md` (findings, evidence, screenshots, links)
- **Tone**: Adobe Commerce Support Engineer — courteous, confident, empathetic, clear technical explanations
- **Constraints**: Do not omit technical details; avoid "I" and "me"; include images and links from the source. **Do not refer to source file names** (e.g. dyn.md, find.md) in any output file content.

---

## Output folder structure

**Create all new files under a new folder** in the workspace root.

1. **Output root**: Create `investigation-output/` in the workspace root (or use a named folder such as `investigation-output-{ticket-id}` if a ticket ID is known). All generated files go under this folder.
2. **Images folder**: Create `investigation-output/images/`. Copy **all images** referenced in `dyn.md` and `find.md` (e.g. `![alt](image.png)`) into this folder. In generated markdown, reference them as `images/<filename>` so the output folder is self-contained.
3. **Generated files** (all under `investigation-output/`):
   - `dyn_customer.md` — customer-facing response
   - `jira_findings.md` — Summary panel for the top of the Jira ticket (so anyone viewing the ticket can understand the issue without reading through all comments)
   - `jira_internal.md` — combined internal Jira document for team (from dyn.md + find.md)

---

## 1. Customer-facing response (dynamic_comment)

**Output file**: `investigation-output/dyn_customer.md`

**Instructions**: Read the full content of `dyn.md`. Generate a polished, customer-facing investigation response. Keep output organized, easy to read, and professional. Include images and links from `dyn.md`; reference images as `images/<filename>` (they are copied to `investigation-output/images/`).

**Response structure** (use exactly):

```
Hello,

Thank you for contacting Adobe Commerce Support, and we appreciate your patience while we reviewed your request.

<content goes here>

If you have any questions or would like further clarification regarding the investigation, please don't hesitate to reach out. We value your partnership and are always glad to assist you.

Best Regards,
B G Kavinga
Adobe Commerce Support Team
```

Replace `<content goes here>` with the investigation summary and findings from `dyn.md`.

---

## 2. Jira ticket summary panel (jira_findings)

**Output file**: `investigation-output/jira_findings.md`

**Instructions**: This is **not** the customer-facing summary. It is a panel/block meant to be placed at the **top of the Jira ticket** so anyone (support, engineering, stakeholders) can quickly understand the issue without scrolling through all comments. Read the full content of `dyn.md` and generate a short summary with only key points for this at-a-glance panel.

**Response structure** (use this Jira panel format exactly):

```
{panel:borderStyle=dashed|borderColor=#cccccc|titleBGColor=#dddddd|bgColor=#deebff}
* *What is the issue? What happened?*
[Brief overview of what was investigated.]
* *What is the root cause?*
[As much detail as possible about the root cause.]
* *What are the recommendations?*
[Recommendations sent to the customer.]
{panel}
```

Save the final output as `investigation-output/jira_findings.md` in markdown format.

---

## 3. Internal Jira document (team sharing)

**Output file**: `investigation-output/jira_internal.md`

**Instructions**: Combine details from **both** `dyn.md` and `find.md` into a single internal document for sharing with the team in internal Jira. This is for internal use only (not customer-facing). Include:

- **From dyn.md**: Investigation notes, steps taken, logs, observations, conclusions, and any links or references.
- **From find.md**: Findings, evidence, repro steps, screenshots (reference as `images/<filename>` after copying to `investigation-output/images/`), links to local files (logs, stack traces), and external links.

Structure the combined content so the team has full context: issue summary, what was checked, evidence, root cause, and recommendations. Use clear headings and keep technical detail; internal audience may need logs, code references, and screenshots. Do not mention dyn.md, find.md, or any other source file names in the output.

**Format: Use Atlassian Confluence Wiki Markup** so the content pastes cleanly into Jira/Confluence and renders correctly for the internal team. Reference: [Confluence Wiki Markup](https://confluence.atlassian.com/doc/confluence-wiki-markup-251003035.html).

Common wiki markup to use in the internal summary:

| Purpose | Wiki markup |
|--------|-------------|
| Headings | `h1.`, `h2.`, `h3.` (e.g. `h2. Issue overview`) |
| Bold | `*bold text*` |
| Bullet list | `*` at line start (nest with `**`, `***`) |
| Numbered list | `#` at line start |
| Panel (box) | `{panel:title=...}...{panel}` or `{panel:borderStyle=dashed}...{panel}` |
| Monospace/code | `{{code or path}}` |
| Link | `[URL]` or `[link text|URL]` |
| Horizontal rule | `----` on its own line |

**Suggested structure** for `jira_internal.md` (in Confluence Wiki Markup). Do not use source file names in headings or body:

```
h1. Internal investigation summary

h2. Issue overview
[One-paragraph summary.]

h2. Investigation notes
[Key notes, steps, logs, observations. Use * for bullets, {{path}} for paths/code.]

h2. Findings and evidence
[Findings, repro steps, screenshots, file links, external references.]

h2. Root cause
[Detailed root cause for internal use.]

h2. Recommendations
[What was recommended to the customer and any follow-up for the team.]
```

Save as `investigation-output/jira_internal.md`. Reference images as `images/<filename>`. Prefer wiki markup throughout so the document is ready to paste into internal Jira/Confluence.

---

## Checklist

- [ ] Created `investigation-output/` and `investigation-output/images/` in workspace root
- [ ] Copied all images from dyn.md and find.md into `investigation-output/images/`
- [ ] Used full content of `dyn.md` (and `find.md` for jira_internal.md); no details omitted
- [ ] Tone is Support Engineer: courteous, confident, empathetic (customer outputs only)
- [ ] No first person (I, me) in customer response
- [ ] Images and links referenced as `images/<filename>` in all outputs
- [ ] Output files: `investigation-output/dyn_customer.md`, `investigation-output/jira_findings.md`, `investigation-output/jira_internal.md`; no output mentions dyn.md, find.md, or other source file names
- [ ] Jira findings panel is short and scannable (key points only), for display at top of ticket; internal Jira document is detailed for team
- [ ] Internal Jira document uses Confluence Wiki Markup (see [Confluence Wiki Markup](https://confluence.atlassian.com/doc/confluence-wiki-markup-251003035.html))
