import unittest

from app.utils import classonlymethod


class ClassonlymethodTest(unittest.TestCase):
    def setUp(self):
        class Tester(object):
            @classonlymethod
            def special_method(cls):
                return cls
        
        self.Tester = Tester

    def test_calls_from_instances(self):
        Tester = self.Tester 

        with self.assertRaises(AttributeError):
            Tester().special_method() 

        self.assertEqual(Tester.special_method(), Tester)

    def test_classmethod_behavior(self):
        class SpecificTester(self.Tester):
            '''
            Just a sublcass to prove it.
            '''

        self.assertEqual(SpecificTester.special_method(), SpecificTester)

