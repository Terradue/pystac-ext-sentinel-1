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

"""Read and write Sentinel-1 v0.2.0 Item properties and Collection summaries."""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, Literal, TypeVar, cast

from pystac.extensions.base import (
    ExtensionManagementMixin,
    PropertiesExtension,
    SummariesExtension,
)
from pystac.extensions.hooks import ExtensionHooks
from pystac.summaries import RangeSummary
from pystac.utils import datetime_to_str, map_opt, str_to_datetime

import pystac

if TYPE_CHECKING:
    from datetime import datetime

T = TypeVar("T", bound=pystac.Item)

SCHEMA_URI = "https://stac-extensions.github.io/sentinel-1/v0.2.0/schema.json"

PREFIX = "s1:"
DATATAKE_ID_PROP = PREFIX + "datatake_id"
INSTRUMENT_CONFIGURATION_ID_PROP = PREFIX + "instrument_configuration_ID"
ORBIT_SOURCE_PROP = PREFIX + "orbit_source"
PROCESSING_DATETIME_PROP = PREFIX + "processing_datetime"
PRODUCT_IDENTIFIER_PROP = PREFIX + "product_identifier"
PRODUCT_TIMELINESS_PROP = PREFIX + "product_timeliness"
RESOLUTION_PROP = PREFIX + "resolution"
SLICE_NUMBER_PROP = PREFIX + "slice_number"
TOTAL_SLICES_PROP = PREFIX + "total_slices"
PROCESSING_LEVEL_PROP = PREFIX + "processing_level"
SHAPE_PROP = PREFIX + "shape"
_MIN_SHAPE_DIMENSIONS = 2


def _validate_shape(value: list[int] | None) -> list[int] | None:
    """Check the deprecated shape field, rejecting short arrays and non-integers.

    Raises:
        ValueError: If fewer than two dimensions or non-integer values are supplied.
    """
    if value is None:
        return None
    if len(value) < _MIN_SHAPE_DIMENSIONS:
        raise ValueError(f"{SHAPE_PROP} must contain at least two integers.")
    if not all(
        isinstance(dimension, int) and not isinstance(dimension, bool) for dimension in value
    ):
        raise ValueError(f"{SHAPE_PROP} must contain only integers.")
    return value


class Sentinel1Extension(
    Generic[T],
    PropertiesExtension,
    ExtensionManagementMixin[pystac.Item | pystac.Collection],
):
    """Extension API for the Sentinel-1 extension."""

    name: Literal["s1"] = "s1"

    # Preserve the public positional signature used by existing callers.
    def apply(  # noqa: PLR0913, PLR0917
        self,
        datatake_id: str | None = None,
        instrument_configuration_id: str | None = None,
        orbit_source: str | None = None,
        processing_datetime: datetime | None = None,
        product_identifier: str | None = None,
        product_timeliness: str | None = None,
        resolution: str | None = None,
        slice_number: str | None = None,
        total_slices: str | None = None,
        processing_level: str | None = None,
        shape: list[int] | None = None,
    ) -> None:
        """Set all fields in place, removing fields whose arguments are omitted.

        Deprecated fields remain available for compatibility with existing Items.
        Assignments are sequential; a shape error leaves earlier changes in place.

        Raises:
            ValueError: If shape has fewer than two elements, non-integers, or booleans.
        """
        self.datatake_id = datatake_id
        self.instrument_configuration_id = instrument_configuration_id
        self.orbit_source = orbit_source
        self.processing_datetime = processing_datetime
        self.product_identifier = product_identifier
        self.product_timeliness = product_timeliness
        self.resolution = resolution
        self.slice_number = slice_number
        self.total_slices = total_slices
        self.processing_level = processing_level
        self.shape = shape

    @property
    def datatake_id(self) -> str | None:
        """The datatake identifier as a string."""
        return self._get_property(DATATAKE_ID_PROP, str)

    @datatake_id.setter
    def datatake_id(self, value: str | None) -> None:
        self._set_property(DATATAKE_ID_PROP, value)

    @property
    def instrument_configuration_id(self) -> str | None:
        """The instrument configuration ID, stored as s1:instrument_configuration_ID."""
        return self._get_property(INSTRUMENT_CONFIGURATION_ID_PROP, str)

    @instrument_configuration_id.setter
    def instrument_configuration_id(self, value: str | None) -> None:
        self._set_property(INSTRUMENT_CONFIGURATION_ID_PROP, value)

    @property
    def orbit_source(self) -> str | None:
        """The orbit source, such as PREORB or RESORB."""
        return self._get_property(ORBIT_SOURCE_PROP, str)

    @orbit_source.setter
    def orbit_source(self, value: str | None) -> None:
        self._set_property(ORBIT_SOURCE_PROP, value)

    @property
    def processing_datetime(self) -> datetime | None:
        """The deprecated processing timestamp; prefer processing:datetime."""
        return map_opt(str_to_datetime, self._get_property(PROCESSING_DATETIME_PROP, str))

    @processing_datetime.setter
    def processing_datetime(self, value: datetime | None) -> None:
        self._set_property(PROCESSING_DATETIME_PROP, map_opt(datetime_to_str, value))

    @property
    def product_identifier(self) -> str | None:
        """The deprecated product identifier; prefer the Item ID or source links."""
        return self._get_property(PRODUCT_IDENTIFIER_PROP, str)

    @product_identifier.setter
    def product_identifier(self, value: str | None) -> None:
        self._set_property(PRODUCT_IDENTIFIER_PROP, value)

    @property
    def product_timeliness(self) -> str | None:
        """The deprecated timeliness; prefer product extension timeliness fields."""
        return self._get_property(PRODUCT_TIMELINESS_PROP, str)

    @product_timeliness.setter
    def product_timeliness(self, value: str | None) -> None:
        self._set_property(PRODUCT_TIMELINESS_PROP, value)

    @property
    def resolution(self) -> str | None:
        """The deprecated resolution class; prefer spatial or SAR resolution fields."""
        return self._get_property(RESOLUTION_PROP, str)

    @resolution.setter
    def resolution(self, value: str | None) -> None:
        self._set_property(RESOLUTION_PROP, value)

    @property
    def slice_number(self) -> str | None:
        """The slice number as a string."""
        return self._get_property(SLICE_NUMBER_PROP, str)

    @slice_number.setter
    def slice_number(self, value: str | None) -> None:
        self._set_property(SLICE_NUMBER_PROP, value)

    @property
    def total_slices(self) -> str | None:
        """The total number of slices as a string."""
        return self._get_property(TOTAL_SLICES_PROP, str)

    @total_slices.setter
    def total_slices(self, value: str | None) -> None:
        self._set_property(TOTAL_SLICES_PROP, value)

    @property
    def processing_level(self) -> str | None:
        """The deprecated processing level; prefer processing:level."""
        return self._get_property(PROCESSING_LEVEL_PROP, str)

    @processing_level.setter
    def processing_level(self, value: str | None) -> None:
        self._set_property(PROCESSING_LEVEL_PROP, value)

    @property
    def shape(self) -> list[int] | None:
        """The deprecated array dimensions; prefer proj:shape."""
        return self._get_property(SHAPE_PROP, list)

    @shape.setter
    def shape(self, value: list[int] | None) -> None:
        """Set or remove the deprecated shape field.

        Raises:
            ValueError: If shape has fewer than two elements, non-integers, or booleans.
        """
        self._set_property(SHAPE_PROP, _validate_shape(value))

    @classmethod
    def get_schema_uri(cls) -> str:
        """Return the upstream Sentinel-1 v0.2.0 schema identifier."""
        return SCHEMA_URI

    @classmethod
    def ext(cls, obj: T, add_if_missing: bool = False) -> Sentinel1Extension[T]:
        """Wrap an Item, optionally declaring the extension on it.

        Raises:
            pystac.ExtensionNotImplemented: If the extension is absent and not added.
            pystac.ExtensionTypeError: If the object is not an Item.
        """
        if isinstance(obj, pystac.Item):
            cls.ensure_has_extension(obj, add_if_missing)
            return cast("Sentinel1Extension[T]", ItemSentinel1Extension(obj))
        raise pystac.ExtensionTypeError(cls._ext_error_message(obj))

    @classmethod
    def summaries(
        cls, obj: pystac.Collection, add_if_missing: bool = False
    ) -> SummariesSentinel1Extension:
        """Wrap Collection summaries, optionally declaring the extension.

        Raises:
            pystac.ExtensionNotImplemented: If the extension is absent and not added.
        """
        cls.ensure_has_extension(obj, add_if_missing)
        return SummariesSentinel1Extension(obj)


class ItemSentinel1Extension(Sentinel1Extension[pystac.Item]):
    """Store Sentinel-1 metadata directly in a PySTAC Item's properties.

    Attributes:
        item: The Item whose properties are read and mutated by this wrapper.
    """

    item: pystac.Item

    def __init__(self, item: pystac.Item) -> None:
        self.item = item
        self.properties = item.properties

    def __repr__(self) -> str:
        return f"<ItemSentinel1Extension Item id={self.item.id}>"


class SummariesSentinel1Extension(SummariesExtension):
    """Read and replace Sentinel-1 summaries without aggregating Items."""

    @property
    def datatake_id(self) -> list[str] | None:
        """The list of datatake id values, or None when absent."""
        return self.summaries.get_list(DATATAKE_ID_PROP)

    @datatake_id.setter
    def datatake_id(self, value: list[str] | None) -> None:
        self._set_summary(DATATAKE_ID_PROP, value)

    @property
    def instrument_configuration_id(self) -> list[str] | None:
        """The list of instrument configuration id values, or None when absent."""
        return self.summaries.get_list(INSTRUMENT_CONFIGURATION_ID_PROP)

    @instrument_configuration_id.setter
    def instrument_configuration_id(self, value: list[str] | None) -> None:
        self._set_summary(INSTRUMENT_CONFIGURATION_ID_PROP, value)

    @property
    def orbit_source(self) -> list[str] | None:
        """The list of orbit source values, or None when absent."""
        return self.summaries.get_list(ORBIT_SOURCE_PROP)

    @orbit_source.setter
    def orbit_source(self, value: list[str] | None) -> None:
        self._set_summary(ORBIT_SOURCE_PROP, value)

    @property
    def processing_datetime(self) -> RangeSummary[datetime] | None:
        """The processing datetime range, or None when absent."""
        return map_opt(
            lambda summary: RangeSummary(
                str_to_datetime(summary.minimum), str_to_datetime(summary.maximum)
            ),
            self.summaries.get_range(PROCESSING_DATETIME_PROP),
        )

    @processing_datetime.setter
    def processing_datetime(self, value: RangeSummary[datetime] | None) -> None:
        self._set_summary(
            PROCESSING_DATETIME_PROP,
            map_opt(
                lambda summary: RangeSummary(
                    datetime_to_str(summary.minimum), datetime_to_str(summary.maximum)
                ),
                value,
            ),
        )

    @property
    def product_identifier(self) -> list[str] | None:
        """The list of product identifier values, or None when absent."""
        return self.summaries.get_list(PRODUCT_IDENTIFIER_PROP)

    @product_identifier.setter
    def product_identifier(self, value: list[str] | None) -> None:
        self._set_summary(PRODUCT_IDENTIFIER_PROP, value)

    @property
    def product_timeliness(self) -> list[str] | None:
        """The list of product timeliness values, or None when absent."""
        return self.summaries.get_list(PRODUCT_TIMELINESS_PROP)

    @product_timeliness.setter
    def product_timeliness(self, value: list[str] | None) -> None:
        self._set_summary(PRODUCT_TIMELINESS_PROP, value)

    @property
    def resolution(self) -> list[str] | None:
        """The list of resolution values, or None when absent."""
        return self.summaries.get_list(RESOLUTION_PROP)

    @resolution.setter
    def resolution(self, value: list[str] | None) -> None:
        self._set_summary(RESOLUTION_PROP, value)

    @property
    def slice_number(self) -> list[str] | None:
        """The list of slice number values, or None when absent."""
        return self.summaries.get_list(SLICE_NUMBER_PROP)

    @slice_number.setter
    def slice_number(self, value: list[str] | None) -> None:
        self._set_summary(SLICE_NUMBER_PROP, value)

    @property
    def total_slices(self) -> list[str] | None:
        """The list of total slices values, or None when absent."""
        return self.summaries.get_list(TOTAL_SLICES_PROP)

    @total_slices.setter
    def total_slices(self, value: list[str] | None) -> None:
        self._set_summary(TOTAL_SLICES_PROP, value)

    @property
    def processing_level(self) -> list[str] | None:
        """The list of processing level values, or None when absent."""
        return self.summaries.get_list(PROCESSING_LEVEL_PROP)

    @processing_level.setter
    def processing_level(self, value: list[str] | None) -> None:
        self._set_summary(PROCESSING_LEVEL_PROP, value)

    @property
    def shape(self) -> list[list[int]] | None:
        """The list of shape values, or None when absent."""
        return self.summaries.get_list(SHAPE_PROP)

    @shape.setter
    def shape(self, value: list[list[int]] | None) -> None:
        self._set_summary(SHAPE_PROP, value)


class Sentinel1ExtensionHooks(ExtensionHooks):
    """Describe Sentinel-1 identifiers and supported objects for PySTAC hooks."""

    schema_uri: str = SCHEMA_URI
    prev_extension_ids: ClassVar[set[str]] = {"sentinel-1"}
    stac_object_types: ClassVar[set[pystac.STACObjectType]] = {
        pystac.STACObjectType.ITEM,
        pystac.STACObjectType.COLLECTION,
    }


SENTINEL1_EXTENSION_HOOKS: ExtensionHooks = Sentinel1ExtensionHooks()
