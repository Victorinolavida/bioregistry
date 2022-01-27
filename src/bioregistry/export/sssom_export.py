# -*- coding: utf-8 -*-

"""Export the Bioregistry to SSSOM."""

import csv
import logging
from collections import namedtuple
from itertools import starmap
from typing import List, Tuple

import click
import yaml

import bioregistry
from bioregistry import manager
from bioregistry.constants import SSSOM_METADATA_PATH, SSSOM_PATH

__all__ = [
    "export_sssom",
    "INTERNAL_PREFIX_MAP",
    "get_rows",
]

logger = logging.getLogger(__name__)

Row = namedtuple("Row", "subject_id predicate_id object_id match_type")

INTERNAL_PREFIX_MAP = manager.get_internal_prefix_map()

METADATA = {
    "license": "https://creativecommons.org/publicdomain/zero/1.0/",
    "mapping_provider": "https://github.com/biopragmatics/bioregistry",
    "mapping_set_group": "bioregistry",
    "mapping_set_id": "bioregistry",
    "mapping_set_title": "Bioregistry",
    "curie_map": INTERNAL_PREFIX_MAP,
}


def get_rows() -> List[Tuple[str, str, str, str, str, str]]:
    """Get SSSOM triples."""
    rows = []
    for prefix, resource in sorted(bioregistry.read_registry().items()):
        rows.extend(
            ("bioregistry", prefix, "skos", "exactMatch", metaprefix, metaidentifier)
            for metaprefix, metaidentifier in sorted(resource.get_mappings().items())
            if metaprefix in INTERNAL_PREFIX_MAP
        )
        rows.extend(
            sorted(
                (
                    "bioregistry",
                    prefix,
                    "bioregistry.schema",
                    "0000018",
                    "bioregistry",
                    appears_in,
                )
                for appears_in in sorted(bioregistry.get_appears_in(prefix) or [])
            )
        )
        rows.extend(
            (
                "bioregistry",
                prefix,
                "bioregistry.schema",
                "0000017",
                "bioregistry",
                depends_on,
            )
            for depends_on in sorted(bioregistry.get_depends_on(prefix) or [])
        )
        if resource.part_of and bioregistry.normalize_prefix(resource.part_of):
            rows.append(("bioregistry", prefix, "bfo", "0000050", "bioregistry", resource.part_of))
        if resource.provides:
            rows.append(
                (
                    "bioregistry",
                    prefix,
                    "bioregistry.schema",
                    "0000011",
                    "bioregistry",
                    resource.provides,
                )
            )
        if resource.has_canonical:
            rows.append(
                (
                    "bioregistry",
                    prefix,
                    "bioregistry.schema",
                    "0000016",
                    "bioregistry",
                    resource.has_canonical,
                )
            )

    rows.extend(
        ("bioregistry.collection", identifier, "bfo", "0000050", "bioregistry", prefix)
        for identifier, collection in sorted(bioregistry.read_collections().items())
        for prefix in sorted(collection.resources)
    )

    return rows


@click.command()
def export_sssom():
    """Export the meta-registry as SSSOM."""
    rows = get_rows()
    with SSSOM_PATH.open("w") as file:
        writer = csv.writer(file, delimiter="\t")
        writer.writerow(Row._fields)
        writer.writerows(starmap(_make_row, rows))
    with SSSOM_METADATA_PATH.open("w") as file:
        yaml.safe_dump(METADATA, file)


def _make_row(mp1: str, mi1: str, rp: str, ri: str, mp2: str, mi2: str) -> Row:
    return Row(
        subject_id=f"{mp1}:{mi1}",
        predicate_id=f"{rp}:{ri}",
        object_id=f"{mp2}:{mi2}",
        match_type="sssom:HumanCurated",
    )


if __name__ == "__main__":
    export_sssom()
