# Contributing

Thanks for your interest in contributing.

This is currently a solo-maintained KiCad project, but outside collaboration is welcome when it improves quality, clarity, or manufacturability.

## Code of Conduct

By participating, you agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Before You Start

Please open an issue before making large or structural changes.
Small fixes can go directly to a pull request via a fork.

Examples of useful issues:

* Schematic errors or unclear net naming
* PCB layout concerns (clearance, routing, grounding, placement)
* Manufacturing output problems (BOM, pick-and-place, fabrication notes)
* Documentation gaps

## Contribution Workflow

1. Fork the repository and create a branch from `main`.
2. Keep your change focused and easy to review.
3. Update related documentation if behavior, structure, or outputs change.
4. Open a pull request with a clear description of what changed and why.

## KiCad-Specific Guidelines

To keep diffs reviewable and avoid accidental churn:

* Use a recent stable KiCad version.
* Avoid unrelated symbol/footprint/library cleanup in the same pull request.
* Keep generated outputs in sync only when relevant to the change.
* If modifying libraries under `lib/`, explain compatibility impact in the pull request.

## Pull Request Checklist

Before submitting, please confirm:

* The design files open correctly in KiCad.
* The change is scoped to one problem or feature.
* New files are intentional and necessary.
* Commit messages and PR title are descriptive.

## Review and Merge Expectations

I review contributions as time allows.
Feedback may request revisions before merge.

Not all contributions will be merged, especially if they conflict with project direction, but all constructive contributions are appreciated.