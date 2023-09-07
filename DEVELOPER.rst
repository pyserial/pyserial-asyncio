====================
Notes for developers
====================

Creating a release
==================

- Ensure that the ``version`` in ``serial_asyncio_fast/__init__.py`` is updated
  and in the form of major.minor[.patchlevel]
- Ensure all changes, including version, is committed then create a tag with
  the same value as the version but prefixed with a ``v`` (e.g. "v0.5")
- Push to GitHub, merge into master if it is a branch. The GitHub Actions
  are set-up to build the default branch.
- Inspect the built wheel and tar.gz files for correctness, test.
- Trigger the upload to PyPi by using GitHub web interface "Releases" and
  create a new release from the tag.
