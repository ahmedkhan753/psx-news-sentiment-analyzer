
import unittest
from .functions import *
from .constants import *

class TestUtilsFunctions(unittest.TestCase):
    def test_getPort(self):
        port = getPort()
        self.assertEqual(port, '4200', "should return 4200 when no env is provided")

    def test_return_false_when_not_production(self):
        env_name = isProduction('local')
        self.assertEqual(env_name, False, "should return false")
    
    def test_return_true_when_production(self):
        env_name = isProduction(ENV_PPRODUCTION)
        self.assertEqual(env_name, True, "should return true when env is actually prodction")

if __name__ == '__main__':
    unittest.main()