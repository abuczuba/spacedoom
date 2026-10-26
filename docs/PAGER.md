# Retired phone publisher

The ntfy transport and all active integrations are removed. The dashboard still
uses its existing validated lifecycle events for shimmer, stopped dots, approval
alerts, acknowledgment and attention navigation. No phone transport is built into
the dashboard. Collie is an independent installation with its own lifecycle and
phone-delivery acceptance; dotfiles bootstrap does not install or activate it.

Historical test records and immutable releases are retained as evidence and for
rollback. Their old publisher instructions do not describe the current setup.
Do not restore the retired private destination configuration during normal
dashboard recovery. See STATUS.md for the removal release and recovery details.
