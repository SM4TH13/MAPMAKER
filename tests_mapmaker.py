import unittest
import fonctions_utile as fu

class TestMapMaker(unittest.TestCase):
    def setUp(self):
        # Grille 3x3 vide
        self.grille = [[None for _ in range(3)] for _ in range(3)]

    def test_tuile_valide(self):
        # Une tuile doit faire 4 caractères
        self.assertTrue(fu.tuile_valide("RGRG"))
        self.assertFalse(fu.tuile_valide("RG"))
        self.assertFalse(fu.tuile_valide(None))

    def test_grille_remplie(self):
        self.assertFalse(fu.grille_remplie(self.grille))
        remplie = [["GGGG"]*3 for _ in range(3)]
        self.assertTrue(fu.grille_remplie(remplie))

    def test_emplacement_valide(self):
        self.grille[0][0] = "GGGG"
        self.assertTrue(fu.emplacement_valide(self.grille, 0, 1, "GGGG"))

if __name__ == '__main__':
    unittest.main()
