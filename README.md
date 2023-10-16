# bastienp7_dashboard
Folder contains files for dashboard

Explication des fonctionnalités de l'API et du Dashboard réalisés pour l'entreprise Prêt à dépenser.

L’API est développée en Python. J’ai opté pour un hébergement sous Heroku qui permet de relier automatiquement mon projet Github et de le déployer à chaque nouvelle modification sans avoir à créer l’API à chaque fois.

On trouve les éléments du dashboard à savoir une page pour les clients et une page pour les prospects.
Il peut sur la page d'accueil accéder à l'interprétation globale par rapport à l'ensemble du dataset en cliquant sur le lien  dans le sidebar. L’importance des variables dans le résultat du score est donc réalisé grâce à l’affichage d’un graphique issu de la méthode Shap.

Le Dashboard est affiché grâce à la librairie Streamlit et le fichier Dashboard.py (les pages HTML ne sont pas nécessaires avec Streamlit). Une fois arrivé sur cette page, deux choix s’offrent à l’utilisateur, soit il peut réaliser une simulation pour un client de l’entreprise ou soit pour un prospect. En fonction du choix nous n’aurons pas les mêmes éléments à enregistrer connaissant déjà les informations des clients. Dans ce cas-là seule la référence sera nécessaire. Dans le second nous aurons besoin d’étudier sa situation en recueillant divers éléments. Dans les deux cas en validant nous obtenons une réponse claire pour nous informer si le prêt a un avis favorable ou non. Nous retrouvons aussi la situation de cet individu et son positionnement par rapport à l’ensemble des clients de l’entreprise. Cela nous donne donc une indication que les éléments qui peuvent améliorer le résultat en cas d’avis défavorable. Pour le choix de la page client nous utilisons Page_client.py. Pour le choix de la page prospect, nous utilisons le fichier Page_prospect.py qui réalise une simulation en utilisant le modèle XGBoost généré avec MLFLOW dans les notebooks de préparation. On retrouve également comme indication le score lorsque nous réalisons une prédiction sur la page des clients.

Le fait d’avoir cette interaction entre l’API et le Dashboard est essentiel pour une bonne fluidité lors du rendez-vous avec le client/prospect et apporter une réponse rapide mais aussi créer une expérience utilisateur de qualité.
