from test.runner import perform_test

class TestCamt:
    def test_camt054_001_04(self):
        # assert perform_test('camt.054.001.04.xsd', 'test-camt.054.001.04.xml')
        pass

    def test_camt054(self):
        assert perform_test('camt054.xsd', 'test-camt054.xml')

    def test_pacs_008_001_02(self):
        # assert perform_test('pacs.008.001.02.xsd', 'test-pacs.008.001.02.xml')
        pass
