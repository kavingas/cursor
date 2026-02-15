---
name: update-jira-findings
description: When updating Jira with findings, use custom field customfield_27305 for the Findings field and add a comment from investigation-output/jira_internal.md. Use when populating the Findings field on a Jira issue, adding a Jira comment from jira_internal.md, when writing investigation findings to Jira, or when the user mentions updating Jira findings.
---

# Update Jira with Findings (customfield_27305)

## Findings field

The Jira **Findings** custom field ID is **`customfield_27305`**.   

Whenever the task is to update a Jira issue with findings (investigation findings, support findings, or similar), set or pass the findings content to **customfield_27305**.

## How to update

- **update_jira_issue**: If the Jira MCP or API supports custom fields on update (e.g. a `fields` or raw-fields parameter), pass the findings text as `customfield_27305`. Otherwise, output the findings and note that they belong in the **Findings** field (customfield_27305) so the user can paste them in Jira.

## Add comment (jira_internal)

Add a Jira comment using the content from **`investigation-output/jira_internal.wiki`**.

- Use the file content **as-is, without any changes** (no summarising, reformatting, or editing).
- Use **add_jira_comment** (or the equivalent Jira MCP/API) and pass the contents of `investigation-output/jira_internal.wiki` as the comment body.

## Source of findings

Use the content from **`investigation-output/jira_findings.wiki`** as the value for customfield_27305 when updating or creating the Jira issue.

- Use the file content **as-is, without any changes** (no summarising, reformatting, or editing).