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

# Sentinel-1 fields

The [upstream specification](https://github.com/stac-extensions/sentinel-1) and [v0.2.0 JSON Schema](https://stac-extensions.github.io/sentinel-1/v0.2.0/schema.json) define Item properties and Collection summaries. Values below are stored in Item `properties`.

| STAC field | Python property | Python value |
| --- | --- | --- |
| `s1:datatake_id` | `datatake_id` | `str`, e.g. `"420895"` |
| `s1:instrument_configuration_ID` | `instrument_configuration_id` | `str`, e.g. `"7"` |
| `s1:orbit_source` | `orbit_source` | `str`, e.g. `"PREORB"` |
| `s1:slice_number` | `slice_number` | `str`, e.g. `"17"` |
| `s1:total_slices` | `total_slices` | `str`, e.g. `"17"` |

At least one of these five fields must exist for schema validation, including in Collection summaries. The schema does not constrain their string contents or relate slice counts to each other.

## Deprecated fields

These fields remain readable and writable for compatibility. The wrapper does not automatically migrate them or emit deprecation warnings.

| STAC field / Python property | Python value | Upstream replacement |
| --- | --- | --- |
| `s1:resolution` / `resolution` | `str` | `gsd`, raster `spatial_resolution`, or SAR `sar:resolution_range` and `sar:resolution_azimuth` |
| `s1:product_identifier` / `product_identifier` | `str` | Item `id` or source links such as `via` and `derived_from` |
| `s1:product_timeliness` / `product_timeliness` | `str` | `product:timeliness_category` and `product:timeliness` |
| `s1:processing_datetime` / `processing_datetime` | `datetime` | `processing:datetime` |
| `s1:processing_level` / `processing_level` | `str` | `processing:level` |
| `s1:shape` / `shape` | `list[int]` | `proj:shape` |

The specification describes resolution classes `full`, `high`, and `medium`; its JSON Schema only requires a string. Shape has at least two integer elements; the schema imposes no positivity constraint or exact dimension count.

## Access and validation

All getters can return `None` for absent fields. Setters accept `None` to remove fields. `apply()` clears omitted values.

Processing datetimes are serialized with PySTAC's datetime utilities and parsed back on access. Use timezone-aware datetimes. The shape setter rejects short arrays, non-integers, and booleans with `ValueError`. Other setters rely on annotations and do not provide complete schema validation. Reading a field does not rerun setter checks.

## Collection summaries

`Sentinel1Extension.summaries(collection)` exposes all eleven properties. String fields use `list[str]`; `shape` uses `list[list[int]]`; `processing_datetime` uses `RangeSummary[datetime]` with serialized string bounds. Getters return `None` when the corresponding summary form is absent. Assigning `None` removes the summary.

Setters replace whole summaries without aggregating Items. Summary shape values are not checked by the Item shape validator. Upstream's extension schema checks the presence of a current summary field but does not validate the values of Collection summaries.
