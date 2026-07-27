# Personal Codex Skills

This repository tracks the locally authored Codex skills installed under
`~/.codex/skills`.

## Tracked skills

- `analyze-code`
- `manage-superpowers`
- `publish-to-ai-infra-wiki`
- `save-answer-as-markdown`
- `weekly-report-ppt`

System skills and third-party skills such as `find-skills` and
`grill-with-docs` are intentionally excluded. The root `.gitignore` uses an
allowlist so newly installed third-party skills are not accidentally committed.

## Local use

Clone this repository as `~/.codex/skills`, or copy the tracked skill
directories into an existing `~/.codex/skills` installation. Restart Codex
after installing or updating skills so the next session loads the current
definitions.
