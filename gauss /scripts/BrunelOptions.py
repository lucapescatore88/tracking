#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# @file   BrunelOptions.py
# @author Albert Puig (albert.puig@cern.ch)
# @date   26.10.2014
# =============================================================================
"""Options for configuring Brunel."""


__all__ = ['get_brunel_options', 'get_available_options']


def get_brunel_options(reco_version, year):
    """Get digitization (Brunel) options.

    :param reco_version: Recontruction version.
    :type reco_version: str
    :param year: Year for which to get the options.
    :type year: int

    :returns: Configuration options.
    :rtype: dict (or None if not found)

    """
    year = int(year)
    return _brunel_opt.get((reco_version, year), None)


def get_available_options():
    """Get list of available options.

    :returns: List of available options in (reco, year) format.
    :rtype: list of tuples

    """
    return _brunel_opt.keys()


_brunel_opt = {}

_brunel_opt[('Reco14a', 2012)] = {'brunel_version': 'v43r2p7',
                                  'brunel_appconfig': 'v3r164',
                                  'brunel_options': '$APPCONFIGOPTS/Brunel/DataType-2012.py '
                                                    '$APPCONFIGOPTS/Brunel/MC-WithTruth.py '
                                                    '$APPCONFIGOPTS/Persistency/Compression-ZLIB-1.py'}

_brunel_opt[('Reco14a', 2011)] = {'brunel_version': 'v43r2p7',
                                  'brunel_appconfig': 'v3r171',
                                  'brunel_options': '$APPCONFIGOPTS/Brunel/DataType-2011.py '
                                                    '$APPCONFIGOPTS/Brunel/MC-WithTruth.py '
                                                    '$APPCONFIGOPTS/Persistency/Compression-ZLIB-1.py'}

# EOF
