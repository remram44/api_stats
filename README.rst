api_stats tool
==============

api_stats is a Python tool aimed at recording statistics from an API endpoint. For example, the GitHub API gives out a single number of downloads for each release; by running this tool, you can easily graph rolling averages and historical figures.

Quickstart
----------

api_stats loads a "configuration file" that tells it what to fetch and which fields to record. This file is a Python script that will be loaded by api_stats, with a single global ``stats`` that acts as the interface with the program. This interface currently offers two functions: ``record(key, value)``, and ``get_json(url)``.

Here is an example configuration file, that records the number of downloads of each file from GitHub releases::

    releases = stats.get_json(
        "https://api.github.com/repos/remram44/api_stats/releases")
    for release in releases:
        relname = release.get('tag_name') or release['name']
        for asset in release['assets']:
            stats.record('%s/%s' % (relname, asset['name']),
                         asset['download_count'])
