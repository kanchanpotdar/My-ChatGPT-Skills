/**
 * Professional Report Generator — docx-js Template
 *
 * This is a reference template, not a runnable script. Adapt it for each report
 * by changing the content, sections, tables, and color palette as needed.
 *
 * IMPORTANT: Before using this template, always read the docx skill's SKILL.md
 * for the canonical formatting rules (table widths, image types, list numbering, etc.).
 *
 * Usage:
 *   1. Copy this template into your working directory
 *   2. Replace placeholder content with your actual report content
 *   3. Add/remove sections, tables, and bullet lists as needed
 *   4. Run with: node create_report.js
 *   5. Validate with: python <docx-skill-path>/scripts/office/validate.py output.docx
 */

const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, LevelFormat,
  TableOfContents, HeadingLevel, BorderStyle, WidthType, ShadingType,
  PageNumber, PageBreak
} = require("docx");

// ============================================================
// COLOR PALETTE — Customize per report or client brand
// ============================================================
const COLORS = {
  DARK_BLUE: "1B3A5C",     // Headings, header cells
  MEDIUM_BLUE: "2E75B6",   // Subheadings, accents, rules
  LIGHT_BLUE: "D5E8F0",    // Highlight backgrounds
  DARK_GRAY: "333333",     // Body text
  MEDIUM_GRAY: "666666",   // Secondary text, footers
  LIGHT_GRAY: "F2F2F2",    // Alternating row shading
  ACCENT_GREEN: "3A7D44",  // Positive indicators
  ACCENT_RED: "C0392B",    // Negative indicators / warnings
  ACCENT_ORANGE: "E67E22",  // Neutral highlights
};

// ============================================================
// REUSABLE TABLE HELPERS
// ============================================================
const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };
const cellMargins = { top: 80, bottom: 80, left: 120, right: 120 };

// US Letter with 1-inch margins: content width = 9360 DXA
const CONTENT_WIDTH = 9360;

function headerCell(text, width) {
  return new TableCell({
    borders,
    width: { size: width, type: WidthType.DXA },
    shading: { fill: COLORS.DARK_BLUE, type: ShadingType.CLEAR },
    margins: cellMargins,
    verticalAlign: "center",
    children: [new Paragraph({
      children: [new TextRun({
        text, bold: true, color: "FFFFFF", font: "Arial", size: 20
      })]
    })]
  });
}

function dataCell(text, width, fill) {
  return new TableCell({
    borders,
    width: { size: width, type: WidthType.DXA },
    shading: fill ? { fill, type: ShadingType.CLEAR } : undefined,
    margins: cellMargins,
    children: [new Paragraph({
      children: [new TextRun({ text, font: "Arial", size: 20, color: COLORS.DARK_GRAY })]
    })]
  });
}

// ============================================================
// TEXT HELPERS
// ============================================================
function heading1(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun(text)] });
}
function heading2(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(text)] });
}
function heading3(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun(text)] });
}
function para(text) {
  return new Paragraph({
    spacing: { after: 200 },
    children: [new TextRun({ font: "Arial", size: 22, color: COLORS.DARK_GRAY, text })]
  });
}
function boldPara(boldText, normalText) {
  return new Paragraph({
    spacing: { after: 200 },
    children: [
      new TextRun({ font: "Arial", size: 22, bold: true, color: COLORS.DARK_GRAY, text: boldText }),
      new TextRun({ font: "Arial", size: 22, color: COLORS.DARK_GRAY, text: normalText })
    ]
  });
}

// ============================================================
// PAGE CONFIGURATION
// ============================================================
const pageSize = { width: 12240, height: 15840 }; // US Letter
const pageMargin = { top: 1440, right: 1440, bottom: 1440, left: 1440 }; // 1 inch

// ============================================================
// DOCUMENT STRUCTURE
// ============================================================

// ** REPORT METADATA — Replace these for each report **
const REPORT_TITLE = "Your Report Title Here";
const REPORT_SUBTITLE = "Subtitle or Tagline";
const REPORT_DATE = "April 2026";
const REPORT_SOURCES_LINE_1 = "Sources include: Organization A, Organization B, Organization C";
const REPORT_SOURCES_LINE_2 = "Organization D, Organization E, and others";

const doc = new Document({
  // -- STYLES --
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } },
    paragraphStyles: [
      {
        id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 36, bold: true, font: "Arial", color: COLORS.DARK_BLUE },
        paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 }
      },
      {
        id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Arial", color: COLORS.MEDIUM_BLUE },
        paragraph: { spacing: { before: 280, after: 160 }, outlineLevel: 1 }
      },
      {
        id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 24, bold: true, font: "Arial", color: COLORS.DARK_GRAY },
        paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 2 }
      },
    ]
  },

  // -- NUMBERING (for bullet and numbered lists) --
  numbering: {
    config: [
      {
        reference: "bullets",
        levels: [{
          level: 0, format: LevelFormat.BULLET, text: "\u2022",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } }
        }]
      },
      {
        reference: "numbers",
        levels: [{
          level: 0, format: LevelFormat.DECIMAL, text: "%1.",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } }
        }]
      },
    ]
  },

  sections: [
    // =============================================
    // SECTION 1: TITLE PAGE
    // =============================================
    {
      properties: { page: { size: pageSize, margin: pageMargin } },
      children: [
        new Paragraph({ spacing: { before: 3600 } }),
        new Paragraph({
          alignment: AlignmentType.CENTER, spacing: { after: 200 },
          children: [new TextRun({
            text: "RESEARCH REPORT", font: "Arial", size: 24,
            color: COLORS.MEDIUM_BLUE, bold: true, allCaps: true
          })]
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER, spacing: { after: 100 },
          border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: COLORS.MEDIUM_BLUE, space: 12 } },
          children: [new TextRun({
            text: REPORT_TITLE, font: "Arial", size: 48, bold: true, color: COLORS.DARK_BLUE
          })]
        }),
        new Paragraph({ spacing: { before: 400 } }),
        new Paragraph({
          alignment: AlignmentType.CENTER, spacing: { after: 100 },
          children: [new TextRun({
            text: REPORT_SUBTITLE, font: "Arial", size: 26,
            color: COLORS.MEDIUM_GRAY, italics: true
          })]
        }),
        new Paragraph({ spacing: { before: 1200 } }),
        new Paragraph({
          alignment: AlignmentType.CENTER, spacing: { after: 100 },
          children: [new TextRun({ text: REPORT_DATE, font: "Arial", size: 24, color: COLORS.MEDIUM_GRAY })]
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER, spacing: { before: 600, after: 100 },
          children: [new TextRun({ text: REPORT_SOURCES_LINE_1, font: "Arial", size: 20, color: COLORS.MEDIUM_GRAY })]
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: REPORT_SOURCES_LINE_2, font: "Arial", size: 20, color: COLORS.MEDIUM_GRAY })]
        }),
      ]
    },

    // =============================================
    // SECTION 2: TABLE OF CONTENTS
    // =============================================
    {
      properties: { page: { size: pageSize, margin: pageMargin } },
      headers: {
        default: new Header({
          children: [new Paragraph({
            border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: COLORS.MEDIUM_BLUE, space: 4 } },
            children: [new TextRun({
              text: REPORT_TITLE, font: "Arial", size: 18, color: COLORS.MEDIUM_BLUE, italics: true
            })]
          })]
        })
      },
      footers: {
        default: new Footer({
          children: [new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [
              new TextRun({ text: "Page ", font: "Arial", size: 18, color: COLORS.MEDIUM_GRAY }),
              new TextRun({ children: [PageNumber.CURRENT], font: "Arial", size: 18, color: COLORS.MEDIUM_GRAY })
            ]
          })]
        })
      },
      children: [
        heading1("Table of Contents"),
        new TableOfContents("Table of Contents", { hyperlink: true, headingStyleRange: "1-3" }),
        new Paragraph({ children: [new PageBreak()] }),
      ]
    },

    // =============================================
    // SECTION 3: MAIN CONTENT
    // =============================================
    {
      properties: { page: { size: pageSize, margin: pageMargin } },
      headers: {
        default: new Header({
          children: [new Paragraph({
            border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: COLORS.MEDIUM_BLUE, space: 4 } },
            children: [new TextRun({
              text: REPORT_TITLE, font: "Arial", size: 18, color: COLORS.MEDIUM_BLUE, italics: true
            })]
          })]
        })
      },
      footers: {
        default: new Footer({
          children: [new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [
              new TextRun({ text: "Page ", font: "Arial", size: 18, color: COLORS.MEDIUM_GRAY }),
              new TextRun({ children: [PageNumber.CURRENT], font: "Arial", size: 18, color: COLORS.MEDIUM_GRAY })
            ]
          })]
        })
      },
      children: [
        // ---- EXECUTIVE SUMMARY ----
        heading1("1. Executive Summary"),
        para("Replace this with a 200-400 word summary of the report's key findings. Write this section LAST, after all other content is complete. Include specific numbers and takeaways, not vague generalities."),

        new Paragraph({ children: [new PageBreak()] }),

        // ---- MAIN SECTIONS ----
        heading1("2. Section Title"),
        heading2("2.1 Subsection"),
        para("Body text with inline citations (Author/Organization, Year). Every factual claim should have a source."),

        // ---- EXAMPLE TABLE ----
        // Adjust columnWidths to sum to CONTENT_WIDTH (9360)
        new Table({
          width: { size: CONTENT_WIDTH, type: WidthType.DXA },
          columnWidths: [3120, 3120, 3120],
          rows: [
            new TableRow({ children: [
              headerCell("Column A", 3120),
              headerCell("Column B", 3120),
              headerCell("Column C", 3120),
            ]}),
            new TableRow({ children: [
              dataCell("Row 1 data", 3120, COLORS.LIGHT_GRAY),
              dataCell("Row 1 data", 3120, COLORS.LIGHT_GRAY),
              dataCell("Row 1 data", 3120, COLORS.LIGHT_GRAY),
            ]}),
            new TableRow({ children: [
              dataCell("Row 2 data", 3120),
              dataCell("Row 2 data", 3120),
              dataCell("Row 2 data", 3120),
            ]}),
          ]
        }),
        new Paragraph({ spacing: { after: 200 } }),

        // ---- EXAMPLE BULLET LIST ----
        new Paragraph({
          numbering: { reference: "bullets", level: 0 },
          spacing: { after: 120 },
          children: [
            new TextRun({ font: "Arial", size: 22, color: COLORS.DARK_GRAY, bold: true, text: "Key point: " }),
            new TextRun({ font: "Arial", size: 22, color: COLORS.DARK_GRAY, text: "Explanation of the key point with supporting data." })
          ]
        }),

        new Paragraph({ children: [new PageBreak()] }),

        // ---- MORE SECTIONS as needed ----
        heading1("3. Next Section"),
        para("Continue adding sections..."),

        new Paragraph({ children: [new PageBreak()] }),

        // ---- BIBLIOGRAPHY (always last) ----
        heading1("Bibliography"),
        // Use hanging indent for bibliography entries
        ...[
          "[1] Author (Year). \"Title.\" Organization/Journal. Description of source.",
          "[2] Author (Year). \"Title.\" Organization/Journal. Description of source.",
        ].map(ref => new Paragraph({
          spacing: { after: 160 },
          indent: { left: 360, hanging: 360 },
          children: [new TextRun({ font: "Arial", size: 20, color: COLORS.DARK_GRAY, text: ref })]
        })),

        // ---- END-OF-REPORT MARKER ----
        new Paragraph({ spacing: { before: 600 } }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          border: { top: { style: BorderStyle.SINGLE, size: 4, color: COLORS.MEDIUM_BLUE, space: 8 } },
          spacing: { before: 200 },
          children: [new TextRun({
            text: "End of Report", font: "Arial", size: 20, color: COLORS.MEDIUM_GRAY, italics: true
          })]
        }),
      ]
    }
  ]
});

// ============================================================
// GENERATE THE FILE
// ============================================================
const OUTPUT_PATH = "/sessions/ecstatic-funny-hopper/mnt/outputs/report.docx";

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(OUTPUT_PATH, buffer);
  console.log("Document created successfully at:", OUTPUT_PATH);
});
