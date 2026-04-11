import unittest
import os

class TestIntegrity(unittest.TestCase):
    def test_directories(self):
        dirs = ['data/raw', 'data/clean', 'data/analysis_ready']
        for d in dirs:
            self.assertTrue(os.path.isdir(d))

    def test_required_files(self):
        files = ['README.md', 'LICENSE', 'CITATION.cff']
        for f in files:
            self.assertTrue(os.path.exists(f))

if __name__ == '__main__':
    unittest.main()
