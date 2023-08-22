from fcc2zim.constants import VERSION


# dummy test just to check that everything is in place to add more tests / report
# coverage
def test_version():
    assert VERSION and len(VERSION) > 0
