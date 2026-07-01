# Minimality Ladder
## Document map

- Ladder
- Safety floor
- Review signals

## Ladder

Stop at the first rung that solves the task:

1. Does this need to exist?
2. Already in this codebase?
3. Standard library or platform feature?
4. Installed dependency already covers it?
5. One-home or one-line change?
6. Only then write new minimal code.

## Safety floor

Never remove validation, auth/permission checks, data-loss protection, error handling for external paths, accessibility, or verification just to reduce code.

## Review signals

New dependency, generic abstraction, broad churn, custom platform replacement, or missing safety check requires explicit evidence or approval.
