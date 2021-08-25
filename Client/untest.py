import unittest
import keepreq


class MyTest(unittest.TestCase):

    def setUp(self):
        self.note_server_client = keepreq.NoteServerClient('http://127.0.0.1:5000/')

    def test_view_cat(self):
        self.assertEqual(keepreq.work_parse(['-s', 'http://127.0.0.1:5000/', 'view', '--categories']), True)


    def test_add_cat(self):
        self.assertEqual(keepreq.work_parse(['-s', 'http://127.0.0.1:5000/', 'add', '--category', 'Expenses']), True)
        categories, res_code = self.note_server_client.view_categories()



if __name__ == '__main__':
    unittest.main()
