## Functional testing suite for SeisHub.

The goal is to treat SeisHub as a black box and just test its behaviour. This
is not meant to replace the SeisHub internal unit tests but rather augment and
complement it. Certain things are just hard/impossible to test with unit
testing, especially in a complex software package.

So far it is very simple but the plan is to enhance it quite a bit.

Currently only works with this SeisHub branch:

[https://github.com/krischer/seishub.core/tree/granular_authorization](https://github.com/krischer/seishub.core/tree/granular_authorization)

### Requirements

* seishub.core
* setuptools
* colorama

### Installation

Checkout the repository

```bash
git clone https://github.com/krischer/seishub.functional_tests
cd seishub.functional_tests
```

and then either

```bash
python setup.py install
```

or (if you prefer `pip` and have it installed)

```bash
pip install .
```

should do the trick.

### Usage

```bash
python -m seishub.functional_tests
```

By default stdout, stderr, and stdin from the SeisHub server are caught by the
test runner. To enable debugging, e.g. setting a trace or something similar,
this must not be the case. Disable it with

```bash
python -m seishub.functional_tests debug
```
