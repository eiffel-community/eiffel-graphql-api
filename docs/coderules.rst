.. _coderules:

##########
Code Rules
##########

Eiffel GraphQL API code rules.

Tox <https://tox.readthedocs.io> is executed on each pull request to execute all tests, linters and code rules.
This can also be run locally by installing tox <https://tox.readthedocs.io/en/latest/install.html> and running the command.

Standard

* black <https://github.com/psf/black> for general code formatting.
* pydocstyle <http://www.pydocstyle.org> for checking docstring formats using pep257 <https://www.python.org/dev/peps/pep-0257>.
* pylint <https://www.pylint.org> as the main linter.
