import unittest
import os
import sys
sys.path += ["./service"]

print(os.getcwd())

import brewconfig as b


class MyTestCase(unittest.TestCase):
    def test_read_config(self):
        bc = b.BrewConfig()
        config = bc.read_config()
        self.assertTrue(bc.get("braubar"), "config is null")

    def test_get(self):
        config = b.BrewConfig()
        config_version = config.get("braubar")["version"]
        expected_version = "0.1.0"
        self.assertEqual(config_version, expected_version, "values of versions not equal")

    def test_set(self):
        config = b.BrewConfig()
        test = {"foo": "123", "bar": "asd", "baz": "FOO"}
        config.set("test", test)
        self.assertEqual(config.get("test"), test)


if __name__ == '__main__':
    unittest.main()
