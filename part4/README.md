# 🧠 HBnB - Couche logique d'entreprise

Ce dossier contient l'implémentation des classes métiers principales de l'application HBnB, utilisées pour modéliser les entités de base : User, Place, Review, Amenity ainsi qu'une classe BaseModel partagée.

## 📦 Structure des fichiers

Modèles/

├── base_model.py # Classe parent avec UUID, timestamps et logique commune

├── user.py # Modèle d'utilisateur

├── place.py # Modèle de lieu

├── review.py # Modèle d'avis

└── amenity.py # Modèle de commodité


---

## 🔖 Modèle de base

Classe parent commune à tous les modèles métiers.

### Attributs :

- id : identifiant unique (UUID4)

- created_at : date de création

- updated_at : dernière mise à jour

### Méthodes :

- save() : met à jour updated_at

- update(data: dict) : met à jour plusieurs attributs via un dictionnaire

---

## 👤 Utilisateur

Représente un utilisateur inscrit.

### Attributs :

- id : UUID

- first_name : prénom (obligatoire, max 50)

- nom_de famille : nom (obligatoire, max 50)

- email : e-mail unique et valide

- is_admin : booléen (faux par défaut)

- created_at, updated_at : timestamps hérités

### Exemple :

From models.user import User

Utilisateur = Utilisateur("Alice", "Smith", "alice@example.com")

Print(user.email) # alice@example.com


---

## 🏠 Lieu

Représente un logement proposé par un utilisateur.

### Attributs :

- title : titre du lieu (obligatoire, max 100)

- description : texte libre

- price : prix à la nuit (float > 0)

- latitude, longitude : coordonnées (-90 à 90 / -180 à 180)

- propriétaire : instance de l'utilisateur

- reviews : liste de Review

- amenities : liste d'agrément

- created_at, updated_at : timestamps hérités

### Méthodes :

- add_review(review) : associer un avis

- add_amenity(amenity) : associer une commodité

### Exemple :

Place = Place("Villa Bleue", "Piscine privée", 120.0, 48.85, 2.35, utilisateur)


---

## ✍️ Examen

Représente un avis laissé par un utilisateur sur un lieu.

### Attributs :

- texte : contenu de l'avis (obligatoire)

- rating : note (entre 1 et 5)

- place : instance de Place

- utilisateur : instance de l'utilisateur

- created_at, updated_at : timestamps hérités

### Exemple :

Review = Review("Excellent séjour !", 5, lieu, utilisateur)

Place.add_review(review)


---

## 🛏️ Commodité

Représente une commodité proposée avec un logement (Wi-Fi, Parking, etc.).

### Attributs :

- nom : nom de la commodité (obligatoire, max 50)

- created_at, updated_at : timestamps hérités

### Exemple :

Wifi = Commenity("Wi-Fi")

Place.add_amenity(wifi)


---

## 🧪 Exemple global

From models.user import User

De models.place import Place

À partir de models.review import Review

De models.amenity import Amenity

Propriétaire = Utilisateur("Bob", "Marley", "bob@hbnb.com")

Place = Place("Cabane", "Au calme", 80, 44.0, 3.0, propriétaire)

Review = Review("Top !", 5, lieu, propriétaire)

Wifi = Commenity("Wi-Fi")

Place.add_review(review)

Place.add_amenity(wifi)

Print(place.reviews[0].text) # Haut !

Print(place.amenities[0].name) # Wi-Fi


---

## 🛠️ Dépendances

- Python 3.8+

- Aucune base de données requise (stockage en mémoire)

- Module uuid et datetime intégrés

- re pour l'e-mail de validation

---

## :clipboard: Diagramme ER

![Diagramme ER](https://i15.servimg.com/u/f15/19/74/13/62/untitl10.png)

### Entités Principales : ###

USER (Utilisateur) : Représente les utilisateurs de ton application. Chaque utilisateur a des attributs comme un ID, un nom, un prénom, un email, un mot de passe, et un indicateur s'il est administrateur ou non.

PLACE (Lieu) : Représente les propriétés ou les lieux que les utilisateurs peuvent créer ou gérer. Les attributs incluent un ID, un titre, une description, un prix, les coordonnées de latitude et de longitude, et l'ID de l'utilisateur qui en est le propriétaire.

AMENITY (Amenité) : Représente les caractéristiques ou services disponibles dans un lieu, comme une piscine ou le Wi-Fi. Chaque amenité possède un ID et un nom.

REVIEW (Commentaire) : Représente des évaluations ou des avis laissés par les utilisateurs sur un lieu. Chaque commentaire a un ID, un texte, un rating (évaluation en chiffres) et fait référence à l'utilisateur et au lieu concerné.

### Relations : ###

USER ||--o{ PLACE : Cela signifie qu'un utilisateur peut créer plusieurs lieux, mais chaque lieu a un seul créateur (l'utilisateur).

USER ||--o{ REVIEW : Un utilisateur peut également laisser plusieurs commentaires, mais chaque commentaire est associé à un seul utilisateur.

PLACE ||--o{ REVIEW : Un lieu peut avoir plusieurs commentaires, mais chaque commentaire se réfère à un seul lieu.

PLACE ||--o{ AMENITY : Un lieu peut avoir plusieurs accompagnements, mais chaque accompagnement peut être associé à plusieurs lieux.

PLACE_AMENITY : C'est une table de liaison qui permet de relier des lieux et des aménités, permettant à un lieu d'avoir plusieurs aménités et inversement.

### Table de Liaison : ###

PLACE_AMENITY : Cette table contient des clés étrangères pour le place_id et amenity_id afin de créer des relations entre les lieux et les aménités.

## 📄 Licence

Projet réalisé dans le cadre de la formation Holberton School (HBnB v2 - Business Logic).
