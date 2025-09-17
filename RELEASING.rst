A reminder for the maintainers on how to make a new release.

Note that the VERSION should follow the semantic versioning as ``X.Y.Z`` (e.g. ``v1.0.5``).

1. Create a ``release-VERSION`` branch from ``upstream/master``.
2. Update ``CHANGELOG.rst``.
3. Push the branch to ``upstream``.
4. Once all tests pass, start the ``deploy`` workflow manually or via::

    gh workflow run deploy.yml --repo ESSS/barril --ref release-VERSION -f version=VERSION

5. Merge the PR.
