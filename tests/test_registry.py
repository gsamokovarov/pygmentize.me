import unittest

from app.registry import Registrable, Registry


class RegistrableTest(unittest.TestCase):
    def tearDown(self):
        Registry.clear()

    def test_proper_register(self):
        Ent = type('Ent', (Registrable,), {})
        Ent.make_registry()

        self.assertTrue(issubclass(Ent, Registry))

        Sub = type('Sub', (Ent,), {})
        Sub.register()

        self.assertTrue(Sub in Registry.entries_for(Ent))

    def test_registry_unregisterable(self):
        with self.assertRaises(TypeError):
            Ent = type('Ent', (Registrable,), {})
            Ent.make_registry()

            # We should blow up here.
            Ent.register()

    def test_specific_registry_clearing(self):
        Ent = type('Ent', (Registrable,), {})
        Ent.make_registry()

        Sub = type('Sub', (Ent,), {})
        Sub.register()

        self.assertTrue(Sub in Registry.entries_for(Ent))

        Registry.clear(Ent)

        self.assertFalse(Sub in Registry.entries_for(Ent))

    def test_global_registries_clearing(self):
        Ent1 = type('Ent1', (Registrable,), {})
        Ent1.make_registry()
         
        Ent2 = type('Ent2', (Registrable,), {})
        Ent2.make_registry()

        Registry.clear()

        with self.assertRaises(TypeError):
            Registry.entries_for(Ent1)

        with self.assertRaises(TypeError):
            Registry.entries_for(Ent2)

    #def test_multiple_registries_along_the_chain(self):
    #    Ent = type('Ent1', (Registrable,), {})
    #    Ent.make_registry()

    #    with self.assertRaises(TypeError):
    #        SpecEnt = type('SpecEnt', (Ent,), {})
    #        SpecEnt.make_registry()

