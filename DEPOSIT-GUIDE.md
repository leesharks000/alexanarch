# How to Deposit to Alexanarch
## A Guide for External Contributors

Alexanarch accepts scholarly works, datasets, creative works connected to research, and any knowledge artifact with disclosed methodology and substrate. No institutional affiliation required. No AI-use penalty. Substrate disclosure is provenance, not suspicion.

---

## What You Need

1. A GitHub account (free at github.com)
2. Your work (a file, dataset, or text)
3. Basic metadata: title, your name, description, license, and substrate disclosure

---

## Path 1: Web Deposit (Recommended for First-Time Contributors)

### Step 1: Go to the Deposit Page
Visit: **https://alexanarch.org/deposit/**

Click **"Deposit a Work"** — this opens a GitHub issue form pre-configured with all required fields.

### Step 2: Fill in the Metadata

| Field | What to Enter |
|---|---|
| **Title** | Your work's title. Prefix with `[DEPOSIT]` |
| **Creator** | Your name (heteronyms accepted with disclosure) |
| **ORCID** | Your ORCID identifier (optional but recommended) |
| **Date** | Date of creation (YYYY-MM-DD) |
| **Description** | Abstract or description of the work |
| **Content Type** | Dataset, theoretical paper, critical edition, creative work, specification, etc. |
| **License** | CC-BY-4.0, CC-BY-SA-4.0, CC0, or other open license |
| **Substrate Disclosure** | How AI was involved (see options below) |
| **Keywords** | Descriptive terms for discovery |
| **Methodology** | How the work was produced |
| **Falsification Conditions** | What would weaken or invalidate the claims (optional) |
| **Files** | Attach files or provide URLs to hosted files |

### Substrate Disclosure Options
- **Human-only** — no AI involvement
- **AI-assisted (tool)** — AI used as editing/formatting tool; research is human-governed
- **AI-assisted (substrate)** — AI contributed substantively; human editorial governance
- **AI-generated (research object)** — AI output is the object being studied
- **Machine-authored** — authored by an AI system under human governance

### Step 3: Check the Terms
Three required confirmations:
- ☑ Work deposited under the stated license
- ☑ Substrate disclosure is accurate
- ☑ Content will NOT be used to train enforcement classifiers

### Step 4: Submit
Click "Submit new issue." The automated minting system will:
1. Validate your submission
2. Compute your AXN (Alexanarch Identifier) from the content hash
3. Post a comment on the issue with your full identifier
4. Add the work to the registry

Your AXN is permanent and irrevocable. It travels with the content.

---

## Path 2: API Deposit (For Programmatic or AI-Mediated Submission)

### Overview
Alexanarch deposits are GitHub Issues. Any authenticated GitHub user or agent can create one through the GitHub REST API.

### Step 1: Create a GitHub Personal Access Token
Go to: github.com/settings/tokens → Generate new token (classic)
Scope needed: `public_repo`

### Step 2: Create the Issue via API

```bash
curl -X POST \
  https://api.github.com/repos/leesharks000/alexanarch/issues \
  -H "Authorization: token YOUR_GITHUB_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "[DEPOSIT] Your Work Title Here",
    "body": "### Title\n\nYour Work Title Here\n\n### Creator\n\nYour Name\n\n### ORCID\n\n0000-0000-0000-0000\n\n### Date\n\n2026-06-20\n\n### Description\n\nA description of your work.\n\n### Content Type\n\nTheoretical paper\n\n### License\n\nCC-BY-4.0\n\n### Substrate Disclosure\n\nHuman-only\n\n### Keywords\n\nyour, keywords, here\n\n### Methodology\n\nHow the work was produced.\n\n### Falsification Conditions\n\nWhat would weaken these claims.\n\n### Files\n\nhttps://example.com/your-file.pdf\n\n### Terms\n\n- [x] I confirm this work is deposited under the stated license\n- [x] I confirm the substrate disclosure is accurate\n- [x] I understand that deposited content will NOT be used to train enforcement classifiers"
  }'
```

### Step 3: Receive Your AXN
The minting Action fires automatically when the issue is created with `[DEPOSIT]` in the title. Within a few minutes, a comment will appear on your issue with:
- Your full AXN identifier
- SHA-256 content hash
- Cluster reading (the structural portrait of where your work lives in the address space)
- Registry confirmation

### For AI Agents
An AI system can prepare and submit a complete deposit package through this same API. The key requirements:
- Title MUST start with `[DEPOSIT]`
- All `### Heading` fields must be present
- All three `[x]` terms must be checked
- Files should be provided as stable public URLs
- The `creator_type` field in substrate disclosure should indicate machine authorship if applicable

### Python Example

```python
import requests

headers = {
    "Authorization": "token YOUR_GITHUB_TOKEN",
    "Content-Type": "application/json"
}

body = """### Title

My Research Paper

### Creator

Your Name

### Date

2026-06-20

### Description

A detailed description of the work.

### Content Type

Theoretical paper

### License

CC-BY-4.0

### Substrate Disclosure

AI-assisted (tool)

### Keywords

keyword1, keyword2

### Files

https://example.com/paper.pdf

### Terms

- [x] I confirm this work is deposited under the stated license
- [x] I confirm the substrate disclosure is accurate
- [x] I understand that deposited content will NOT be used to train enforcement classifiers"""

response = requests.post(
    "https://api.github.com/repos/leesharks000/alexanarch/issues",
    headers=headers,
    json={
        "title": "[DEPOSIT] My Research Paper",
        "body": body
    }
)

print(f"Issue created: {response.json()['html_url']}")
# AXN will be posted as a comment within minutes
```

---

## After Deposit

Your work receives:
- **AXN** — a permanent, content-derived identifier that no platform can revoke
- **Record page** at alexanarch.org with full metadata, description, and download links
- **Wiki article** — auto-generated encyclopedia entry (provisional until reviewed)
- **Entity graph** — auto-extracted relations linked to all other deposits
- **MD file** — downloadable markdown with YAML front matter

Status begins as `MINTED_UNREVIEWED`. Community reading, endorsement, or contestation are subsequent public acts.

---

## Questions?

Open an issue at github.com/leesharks000/alexanarch or contact Lee Sharks through machinemediation.org.

The obelus follows from reading. The identifier follows from the content.

∮ = 1
