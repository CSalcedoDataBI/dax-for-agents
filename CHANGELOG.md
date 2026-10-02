# Changelog

## [0.8.0](https://github.com/CSalcedoDataBI/dax-for-agents/compare/v0.7.0...v0.8.0) (2026-10-02)


### Features

* **plugin:** directory listing icon ([4579f05](https://github.com/CSalcedoDataBI/dax-for-agents/commit/4579f05fb86d6bb97d0eeeb2a6f30eef396356e0)), closes [#21](https://github.com/CSalcedoDataBI/dax-for-agents/issues/21)

## [0.7.0](https://github.com/CSalcedoDataBI/dax-for-agents/compare/v0.6.0...v0.7.0) (2026-10-02)


### ⚠ BREAKING CHANGES

* skills are now dax-for-agents:dax-reference and so on, not dax:dax-reference. Install with /plugin install dax-for-agents@dax-for-agents; an install under the old name has to be removed and reinstalled.

### Features

* **evals:** a provider layer, and a run that says why it failed ([3f49045](https://github.com/CSalcedoDataBI/dax-for-agents/commit/3f490453cd6a09eb422be256d538eaf30870991a))
* **evals:** a run that survives being killed ([f7b6d0c](https://github.com/CSalcedoDataBI/dax-for-agents/commit/f7b6d0c727fc763ed57bd94df725c02f81852ce9))
* **evals:** grow the invented-function bank from 12 to 72 questions ([5ba87cc](https://github.com/CSalcedoDataBI/dax-for-agents/commit/5ba87cc8da172497bced0d9703b81f595c034047))
* **evals:** the A/B across three models, and the counter that was over-counting ([8ce3dde](https://github.com/CSalcedoDataBI/dax-for-agents/commit/8ce3dde7325b5d087ead40f0c9a3cdf85782f4c7))
* **evals:** the A/B outside Anthropic — two DeepSeek models ([4a26394](https://github.com/CSalcedoDataBI/dax-for-agents/commit/4a263947bb15e487dcb107bc12423fb30d1ca022))
* **lab:** open every lab report on the author's Thank You page ([0d8f389](https://github.com/CSalcedoDataBI/dax-for-agents/commit/0d8f3891700be09c7c149e11d4dac776977c5a6c))
* **lab:** Thank You page sends "Archivos y plantillas" to this repo ([9fc7447](https://github.com/CSalcedoDataBI/dax-for-agents/commit/9fc744716b1a4d0f4546b2b3242046e0c115fd32))
* **lab:** Thank You tagline names DAX and M ([aa7bfb4](https://github.com/CSalcedoDataBI/dax-for-agents/commit/aa7bfb44630597506b30ace7345e0547731c2347))
* rename the plugin from dax to dax-for-agents ([37015a5](https://github.com/CSalcedoDataBI/dax-for-agents/commit/37015a50384f46a5c56a04db7a8d9f20231179ca)), closes [#21](https://github.com/CSalcedoDataBI/dax-for-agents/issues/21)


### Bug Fixes

* **dax-reference:** REMOVEFILTERS and ALLCROSSFILTERED return neither ([e78ba8b](https://github.com/CSalcedoDataBI/dax-for-agents/commit/e78ba8b0faeacb6edc27c79383cdc25387d859e4)), closes [#21](https://github.com/CSalcedoDataBI/dax-for-agents/issues/21)
* **dax-reference:** seven table functions catalogued as scalar ([d948a52](https://github.com/CSalcedoDataBI/dax-for-agents/commit/d948a52e485ec1e3ac92e81aa3e2c54caae9a479)), closes [#21](https://github.com/CSalcedoDataBI/dax-for-agents/issues/21)
* **dax-udf-authoring:** a VAL vs EXPR example that shows the difference ([f95ae4c](https://github.com/CSalcedoDataBI/dax-for-agents/commit/f95ae4c4c76c7ba9f5f3fcdf1ff7426bb56de6c5)), closes [#21](https://github.com/CSalcedoDataBI/dax-for-agents/issues/21)
* **evals:** an empty answer was scoring the best possible result ([3d144cb](https://github.com/CSalcedoDataBI/dax-for-agents/commit/3d144cb94121f86bf9df0bb8ae2e0d60eab756ea))
* **lab:** Thank You subtitle speaks of DAX, not Deneb ([32e3b58](https://github.com/CSalcedoDataBI/dax-for-agents/commit/32e3b58b47cb3397145a737c9d3c307582fb3ecd))

## [0.6.0](https://github.com/CSalcedoDataBI/dax-for-agents/compare/v0.5.0...v0.6.0) (2026-08-29)


### Features

* **evals:** measure the README's thesis, and find where it actually bites ([a124a93](https://github.com/CSalcedoDataBI/dax-for-agents/commit/a124a932097b62a58589ffa8176a212263a18f30))
* **lab:** ask the engine which functions exist, and record where it disagrees ([ba85611](https://github.com/CSalcedoDataBI/dax-for-agents/commit/ba85611f0b2407dc9820512b00fc56b75ea69ed1))
* **scripts:** one command that runs what CI runs, read from the workflow ([2f9cf83](https://github.com/CSalcedoDataBI/dax-for-agents/commit/2f9cf833547c699d4f61257b806e332ab07ecd28))
* **sync:** convert Learn's HTML back into the markdown the sync reads ([c28985a](https://github.com/CSalcedoDataBI/dax-for-agents/commit/c28985a853b62a01f6d9362d1658d5e18ac0ce7d))
* **sync:** read the applies-to contract off Learn, verified on all 479 ([6ab7618](https://github.com/CSalcedoDataBI/dax-for-agents/commit/6ab76185942b70272fc979623d156377abe78708))
* **sync:** the category indexes and the toc, and a full run off Learn ([bf682c4](https://github.com/CSalcedoDataBI/dax-for-agents/commit/bf682c4fd1aa49460a5fb73051e6434112a072b7))
* **sync:** the two unlisted concepts, and what the remaining differences are ([9473d29](https://github.com/CSalcedoDataBI/dax-for-agents/commit/9473d29682bb3759aaed0682cab5049a8e03b6f2))


### Bug Fixes

* **catalog:** three names an engine would reject, and the gate that finds them ([17e0e3e](https://github.com/CSalcedoDataBI/dax-for-agents/commit/17e0e3e8a8654bd28884bc90f8297f3090ddc08f))
* **ci:** a green sync-check now requires an answer that is actually a sha ([d4b4a4e](https://github.com/CSalcedoDataBI/dax-for-agents/commit/d4b4a4e2806718e19d7e47e1df8986355536660b))
* **generated:** point the 87 dead images at Learn, which serves every one ([1ec1b17](https://github.com/CSalcedoDataBI/dax-for-agents/commit/1ec1b1701e6575c7f1a0c80341112acf352046a8))
* **metadata:** make the 45 invisible example files reachable again ([f2e660d](https://github.com/CSalcedoDataBI/dax-for-agents/commit/f2e660d5270a560ee7687b647f9665f3ad003519))
* **upstream:** decide the freeze, and stop the sentinel asking a dead question ([42afceb](https://github.com/CSalcedoDataBI/dax-for-agents/commit/42afceb6f225c933a7115785582dd97cfed27bc4))

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
