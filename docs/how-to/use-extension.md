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

# Work with Sentinel-1 metadata

The examples continue from the Item created in the [tutorial](../tutorials/first-steps.md).

## Update or remove one field

```python
sentinel1 = Sentinel1Extension.ext(item)
sentinel1.orbit_source = "RESORB"
sentinel1.total_slices = None
assert "s1:total_slices" not in item.properties
```

`ext(item)` requires the extension to be declared already. Use `add_if_missing=True` when first attaching it. Assigning `None` removes a field. `apply()` sets every field and removes omitted values; individual setters preserve other fields.

## Manage Collection summaries

```python
collection = pystac.Collection(
    id="example-sentinel-1-collection",
    description="Synthetic Sentinel-1 products",
    extent=pystac.Extent(
        pystac.SpatialExtent([-180, -90, 180, 90]),
        pystac.TemporalExtent([[acquisition_datetime, None]]),
    ),
    license="proprietary",
)
summaries = Sentinel1Extension.summaries(collection, add_if_missing=True)
summaries.datatake_id = ["420895", "420896"]
summaries.orbit_source = ["PREORB", "RESORB"]
assert collection.summaries.to_dict()["s1:datatake_id"] == ["420895", "420896"]
summaries.orbit_source = None
assert "s1:orbit_source" not in collection.summaries.to_dict()
```

Summary setters replace whole lists, and getters return the whole list. Summaries are not computed automatically from Items. The summary wrapper has no `apply()` method.

For compatibility, the deprecated processing timestamp supports a datetime range:

```python
from pystac.summaries import RangeSummary

summaries.processing_datetime = RangeSummary(
    acquisition_datetime, acquisition_datetime
)
assert summaries.processing_datetime.minimum == acquisition_datetime
```

Use `processing:datetime` for new products. Other deprecated fields remain available as described in the [field reference](../reference/fields.md).

## Supported objects

`Sentinel1Extension.ext()` accepts Items. Collections use `summaries()`. Assets and item asset definitions are outside the scope of this extension and have no wrappers.
