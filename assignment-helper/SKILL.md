# Assignment Helper (UOW Specialist)

Helps decompose complex assignment PDF/DOCX task descriptions and marking criteria into actionable plans.

## Workflow

1.  **Parse Task**: Scans for `Assignment_Task.pdf`, `Task.docx`, or `Criteria.pdf`.
2.  **Marking Analysis**: Extracts exactly what is required for full marks (HD level).
3.  **Checklist**: Generates a `CHECKLIST.md` with due dates and requirements.
4.  **Skeleton**: Scaffolds a starting file (e.g., LaTeX for CSIT940 or Python for CSCI933).

## Usage

- `/assignment-helper <course_folder>`: Scans and initializes an assignment task.
- `/assignment-helper <course_folder> --hd-check`: Cross-references your work against the marking rubric.
