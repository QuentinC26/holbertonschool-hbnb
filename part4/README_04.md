# Readme Part4

### Pour faire fonctionner le serveur, j'ai fait des tests dans cet ordre là :

* Création d'un users
* Authentification du web token
* Connexion sur le site

Pour commencer les tests, il faut être dans le chemin suivant :

**holbertonschool-hbnb/part4**

Une fois dedans, il faut taper python3 run.py pour lancer le serveur.

De là, on peut tester le users, pour le créer j'ai utilisez cette base :

{
  * "first_name": "John",
  * "last_name": "Doe",
  * "email": "john.doe@gmail.com",
  * "password": "jesuisunecornichon"
}

Pour les autres commandes qui concerne les users, vous pouvez aussi utiliser les deux autres utilisateurs :



    * "first_name": "Quentin",
    * "last_name": "Zuzlewski",
    * "email": "q.zuzlewski@gmail.com"


    
ou



    * "first_name": "Isabelle",
    * "last_name": "Dutronc",
    * "email": "isa.ductronc@gmail.com"



Quentin et Isabelle ont le même mot de passe : test

Le hbnb reste assez visuel :

* le bouton login nous ramène vers la connexion
* le bouton details nous permet de voir les détails d'un lieu
* le bloc note nous permet d'accéder au formulaire pour ajouter un avis

**Attention :** Malgré tout mes efforts, je ne suis pas parvenu à faire fonctionner le formulaire pour ajouter un avis alors il faut le créer via postman ou curl.
