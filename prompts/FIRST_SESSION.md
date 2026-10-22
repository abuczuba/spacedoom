# Continuing a dotfiles session

Read AGENTS.md and docs/STATUS.md first. The starter's read-only M1 phase has
been completed and the user has authorized ongoing repository development,
validation, documentation and reviewed local commits.

Work only in this dotfiles checkout and owned temporary test directories.
Inspect exact relevant Ghostty/tmux sources and adjacent interactions as needed;
do not broadly scan home, access private data or touch unrelated repositories.

Use the development → copied release → exact live path architecture. Never
link live configuration into the development checkout. Repository authorization
does not authorize staging to the real deployment root, migration, external
symlinks, activation, rollback/restoration, application reload/restart, packages,
macOS changes or pushes. Obtain operation-specific approval at those boundaries.

No production release or live migration exists unless STATUS.md records the
actual evidence. Read docs/WORKFLOW.md before proposing the next deployment
operation; do not treat examples or --approve flags as consent.
