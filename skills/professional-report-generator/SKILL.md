---
name: professional-report-generator
description: "Creates professional, publication-ready research reports as Word documents (.docx) on any topic. The skill conducts web research, structures findings into a multi-section report with executive summary, data tables, source citations, and bibliography, then produces a formatted .docx with title page, table of contents, headers/footers, and consistent typography. Use this skill whenever someone asks for a 'report', 'research report', 'white paper', 'briefing', 'analysis report', 'industry report', 'market overview', 'competitive analysis', 'trend report', 'deep dive', or any professional document that requires web research and structured findings. Also trigger when someone says things like 'research X and write it up', 'put together a report on Y', 'I need a professional document about Z', 'create a briefing on...', 'write up an analysis of...', or 'compile research on...'. Works with any topic, any industry, and any level of depth."
---

# Professional Report Generator

This skill produces publication-ready research reports as .docx files. It handles the full pipeline: clarifying scope with the user, conducting multi-source web research, structuring findings, and generating a professionally formatted Word document.

## Why this skill exists

Writing a good research report involves two distinct challenges: (1) finding and synthesizing quality information, and (2) producing a well-formatted, professional document. Most people are decent at one or the other, but doing both well in a single pass is time-consuming. This skill handles the mechanical parts — research gathering, document formatting, citation management, table construction — so the human can focus on what matters: defining the right questions and evaluating the output.

## Workflow

### Step 1: Clarify scope (quick interview)

Before starting research, ask the user 3-4 focused questions using AskUserQuestion. The goal is to understand scope without over-interviewing. Good questions to ask (pick the most relevant 3-4 based on context):

- **Audience**: Who will read this? (executives, technical team, clients, general public)
- **Depth**: How long should it be? Suggest a default based on the topic (e.g., "I'd suggest around 2,500-3,000 words — does that sound right?")
- **Angle**: Any specific aspects to focus on? Or should it be a broad overview?
- **Sections**: Do they want a specific structure, or should you propose one?
- **Recency**: How important is cutting-edge data? (e.g., "last 6 months only" vs. "historical context is fine")

If the user already provided a detailed brief (like a list of sections they want), skip the questions they've already answered and just confirm the remaining gaps.

### Step 2: Conduct web research

Use WebSearch to gather data from multiple angles. A strong research report typically needs 4-6 distinct searches to cover the topic properly. Think about it like a journalist working a story — you need:

- **Core data**: The main statistics and findings on the topic
- **Industry/sector specifics**: How the topic plays out in different contexts
- **Contrarian views**: What critics or skeptics say (this adds credibility)
- **Forward-looking perspectives**: Forecasts, projections, expert predictions
- **Source diversity**: Mix academic, industry, government, and journalistic sources

Run searches in parallel where possible. Aim for 10-15 citable sources in the final report. Keep track of every source as you go — you'll need author, title, organization, year, and URL for the bibliography.

### Step 3: Plan the report structure

Based on the research and the user's requirements, draft a report outline. A strong professional report typically includes:

1. **Title Page** — Topic, subtitle, date, source attribution
2. **Table of Contents** — Auto-generated from headings
3. **Executive Summary** — The whole report compressed into 200-400 words. Write this LAST (after all other sections) even though it appears first
4. **Main Body** — 3-6 major sections depending on scope. Each section should have a clear thesis supported by data
5. **Analysis/Discussion** — Synthesis, implications, what the data means
6. **Forecast/Outlook** (if appropriate) — Where things are headed
7. **Bibliography** — All cited sources, formatted consistently

Adapt this structure to fit the topic. A competitive analysis might have "Company Profiles" instead of "Industry Deep-Dives." A market overview might lead with "Market Size and Growth." The structure should serve the content, not the other way around.

### Step 4: Write the content

Write in professional but accessible prose. Some guidelines that produce better reports:

- **Lead with findings, not methodology.** Readers want conclusions first, then supporting evidence.
- **Every claim gets a citation.** Use inline citations like "(McKinsey, 2025)" or "(Author, Organization, Year)" — these will appear in the body text and map to the bibliography.
- **Use data tables for comparisons.** When you have 3+ items with multiple attributes, a table communicates faster than prose. Include 2-4 tables in a typical report.
- **Include contrarian perspectives.** A report that only presents one side reads like marketing. A section on limitations, criticism, or dissenting views adds intellectual credibility.
- **Write the executive summary last.** It should distill the entire report into key takeaways, not just introduce the topic.

### Step 5: Generate the .docx file

Read the `docx` skill's SKILL.md first — it contains critical formatting rules for the `docx` npm package. Then use the document generation template in `references/docx-template.js` as your starting point.

**Before writing any JavaScript, always:**
1. Read the docx skill at the path listed in available skills (it has the canonical formatting rules)
2. Read `references/docx-template.js` in this skill's directory for the report-specific template

The template provides:
- Title page with topic, subtitle, date, and source attribution
- Table of contents (auto-generated from headings)
- Consistent header/footer with report title and page numbers
- Professional typography (Arial, proper heading hierarchy)
- Color-coded data tables with alternating row shading
- Properly formatted bibliography with hanging indents
- Bullet lists using LevelFormat.BULLET (never unicode bullets)
- Page breaks between major sections

**Customization guidance:**
- Adapt the color palette to match the topic or client brand if specified
- Add or remove table columns based on the data you have
- Scale the number of sections to match the requested word count
- For shorter reports (under 1,500 words), skip the title page and TOC

After generating, validate with `validate.py` from the docx skill's scripts directory.

### Step 6: Deliver

Save the final .docx to the outputs directory. Present it with `present_files` if available. Keep the closing message brief — the document speaks for itself.

## Report Quality Checklist

Before delivering, mentally verify:

- [ ] Every factual claim has a source citation in the text
- [ ] Bibliography entries match the in-text citations
- [ ] Tables have clear headers and consistent formatting
- [ ] Executive summary captures the 3-5 most important findings
- [ ] The report has a logical flow from section to section
- [ ] Word count is within ~20% of the requested length
- [ ] No orphaned sections (sections referenced but not written, or vice versa)

## Adapting to different report types

The core workflow is the same regardless of report type, but emphasis shifts:

| Report Type | Key Emphasis | Typical Length |
|------------|-------------|---------------|
| Research Report | Data, sources, analysis | 2,500-4,000 words |
| Competitive Analysis | Company comparisons, SWOT | 2,000-3,500 words |
| Market Overview | Market size, segments, trends | 2,000-3,000 words |
| Trend Report | Timeline, drivers, forecasts | 1,500-2,500 words |
| Industry Briefing | Quick snapshot, key metrics | 1,000-1,500 words |
| White Paper | Problem-solution, thought leadership | 3,000-5,000 words |

## Common pitfalls to avoid

- **Over-researching.** 4-6 searches is usually enough. Don't spend 20 minutes researching when 10 will do.
- **Citation-free zones.** If you have a paragraph with no citations, you're either editorializing or you forgot to cite. Both are problems in a research report.
- **Table overload.** 2-4 tables is the sweet spot for a 3,000-word report. More than that and the document feels like a spreadsheet.
- **Generic executive summaries.** The executive summary should contain specific numbers and findings, not vague statements like "AI is transforming many industries."
