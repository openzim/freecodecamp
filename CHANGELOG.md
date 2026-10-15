# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- Fix illustration kind in offliner definition (should be `illustration`, not `image`)
- Properly display RTL languages (e.g. Arabic) with a right-to-left layout, while keeping code snippets left-to-right (#170)
- Validate motivation.json content at scrape time so a missing or malformed file fails the build instead of producing a ZIM silently missing this data (#169)

## [2.1.0] - 2026-10-13

### Added

- Add a visual red flash when "Check Your Code" tests fail (#126)
- Add dark theme support using prefers-color-scheme (#131)
- Add support for Arabic and Korean courses (#154)
- Add rendering integration test covering challenge execution offline, against a real "debugging" challenge (#151)
- Validate locale files against known UI translation keys and placeholders at scrape time, failing the build on mismatch (#142)

### Changed

- Upgrade to Node.JS 26, Debian trixie base image, and upgrade Python and JS dependencies, including Vite 8, Vuetify 4, Pinia 4, Vue Router 5, TypeScript 6 (#152, #160)
- Migrate zimui from yarn 1 (classic) to modern yarn, provisioned through corepack (#159)
- Upgrade vendored MathJax from 3.2.2 to 4.1.3 (#158)
- Migrate challenge execution to `@freecodecamp/curriculum-helpers`'s worker-based test-runner, better isolating challenge code from UI code (#60, #157)

### Fixed

- Fix interpolation for placeholders in translation strings (#139)
- Fix prettier and eslint check in zimui QA CI.(#146)
- Bundled ZIM UI inside pip package (#144)
- Fix fetch of non-English client UI translations, moved upstream to i18n-curriculum (#154)

## [2.0.3] - 2025-11-25

### Added

- Add support for simplified and traditional Chinese (#135)

## [2.0.2] - 2025-11-14

### Changed

- Upgrade to Python 3.14 (and dependencies) and Node.JS 24 (and dependencies) (#134)

### Fixed

- Adapt to changes of data structure on freeCodeCamp repo (#130)

## [2.0.1] - 2025-07-18

### Fixed

- Remove useless call to Fetch API causing issue on kiwix-desktop (#122)
- Extract inline JS to plain files in UI (#123)

## [2.0.0] - 2025-03-11

### Added

- Make the UI responsive (#22)
- Enhance the UI design to be closer to original FCC UI (#23)
- Add support for custom ZIM illustration (#79)

### Changed

- Upgrade Python and JS dependencies (#120)

## [1.3.0] - 2025-01-24

### Changed

- Upgrade to Python 3.13 and Node.JS 22, adopt new openZIM practices, upgrade all dependencies (including zimscraperlib 5.x), add support for 'legacy' browsers (#43 + #77)
- Add clearer visual indication of external links (#70)
- Cleanup JS code with a Pinia store and add header toolbar (#73)

### Fixed

- Fix ukrainian typo (#65)
- Remove undecided Chinese codes
- Remove obsolete/missing arabic code
- Add missing support for swahili (#66)
- Do not parse the whole markdown as YAML, but only the frontmatter (#64)
- Properly parse/present mathjax code (#57)
- Fix display of tables in challenge instructions (#75)

## [1.2.0] - 2025-01-16

### Fixed

- Fix support for all FCC supported spoken languages (#20)
- Remove incomplete support of dark mode, no more white on white text: not readable (#33)
- Parse properly markdown property with colon and quotes (#6)
- Move button to go to next challenge so that it is more obvious (#56)
- Fix Javascript - and other - hints which are failing due to missing helpers (#53)
- Add breadcrumbs and fix course title (#61)
- Fix description of curriculum / challenge which might contain HTML code (#58)

### Added

- Add --overwrite CLI argument to not fail when ZIM already exists (#44)
- Implement a cheat mode to ease software manual testing (#54)

### Changed

- Clarify which courses / challenges are supported and display a nice error when it is not supported (#21)

## [1.1.1] - 2023-12-18

### Fixed

- Replace ENTRYPOINT by CMD in Docker image
- Force Python 3.11 (do not yet use 3.12)

## [1.1.0] - 2023-08-31

### Changed

- Remove "\_dir" or "-dir" prefix from input flag and variables/arguments names

## [1.0.0] - 2023-08-29

### Added

- Initial version, supporting only Javascript challenges
