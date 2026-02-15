---
name: m2install-script
description: Reference for m2install.sh options and workflows. Simplifies Magento 2 installation and deployment of client dumps from Magento 2 Support Extension. Use when running m2install.sh, installing Magento 2 from dumps, restoring Support Extension dumps, or when the user mentions m2install, Magento 2 install, or client dump deployment.
---

**When asked to set up or install an instance:** run `m2install.sh` from the folder path **derived from the Magento version**, not the current workspace. Use the project folder naming below (e.g. 2.4.7-p8 → `m247p8`), under the user's project root (e.g. `~/Sites/m247p8`). Run: `cd ~/Sites/<m24XpY>` then `m2install.sh …`.

# m2install.sh Reference

m2install.sh simplifies Magento 2 installation and deployment of client dumps created by the Magento 2 Support Extension.

## Project folder naming

Use short folder names from the Magento version:

**Pattern:** `2.4.X-pY` → `m24XpY` (drop dots and hyphen).

| Version  | Folder name |
|----------|-------------|
| 2.4.6-p1 | m246p1      |
| 2.4.7-p8 | m247p8      |
| 2.4.8-p2 | m248p2      |
| 2.4.9-p1 | m249p1      |

Create the folder under the user's project root (e.g. `~/Sites/<folder>` or their chosen base path).

## Restore from Support Extension dumps

When dumps are already in the project folder (e.g. `database.sql.gz` and `*.code.tgz` from the Support Extension widget):

1. **Run from the version-derived folder:** `cd` into the folder named from the Magento version (see table above), e.g. for 2.4.7-p8 use `cd ~/Sites/m247p8`, then run `m2install.sh` there. Do not use the current workspace path.
2. Optionally set `.m2install.conf` with `HTTP_HOST=` for your local URL.
3. Full restore (no prompts):  
   `m2install.sh -f`
4. Or specific steps only, e.g. DB + config:  
   `m2install.sh -f --step restore_db,configure_db,configure_files`

## Usage

```bash
m2install.sh [options]
```

## Options (quick reference)

| Option | Description |
|--------|-------------|
| `-h`, `--help` | Show help |
| `-s`, `--source (git, composer)` | Source of code |
| `-f`, `--force` | Install/restore without confirmations |
| `--sample-data (yes, no)` | Install sample data |
| `--ee` | Install Enterprise Edition |
| `--b2b` | Install B2B Extension |
| `--prex` | Install Product Recommendations |
| `--live-search` | Install Live Search |
| `-v`, `--version` | Magento version (Composer version or GIT branch) |
| `--mode (dev, prod)` | Magento mode. Dev skips static & di generation |
| `--quiet` | Suppress command output |
| `--skip-post-deploy` | Skip post-deploy script if present |
| `--skip-post-overwrite` | Skip post overwrite of original files |
| `--step <steps>` | Run only specified steps (comma, no spaces) |
| `--restore-table` | Restore only a specific table from DB dumps |
| `--debug` | Enable debug mode |
| `--php <path>` | PHP CLI path (e.g. `php71` or `/usr/bin/php71`) |
| `--remote-db` | Remote database name |
| `--es-host`, `--elasticsearch-host` | Elasticsearch host |
| `--es-port`, `--elasticsearch-port` | Elasticsearch port |
| `--uninstall` | Remove database and application from current folder |
| `--ee-path </path/to/ee>` | **(Deprecated)** Use `--ee` instead |

## Step values for `--step`

Steps (comma-separated, no spaces):

- `restore_code` – Restore code from dump
- `restore_db` – Restore database
- `configure_db` – Configure database
- `configure_files` – Configure files
- `installB2B` – B2B install (use with `--b2b`)
- `installPrex` – Product Recommendations install
- `installLiveSearch` – Live Search install

## Example invocations

**Restore DB and configure DB only:**
```bash
m2install.sh --step restore_db,configure_db
```

**B2B install step only:**
```bash
m2install.sh --step installB2B --b2b
```

**Product Recommendations only:**
```bash
m2install.sh --step installPrex
```

**Live Search only:**
```bash
m2install.sh --step installLiveSearch
```

**Full install with options (no prompts):**
```bash
m2install.sh -s composer -f --ee -v 2.4.6-p1 --mode dev
```

**Uninstall:**
```bash
m2install.sh --uninstall
```

## When to use this skill

- User asks how to run m2install.sh or which flags to use
- **User asks to set up or install an instance** — run `m2install.sh` from the folder derived from the version (e.g. 2.4.7-p8 → `~/Sites/m247p8`), not the current workspace (e.g. `cd ~/Sites/m247p8 && m2install.sh -f`)
- Restoring a client dump from Support Extension
- Installing Magento 2 (CE/EE) or adding B2B, Product Recommendations, or Live Search
- Running specific steps (e.g. only DB restore or only B2B install)
- Debugging or customizing install (PHP path, Elasticsearch, quiet mode)
