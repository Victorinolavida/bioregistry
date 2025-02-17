# -*- coding: utf-8 -*-

"""Constants and utilities for registries."""

import os
import pathlib

import pystow

__all__ = [
    "HERE",
    "DATA_DIRECTORY",
    "BIOREGISTRY_PATH",
    "METAREGISTRY_PATH",
    "COLLECTIONS_PATH",
    "MISMATCH_PATH",
    "BIOREGISTRY_MODULE",
]

HERE = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))
DATA_DIRECTORY = HERE / "data"
BIOREGISTRY_PATH = DATA_DIRECTORY / "bioregistry.json"
METAREGISTRY_PATH = DATA_DIRECTORY / "metaregistry.json"
COLLECTIONS_PATH = DATA_DIRECTORY / "collections.json"
MISMATCH_PATH = DATA_DIRECTORY / "mismatch.json"

BIOREGISTRY_MODULE = pystow.module("bioregistry")

ROOT = HERE.parent.parent.resolve()
DOCS = ROOT.joinpath("docs")
DOCS_DATA = DOCS.joinpath("_data")
DOCS_IMG = DOCS.joinpath("img")


EXPORT_DIRECTORY = ROOT.joinpath("exports")

EXPORT_CONTEXTS = EXPORT_DIRECTORY / "contexts"
CONTEXT_BIOREGISTRY_PATH = EXPORT_CONTEXTS / "bioregistry.context.jsonld"
SHACL_TURTLE_PATH = EXPORT_CONTEXTS / "bioregistry.context.ttl"
CONTEXT_OBO_PATH = EXPORT_CONTEXTS / "obo.context.jsonld"
SHACL_OBO_TURTLE_PATH = EXPORT_CONTEXTS / "obo.context.ttl"
CONTEXT_OBO_SYNONYMS_PATH = EXPORT_CONTEXTS / "obo_synonyms.context.jsonld"
SHACL_OBO_SYNONYMS_TURTLE_PATH = EXPORT_CONTEXTS / "obo_synonyms.context.ttl"

EXPORT_RDF = EXPORT_DIRECTORY.joinpath("rdf")
SCHEMA_SVG_PATH = EXPORT_RDF / "schema.svg"
SCHEMA_PDF_PATH = EXPORT_RDF / "schema.pdf"
SCHEMA_TURTLE_PATH = EXPORT_RDF / "schema.ttl"
SCHEMA_NT_PATH = EXPORT_RDF / "schema.nt"
SCHEMA_JSONLD_PATH = EXPORT_RDF / "schema.jsonld"
RDF_TURTLE_PATH = EXPORT_RDF / "bioregistry.ttl"
RDF_NT_PATH = EXPORT_RDF / "bioregistry.nt"
RDF_JSONLD_PATH = EXPORT_RDF / "bioregistry.jsonld"

EXPORT_SSSOM = EXPORT_DIRECTORY.joinpath("sssom")
SSSOM_PATH = EXPORT_SSSOM / "bioregistry.sssom.tsv"
SSSOM_METADATA_PATH = EXPORT_SSSOM / "bioregistry.sssom.yml"

EXPORT_REGISTRY = EXPORT_DIRECTORY.joinpath("registry")
REGISTRY_YAML_PATH = EXPORT_REGISTRY / "registry.yml"
REGISTRY_JSON_PATH = EXPORT_REGISTRY / "registry.json"
REGISTRY_TSV_PATH = EXPORT_REGISTRY / "registry.tsv"

EXPORT_METAREGISTRY = EXPORT_DIRECTORY.joinpath("metaregistry")
METAREGISTRY_YAML_PATH = EXPORT_METAREGISTRY / "metaregistry.yml"
METAREGISTRY_TSV_PATH = EXPORT_METAREGISTRY / "metaregistry.tsv"

EXPORT_COLLECTIONS = EXPORT_DIRECTORY.joinpath("collections")
COLLECTIONS_YAML_PATH = EXPORT_COLLECTIONS / "collections.yml"
COLLECTIONS_TSV_PATH = EXPORT_COLLECTIONS / "collections.tsv"

#: The URL of the remote Bioregistry site
BIOREGISTRY_REMOTE_URL = pystow.get_config("bioregistry", "url") or "https://bioregistry.io"

#: Resolution is broken on identifiers.org for the following
IDOT_BROKEN = {
    "gramene.growthstage",
    "oma.hog",
    "obi",
    "mir",  # Added on 2021-10-08
    "storedb",  # Added on 2021-10-12
}

URI_FORMAT_KEY = "uri_format"

#: MIRIAM definitions that don't make any sense
MIRIAM_BLACKLIST = {
    # this one uses the names instead of IDs, and points to a dead resource.
    # See https://github.com/identifiers-org/identifiers-org.github.io/issues/139
    "pid.pathway",
}
IDENTIFIERS_ORG_URL_PREFIX = "https://identifiers.org/"

#: The priority list
LINK_PRIORITY = [
    "custom",
    "default",
    "bioregistry",
    "miriam",
    "ols",
    "obofoundry",
    "n2t",
    "bioportal",
    "scholia",
]
