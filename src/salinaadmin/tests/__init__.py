import unittest

import test_urls


def suite():
    """The suite() function in the test module creates an appropriate test
    suite. This standard Python Unittest convention is understood by Django.
    @return a TestSuite 
    """
    return unittest.TestSuite([
        unittest.TestLoader().loadTestsFromModule(test_urls),
    ])

