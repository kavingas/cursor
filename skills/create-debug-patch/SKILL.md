---
name: create-debug-patch
description: Creates a <JIRA_ID>_DEBUG branch in both the Adobe Commerce CE and EE repos from a given base version, and adds the Debugger.php helper to CE. Use when starting a new debug-patch/investigation branch, or when the user mentions debug patch, DEBUG branch, or Debugger helper.
---

# Create debug patch

Automates the manual debug-patch workflow: create a `<JIRA_ID>_DEBUG` branch in both the CE and EE repos from a given base version, and add the `Magento\Framework\Debugger` helper class to the CE repo (it always goes in CE, even when the actual debug log statements are only added in EE).

## Input

Invocation: `/create-debug-patch <JIRA_ID> <BASE_VERSION>`

Example: `/create-debug-patch ACSD-71974 2.4.7-p10`

- `JIRA_ID` — ticket key, e.g. `ACSD-71974`.
- `BASE_VERSION` — any valid git ref present in both repos (release tag like `2.4.7-p10`, or a branch like `2.4-develop`).

If either argument is missing, ask the user for it before proceeding.

## Repos

- CE: `/Users/kavingas/Git/magento2ce`
- EE: `/Users/kavingas/Git/magento2ee`

## Steps

1. **Safety checks in both repos** (do this before touching anything):
   - `git -C <repo> status --porcelain --untracked-files=no` must be empty (untracked files are fine and ignored — e.g. scratch notes — since they don't block branch creation). If it's non-empty, stop and tell the user to commit or stash their changes first — never discard uncommitted work.
   - `git -C <repo> rev-parse --verify --quiet <BASE_VERSION>` must resolve. If it doesn't in a repo, suggest `git -C <repo> fetch --tags` (for a tag) or `git -C <repo> fetch origin <BASE_VERSION>` (for a branch) and stop — don't fetch automatically without telling the user.
   - `git -C <repo> rev-parse --verify --quiet <JIRA_ID>_DEBUG` — if this already resolves (branch exists) in either repo, stop and ask the user whether to reuse the existing branch or use a different `JIRA_ID`. Never force-recreate or overwrite it.

2. **Create the branch in each repo**, once checks pass in both:
   ```
   git -C /Users/kavingas/Git/magento2ce checkout -b <JIRA_ID>_DEBUG <BASE_VERSION>
   git -C /Users/kavingas/Git/magento2ee checkout -b <JIRA_ID>_DEBUG <BASE_VERSION>
   ```

3. **Add the Debugger helper to CE only.** `Debugger.php` is not part of `2.4-develop` or any release tag — it must be freshly added and committed on every new debug branch. Copy the canonical copy bundled with this skill (`assets/Debugger.php`, next to this file) to:
   ```
   /Users/kavingas/Git/magento2ce/lib/internal/Magento/Framework/Debugger.php
   ```
   Then commit it in the CE repo only:
   ```
   git -C /Users/kavingas/Git/magento2ce add lib/internal/Magento/Framework/Debugger.php
   git -C /Users/kavingas/Git/magento2ce commit -m "<JIRA_ID>: Add Debugger helper for debug logging"
   ```
   Do not add or commit anything in the EE repo.

4. **Print a ready-to-use log snippet** with `<JIRA_ID>` substituted, for the user to paste and adapt at the relevant code location(s) themselves (log points vary per investigation, so don't guess where to insert them):
   ```php
   $debugger = \Magento\Framework\Debugger::getInstance('<JIRA_ID>');
   $debugger->log('<JIRA_ID> DEBUG: <describe what fired>', [
       // relevant variables
   ], true);
   ```

5. **Do not push.** Finish with a short summary: branches created (and base ref used) in both repos, confirmation that the Debugger.php commit landed in CE only, and a reminder that the user should add their actual debug log calls, review the diff, and push manually (`git push -u origin <JIRA_ID>_DEBUG`) when ready.
