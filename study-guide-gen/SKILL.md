# Study Guide Generator (UOW Edition)

This skill converts course materials (PDF, PPTX) into structured Markdown study guides using `markitdown`.

## Workflow

1.  **Select Course**: User specifies a course folder (e.g., `CSCI933`).
2.  **Batch Convert**: Scan the folder for non-Markdown lecture notes.
3.  **Generate Index**: Create or update `INDEX.md` in the course folder, listing topics and key definitions extracted from files.
4.  **Create Summary**: Consolidate multiple lecture notes into a single `STUDY_GUIDE.md` for the current week/topic.

## Usage

- `/study-guide-gen <course_folder>`: Scans and indexes the course folder.
- `/study-guide-gen <course_folder> --summarize`: Creates a comprehensive topic-wise summary.
- `/study-guide-gen <course_folder> --flashcards`: Generates Anki-style flashcards for all lecture materials.
- `/study-guide-gen <course_folder> --quiz`: Creates practice quizzes from lecture content.
- `/study-guide-gen <course_folder> --full`: Runs all generation features (summary + flashcards + quiz + concepts).

## Tool Requirements

- `markitdown`: Used for converting PDF/PPTX to text-heavy Markdown.
- `read_file`: Used for analyzing specific exam-relevant sections.
