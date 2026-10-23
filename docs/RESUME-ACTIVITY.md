# cdev remote lifecycle repair

Codex 0.163.0's explicit remote TUI sends an empty `thread/resume.config`,
discarding launcher `-c hooks.*` overrides. A real fresh turn reached working
and stopped; reopening its exact UUID completed a real turn with no dashboard
events. A metadata-only wire trace confirmed the missing overrides. The shared
server also retains thread ownership after the terminal disconnects; removing
remote resume would reintroduce writer-lock conflicts.

The launcher now sends the same eight trusted definitions through the official
per-thread resume API before attaching the TUI. Commands, source keys, hashes,
global workmux hooks and approval policies remain unchanged. There is no proxy,
new lifecycle source, trust bypass, or global hook installation.

Remote hook processes resolve their session UUID through an account-private
`/private/tmp/dotfiles-cdev-UID/` registration (directory 0700, files 0600).
Events require the kernel-reported Unix peer PID and birth identity in their
ancestry, a live registered frontend/launcher pair, the exact UUID, launch token,
tmux server birth and pane root PID. Titles, window numbers and cwd do not select
an agent. Ended registrations reject events, retain bounded retired-turn IDs,
and can be replaced after verified launcher exit. Local hook validation is
unchanged. An unavailable bridge leaves Codex usable and unlabelled.

The registry contains runtime identity only. It is disposable across reboot;
existing running clients are not instrumented retroactively. Reopen naturally
through cdev to gain the repaired integration. Rollback uses the prior immutable
release pointer; no tmux reload or editor restart is required.

References: [App Server](https://learn.chatgpt.com/docs/app-server),
[hooks and native trust](https://learn.chatgpt.com/docs/hooks).
