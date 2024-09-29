from test.runner import perform_test

class TestCamt:
    def test_camt054_001_04(self):
        pass

    def test_camt054(self):
        assert perform_test('test/camt054.xsd', 'test/test-camt054.xml')

    def test_pacs_008_001_02(self):
        pass
