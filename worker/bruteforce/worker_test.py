import unittest
from bruteforce import worker


class TestStringMethods(unittest.TestCase):
    def test_collision_detection_with_one_level_recursion(self):
        self.assertEqual('a', worker.find_hash_collision('0cc175b9c0f1b6a831c399e269772661'))

    def test_collision_detection_with_two_level_recursion(self):
        self.assertEqual('ab', worker.find_hash_collision('187ef4436122d1cc2f40dc2b92f0eba0'))

    def test_collision_detection_with_ten_level_recursion(self):
        self.assertEqual('abc', worker.find_hash_collision('900150983cd24fb0d6963f7d28e17f72'))


if __name__ == '__main__':
    unittest.main()
