<!--
Copyright 2026 Terradue

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

# Sentinel-1 PySTAC extension

`pystac-ext-sentinel-1` reads and writes Sentinel-1 metadata on PySTAC Items and Collection summaries using the `s1:` prefix. Import `Sentinel1Extension` from `pystac.extensions.sentinel1`.

The implementation targets the [upstream Sentinel-1 v0.2.0 specification](https://github.com/stac-extensions/sentinel-1) and declares `https://stac-extensions.github.io/sentinel-1/v0.2.0/schema.json`. The package version is independent of the specification version.

```bash
python -m pip install pystac-ext-sentinel-1
```

- [Create a Sentinel-1 Item](tutorials/first-steps.md) and round-trip its metadata.
- [Update fields and Collection summaries](how-to/use-extension.md).
- [Look up fields and deprecated replacements](reference/fields.md).
- [Browse the Python API](reference/api.md).
- [Understand validation and scope](explanation/architecture.md).

Upstream classifies this extension as a proposal. Its remaining current fields are specific to Sentinel-1; use them when they are useful to your consumers. Most former fields now have replacements in general-purpose extensions.
