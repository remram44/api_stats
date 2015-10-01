api_stats tool
==============

api_stats is a Python tool aimed at recording statistics from an API endpoint. For example, the GitHub API gives out a single number of downloads for each release; by running this tool, you can easily graph rolling averages and historical figures.

Quickstart
----------

api_stats loads a "configuration file" that tells it what to fetch and which fields to record. This file is a Python script that will be loaded by api_stats, with a single global ``stats`` that acts as the interface with the program. This interface currently offers two functions: ``record(key, value)``, and ``get_json(url)``.

Here is an example configuration file, that records the number of downloads of each file from GitHub releases:

..  code-block:: python

    releases = stats.get_json(
        "https://api.github.com/repos/remram44/api_stats/releases")
    for release in releases:
        relname = release.get('tag_name') or release['name']
        for asset in release['assets']:
            stats.record('%s/%s' % (relname, asset['name']),
                         asset['download_count'])

Then you can plot the data, for example using matplotlib:

..  code-block:: bash

    python -m api_stats.plot -m '^(.+)$' 'api_stats:\g<1>' data.jsonl

A more complex example
----------------------

You might want to use functions to factor the retrieval of data points from a specific source:

..  code-block:: python

    def github(repo):
        releases = stats.get_json(
            "https://api.github.com/repos/%s/releases" % repo)
        for release in releases:
            if release['draft']:
                continue
            relname = release.get('tag_name') or release['name']
            for asset in release['assets']:
                stats.record('github/%s/%s/%s' % (repo, relname, asset['name']),
                             asset['download_count'])


    github('VisTrails/VisTrails')
    github('remram44/api_stats')


    def pypi(pkg):
        releases = stats.get_json(
            "https://pypi.python.org/pypi/%s/json" % pkg)['releases']
        for relname, release in releases.items():
            for asset in release:
                stats.record('pypi/%s/%s/%s' % (pkg, relname, asset['filename']),
                             asset['downloads'])


    pypi('VisTrails')
    pypi('api_stats')

This will record data under ``pypi/<pkg_name>/<version>/<filename>`` and ``github/<owner>/<repo>/<version>/<filename>``. You can then plot the data, one figure per project, aggregated by version but adding PyPI and GitHub together, using:

..  code-block:: bash

    python -m api_stats.plot \
        -m '^pypi/([^/]+)/([^/]+)/.+$' '\g<1>:\g<2>' \
        -m '^github/[^/]+/([^/]+)/v([^/]+)/.+$' '\g<1>:\g<2>' \
        releases.jsonl

..  image:: https://cloud.githubusercontent.com/assets/426784/10232482/0550d7e0-6857-11e5-835f-86631dd89b4d.png
    :alt: Example Plot with matplotlib
