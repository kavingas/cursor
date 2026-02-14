# Cursor Skills – Adobe Commerce Support

A collection of [Cursor Agent Skills](https://docs.cursor.com/context/rules-for-ai#agent-skills) for Adobe Commerce support workflows: Jira ticket creation, Confluence/wiki formatting, and investigation response generation.

## Skills

| Skill | Description |
|-------|-------------|
| **markdown-to-wiki** | Converts markdown to Confluence wiki markup for pasting into Confluence or Jira. Use when you need wiki markup, Confluence format, or Atlassian markup. |
| **acsd-to-acp2e** | Creates two ACP2E Jira tickets from an ACSD issue: one **Customer Request** and one **Backport Request**. Fills the Jira Bug Report template from `acp2e.md` and maps Support Tickets, Customer Names, Project Page, Affects Version/s, and other custom fields. |
| **investigation-to-response** | Generates customer-facing investigation responses and Jira panel comments from Adobe Commerce support notes. Reads `dyn.md` and `find.md`, outputs `dyn_customer.md`, `jira_findings.md`, and `jira_internal.md` under an `investigation-output/` folder. |

## Structure

```
skills/
├── markdown-to-wiki/
│   └── SKILL.md
├── acsd-to-acp2e/
│   ├── SKILL.md
│   └── jira-bug-report-template.md
└── investigation-to-response/
    ├── SKILL.md
    └── investigation-output/
        ├── README.md
        └── jira_internal.md
```

## Using these skills

These skills are intended to be used by Cursor’s AI agent. Ensure they are available in your Cursor skills location (e.g. `~/.cursor/skills/` or linked from this repo). Cursor will invoke them automatically when your request matches their descriptions (e.g. “convert this to Confluence wiki”, “create ACP2E from ACSD”, “write a customer response from my investigation notes”).

## Requirements

- **acsd-to-acp2e**: Jira MCP or API access; `acp2e.md` in workspace root when creating tickets.
- **investigation-to-response**: `dyn.md` and optionally `find.md` in the workspace for investigation inputs.

## License

Use as needed for your workflows.
