---
name: markdown-to-wiki
description: Converts markdown files to Confluence wiki markup for pasting into Confluence or Jira. Use when converting markdown to wiki markup, preparing content for Confluence, or when the user mentions wiki markup, Confluence format, or Atlassian markup.
---

# Markdown to Confluence Wiki Markup

Convert markdown content to [Confluence wiki markup](https://confluence.atlassian.com/doc/confluence-wiki-markup-251003035.html) so it pastes and renders correctly in Confluence or Jira.

## When to use

- User asks to convert markdown to wiki markup
- Content will be pasted into Confluence or Jira
- User mentions Confluence, wiki markup, or Atlassian formatting

## Conversion reference

Apply these substitutions when converting markdown to wiki markup.

### Headings

| Markdown | Wiki markup |
|----------|-------------|
| `# Heading` | `h1. Heading` |
| `## Heading` | `h2. Heading` |
| `###` … `######` | `h3.` … `h6.` |

Use `hn.` at the start of the line (n = 1–6). Space after the period is required.

### Text effects

| Markdown | Wiki markup |
|----------|-------------|
| `**bold**` or `__bold__` | `*bold*` |
| `*italic*` or `_italic_` | `_italic_` |
| `` `code` `` | `{{code}}` |
| `~~deleted~~` | `-deleted-` |
| Blockquote `>` | `bq. ` at line start |
| `^superscript^` | `^superscript^` (same) |
| `~subscript~` | `~subscript~` (same) |

**Note:** In wiki markup, `*` is bold and `_` is italic. For italic next to another word, use braces: `Thing{_}x_`.

### Lists

| Markdown | Wiki markup |
|----------|-------------|
| `- item` or `* item` | `* item` (space between * and text) |
| Nested bullets | Add one more `*` per level: `**`, `***` |
| `1. item` | `# item` |
| Nested numbered | `##`, `###` for sub-levels |
| List line break within item | `\\\\` (double backslash) |

Empty lines can break lists; use `\\\\` for line breaks inside a list item.

### Converting markdown links to wiki format

Convert every markdown link to the Confluence wiki link form. Use the pipe `|` to separate parts (alias, URL, tooltip).

| Markdown | Wiki markup |
|----------|-------------|
| `[link text](url)` | `[link text\|url]` — alias first, then URL |
| `[link text](url "tooltip")` or `[link text](url 'tooltip')` | `[link text\|url\|tooltip]` — alias, URL, then tooltip |
| `[text](#anchor)` (same-page anchor) | `[text\|#anchor]` or `[#anchor]` if link text = anchor |
| `[text](pagename#anchor)` (in-space page + anchor) | `[text\|pagename#anchor]` (heading anchors are case-sensitive, no spaces) |
| `[url]` (bare URL / autolink) | `[url]` — leave as-is |
| `<https://example.com>` | `[https://example.com]` or `[label\|https://example.com]` |

**Confluence-specific link forms** (use when the target is Confluence/Jira):

| Target | Wiki markup |
|--------|-------------|
| Page in current space | `[pagetitle]` or `[link text\|pagetitle]` |
| Page in another space | `[spacekey:pagetitle]` or `[link text\|spacekey:pagetitle]` |
| Anchor on another page | `[pagetitle#headingname]` (heading name case-sensitive, no spaces) |
| User profile | `[~username]` |
| External URL | `[http://...]` or `[link text\|http://...]` |
| Attachment on page | `[pagetitle^filename.ext]` |

**Rules when converting:**

1. **Alias (link text):** Wiki uses `[alias|destination]`. So `[Display text](url)` → `[Display text|url]`.
2. **Tooltip:** If markdown has a title, add it as a third part: `[alias|url|tooltip]`.
3. **Pipes in text or URL:** If the link text or URL contains `|`, Confluence may break; prefer link text without pipes or use a short alias.
4. **Reference-style links:** Resolve `[text][ref]` by replacing `[ref]` with the defined URL, then convert the result as above (e.g. `[ref]: https://x.com` → use `[text|https://x.com]`).

### Images

| Markdown | Wiki markup |
|----------|-------------|
| `![alt](url)` | `!url!` or `!url\|alt=alt!` |
| `![alt](attachment.png)` (attachment) | `!attachment.png!` |
| Image on another page | `!pagetitle^image.png!` |
| Thumbnail | `!image.jpg\|thumbnail!` |

### Other

| Markdown | Wiki markup |
|----------|-------------|
| `---` or `***` (horizontal rule) | `----` on its own line |
| Paragraph break | Blank line (same as markdown) |
| Line break in paragraph | `\\\\` |
| Table \| col \| | `\|\|header1\|\|header2\|\|` then `\|cell1\|cell2\|` |

### Tables (wiki markup)

- Header row: `||col1||col2||col3||` (double bars for header cells)
- Data rows: `|cell1|cell2|cell3|` (single bars; one `|` between cells)

### Macros (when needed)

- Panel: `{panel:title=My Title}content{panel}`
- Code block: use `{code}...{code}` or keep as `{{inline}}` for short snippets
- Color: `{color:red}text{color}`

## Workflow

1. **Read** the markdown file(s) the user specifies (or the current/open file).
2. **Convert** using the table above. Walk through the content and replace:
   - Headings first
   - Then lists (bullets and numbers)
   - Then bold, italic, code
   - Then links and images
   - Then tables and blockquotes
   - Horizontal rules and line breaks
3. **Output** the result to a **new file with a `.wiki` extension and the same base name and path as the source.**
   - Example: `README.md` → `README.wiki`
   - Example: `docs/guide.md` → `docs/guide.wiki`
   - Write the converted wiki markup into this new file. Do not overwrite the original markdown file.
   - If the user explicitly asks for a different output (e.g. in-place replace or paste in reply), follow that instead.

## Gotchas

- **Escaping:** In wiki markup, `|` in link text or URL can need escaping; use `[text\|url]`.
- **Code blocks:** Confluence uses `{code:language}` ... `{code}` for multi-line; `{{...}}` for inline.
- **No edit-back:** Confluence converts wiki markup to storage format on paste; you can’t edit as wiki markup after that.
- **Images:** Attached images: `!filename.png!`. External: `!http://example.com/image.png!`.

## Reference

Full syntax: [Confluence Wiki Markup](https://confluence.atlassian.com/doc/confluence-wiki-markup-251003035.html) (headings, lists, tables, text effects, links, images, macros).
