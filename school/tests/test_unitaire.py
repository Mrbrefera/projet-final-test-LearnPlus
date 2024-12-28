from django.test import TestCase
from django.contrib.auth.models import User
from school.models import Filiere, Matiere, Niveau, Classe, Chapitre, Cours

class SchoolModelTest(TestCase):

    def setUp(self):
        # Configuration initiale
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.filiere = Filiere.objects.create(nom="Sciences")
        self.niveau = Niveau.objects.create(nom="Terminale")
        self.classe = Classe.objects.create(niveau=self.niveau, numeroClasse=1, filiere=self.filiere)
        self.matiere = Matiere.objects.create(
            nom="Mathématiques",
            description="Cours de mathématiques avancés"
        )
        self.chapitre = Chapitre.objects.create(
            classe=self.classe,
            matiere=self.matiere,
            titre="Chapitre 1",
            description="Introduction aux limites",
            duree_en_heure=10,
            instructeur=self.user
        )
        self.cours = Cours.objects.create(
            chapitre=self.chapitre,
            titre="Cours 1: Les Limites",
            description="Introduction détaillée aux limites",
            video="path/to/video.mp4"
        )

    def test_filiere_creation(self):
        """Vérifie la création d'une filière"""
        self.assertEqual(self.filiere.nom, "Sciences")
        self.assertTrue(self.filiere.status)

    def test_niveau_creation(self):
        """Vérifie la création d'un niveau"""
        self.assertEqual(self.niveau.nom, "Terminale")
        self.assertTrue(self.niveau.status)

    def test_classe_creation(self):
        """Vérifie la création d'une classe et ses relations"""
        self.assertEqual(self.classe.numeroClasse, 1)
        self.assertEqual(self.classe.niveau, self.niveau)
        self.assertEqual(self.classe.filiere, self.filiere)

    def test_matiere_creation(self):
        """Vérifie la création d'une matière"""
        self.assertEqual(self.matiere.nom, "Mathématiques")
        self.assertEqual(self.matiere.description, "Cours de mathématiques avancés")
        self.assertTrue(self.matiere.status)

    def test_chapitre_creation(self):
        """Vérifie la création d'un chapitre"""
        self.assertEqual(self.chapitre.titre, "Chapitre 1")
        self.assertEqual(self.chapitre.duree_en_heure, 10)
        self.assertEqual(self.chapitre.instructeur.username, "testuser")

    def test_cours_creation(self):
        """Vérifie la création d'un cours"""
        self.assertEqual(self.cours.titre, "Cours 1: Les Limites")
        self.assertEqual(self.cours.description, "Introduction détaillée aux limites")
        self.assertEqual(self.cours.video, "path/to/video.mp4")

    def test_slug_generation(self):
        """Vérifie que le slug est généré automatiquement pour chaque modèle"""
        self.matiere.save()
        self.assertIn("mathematiques", self.matiere.slug)

        self.chapitre.save()
        self.assertIn("chapitre-1", self.chapitre.slug)

        self.cours.save()
        self.assertIn("cours-1-les-limites", self.cours.slug)

    def test_classe_string_representation(self):
        """Vérifie la représentation en chaîne d'une classe"""
        self.assertEqual(str(self.classe), "Terminale 1")

    def test_chapitre_string_representation(self):
        """Vérifie la représentation en chaîne d'un chapitre"""
        self.assertEqual(str(self.chapitre), "Chapitre 1")

    def test_cours_string_representation(self):
        """Vérifie la représentation en chaîne d'un cours"""
        self.assertEqual(str(self.cours), "Cours 1: Les Limites")

    def test_update_matiere(self):
        """Vérifie que la mise à jour d'une matière fonctionne"""
        self.matiere.nom = "Physique"
        self.matiere.save()
        self.assertEqual(self.matiere.nom, "Physique")

    def test_delete_filiere(self):
        """Vérifie que la suppression d'une filière fonctionne"""
        filiere_id = self.filiere.id
        self.filiere.delete()
        with self.assertRaises(Filiere.DoesNotExist):
            Filiere.objects.get(id=filiere_id)

    def test_relations_between_models(self):
        """Vérifie les relations entre les modèles"""
        self.assertEqual(self.chapitre.classe, self.classe)
        self.assertEqual(self.chapitre.matiere, self.matiere)
        self.assertEqual(self.cours.chapitre, self.chapitre)
