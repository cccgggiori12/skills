#!/usr/bin/env bash
set -euo pipefail

usage() {
  printf '%s\n' \
    'Usage: manage-superpowers.sh status' \
    '       manage-superpowers.sh cleanup [--dry-run]'
}

action="${1:-status}"
dry_run=0
if [[ "${2:-}" == "--dry-run" ]]; then
  dry_run=1
elif [[ $# -gt 1 ]]; then
  usage >&2
  exit 2
fi

if [[ "$action" != "status" && "$action" != "cleanup" ]]; then
  usage >&2
  exit 2
fi

codex_bin="${CODEX_BIN:-codex}"
codex_state_dir="${CODEX_STATE_DIR:-${CODEX_HOME:-${HOME}/.codex}}"
active_cache="${codex_state_dir}/plugins/cache/openai-curated-remote/superpowers"
config_file="${codex_state_dir}/config.toml"

case "$active_cache" in
  "${codex_state_dir}"/plugins/cache/openai-curated-remote/superpowers) ;;
  *)
    printf 'Refusing unexpected cache path: %s\n' "$active_cache" >&2
    exit 3
    ;;
esac

show_status() {
  printf 'plugin_status:\n'
  local plugin_line
  plugin_line="$($codex_bin plugin list 2>/dev/null | awk '/^superpowers@/{print; found=1} END{if (!found) print "superpowers entry absent"}')"
  printf '%s\n' "$plugin_line"

  if [[ -e "$active_cache" ]]; then
    printf 'active_cache: present (%s)\n' "$active_cache"
  else
    printf 'active_cache: absent (%s)\n' "$active_cache"
  fi

  if [[ -f "$config_file" ]] && grep -n 'superpowers' "$config_file"; then
    printf 'config_reference: present (%s)\n' "$config_file"
  else
    printf 'config_reference: absent (%s)\n' "$config_file"
  fi
}

if [[ "$action" == "status" ]]; then
  show_status
  exit 0
fi

if [[ $dry_run -eq 1 ]]; then
  printf 'DRY RUN: %q plugin remove %q --json\n' "$codex_bin" 'superpowers@openai-curated'
  printf 'DRY RUN: rm -rf -- %q\n' "$active_cache"
  show_status
  exit 0
fi

printf 'Removing local plugin registration...\n'
if ! "$codex_bin" plugin remove superpowers@openai-curated --json; then
  printf 'Plugin remove returned non-zero; continuing with exact-cache cleanup.\n' >&2
fi

if [[ -e "$active_cache" ]]; then
  rm -rf -- "$active_cache"
  printf 'Removed active cache: %s\n' "$active_cache"
else
  printf 'Active cache already absent: %s\n' "$active_cache"
fi

printf 'Verification:\n'
show_status
