# -*- coding: utf-8 -*-

"""Generate a small knowledge graph relating entities."""

import click
from ndex2 import NiceCXBuilder

import bioregistry
import bioregistry.version
import pystow
from bioregistry.export.sssom_export import INTERNAL_PREFIX_MAP, get_rows
from more_click import verbose_option

NDEX_UUID = "aa78a43f-9c4d-11eb-9e72-0ac135e8bacf"


@click.command()
@verbose_option
def main():
    """Upload the Bioregistry KG to NDEx."""
    upload()
    click.echo(f"see https://bioregistry.io/ndex:{NDEX_UUID}")


def upload():
    """Generate a CX graph and upload to NDEx."""
    cx = NiceCXBuilder()
    cx.set_name("Bioregistry")
    cx.add_network_attribute(
        "description",
        "An integrative meta-registry of biological databases, ontologies, and nomenclatures",
    )
    cx.add_network_attribute("hash", bioregistry.version.get_git_hash())
    cx.add_network_attribute("version", bioregistry.version.get_version())
    cx.set_context(INTERNAL_PREFIX_MAP)

    registry_nodes = {metaprefix: make_registry_node(cx, metaprefix) for metaprefix in bioregistry.read_metaregistry()}
    resource_nodes = {prefix: make_resource_node(cx, prefix) for prefix in bioregistry.read_registry()}
    collection_nodes = {identifier: make_collection_node(cx, identifier) for identifier in bioregistry.read_collections()}

    def _get_node(prefix: str, identifier: str) -> int:
        if prefix == "bioregistry":
            return registry_nodes[identifier]
        elif prefix == "bioregistry.collection":
            return collection_nodes[identifier]
        elif prefix == "bioregistry."

    def _get_relation(prefix: str, identifier: str) -> str:
        pass

    for sp, si, pp, pi, op, oi in get_rows():
        cx.add_edge(
            source=_get_node(sp, si),
            target=_get_node(op, oi),
            interaction=_get_relation(pp, pi),
        )

    nice_cx = cx.get_nice_cx()
    nice_cx.update_to(
        uuid=NDEX_UUID,
        server="http://public.ndexbio.org",
        username=pystow.get_config("ndex", "username"),
        password=pystow.get_config("ndex", "password"),
    )


def make_registry_node(cx: NiceCXBuilder, metaprefix: str) -> int:
    """Generate a CX node for a registry."""
    node = cx.add_node(
        name=bioregistry.get_registry_name(metaprefix),
        represents=f"bioregistry.registry:{metaprefix}",
    )
    homepage = bioregistry.get_registry_homepage(metaprefix)
    if homepage:
        cx.add_node_attribute(node, "homepage", homepage)
    description = bioregistry.get_registry_description(metaprefix)
    if description:
        cx.add_node_attribute(node, "description", description)
    return node


def make_resource_node(cx: NiceCXBuilder, prefix: str) -> int:
    """Generate a CX node for a resource."""
    node = cx.add_node(
        name=bioregistry.get_name(prefix),
        represents=f"bioregistry:{prefix}",
    )
    homepage = bioregistry.get_homepage(prefix)
    if homepage:
        cx.add_node_attribute(node, "homepage", homepage)
    description = bioregistry.get_description(prefix)
    if description:
        cx.add_node_attribute(node, "description", description)
    pattern = bioregistry.get_pattern(prefix)
    if pattern:
        cx.add_node_attribute(node, "pattern", pattern)
    # TODO add more
    return node


def make_collection_node(cx: NiceCXBuilder, collection_id: str) -> int:
    """Make a collection node."""
    collection = bioregistry.get_collection(collection_id)
    if collection is None:
        raise ValueError
    node = cx.add_node(
        name=collection.name,
        represents=f"bioregistry.collection:{collection_id}",
    )
    if collection.description:
        cx.add_node_attribute(node, "description", collection.description)
    return node


if __name__ == "__main__":
    main()
