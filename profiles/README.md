# Public Profiles

This directory defines the public install profiles for the repository.

Rules:

- Each `*.txt` file is a public profile.
- One slug per line.
- Blank lines are ignored.
- Lines starting with `#` are comments.
- Every slug in a profile must exist in `skills_manifest.csv`.

Current aliases resolved by the installer:

- `public-default` = `core-meta + development-core`
- `all-public` = union of every profile in this directory

The public catalog and the maintainer's local workspace are intentionally different.
Some local-only skills are still under evaluation and are not yet promoted into the
public catalog or public profiles.
