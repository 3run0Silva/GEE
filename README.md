# EH
GEEvents
Projet de cour python




Introduction :

Cette application vise à amener à l’utilisateur de façon simple et intuitive l’information sur les évènements à Genève qui se trouve dispersé à travers le web et qui demande des recherches, ou même la connaissance préalable de l’évènement.




Développeur / Développeuse


À propos de ce projet :

Ce projet utilise une architecture MVC
Ce projet a été conçue utilisent les technologies suivantes
Principal :
•	Python
•	Flask
•	Selenium
•	Firebase
Secondaires :
•	HTML/CSS
•	Bootstrap
•	Javascript
Dépendances :
•	Axios : $ npm install axios
•	Flask-cors : $ pip install -u flask-cors
•	Firebase-admin : $ pip install –user firebase-admin

L’ides du projet et tout simplement de scraper le web pour information sur les événements à Genève et les stocker sur une base de données NoSQL (Firebase), une fois les données stockées on utilise une API pour gérer la communication entre le front et le back, pour terminer un simple front qui perme a l’utilisateur de lance de requêtes ver la base de données pour avoir la data sur les événements 


Environnent de projet :

[Docker ?]


Documentation de l’API :

API ENDPOINTS :
•	GET all events
o	URL : /Events
o	Méthode : GET
o	Paramètres : Aucun
o	Réponse : Liste de tous les événements.
o	Example de réponse : http://127.0.0.1:5000/events

•	GET events by tag
o	URL : /Events/tag/<tag>
o	Méthode : GET
o	Paramètres :
	`tag` (requis) : Le tag des événements à filtrer.
o	Réponse : Liste des événements filtrés par tag.
o	Example de réponse : http://127.0.0.1:5000/events/tag/Dance
•	GET events by date
o	URL : /Events/date ?day=<day>&month=<month>&year=<year>
o	Méthode : GET
o	Paramètres :
	 `day`, `month`, `year`(requis) : La date à filtrer.
o	Réponse : Liste des événements filtrés par jour, mois ou année.
o	Example de réponse : http://127.0.0.1:5000/events/date?day=18&month=04&year=2024




Gestion des erreurs : 

Codes d’erreur communs :
•	404 ( Not found )

Le Frontend : vue que le projet de python vise plutôt le backend de l’application, j’ai fait un frontend en utilisent vanille javascript plus HTML et CSS/Bootstrap basic pour cette première phase du projet de cette forme on peut quand même teste notre API sans avoir besoin d’outils supplémentaire.



 ...
