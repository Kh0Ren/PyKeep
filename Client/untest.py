import unittest
import keepreq


class MyTest(unittest.TestCase):

    def test_par(self):
        self.assertEqual(keepreq.work_parse(['-s', 'http://127.0.0.1:5000/', 'view', '--categories']), True)




if __name__ == '__main__':
    unittest.main()
