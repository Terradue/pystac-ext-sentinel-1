# Copyright 2026 Terradue
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for pystac.extensions.sentinel1."""

import json
from datetime import datetime
from pathlib import Path

import pytest
from pystac.summaries import RangeSummary
from pystac.utils import str_to_datetime
from pystac.validation.stac_validator import JsonSchemaSTACValidator

import pystac
from pystac import Collection, ExtensionTypeError, Item
from pystac.extensions import sentinel1
from pystac.extensions.sentinel1 import (
    SCHEMA_URI,
    Sentinel1Extension,
    SummariesSentinel1Extension,
)


@pytest.fixture
def validator() -> JsonSchemaSTACValidator:
    schema_path = Path(__file__).parent / "data" / "sentinel-1-v0.2.0.schema.json"
    validator = JsonSchemaSTACValidator()
    validator.schema_cache[SCHEMA_URI] = json.loads(schema_path.read_text())
    return validator


@pytest.fixture
def item() -> Item:
    item = pystac.Item(
        id="sentinel1-item",
        geometry=None,
        bbox=None,
        datetime=datetime(2020, 1, 1),
        properties={},
    )
    Sentinel1Extension.add_to(item)
    return item


@pytest.fixture
def collection() -> Collection:
    return Collection(
        id="sentinel1-collection",
        description="Synthetic Sentinel-1 collection",
        extent=pystac.Extent(
            pystac.SpatialExtent([-180, -90, 180, 90]),
            pystac.TemporalExtent([[str_to_datetime("2020-01-01T00:00:00Z"), None]]),
        ),
        license="proprietary",
    )


def test_stac_extensions(item: Item) -> None:
    assert Sentinel1Extension.has_extension(item)


def test_item_repr(item: Item) -> None:
    assert Sentinel1Extension.ext(item).__repr__() == f"<ItemSentinel1Extension Item id={item.id}>"


def test_no_args_fails(item: Item, validator: JsonSchemaSTACValidator) -> None:
    Sentinel1Extension.ext(item).apply()
    with pytest.raises(pystac.STACValidationError):
        item.validate(validator=validator)


def test_apply_and_validate(item: Item, validator: JsonSchemaSTACValidator) -> None:
    processing_datetime = str_to_datetime("2020-01-02T03:04:05Z")

    Sentinel1Extension.ext(item).apply(
        datatake_id="123456",
        instrument_configuration_id="9",
        orbit_source="RESORB",
        processing_datetime=processing_datetime,
        product_identifier="S1A_IW_GRDH_1SDV_20200101T000000",
        product_timeliness="Fast-24h",
        resolution="high",
        slice_number="2",
        total_slices="9",
        processing_level="LEVEL1",
        shape=[10980, 10980],
    )

    ext = Sentinel1Extension.ext(item)
    assert ext.datatake_id == "123456"
    assert ext.instrument_configuration_id == "9"
    assert ext.orbit_source == "RESORB"
    assert ext.processing_datetime == processing_datetime
    assert ext.product_identifier == "S1A_IW_GRDH_1SDV_20200101T000000"
    assert ext.product_timeliness == "Fast-24h"
    assert ext.resolution == "high"
    assert ext.slice_number == "2"
    assert ext.total_slices == "9"
    assert ext.processing_level == "LEVEL1"
    assert ext.shape == [10980, 10980]

    item.validate(validator=validator)


def test_shape_must_have_two_values(item: Item) -> None:
    with pytest.raises(ValueError, match=r"must contain at least two integers"):
        Sentinel1Extension.ext(item).shape = [10980]


def test_from_dict() -> None:
    document = {
        "type": "Feature",
        "stac_version": "1.0.0",
        "id": "sentinel1-item",
        "properties": {
            "datetime": "2020-01-01T00:00:00Z",
            "s1:datatake_id": "123456",
            "s1:shape": [10980, 10980],
        },
        "geometry": None,
        "links": [],
        "assets": {},
        "stac_extensions": [SCHEMA_URI],
    }
    item = pystac.Item.from_dict(document)

    ext = Sentinel1Extension.ext(item)
    assert ext.datatake_id == "123456"
    assert ext.shape == [10980, 10980]


def test_to_from_dict(item: Item) -> None:
    processing_datetime = str_to_datetime("2020-01-02T03:04:05Z")
    Sentinel1Extension.ext(item).apply(
        datatake_id="123456",
        processing_datetime=processing_datetime,
        shape=[100, 200],
    )

    document = item.to_dict()
    assert document["properties"][sentinel1.DATATAKE_ID_PROP] == "123456"
    assert document["properties"][sentinel1.PROCESSING_DATETIME_PROP] == "2020-01-02T03:04:05Z"
    assert document["properties"][sentinel1.SHAPE_PROP] == [100, 200]

    item = pystac.Item.from_dict(document)
    ext = Sentinel1Extension.ext(item)
    assert ext.datatake_id == "123456"
    assert ext.processing_datetime == processing_datetime
    assert ext.shape == [100, 200]


def test_extension_not_implemented(item: Item) -> None:
    item.stac_extensions.remove(Sentinel1Extension.get_schema_uri())

    with pytest.raises(pystac.ExtensionNotImplemented):
        _ = Sentinel1Extension.ext(item)


def test_item_ext_add_to(item: Item) -> None:
    item.stac_extensions.remove(Sentinel1Extension.get_schema_uri())
    assert Sentinel1Extension.get_schema_uri() not in item.stac_extensions

    _ = Sentinel1Extension.ext(item, add_if_missing=True)

    assert Sentinel1Extension.get_schema_uri() in item.stac_extensions


def test_should_raise_exception_when_passing_invalid_extension_object() -> None:
    with pytest.raises(
        ExtensionTypeError,
        match=r"^Sentinel1Extension does not apply to type 'object'$",
    ):
        Sentinel1Extension.ext(object())  # type: ignore[type-var]  # Exercise rejection of an unsupported runtime type.


def test_summaries(collection: Collection) -> None:
    summaries_ext = Sentinel1Extension.summaries(collection, True)
    processing_datetime = RangeSummary(
        str_to_datetime("2020-01-01T00:00:00Z"),
        str_to_datetime("2020-01-02T00:00:00Z"),
    )

    summaries_ext.datatake_id = ["123456", "654321"]
    summaries_ext.processing_datetime = processing_datetime
    summaries_ext.shape = [[10980, 10980]]

    assert summaries_ext.datatake_id == ["123456", "654321"]
    assert summaries_ext.processing_datetime == processing_datetime
    assert summaries_ext.shape == [[10980, 10980]]

    summaries_dict = collection.to_dict()["summaries"]
    assert summaries_dict["s1:datatake_id"] == ["123456", "654321"]
    assert summaries_dict["s1:processing_datetime"] == {
        "minimum": "2020-01-01T00:00:00Z",
        "maximum": "2020-01-02T00:00:00Z",
    }
    assert summaries_dict["s1:shape"] == [[10980, 10980]]


def test_collection_hint(collection: Collection) -> None:
    with pytest.raises(
        ExtensionTypeError,
        match=r"Hint: Did you mean to use `Sentinel1Extension.summaries` instead\?",
    ):
        Sentinel1Extension.ext(collection)  # type: ignore[type-var]  # Collections must use summaries().


def test_summaries_ext_add_to(collection: Collection) -> None:
    if Sentinel1Extension.get_schema_uri() in collection.stac_extensions:
        collection.stac_extensions.remove(Sentinel1Extension.get_schema_uri())

    summaries_ext = Sentinel1Extension.summaries(collection, add_if_missing=True)

    assert isinstance(summaries_ext, SummariesSentinel1Extension)
    assert Sentinel1Extension.get_schema_uri() in collection.stac_extensions


@pytest.mark.parametrize("shape", [[True, 100], [100, False]])
def test_shape_rejects_booleans(item: Item, shape: list[int]) -> None:
    extension = Sentinel1Extension.ext(item)
    extension.shape = [100, 200]
    with pytest.raises(ValueError, match="must contain only integers"):
        extension.shape = shape
    assert extension.shape == [100, 200]


def test_apply_removes_omitted_fields(item: Item) -> None:
    extension = Sentinel1Extension.ext(item)
    extension.apply(datatake_id="123456", orbit_source="RESORB", shape=[100, 200])
    extension.apply(datatake_id="654321")
    assert extension.datatake_id == "654321"
    assert extension.orbit_source is None
    assert extension.shape is None
    assert "s1:shape" not in item.properties


@pytest.mark.parametrize(
    "property_name",
    ["datatake_id", "instrument_configuration_id", "orbit_source", "slice_number", "total_slices"],
)
def test_each_current_field_satisfies_schema(
    item: Item, validator: JsonSchemaSTACValidator, property_name: str
) -> None:
    setattr(Sentinel1Extension.ext(item), property_name, "7")
    item.validate(validator=validator)


def test_deprecated_fields_alone_do_not_satisfy_schema(
    item: Item, validator: JsonSchemaSTACValidator
) -> None:
    Sentinel1Extension.ext(item).apply(resolution="high", shape=[100, 200])
    with pytest.raises(pystac.STACValidationError):
        item.validate(validator=validator)


def test_summary_removal(collection: Collection) -> None:
    summaries = Sentinel1Extension.summaries(collection, add_if_missing=True)
    summaries.datatake_id = ["123456", "654321"]
    summaries.datatake_id = None
    summaries.processing_datetime = None
    assert summaries.datatake_id is None
    assert summaries.processing_datetime is None
    assert "s1:datatake_id" not in collection.summaries.to_dict()
