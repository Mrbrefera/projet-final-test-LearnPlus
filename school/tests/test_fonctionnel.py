from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from school.models import Filiere, Classe, Niveau

class SchoolFunctionalTest(TestCase):

    def setUp(self):
        # Configuration initiale des données
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        self.filiere = Filiere.objects.create(nom="Sciences")
        self.niveau = Niveau.objects.create(nom="Terminale")
        self.classe = Classe.objects.create(niveau=self.niveau, numeroClasse=1, filiere=self.filiere)

    def test_login_view(self):
        """Test de la vue de connexion"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/guest-login.html')

    def test_successful_login(self):
        """Test de connexion réussie"""
        self.client.logout()
        response = self.client.post(reverse('islogin'), {
            'username': 'testuser',
            'password': 'password123'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "success")
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'redirect': 'admin', 'success': True, 'message': 'Vous êtes connectés!!!'}
        )

    def test_failed_login(self):
        """Test de connexion échouée avec mauvais identifiants"""
        self.client.logout()
        response = self.client.post(reverse('islogin'), {
            'username': 'wronguser',
            'password': 'wrongpassword'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Vos identifiants ne sont pas correcte")
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'success': False, 'message': 'Vos identifiants ne sont pas correcte'}
        )

    def test_signup_view(self):
        """Test de la vue d'inscription"""
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/guest-signup.html')

    def test_forgot_password_view(self):
        """Test de la vue de réinitialisation de mot de passe"""
        response = self.client.get(reverse('forgot_password'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/guest-forgot-password.html')

    def test_classe_list_view(self):
        """Test de la liste des classes"""
        response = self.client.get(reverse('classe-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Terminale 1")
        self.assertContains(response, "Sciences")

    def test_classe_detail_view(self):
        """Test de la vue détail d'une classe"""
        response = self.client.get(reverse('classe-detail', args=[self.classe.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Terminale 1")
        self.assertContains(response, "Sciences")

    def test_add_filiere(self):
        """Test d'ajout d'une filière via la vue"""
        response = self.client.post(reverse('filiere-add'), {
            'nom': 'Informatique'
        })
        self.assertEqual(response.status_code, 302)  # Redirection après ajout
        self.assertTrue(Filiere.objects.filter(nom="Informatique").exists())

    def test_update_filiere(self):
        """Test de mise à jour d'une filière"""
        response = self.client.post(reverse('filiere-update', args=[self.filiere.id]), {
            'nom': 'Sciences Appliquées'
        })
        self.filiere.refresh_from_db()
        self.assertEqual(self.filiere.nom, "Sciences Appliquées")

    def test_delete_filiere(self):
        """Test de suppression d'une filière"""
        response = self.client.post(reverse('filiere-delete', args=[self.filiere.id]))
        self.assertEqual(response.status_code, 302)  # Redirection après suppression
        self.assertFalse(Filiere.objects.filter(id=self.filiere.id).exists())

    def test_deconnexion(self):
        """Test de déconnexion"""
        response = self.client.get(reverse('deconnexion'))
        self.assertEqual(response.status_code, 302)  # Redirection vers login
        self.assertRedirects(response, reverse('login'))
