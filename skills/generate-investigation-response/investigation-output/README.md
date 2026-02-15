# Investigation output structure

When the **Adobe Commerce Support Investigation Responses** skill runs, it creates this folder structure in your **workspace root** (e.g. `investigation-output/` or `investigation-output-{ticket-id}/`).

## Folder layout

```
investigation-output/
├── images/           # All images copied from dyn.md and find.md
├── dyn_customer.md   # Customer-facing response
├── jira_findings.md  # Summary panel for top of Jira ticket (quick understanding without reading all comments)
├── jira_internal.md  # Combined dyn.md + find.md for internal Jira (team)
└── README.md         # This file (optional in workspace)
```

## Files

| File | Purpose |
|------|--------|
| **dyn_customer.md** | Polished response to send to the customer. |
| **jira_findings.md** | Panel to place at the top of the Jira ticket so anyone can understand the issue at a glance (what happened, root cause, recommendations). |
| **jira_internal.md** | Full internal document for team Jira (investigation notes + findings/evidence). |
| **images/** | Screenshots and other images referenced in dyn.md/find.md; paths in outputs use `images/<filename>`. |

This README is a reference; the skill creates the actual `investigation-output/` folder in the project where you run it.
