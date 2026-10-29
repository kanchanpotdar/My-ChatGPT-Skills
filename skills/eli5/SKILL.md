---
name: eli5
description: >
  Explain complex topics in extremely simple language using
  interactive, visual-first HTML pages with large illustrations,
  diagrams, and minimal text.
homepage: https://github.com/anthropics/claude-plugins-community/tree/main/eli5
license: MIT
metadata:
  author: "Thariq Shihipar"
  upstream: "eli5@claude-community"
  upstream-version: "1.0.0"
---

# ELI5 — Explain Like I'm Five

## Purpose

Transform complex topics into simple, engaging, visual explanations
that anyone can understand without prior knowledge.

When the user invokes `/eli5 <topic>`, generate a self-contained
HTML explainer that prioritizes visual understanding over text.

## Core Principles

1. **Assume zero prior knowledge.**
   Explain concepts from the beginning without assuming familiarity
   with technical terminology.

2. **Show more, explain less.**
   Prioritize large diagrams, illustrations, visual comparisons,
   and simple animations over lengthy paragraphs.

3. **Use simple language.**
   Explain concepts using everyday words, relatable analogies,
   and short sentences.

4. **Explain progressively.**
   Start with the simplest idea, then introduce additional
   details through small, logical steps.

5. **Preserve accuracy.**
   Simplify explanations without introducing incorrect facts
   or misleading analogies.

## Workflow

### Step 1: Understand the Topic

Identify:
- The main concept the user wants to understand.
- The essential ideas needed to explain it.
- A suitable real-world analogy.
- The most effective way to visualize the concept.

Avoid unnecessary clarification unless the topic is ambiguous.

### Step 2: Structure the Explanation

Organize the explainer into:

1. **Big Picture**
   Introduce the concept using one simple visual and sentence.

2. **How It Works**
   Break the process into 3–5 illustrated steps.

3. **Real-World Example**
   Demonstrate the concept using a familiar situation.

4. **Key Takeaway**
   Summarize the central idea in 1–2 sentences.

Include only sections relevant to the topic.

### Step 3: Generate the HTML Explainer

Create a complete, self-contained HTML document.

Requirements:
- Use HTML, CSS, and vanilla JavaScript.
- Include all required CSS and JavaScript within the file.
- Avoid external dependencies and CDNs.
- Use SVG, CSS illustrations, and diagrams.
- Use large, readable text and generous spacing.
- Make the layout responsive for desktop and mobile.
- Use animations only when they improve understanding.
- Support keyboard navigation and reduced-motion preferences.

### Step 4: Visual Design

Follow these design guidelines:

- Visual-first layout with minimal text.
- Large illustrations and clear diagrams.
- Consistent colors and typography.
- Simple arrows and labels to demonstrate relationships.
- Interactive elements when useful.
- Clean, modern interface without unnecessary decoration.

Prefer one clear illustration over multiple complicated diagrams.

### Step 5: Simplify the Language

- Use short sentences.
- Explain unfamiliar terminology immediately.
- Avoid unnecessary jargon.
- Use relatable examples.
- Limit each explanation to its essential information.
- Avoid large paragraphs.

## Output Requirements

When invoked using `/eli5 <topic>`:

1. Generate a complete HTML explainer.
2. Save it as a single `.html` file when file creation is available.
3. Ensure the page works without an internet connection.
4. Provide the HTML artifact for viewing or saving.
5. Avoid lengthy explanations outside the artifact.

If file creation is unavailable, return the complete HTML source.

## Quality Checklist

Before finalizing, verify:

- Can a beginner understand the main concept?
- Are the visuals accurate and easy to interpret?
- Is the explanation concise?
- Does the HTML work independently?
- Is the page responsive?
- Are interactive elements functional?
- Are animations purposeful rather than decorative?

## Example

Input:
`/eli5 How does a neural network learn?`

Expected output:

A visual HTML explainer showing:

1. A neural network receiving information.
2. Connections between artificial neurons.
3. A prediction being generated.
4. The prediction being compared with the correct answer.
5. Connection weights changing to improve future predictions.

Use animated arrows, simple diagrams, and minimal text
to illustrate the learning process.
