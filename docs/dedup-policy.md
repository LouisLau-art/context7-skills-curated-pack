# De-dup Policy

This repo keeps manifests and installer scripts only. It does not vendor third-party
`SKILL.md` contents, so de-dup decisions optimize for a stable, high-signal install set.

## Stage 0: Source Priority

When two skills materially overlap, prefer sources in this order:

1. Official product or platform repositories
2. Well-known, consistently maintained skill packs
3. Ordinary personal repositories

Personal or obscure sources stay only when they provide clearly unique value that the
stronger source does not cover.

## Stage 1: Overlap Pruning

For each topic cluster, keep at most:

- 1 general-purpose skill
- 1-2 genuinely specialized skills

Delete skills that are mostly wrappers, shallow aliases, or alternate phrasing for the
same workflow.

Name collisions are only a weak signal. Different names can still be duplicates when
they trigger on the same workflow, while same-name skills can coexist if one is
genuinely specialized and does not steal the same activation surface.

## Stage 2: Content Review

Run a manual review when overlap is not obvious from source metadata alone.

Prefer the skill with:

1. Lower trigger-conflict risk with the rest of the curated pack
2. Better scope fit for the actual workflow
3. A clearer trigger description
4. More useful bundled material such as `scripts/`, `references/`, or templates
5. More canonical naming and better maintenance signals

## Stage 3: User-Fit Overrides

This pack is curated for a solo developer workflow that still includes:

- day-to-day web engineering
- documentation and deck creation
- client-facing and product-style communication

De-prioritize clusters that are currently out of scope for this pack, such as:

- skill/plugin/MCP authoring
- mobile-specific workflows when there is no active mobile work
- narrow agent wrappers that duplicate broader built-in workflows

## Notes

- Installs, trust, and verification remain useful signals, but they are tie-breakers,
  not the primary decision rule.
- A higher-scoring skill can still be removed if a stronger-source skill already
  covers the same job with less noise.
