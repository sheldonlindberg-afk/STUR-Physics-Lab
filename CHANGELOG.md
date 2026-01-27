# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [4.3.0] - 2026-01-27 — Public Release

### Added

- PWA support with offline functionality and auto-update
- Service worker registration with cache management
- Physics color legend on 64 theory pages
- VERSION_HISTORY.md documenting framework evolution
- Consistent MathJax configuration across all pages

### Changed

- Header positioning: now fixed (floats) instead of sticky
- All scroll-padding unified via CSS custom properties
- Removed draft/exploratory status markers from all documents
- Standardized all documentation to v4.3
- Updated neutrino ordering status from "needs verification" to "EXACT"

### Fixed

- Content no longer hidden under header on scroll
- Anchor navigation now accounts for header height
- Safe-area-inset handling for notched devices
- MathJax inline configurations replaced with standard setup

### Removed

- AI assistant authorship references
- Conversational draft markers ("Wait," "Hmm," "Actually,")
- Unresolved placeholder markers ("???")
- "Needs verification" hedging language

## [4.2.0] and earlier — Internal Development

Internal development versions. See [VERSION_HISTORY.md](VERSION_HISTORY.md) for detailed framework evolution.
