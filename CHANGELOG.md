# Changelog

## [0.5.0](https://github.com/CSalcedoDataBI/dax-for-agents/compare/v0.4.0...v0.5.0) (2026-08-27)


### Features

* **gates:** count covered functions, so the README can state coverage ([0ffc662](https://github.com/CSalcedoDataBI/dax-for-agents/commit/0ffc6626467e7b63c9db01a1b2b4795572937504)), closes [#5](https://github.com/CSalcedoDataBI/dax-for-agents/issues/5)
* **readme:** a banner and a coverage map, generated from the tree ([de1ba07](https://github.com/CSalcedoDataBI/dax-for-agents/commit/de1ba077ed7ded19d4c2e7c365e523a8c70e12ab))


### Bug Fixes

* **ci:** let the gates see main, and ask them about the release branch ([7a67b89](https://github.com/CSalcedoDataBI/dax-for-agents/commit/7a67b89cd9203400e24ca396e8e2188182da36ec))
* **ci:** name the repository for gh, which has no checkout to read it from ([1e71bee](https://github.com/CSalcedoDataBI/dax-for-agents/commit/1e71beeba65f7b696a3d9cd41c2ae994bb2617c9))
* **ci:** publish the release-branch verdict where the PR can see it ([6a075c5](https://github.com/CSalcedoDataBI/dax-for-agents/commit/6a075c5c4279acb73dfba4451d87fc268097856c))
* **guard:** let history be accounted for, so the guard survives being right ([531e89b](https://github.com/CSalcedoDataBI/dax-for-agents/commit/531e89b29b8469f3f927c402ed28c998c8039a5a))

## [0.4.0](https://github.com/CSalcedoDataBI/dax-for-agents/compare/v0.3.0...v0.4.0) (2026-08-25)


### Features

* add dax-lib-install, a fifth skill that installs a third-party UDF ([633f666](https://github.com/CSalcedoDataBI/dax-for-agents/commit/633f666410ab01379cc0b29925c57710718ff813))

## Changelog

Releases of this repository start at **0.4.0**.

The version number does not: it continues the plugin's line, because `dax` was already
published at 0.3.0 and a version that goes backwards breaks every install that has it.
What starts here is the *history*. This repository's first commit is the 0.3.0 tree as it
arrived, tagged `v0.3.0` so the comparison links below have something to compare against —
the entries for 0.3.0 and earlier were written against a different tree and are not part of
this repository, so keeping them here would only publish links to commits and issues that
do not exist.

This file is maintained by [release-please](https://github.com/googleapis/release-please).
Do not edit it by hand — write Conventional Commits instead.
