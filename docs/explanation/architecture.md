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

# Scope, architecture, and validation

## Package structure

The distribution is named `pystac-ext-sentinel-1`, while the import path is `pystac.extensions.sentinel1`. The wheel excludes the shared `pystac.extensions` initializer owned by PySTAC.

`Sentinel1Extension.ext()` wraps an Item and writes directly into its properties. PySTAC's `to_dict()` handles serialization. The package stores mission metadata; it does not process radar data. Assets and item asset definitions are unsupported, matching the upstream extension scope.

These classes are PySTAC property adapters, not generated schema models. The Taskfile imports quality tasks and has no model-generation task.

## Collection summaries

Collections use `Sentinel1Extension.summaries()`. The helper exposes all Item field names, with lists for string and shape values and a datetime range for processing timestamps. It reads and replaces whole summaries without computing them from Items.

## Validation boundaries

The shape setter enforces at least two integers and rejects booleans. Datetime access uses PySTAC's conversion utilities. Other schema constraints require full validation; annotations do not enforce runtime types. Reading existing metadata does not rerun setter checks.

`apply()` mutates fields sequentially and removes omitted fields. If a later setter fails, earlier assignments remain. Validate inputs first if an application requires an all-or-nothing update.

For full STAC and extension validation, install `python -m pip install "pystac[validation]"` and call `item.validate()`. Remote schemas must be accessible or supplied through a configured validator. Neither `apply()` nor `to_dict()` validates the full schema.

The v0.2.0 schema requires at least one current Sentinel-1 field. An empty extension or deprecated fields alone fail validation. Collection summaries require one current field, but the extension schema does not check their values. See the [field reference](../reference/fields.md).

Repository tests cache an unmodified copy of the upstream extension schema in `tests/data/sentinel-1-v0.2.0.schema.json` so validation does not depend on network access. Refresh it from the upstream `json-schema/schema.json` when changing the supported specification version.

## Migration hooks

`SENTINEL1_EXTENSION_HOOKS` declares the schema identifier, legacy identifier `sentinel-1`, and Item/Collection object types. The module exposes the hook without automatically registering it with PySTAC. It does not move deprecated fields into other extensions.
