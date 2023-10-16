#Importation des librairies
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import requests
import seaborn as sns
import shap
import pickle
import json
import base64
#from github import Github
#from github import Auth
#Librairie pour utiliser google drive
#import os
#from pydrive.auth import GoogleAuth
#from pydrive.drive import GoogleDrive


#Initialisation pour google drive
#gauth = GoogleAuth()
#drive = GoogleDrive(gauth)
#Dossier contenant les fichiers upload/download de google drive
#folder = '1lmP2vJKEzZNwh4V2zTgMRFUcVlT6Bj-X'
#directory = "C:/Users/Bastien/bastienp7_api_streamlit/bastienp7_api-main/data_saved"
#Fonctions pour upload/download fichier sur google drive
# Upload files

#directory = "D:/pyGuru/Youtube/Google services/Google drive backup/data"
#for f in os.listdir(directory):
#	filename = os.path.join(directory, f)
#	gfile = drive.CreateFile({'parents' : [{'id' : folder}], 'title' : f})
#	gfile.SetContentFile(filename)
#	gfile.Upload()

# Download files
#file_list = drive.ListFile({'q' : f"'{folder}' in parents and trashed=false"}).GetList()
#for index, file in enumerate(file_list):
#	print(index+1, 'file downloaded : ', file['title'])
#	file.GetContentFile(file['title'])

#githubAPIURL = "https://api.github.com/repos/BBastien17/bastienp7_api/contents/conv_csv_data.csv"
#githubToken = "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"

#Importation du modèle mlflow
with open(f'xgb_model_final/model.pkl', 'rb') as f:
    model = pickle.load(f)

#commenter les 3 lignes suivantes pour les tests
#load_fichierSauvegarde2 = open("shap_model_data_X_train", "rb")
#explainer = pickle.load(load_fichierSauvegarde2)
#load_fichierSauvegarde2.close()


#Utilisation d'un fonction pour comparer un individu au reste de la population
def compare_client(data_work, data_list_result_transf):
    data_num = data_work.select_dtypes(['int64','float64'])
    data_num_prospect = data_list_result_transf.select_dtypes(['int64','float64'])
    i = 0
    for data_work in data_num:
        #Première ligne pour vérifier la valeur de l'individu
        #st.write(data_num_client.iloc[0, i])
        fig = plt.figure(figsize=(20, 5))
        sns.boxplot(x=data_num[data_work])
        plt.axvline(data_num_prospect.iloc[0, i], color='red', label='Individu', linewidth=4)
        st.pyplot(fig)
        i = i + 1

#Utilisation d'une fonction pour définir la page prospect
#Création d'un formulaire à compléter
def page_p (data_work) :

    st.title("Demande d'étude de financement :")

    type_pret_client = st.radio("Type de prêt :",
                                key="Type_de_pret",
                                options=['Prêts de trésorerie', 'Prêts renouvelables'])
    
    genre_client = st.radio("Genre :",
                            key="Genre",
                            options=['Masculin', 'Féminin'])
    
    age_client = st.number_input('Âge du client',
                                 min_value=18, value=25, max_value=100, step=1)
    
    niveau_etudes_client = st.radio("Niveau d'études :",
                                    key="Niveau_d_etudes",
                                    options=['3 à 4', '5 à 8'])
    
    reg_matrimonial = st.radio("Régime matrimoniale :",
                               key="Regime_matrimonial",
                               options=['célibataire', "marié(e)", 'autre'])
    
    nb_enfant = st.number_input("Nombre d'enfants",
                                min_value=0, value=0, max_value=19, step=1)
    
    nb_membre_famille = st.number_input("Nombre de membres de la famille",
                                        min_value=1, value=1, max_value=20, step=1)

    mt_revenus = st.number_input('Montant annuel des revenus',
                                 min_value=0, value=40000, max_value=117000000, step=1)
    
    lieu_habitation = st.number_input("Note d'évaluation du lieu d'habitation",
                                      min_value=1, value=1, max_value=3, step=1)
    
    nb_demande = st.number_input('Nombre de demande de financement du client',
                                 min_value=0, value=0, max_value=25, step=1)

    mt_prets = st.number_input('Montant des prêts',
                               min_value=0, value=0, max_value=4050000, step=1)

    mt_annuites = st.number_input('Montant des annuités',
                                  min_value=0, value=0, max_value=300425, step=1)

    nb_jours_credits = st.number_input('Nombre de jours de crédits',
                                       min_value=0, value=0, max_value=2922, step=1)
    
    mt_anticipation = st.number_input("Montant de l'anticipation",
                                      min_value=-169033, value=0, max_value=555000, step=1)

    delai_anticipation = st.number_input("Délai d'anticipation",
                                         min_value=-605, value=0, max_value=392, step=1)
        

    #Création d'un dictionnaire où l'on stocke les résultats
    list_result = {'Type_de_pret':[type_pret_client], 'Genre':[genre_client],
                   'Age':[age_client], 'Niveau_d_etudes':[niveau_etudes_client],
                   'Regime_matrimonial':[reg_matrimonial], 'Nb_enfants': [nb_enfant],
                   'Nb_membre_famille':[nb_membre_famille], 'Montant_des_revenus':[mt_revenus],
                   'Note_region_client':[lieu_habitation], 'Nb_demande_client':[nb_demande],
                   'Montants_du_pret':[mt_prets], 'Montant_des_annuites':[mt_annuites],
                   'Nb_jours_credits':[nb_jours_credits], 'Montant_anticipation_pret':[mt_anticipation],
                   'Delai_anticipation_pret':[delai_anticipation]}

    #On transforme ensuite le dictionnaire en dataframe
    data_list_result = pd.DataFrame(data=list_result)
    #On oublie pas de préparer la transformation des variables catégorielles en variables numériques plus tard
    transf_data_categ = {'Prêts de trésorerie': 0, 'Prêts renouvelables': 1,
                         'autre': 0, 'célibataire': 1, 'marié(e)': 2,
                         'Masculin': 1, 'Féminin': 0,
                         '3 à 4': 0, '5 à 8': 1}   

    #Utile pour les tests afin de vérifiers que nous avons que des variables numériques  
    #list_of_data_type = data_pred.info()
    #st.write(list_of_data_type)
    #st.text(data_pred.info(verbose=True))


    #Préparation du dataframe pour le transformer en json et les variables catégorielles en variables numériques
    data_list_result_transf = data_list_result.replace(transf_data_categ)
    select_data_infos = data_list_result_transf.iloc[0]

    #Création d'un bouton pour lancer le scoring
    predict_btn = st.button('Résultat de la demande de financement', key = "prospects_button")
    if predict_btn:

        #Conversion des données client en csv
        conv_csv_data = select_data_infos.to_csv(r'conv_csv_data.csv')
        f = open("conv_csv_data.csv", "r", encoding="utf-8")
        files = {"file": f}
        #Envoi du fichier csv vers l'API
        req = requests.post("http://127.0.0.1:5000/streamlit_prediction", files=files)
        #Récupération des résultats de l'API
        resultat = req.json()
        rec = resultat["predictions"]
        result_predict = rec[0]
        st.write("Variable result_predict : ", result_predict)

        #Enregistrement des données du client
        #conv_csv_data = data_list_result_transf.to_csv(r'data_saved/conv_csv_data.csv',sep='\t', index=False)

        #with open("conv_csv_data.csv", "rb") as f:
            # Encoding "my-local-image.jpg" to base64 format
        #    encodedData = base64.b64encode(f.read())

        #    headers = {
        #        "Authorization": f'''Bearer {githubToken}''',
        #        "Content-type": "application/vnd.github+json"
        #    }
        #    data = {
        #        "message": "Enregistrement des donnees sur le csv",  # Put your commit message here.
        #        "content": encodedData.decode("utf-8")
        #    }

        #    r = requests.put(githubAPIURL, headers=headers, json=data)
        #    print(r.text)  # Printing the response

        #Envoi de la valeur saisie sur one drive
        #upload_file_list = ['conv_csv_data.csv']
        #for f in os.listdir(directory):
        #    filename = os.path.join(directory, f)
        #    gfile = drive.CreateFile({'parents': [{'id': folder}], 'title': f})
        #    gfile.SetContentFile(filename)
        #    gfile.Upload()


        #for upload_file in upload_file_list:
        #    gfile = drive.CreateFile({'parents': [{'id': folder}]})



        # Read file and set it as the content of this instance. gfile.SetContentFile(upload_file) gfile.Upload() # Upload the file.
        #filename = os.path.join(conv_csv_data)
        #gfile = drive.CreateFile({'parents': [{'id': folder}], 'title': conv_csv_data})
        #gfile.SetContentFile(filename)
        #gfile.Upload()
        #st.write("Envoi des données client")


        #st.write("Predict button was pressed")

        #Lecture fichier csv sur github
        #csv_url = 'https://raw.githubusercontent.com/BBastien17/bastienp7_api/main/conv_csv_data.csv'
        #conv_data_csv = pd.read_csv(csv_url, sep='\t', error_bad_lines=False)
        #st.write("variable conv_data_csv : ", conv_data_csv)
        #st.write(conv_data_csv)
        #test_val = conv_data_csv.values.tolist()
        #st.write(test_val)

        #Last
        #req = requests.get("https://bastienp7-api-64085d97a29c.herokuapp.com/api/data_stream")
        #Last
        #pred_url = 'https://raw.githubusercontent.com/BBastien17/bastienp7_api/main/pred_result.csv'
        #prospect_pred = pd.read_csv(pred_url, error_bad_lines=False)


        #st.write("variable prospect_pred : ", prospect_pred)

        # score_url = 'https://raw.githubusercontent.com/BBastien17/bastienp7_api/main/score.csv'
        # prospect_score = pd.read_csv(score_url, error_bad_lines=False)
        # st.write("variable conv_data_csv : ", prospect_score)

        #Last
        #result_predict = prospect_pred.values
        #result_predict = 0

        if result_predict == 0 :
            st.text("Les données fournies permettent d'émettre un avis favorable à la demande de prêt.")
            st.text("Positionnement des caractéristiques du prospect vis à vis du reste de la clientèle :")
            compare_client(data_work, data_list_result_transf)

        elif result_predict == 1 :
            st.text("Les données fournies ne permettent pas d'émettre un avis favorable à la demande de prêt.")
            #Création d'un dataframe avec les valeurs du prospect
            data_line_pred = pd.DataFrame(data_list_result_transf, columns=data_work.columns)
            #Utile pour les tests afin d'afficher les valeurs du client sélectionné
            st.write(data_line_pred)
            #Utilisation de la méthode shap via le pickle
            #shap_values = explainer(data_line_pred)
    
            #Utilisation de  et affichage de l'interprétabilité locale
            fig = shap.plots.bar(shap_values[0])  
            plt.savefig('shap_report_P7.png', bbox_inches='tight')      
            st.image('shap_report_P7.png')
            st.text("Positionnement des caractéristiques du prospect vis à vis du reste de la clientèle :")
            compare_client(data_work, data_list_result_transf)

        
