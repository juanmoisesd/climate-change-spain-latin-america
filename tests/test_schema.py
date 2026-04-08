import unittest
import json
import os

class TestSchema(unittest.TestCase):
    def test_schema_exists(self):
        self.assertTrue(os.path.exists('schema.json'))

    def test_schema_load(self):
        with open('schema.json', 'r') as f:
            schema = json.load(f)
        self.assertEqual(schema['title'], "Climate Change Spain Latin America Data Schema")

if __name__ == '__main__':
    unittest.main()
