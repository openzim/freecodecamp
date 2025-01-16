# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- Fix ukrainian typo (#65)
- Remove undecided Chinese codes
- Add missing support for swahili (#66)

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

- Remove "_dir" or "-dir" prefix from input flag and variables/arguments names

## [1.0.0] - 2023-08-29

### Added

- Initial version, supporting only Javascript challenges
