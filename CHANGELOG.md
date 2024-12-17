# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- Fix support for all FCC supported spoken languages (#20)
- Remove incomplete support of dark mode, no more white on white text: not readable (#33)

### Added

- Add --overwrite CLI argument to not fail when ZIM already exists (#44)

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
