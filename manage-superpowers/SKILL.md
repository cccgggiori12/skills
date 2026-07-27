---
name: manage-superpowers
description: Manage the Codex Superpowers plugin when users ask to uninstall, remove, clean up, audit, or stop invoking it after each restart while retaining other plugins. Separates local install state, active cache, marketplace catalog entries, current-session visibility, and workspace-policy rehydration; supports starting Codex normally and making Superpowers cleanup the first request in the new conversation.
---

# Manage Superpowers

Use the bundled scripts for deterministic status, cleanup, and per-launch startup selection.

## Safety boundary

- Treat `codex plugin remove superpowers@openai-curated` as the supported uninstall action.
- Delete only the exact active cache path resolved by `manage-superpowers.sh`.
- Never delete marketplace/catalog entries under `.codex/.tmp/plugins/plugins/superpowers`; `AVAILABLE` or `not installed` is not an active installation.
- Distinguish visible skill metadata from later skill invocation. In this user's environment, deleting the active Superpowers files after startup prevents later turns from loading its `SKILL.md`, although metadata may remain visible.
- If a Superpowers skill body was already read earlier in the conversation, do not promise that deleting files erases instructions already present in conversation context.
- Explain that local cleanup does not change workspace policy; a later restart may rehydrate Superpowers and require cleanup again.
- Request approval before modifying files outside the current writable workspace or deleting the active cache.

## Workflow

### 1. Inspect without changing state

Run:

```bash
bash <skill-dir>/scripts/manage-superpowers.sh status
```

Report these separately:

1. Local plugin status from `codex plugin list`.
2. Active cache presence.
3. Explicit `superpowers` references in `config.toml`.
4. Marketplace-only visibility, if relevant.

### 2. Perform full local cleanup

Use this only when the user explicitly asks to uninstall, remove, or clean Superpowers:

```bash
bash <skill-dir>/scripts/manage-superpowers.sh cleanup
```

The script runs the supported remove command, deletes the exact active cache, and performs a fresh audit. Report what was removed and that the cache is recoverable through reinstall or workspace rehydration.

Preview without changing state when needed:

```bash
bash <skill-dir>/scripts/manage-superpowers.sh cleanup --dry-run
```

### 3. Make cleanup the first action after each restart

Prefer the installed `codex-choice` launcher. It presents:

1. Start Codex normally with all plugins available, then send an initial request that invokes this skill and cleans Superpowers.
2. Start Codex normally without automatic cleanup.

Direct non-interactive forms are:

```bash
codex-choice --clean-after-start
codex-choice --normal
```

Pass Codex options after the mode. Do not pass a second positional prompt with `--clean-after-start`, because the launcher supplies the initial cleanup prompt.

Do not add `--disable plugins` for this workflow: the user explicitly wants other plugins to remain enabled. Do not clean before a normal startup because workspace policy may immediately rehydrate the plugin; clean it as the first in-session action instead.

## Verification

After cleanup, verify all three conditions:

```text
plugin list: superpowers@openai-curated is not installed
active cache: absent
config reference: absent
```

If a subsequent restart recreates the cache, identify it as workspace/plugin-policy rehydration. Use `codex-choice --clean-after-start` again as the user's accepted per-restart workaround.
