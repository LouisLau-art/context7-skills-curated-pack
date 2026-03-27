---
name: uow-assignment
description: |
  UOW Assignment Helper - Use when starting UOW course assignments to generate standardized answer templates with student ID and auto-extracted questions from PDFs
---

# UOW Assignment Helper

Generates standardized answer templates for University of Wollongong assignments, extracting questions from PDFs and setting up proper document structure.

## When to use

- User asks for help with a UOW assignment
- Starting work on a new assignment from PDF
- Need to extract questions and create answer template

## Quick start

```bash
# Extract questions from assignment PDF and create template
/uow-assignment <assignment.pdf>
```

## Features

- Auto-extracts questions from assignment PDFs
- Generates answer templates with student ID header
- Supports LaTeX (for CSIT940, etc.) and Markdown formats
- Creates proper directory structure

## Output format

Creates a directory with:
- `answers.md` or `answers.tex` - answer template with extracted questions
- `CHECKLIST.md` - assignment requirements checklist
- `submission/` - directory for final submission files
