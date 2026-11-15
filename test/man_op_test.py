import unittest
import flow_draw.manual_operation as manop

class ManOpTest(unittest.TestCase):
    def test_00000(self):
        manop.main()
        self.assertTrue(True)


def suite() -> unittest.TestSuite:
    suite = unittest.TestSuite()
    suite.addTest(ManOpTest('test_00000'))
    return suite



if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())