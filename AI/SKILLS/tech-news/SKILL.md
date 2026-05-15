---
name: tech-news
description: "Use this skill whenever the user asks for a daily AI and tech news briefing, news update, or news digest. Triggers include: 'news briefing', 'daily news', 'what's new in AI', 'tech news today', or any request to summarise recent AI/tech product announcements. This skill defines the exact rules for sourcing, filtering, formatting, and deduplicating news. Always follow ALL constraints below — do not skip any step."
author: User-defined skill, drafted via Claude (claude.ai)
version: 1.0
last_run: May 15, 2026
---

# Daily AI & Tech News Briefing

## Purpose

Produce a concise, well-structured daily briefing of the latest AI and tech news — focused on new product launches and feature announcements — grouped by company, sourced only from articles published within the last 24 hours.

---

## Step-by-Step Workflow

### Step 1 — Search for fresh articles

Search the following trusted sources for AI and tech news. These are the canonical sources for consistency across every daily run:

| Source | URL | Focus |
|--------|-----|-------|
| Tech Startups | techstartups.com | Daily "Top Tech News Today" roundups |
| TechCrunch | techcrunch.com | Product launches, startup news |
| The Verge | theverge.com | Consumer tech, AI products |
| VentureBeat | venturebeat.com | Enterprise AI, model releases |
| LLM Stats | llm-stats.com | Model releases, API updates |
| Releasebot (OpenAI) | releasebot.io/updates/openai | Official OpenAI product updates |
| Crescendo AI News | crescendo.ai/news | Agentic AI, enterprise AI |
| MarTech | martech.org | AI-powered product launches |
| Oracle AI Blog | blogs.oracle.com/ai-and-datascience | Oracle product updates |
| Marketing Profs AI Update | marketingprofs.com | Weekly AI product digest |

**Search queries to use:**
- `AI tech news today [DATE]`
- `AI product launch feature announcement [DATE]`
- `[Company name] new product announcement [DATE]`

---

### Step 2 — Apply the date filter (CRITICAL)

> **Only include articles published within 1 day of the briefing date.**

| Briefing date | Acceptable article dates |
|---------------|--------------------------|
| May 15 | May 14 or May 15 |
| May 16 | May 15 or May 16 |
| May 17 | May 16 or May 17 |
| … and so on | … |

**How to verify publication date:**
- Check the article's `published_time` metadata or visible date stamp.
- Use `web_fetch` on the article URL and check `meta-article:published_time` in the page metadata.
- If the publication date cannot be confirmed, **exclude the article**.
- If a source aggregates older news without clear per-item dates, **exclude that source for that run**.

⚠️ Do NOT include news from articles published more than 1 day before the briefing date, even if the news itself sounds recent.

---

### Step 3 — Filter for relevant news only

Only include items that are:
- **New product launches** (a product, model, tool, or app going live)
- **New feature announcements** (a meaningful update to an existing product)
- **New partnerships or integrations** that result in a product/feature change

**Exclude:**
- Opinion pieces, analysis, or commentary
- Funding rounds (unless a product launch is directly tied to it)
- Layoffs, restructurings, or financial results (unless a new product/feature is announced alongside)
- Regulatory news
- Anything described as "reportedly", "rumoured", or "expected" without a concrete release

---

### Step 4 — Deduplicate against the previous run

> The user will paste the **last briefing date** at the start of each session (e.g. "last run: May 15, 2026").

- Compare newly found news against the previous briefing.
- If a story covers the **same product/feature** already listed in the prior run, **skip it**.
- If a story is a meaningful update or follow-up to a prior story (e.g. more details on a previously announced feature), it **may be included** and should be labelled as an update.
- If no prior briefing date is provided, include all qualifying news from the past 24 hours.

---

### Step 5 — Format the output

Use this exact format:

```
## 🗞️ Daily AI & Tech Briefing — [DATE]
**Sources used (published [DATE-1] to [DATE] only):** [list sources actually used]

---

**[Company Name]**
- [One-sentence summary of news item 1]
- [One-sentence summary of news item 2]

**[Company Name]**
- [One-sentence summary of news item]

---
📌 Next run: Say "news briefing" and include → last run: [DATE]
```

**Formatting rules:**
- Company name appears **once**, bold, as a header for that group.
- Each news item under it is a bullet point — one sentence, clear and factual.
- Do **not** repeat the company name per bullet.
- Do **not** use sub-headers inside a company's section.
- If only one item qualifies for a company, still use the bullet format.
- End every briefing with the `📌 Next run` line so the user can copy it for the next session.

---

### Step 6 — Add a transparency note if needed

If the briefing is shorter than usual due to the date filter excluding older sources, add a brief note:

```
⚠️ Transparency note: Today's briefing is shorter than usual — [X] sources were excluded 
because their articles were published before [DATE-1]. The date filter is working as intended.
```

---

## Example Output

```
## 🗞️ Daily AI & Tech Briefing — May 15, 2026
**Sources used (published May 14–15 only):** techstartups.com, releasebot.io

---

**Meta**
- Launched Incognito Chat, a new private mode for Meta AI conversations across its 
  platforms, giving users control over whether their chats are stored or used for training.
- Rolled out a WhatsApp-specific incognito AI mode where conversations disappear at 
  session end, with age verification and built-in safety filters enabled by default.

**Cisco**
- Cut nearly 4,000 jobs to redirect investment into AI infrastructure, silicon, and 
  security, while raising its annual revenue forecast after booking $5.3B in AI orders.

---
📌 Next run: Say "news briefing" and include → last run: May 15, 2026
```

---

## Session Startup Instructions

When the user starts a new session with "news briefing", expect them to also provide:

```
last run: [DATE]
```

If they do not provide it, ask:
> "What date was your last briefing? I'll use that to filter out anything you've already seen."

If they confirm there was no prior run, treat it as the first run and include all articles from the past 24 hours.

---

## Constraints Summary (Quick Reference)

| Constraint | Rule |
|------------|------|
| Article freshness | Published within 1 day of briefing date only |
| News type | Product launches and feature announcements only |
| Deduplication | Skip anything covered in the previous run |
| Format | Grouped by company; company name listed once |
| Bullets | One sentence per item, no company name repetition |
| Sources | Use the canonical source list; verify publish dates |
| Transparency | Note when fewer items appear due to date filtering |

---

## Notes for the User

- **You trigger it, Claude executes it.** Claude cannot initiate sessions or send reminders. Set a daily reminder on your device and open a new chat when ready.
- **Paste the last run date** at the start of each session so Claude can deduplicate correctly. The easiest way is to copy the `📌 Next run` line from the previous briefing.
- **Memory is off by default** on claude.ai, so Claude has no recall of previous sessions unless you paste the prior briefing or its date.
- You can optionally paste the full previous briefing for stricter deduplication (Claude will cross-check item by item rather than just by date).
- To go deeper on any story, just ask: "Tell me more about [company/topic] from today's briefing."
- To filter by company or topic, ask: "Show me only OpenAI and Google from today."
