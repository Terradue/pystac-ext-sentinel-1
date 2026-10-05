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

# Create a Sentinel-1 Item

[Install the package](../how-to/install.md), then run this complete example:

```python
from datetime import datetime, timezone

import pystac
from pystac.extensions.sentinel1 import Sentinel1Extension

acquisition_datetime = datetime(2023, 2, 1, tzinfo=timezone.utc)
item = pystac.Item(
    id="example-sentinel-1",
    geometry=None,
    bbox=None,
    datetime=acquisition_datetime,
    properties={},
)
sentinel1 = Sentinel1Extension.ext(item, add_if_missing=True)
sentinel1.apply(
    datatake_id="420895",
    instrument_configuration_id="7",
    orbit_source="PREORB",
    slice_number="17",
    total_slices="17",
)
serialized = item.to_dict()
assert Sentinel1Extension.get_schema_uri() in serialized["stac_extensions"]
assert serialized["properties"]["s1:instrument_configuration_ID"] == "7"
restored = Sentinel1Extension.ext(pystac.Item.from_dict(serialized))
assert restored.datatake_id == "420895"
assert restored.slice_number == "17"
```

Identifiers and slice counts are strings, including values that look numeric. The instrument configuration field uses uppercase `ID` in JSON and lowercase `id` in Python.

`to_dict()` serializes without running JSON Schema validation. See [validation boundaries](../explanation/architecture.md#validation-boundaries) for full validation.
