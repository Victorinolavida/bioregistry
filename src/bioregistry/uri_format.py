# -*- coding: utf-8 -*-

"""Tools for getting URI format strings.

.. warning::

    URI format strings are different from URI prefix strings. URI format strings have a ``$1`` where
    the prefix should go, which makes them more general than URI prefix strings.
"""

import warnings
from typing import List, Mapping, Optional, Sequence, Tuple

from .resource_manager import manager

__all__ = [
    "get_uri_format",
    "get_uri_prefix",
    "get_format_urls",
    "get_prefix_map",
    "get_prefix_list",
]


def get_uri_format(prefix: str, priority: Optional[Sequence[str]] = None) -> Optional[str]:
    """Get the URI format string for the given prefix, if it's available.

    :param prefix: The name of the prefix (possibly unnormalized)
    :param priority: The priority order of metaresources to use for URI format string lookup.
        The default is:

        1. Default first party (from bioregistry, prefix commons, or miriam)
        2. OBO Foundry
        3. Prefix Commons
        4. Identifiers.org / MIRIAM
        5. OLS
    :return: The best URI format string, where the ``$1`` should be replaced by the
        identifier. ``$1`` could potentially appear multiple times.

    >>> import bioregistry
    >>> bioregistry.get_uri_format('chebi')
    'https://www.ebi.ac.uk/chebi/searchId.do?chebiId=CHEBI:$1'

    If you want to specify a different priority order, you can do so with the ``priority`` keyword. This
    is of particular interest to ontologists and semantic web people who might want to use ``purl.obolibrary.org``
    URI prefixes over the URI prefixes corresponding to the first-party providers for each resource (e.g., the
    ChEBI example above). Do so like:

    >>> import bioregistry
    >>> bioregistry.get_uri_format('chebi', priority=['obofoundry', 'bioregistry', 'prefixcommons', 'miriam', 'ols'])
    'http://purl.obolibrary.org/obo/CHEBI_$1'
    """
    return manager.get_uri_format(prefix=prefix, priority=priority)


def get_uri_prefix(prefix: str, priority: Optional[Sequence[str]] = None) -> Optional[str]:
    """Get a well-formed URI prefix for usage in a prefix map.

    :param prefix: The prefix to lookup.
    :param priority: The prioirty order for :func:`get_format`.
    :return: The URI prefix. Similar to what's returned by :func:`bioregistry.get_format`, but
        it MUST have only one ``$1`` and end with ``$1`` to use thie function.

    >>> import bioregistry
    >>> bioregistry.get_uri_prefix('chebi')
    'https://www.ebi.ac.uk/chebi/searchId.do?chebiId=CHEBI:'
    """
    return manager.get_uri_prefix(prefix=prefix, priority=priority)


def get_prefix_map(
    *,
    priority: Optional[Sequence[str]] = None,
    include_synonyms: bool = False,
    remapping: Optional[Mapping[str, str]] = None,
    use_preferred: bool = False,
) -> Mapping[str, str]:
    """Get a mapping from Bioregistry prefixes to their URI prefixes.

    :param priority: A priority list for how to generate URI prefix.
    :param include_synonyms: Should synonyms of each prefix also be included as additional prefixes, but with
        the same URI prefix?
    :param remapping: A mapping from bioregistry prefixes to preferred prefixes.
    :param use_preferred: Should preferred prefixes be used? Set this to true if you're in the OBO context.
    :return: A mapping from prefixes to URI prefixes.
    """
    return manager.get_prefix_map(
        priority=priority,
        include_synonyms=include_synonyms,
        remapping=remapping,
        use_preferred=use_preferred,
    )


def get_format_urls(**kwargs) -> Mapping[str, str]:
    """Get a mapping from Bioregistry prefixes to their URI prefixes."""
    warnings.warn("deprecated", DeprecationWarning)
    return get_prefix_map(**kwargs)


def get_prefix_list(**kwargs) -> List[Tuple[str, str]]:
    """Get the default priority prefix list."""
    return manager.get_prefix_list(**kwargs)
