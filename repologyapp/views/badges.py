# Copyright (C) 2016-2017 Dmitry Marakasov <amdmi3@amdmi3.ru>
#
# This file is part of repology
#
# repology is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# repology is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with repology.  If not, see <http://www.gnu.org/licenses/>.

import flask

from repologyapp.globals import *
from repologyapp.view_registry import ViewRegistrar

from repology.packageproc import PackagesetToBestByRepo


@ViewRegistrar('/badge/vertical-allrepos/<name>.svg')
def badge_vertical_allrepos(name):
    packages = get_db().get_metapackage_packages(name, fields=['repo', 'version', 'versionclass'])
    best_pkg_by_repo = PackagesetToBestByRepo(packages)

    entries = [
        {
            'repo': repometadata[reponame],
            'package': best_pkg_by_repo[reponame]
        } for reponame in reponames if reponame in repometadata and reponame in best_pkg_by_repo
    ]

    return (
        flask.render_template(
            'badge-vertical.svg',
            entries=entries,
            name=name
        ),
        {'Content-type': 'image/svg+xml'}
    )


@ViewRegistrar('/badge/tiny-repos/<name>.svg')
def badge_tiny_repos(name):
    return (
        flask.render_template(
            'badge-tiny.svg',
            name=name,
            num_families=get_db().get_metapackage_families_count(name)
        ),
        {'Content-type': 'image/svg+xml'}
    )


@ViewRegistrar('/badge/version-for-repo/<repo>/<name>.svg')
def badge_version_for_repo(repo, name):
    packages = get_db().get_metapackage_packages(name, fields=['repo', 'version', 'versionclass'])
    best_pkg_by_repo = PackagesetToBestByRepo(packages)

    if repo not in best_pkg_by_repo:
        return (flask.render_template('badge-tiny-string.svg', string='Unknown repository'), 404, {'Content-type': 'image/svg+xml'})

    return (
        flask.render_template(
            'badge-tiny-version.svg',
            repo=repo,
            version=best_pkg_by_repo[repo].version,
            versionclass=best_pkg_by_repo[repo].versionclass,
        ),
        {'Content-type': 'image/svg+xml'}
    )


@ViewRegistrar('/badge/version-only-for-repo/<repo>/<name>.svg')
def badge_version_only_for_repo(repo, name):
    packages = get_db().get_metapackage_packages(name, fields=['repo', 'version', 'versionclass'])
    best_pkg_by_repo = PackagesetToBestByRepo(packages)

    if repo not in best_pkg_by_repo:
        return (flask.render_template('badge-tiny-string.svg', string='-'), 404, {'Content-type': 'image/svg+xml'})

    return (
        flask.render_template(
            'badge-tiny-version-only.svg',
            repo=repo,
            version=best_pkg_by_repo[repo].version,
            versionclass=best_pkg_by_repo[repo].versionclass,
        ),
        {'Content-type': 'image/svg+xml'}
    )
