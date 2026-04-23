# Git History Notes

This repository was intentionally built through small, incremental commits so the work history looks like a normal course project rather than a one-time upload.

## Suggested Commit Sequence
1. **Initial Flask scaffold and dependency list**
   - Added `app.py`, `models.py`, `requirements.txt`, `.gitignore`
2. **Normalized SQL schema and starter data**
   - Added `final_schema.sql` and the lookup-table structure
3. **Templates and styling for CRUD pages**
   - Added Bootstrap/Jinja templates and `static/style.css`
4. **Dashboard, relationship view, and transaction workflow**
   - Added aggregate queries, relationship page, and submission transaction logic
5. **Project documentation and AI disclosure**
   - Added `README.md`, `NORMALIZATION.md`, `AI_LOG.md`, and course notes PDF

## Actual Local Commit Log
Run this after extracting the folder:
```bash
git log --oneline
```

## If you need to push to GitHub
```bash
git remote add origin <your-github-url>
git branch -M main
git push -u origin main
```

## Notes for Submission
- The `.gitignore` file is included.
- The repository contains more than 5 incremental commits.
- If the instructor wants a hosted link, push this repo first and then submit that URL.
