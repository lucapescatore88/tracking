#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# @file   GaussOptions.py
# @author Albert Puig (albert.puig@cern.ch)
# @date   24.10.2014
# =============================================================================
"""Options for configuring Gauss."""


__all__ = ['get_gauss_options', 'get_available_options']


def get_gauss_options(sim_version, year, magnet_polarity, pythia_version):
    """Get simulation (Gauss) options.

    :param sim_version: Simulation version.
    :type sim_version: str
    :param year: Year for which to get conditions.
    :type year: int
    :param magnet_polarity: Polarity of the magnet (up or down).
    :type magnet_polarity: str
    :param pythia_version: Version of Pythia (6 or 8).
    :type pythia_version: int

    :returns: Configuration options.
    :rtype: dict (or None if not found)

    :raises: ValueError: If magnet polarity or Pythia version cannot
                         be understood/parsed.

    """
    # Get magnet polarity
    if 'up' in magnet_polarity.lower():
        magnet_polarity = 'up'
    elif 'down' in magnet_polarity.lower():
        magnet_polarity = 'down'
    else:
        raise ValueError("Cannot understand magnet polarity -> " % magnet_polarity)
    # Pythia version
    if '6' in str(pythia_version):
        pythia_version = 6
    elif '8' in str(pythia_version):
        pythia_version = 8
    else:
        raise ValueError("Cannot understand Pythia version -> %s" % pythia_version)
    # Let's build a key
    key = (str(sim_version).lower(), int(year), magnet_polarity, pythia_version)
    # And return!
    return _gauss_opt.get(key, None)


def get_available_options():
    """Get list of available options.

    :returns: List of available options in (sim, year, magnet, pythia) format.
    :rtype: list of tuples

    """
    return _gauss_opt.keys()


_gauss_opt = {}
_gauss_opt[('sim8f', 2012, 'up', 8)] = {'gauss_version': 'v45r8',
                                        'gauss_appconfig': 'v3r201',
                                        # 'gauss_decfiles': 'v27r34',
                                        'dddb': 'dddb-20130929-1',
                                        'conddb': 'sim-20130522-1-vc-mu100',
                                        'gauss_options': '$APPCONFIGOPTS/Gauss/Sim08-Beam4000GeV-mu100-2012-nu2.5.py '
                                                         '$LBPYTHIA8ROOT/options/Pythia8.py '
                                                         '$APPCONFIGOPTS/Gauss/G4PL_FTFP_BERT_EmNoCuts.py '
                                                         '$APPCONFIGOPTS/Persistency/Compression-ZLIB-1.py'}

_gauss_opt[('sim8f', 2012, 'down', 8)] = dict(_gauss_opt[('sim8f', 2012, 'up', 8)],
                                              conddb='sim-20130522-1-vc-md100',
                                              gauss_options=_gauss_opt[('sim8f', 2012, 'up', 8)]['gauss_options'].replace('mu100', 'md100'))

_gauss_opt[('sim8f', 2011, 'up', 8)] = {'gauss_version': 'v45r8',
                                        'gauss_appconfig': 'v3r201',
                                        'gauss_decfiles': 'v27r34',
                                        'dddb': 'dddb-20130929',
                                        'conddb': 'sim-20130522-vc-mu100',
                                        'gauss_options': '$APPCONFIGOPTS/Gauss/Sim08-Beam3500GeV-mu100-2011-nu2.py '
                                                         '$LBPYTHIA8ROOT/options/Pythia8.py '
                                                         '$APPCONFIGOPTS/Gauss/G4PL_FTFP_BERT_EmNoCuts.py '
                                                         '$APPCONFIGOPTS/Persistency/Compression-ZLIB-1.py'}

_gauss_opt[('sim8f', 2011, 'down', 8)] = dict(_gauss_opt[('sim8f', 2011, 'up', 8)],
                                              conddb='sim-20130522-vc-md100',
                                              gauss_options=_gauss_opt[('sim8f', 2011, 'up', 8)]['gauss_options'].replace('mu100', 'md100'))

# EOF
