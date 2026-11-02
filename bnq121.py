# Coéquipiers : Alex Gaudreau, Gabriel Théoret, Raphaël Piché
# Projet : Banque
# Importation des modules nécessaires
from cProfile import label
from tkinter import *
from tkinter import ttk
import random
from tkinter import font
import sqlite3
import sys
import string
from tkinter import *

connexion = sqlite3.connect('base.db')
cursor = connexion.cursor()

# Variables globales
num_compte_dispo = [101, 102, 103, 104, 105, 106, 107, 108, 109, 110]
num_compte_pris = []
# Création de la table banque
requete = """CREATE TABLE IF NOT EXISTS banque(
id INTEGER PRIMARY KEY AUTOINCREMENT,
 num_compte INTEGER NOT NULL, 
 mdp TEXT NOT NULL,
 conf_mdp TEXT NOT NULL,
 phrase TEXT NOT NULL,
 argent INTEGER NOT NULL,
 nb_virement INTEGER NOT NULL)"""
cursor.execute(requete)
# On prend les numéros de compte déjà pris
regard = cursor.execute("select*from banque")
for row in regard:
    num_compte_pris.append(row[1])
    num_compte_dispo.remove(row[1])

connexion.commit()


# Definition de la fenêtre principale pour le client
def fen_client():
    global numero_compte

    # Fonction pour le virement
    def virm():
        global argent, nb_virement
        connexion = sqlite3.connect('base.db')
        cursor = connexion.cursor()
        if montant_virement.get() != "" and combo.get() != "":
            if int(montant_virement.get()) > int(argent):
                fen_erreur = Toplevel(fen_principale)
                fen_erreur.title("Argent insuffisant")
                fen_erreur.geometry("300x150")
                Label(fen_erreur,
                      text="Erreur : T'es pauvre.",
                      fg="red",
                      font=("Arial", 12),
                      wraplength=250).pack(pady=20)
                Button(fen_erreur,
                       text="Réessayer",
                       command=fen_erreur.destroy).pack(pady=10)
            else:
                argent -= int(montant_virement.get())
                nb_virement += 1
                Solde_aff.config(text=f"Solde: {argent}$")
                vir_aff.config(text=f"Nombre de virements: {nb_virement}")
                fen_erreur = Toplevel(fen_principale)
                fen_erreur.title("Virement réussi")
                fen_erreur.geometry("300x150")
                Label(fen_erreur,
                      text="Virement effectué",
                      fg="green",
                      font=("Arial", 12),
                      wraplength=250).pack(pady=20)
                Button(fen_erreur,
                       text="Continuer",
                       command=fen_erreur.destroy).pack(pady=10)
                id_compte = cursor.execute(
                    "SELECT * FROM banque WHERE num_compte=(?)",
                    (numero_compte,))
                for row in id_compte:
                    id_compte = row
                requete = "UPDATE banque set(argent, nb_virement)=(?,?) where (id) = (?)"
                cursor.execute(requete, (argent, nb_virement, id_compte[0]))
                id_compte_pris = cursor.execute(
                    "SELECT * FROM banque WHERE num_compte=(?)",
                    (combo.get(),))
                for row in id_compte_pris:
                    id_compte_pris = row
                    argent_pris_nouveau = row[5] + int(montant_virement.get())
                    nb_virement_pris = row[6] + 1
                requete = "UPDATE banque set(argent, nb_virement)=(?,?) where (id) = (?)"
                cursor.execute(
                    requete,
                    (argent_pris_nouveau, nb_virement_pris, id_compte_pris[0]))
                connexion.commit()
        # toplevel en cas d'erreur
        else:
            fen_erreur = Toplevel(fen_principale)
            fen_erreur.title("Mauvaise entrée")
            fen_erreur.geometry("300x150")
            Label(fen_erreur,
                  text="Veuillez entrer les bonnes informations",
                  fg="red",
                  font=("Arial", 12),
                  wraplength=250).pack(pady=20)
            Button(fen_erreur, text="Réessayer",
                   command=fen_erreur.destroy).pack(pady=10)

    # Fonction pour fermer la fenêtre
    def fermerfen():
        fen_principale.destroy()

    fen_principale = Tk()
    fen_principale.geometry('400x600')

    # titre
    titre = Label(fen_principale,
                  text="BANQUE ARGA",
                  font=("Times New Roman", 25, "bold"),
                  fg="black")
    titre.place(relx=0.5, rely=0.03, anchor=CENTER)
    bienvenu = Label(fen_principale,
                     text='Vous souhaite la bienvenue',
                     font=("Times New Roman", 10, 'italic'),
                     fg="black")
    bienvenu.place(relx=0.5, rely=0.08, anchor=CENTER)

    # Mon compte
    mon_compte = Label(fen_principale,
                       text="Mon compte",
                       font=("Arial", 15, "bold"),
                       fg="black")
    mon_compte.place(relx=0.25, rely=0.2, anchor=CENTER)

    numero_compte_aff = Label(fen_principale,
                              text="Numero Compte: {}".format(numero_compte))
    numero_compte_aff.place(relx=0.25, rely=0.25, anchor=CENTER)

    Solde_aff = Label(fen_principale, text="Solde: {}$".format(str(argent)))
    Solde_aff.place(relx=0.183, rely=0.3, anchor=CENTER)

    vir_aff = Label(fen_principale,
                    text="Nombre de virements: {}".format(nb_virement))
    vir_aff.place(relx=0.27, rely=0.35, anchor=CENTER)

    # virement

    virement = Label(fen_principale,
                     text="Virements",
                     font=("Arial", 15, "bold"),
                     fg="black")
    virement.place(relx=0.75, rely=0.2, anchor=CENTER)
    montant_vir = Label(fen_principale, text="Montant du virement")
    montant_vir.place(relx=0.75, rely=0.25, anchor=CENTER)
    montant_virement = Entry(fen_principale)
    montant_virement.place(relx=0.75, rely=0.279, anchor=CENTER)
    # choix du compte
    choix_compte = Label(fen_principale, text="Choix de compte")
    choix_compte.place(relx=0.75, rely=0.32, anchor=CENTER)
    num_compte_pris.remove(float(numero_compte))
    combo = ttk.Combobox(fen_principale,
                         values=num_compte_pris,
                         state="readonly")
    combo.place(relx=0.75, rely=0.35, anchor=CENTER)
    # bouton pour confirmer le virement
    confirm_virement = Button(fen_principale, text="Confirmer", command=virm)
    confirm_virement.place(relx=0.75, rely=0.40, anchor=CENTER)

    fermer = Button(fen_principale,
                    text="FERMER",
                    command=fermerfen,
                    width=25,
                    fg="red")
    fermer.place(relx=0.5, rely=0.7, anchor=CENTER)

    fen_principale.mainloop()

    # Fonction pour la fenêtre de connexion


def fenetre_connexion():
    global numero_compte, mdp, mdp_connexion, argent, nb_virement
    fen = Tk()
    fen.geometry("450x600")
    fen.resizable(False, False)
    fen.title("Connexion")
    font_entry = font.Font(family='Times New Roman', size=10, slant='italic')

    selected_option = StringVar()
    selected_option.set("Client")  # Option de depart

    choix_client = False
    choix_admin = False

    def prochaine_etape():
        global numero_compte, mdp_connexion, argent, nb_virement
        numero_compte = num_compte_entry.get()
        mdp_connexion = mdp_entry.get()

        if numero_compte == "adm" and mdp_connexion == "123" and choix_admin == True:
            if len(num_compte_dispo) >0 :
                connexion = sqlite3.connect('base.db')
                cursor = connexion.cursor()
                numero_compte = random.choice(num_compte_dispo)
                a = random.randint(100, 500)
                mdp = ''.join(random.choices(string.ascii_lowercase, k=3))
                conf_mdp = mdp
                phrase_mdp = "BONJOUR"

                requete = """INSERT INTO banque(num_compte, mdp, conf_mdp, phrase, argent, nb_virement)
                            VALUES
                            (?,?,?,?,?,?)"""
                nb_virement = 0
                cursor.execute(requete, (numero_compte, mdp, conf_mdp, phrase_mdp,
                                         a, nb_virement))
                connexion.commit()
                connexion.close()
                num_compte_pris.append(numero_compte)
                if numero_compte in num_compte_dispo:
                    num_compte_dispo.remove(numero_compte)

            def base_donne():
                frame_base_donnees.lift()  # met le frame au-dessus
                connexion = sqlite3.connect('base.db')
                cursor = connexion.cursor()
                for compte in num_compte_pris:

                    cursor.execute("SELECT * FROM banque WHERE num_compte=?",(compte,))
                    resultat = cursor.fetchone()
                    solde = resultat[5]
                    label_num = Label(fen_admin,text="Compte: "+str(compte))
                    label_solde = Label(fen_admin,text="Solde: "+str(solde)+"$")
                    position_y = {101:0.2,102:0.35,103:0.5,104:0.65,105:0.8,106:0.2,107:0.35,108:0.5,109:0.65,110:0.8}
                    if compte <= 105:
                        label_num.place(relx=0.3,rely=position_y[compte],anchor=CENTER)
                        label_solde.place(relx=0.3,rely=((position_y[compte])+0.05),anchor=CENTER)
                    else:
                        label_num.place(relx=0.7,rely=position_y[compte],anchor=CENTER)
                        label_solde.place(relx=0.7,rely=((position_y[compte])+0.05),anchor=CENTER)
            def quitter():
                fen_admin.destroy()
                fenetre_connexion()

            def mise_a_jour():
                frame_mise_a_jour.lift()
                choix = Label()
                liste_comptes =ttk.Combobox(fen_admin,
                             values=num_compte_pris,
                             state="readonly")
                liste_comptes.place(relx=0.2,rely=0.4,anchor=CENTER)
                bouton_sup = None
                def supprimer2():
                    def bouton_confirmation():
                        fen_erreur.destroy()
                        connexion = sqlite3.connect("base.db")
                        cursor = connexion.cursor()

                        cursor.execute("DELETE FROM banque WHERE num_compte = ?",(liste_comptes.get(),))

                        connexion.commit()
                        connexion.close()
                        print("Suppression du compte n{} effectuée.".format(liste_comptes.get()))
                        num_compte_pris.remove(int(liste_comptes.get()))
                        num_compte_dispo.append(int(liste_comptes.get()))
                        liste_comptes['values'] = num_compte_pris  # mettre à jour les valeurs
                        liste_comptes.set('')  # vide la sélection actuelle
                        bouton_sup.place_forget()


                    fen_erreur = Toplevel(fen_admin)
                    fen_erreur.title("Confirmation")
                    fen_erreur.geometry("300x100")
                    Label(fen_erreur,
                          text="Êtes vous sûr de vouloir supprimer ce compte?",
                          fg="red",
                          font=("Arial", 12),
                          wraplength=250).pack(pady=20)
                    Button(fen_erreur,
                           text="CONFIRMER",
                           command=bouton_confirmation).pack(pady=3)
                def supprimer():
                    nonlocal bouton_sup
                    if liste_comptes.get() != "":

                        bouton_sup = Button(fen_admin,text="SUPPRIMER",command=supprimer2)
                        bouton_sup.place(relx=0.2,rely=0.7,anchor=CENTER)
                    else:
                        choix.set("")
                        fen_erreur = Toplevel(fen_admin)
                        fen_erreur.title("erreur")
                        fen_erreur.geometry("300x100")
                        Label(fen_erreur,
                              text="Veuillez selectioner un numéro de compte",
                              fg="red",
                              font=("Arial", 12),
                              wraplength=250).pack(pady=20)
                        Button(fen_erreur,
                               text="RÉASSAYEZ",
                               command=fen_erreur.destroy).pack(pady=3)


                choix = StringVar()
                choix.set(None)
                  # valeur par défaut

                r1 = Radiobutton(fen_admin, text="Supprimer un compte", variable=choix, value="Option 1", command=supprimer)
                r1.place(relx=0.2,rely=0.2,anchor=CENTER)
                r2 = Radiobutton(fen_admin, text="Modifier le solde", variable=choix, value="Option 2")
                r2.place(relx=0.8,rely=0.2,anchor=CENTER)



            fen.destroy()
            fen_admin = Tk()
            fen_admin.geometry('400x300')
            menubar = Menu(fen_admin)
            acceuil = Menu(menubar,tearoff= 0)
            frame_mise_a_jour = Frame(fen_admin)
            frame_mise_a_jour.place(relx=0, rely=0, relwidth=1, relheight=1)
            frame_mise_a_jour.lower()  # met le frame derrière les autres widgets (invisible)
            frame_base_donnees = Frame(fen_admin)
            frame_base_donnees.place(relx=0, rely=0, relwidth=1, relheight=1)
            frame_base_donnees.lower()  # cache au départ
            menubar.add_command(label="Base de données", command=base_donne )
            menubar.add_cascade(label="Mise à jour", command=mise_a_jour)
            menubar.add_command(label="Quitter", command=quitter)
            fen_admin.config(menu=menubar)
            fen_admin.mainloop()

        elif choix_admin == False:
            connexion = sqlite3.connect('base.db')
            cursor = connexion.cursor()
            numero_compte = num_compte_entry.get()

            mdp_connexion = mdp_entry.get()

            # On cherche si un utilisateur avec ce numéro et ce mdp existe
            cursor.execute("SELECT * FROM banque WHERE num_compte=? AND mdp=?",
                           (numero_compte, mdp_connexion))
            resultat = cursor.fetchone()

            if resultat:

                argent = resultat[5]
                nb_virement = resultat[6]

                fen.destroy()
                fen_client()
            else:
                fen_erreur = Toplevel(fen)
                fen_erreur.title("Erreur de connexion")
                fen_erreur.geometry("300x100")
                Label(fen_erreur,
                      text="Numéro de compte ou mot de passe incorrect.",
                      fg="red",
                      font=("Arial", 12),
                      wraplength=250).pack(pady=20)
                Button(fen_erreur,
                       text="Réessayer",
                       command=fen_erreur.destroy).pack(pady=10)

        else:
            fen_erreur = Toplevel(fen)
            fen_erreur.title("Erreur de connexion")
            fen_erreur.geometry("300x100")
            Label(fen_erreur,
                  text="Identifiant admin ou mot de passe incorrect.",
                  fg="red",
                  font=("Arial", 12),
                  wraplength=250).pack(pady=20)
            Button(fen_erreur, text="Réessayer",
                   command=fen_erreur.destroy).pack(pady=10)



    def fc_client():
        nonlocal choix_admin, choix_client
        choix_client = True
        choix_admin = False
        num_compte_titre.config(text="Numéro de compte")
        bouton_mdp_oublie.config(bg="white")

    def fc_admin():
        nonlocal choix_admin, choix_client
        choix_admin = True
        choix_client = False
        num_compte_titre.config(text="Identifiant admin")
        bouton_mdp_oublie.config(bg="grey")

    def mdp_oublie():
        if choix_admin == False:
            fen.withdraw()
            num_compte_mdp_oublie = input(
                "Quel est votre numéro de compte? : ")
            phrase_mdp_o = input("Quel était votre phrase de rappel? : ")
            connexion = sqlite3.connect('base.db')
            cursor = connexion.cursor()

            # On cherche si un utilisateur avec ce numéro et ce mdp existe
            cursor.execute("SELECT * FROM banque WHERE num_compte=? AND phrase=?",
                           (num_compte_mdp_oublie, phrase_mdp_o))
            resultat = cursor.fetchone()
            if resultat:
                print("Votre mot de passe est {}".format(resultat[2]))
            fen.deiconify()

    titre = Label(fen,
                  text="BANQUE ARGA",
                  font=("Times New Roman", 25, "bold"),
                  fg="black")
    titre.place(relx=0.5, rely=0.10, anchor=CENTER)
    bienvenu = Label(fen,
                     text='Vous souhaite la bienvenue',
                     font=("Times New Roman", 10, 'italic'),
                     fg="black")
    bienvenu.place(relx=0.5, rely=0.15, anchor=CENTER)

    num_compte_titre = Label(fen,
                             text="Numéro de compte",
                             font=('Times New Roman', 10))
    num_compte_titre.place(relx=0.5, rely=0.30, anchor=CENTER)
    num_compte_entry = Entry(fen, justify='center', width=10, font=font_entry)
    num_compte_entry.place(relx=0.5, rely=0.35, anchor=CENTER)

    mdp_titre = Label(fen, text="Mot de passe", font=('Times New Roman', 10))
    mdp_titre.place(relx=0.5, rely=0.40, anchor=CENTER)
    mdp_entry = Entry(fen, justify='center', width=10, font=font_entry)
    mdp_entry.place(relx=0.5, rely=0.45, anchor=CENTER)

    bouton_acces = Button(fen,
                          text="Connexion",
                          font=("Times New Roman", 20, 'italic'),
                          command=prochaine_etape)
    bouton_acces.place(relx=0.5, rely=0.9, anchor=CENTER)

    radio1 = Radiobutton(fen,
                         text="Client",
                         font=('Courier New', 10),
                         variable=selected_option,
                         value="Client",
                         command=fc_client)
    radio2 = Radiobutton(fen,
                         text="Admin",
                         font=('Courier New', 10),
                         variable=selected_option,
                         value="Admin",
                         command=fc_admin)

    radio1.place(relx=0.5, rely=0.57, anchor=CENTER)
    radio2.place(relx=0.5, rely=0.60, anchor=CENTER)

    bouton_mdp_oublie = Button(fen,
                               text="Mot de passe oublié?",
                               font=("Times New Roman", 10, 'italic'),
                               activeforeground='#F0F0F0',
                               command=mdp_oublie)
    bouton_mdp_oublie.place(relx=0.5, rely=0.5, anchor=CENTER)
    fen.mainloop()


def interface_console():
    global mdp, numero_compte, phrase_mdp, argent
    connexion = sqlite3.connect('base.db')
    cursor = connexion.cursor()

    # Partie 1 : le choix
    touche_valide = False
    while touche_valide == False:
        touche = input(
            "Touchez A pour vous connecter à l'application ou tapez U pour créer un nouvel utilisateur: "
        ).upper()
        print("Vous avez tapé la touche {}".format(touche))

        # Partie 2 : numéro de compte
        if touche == "U":
            conf_mdp_true_false = False
            touche_valide = True
            if len(num_compte_dispo) == 0:
                print(
                    "Nous sommes désolé de vous annoncer que nous sommes malheureusement plein pour le moment. Veuillez réessayer plus tard."
                )
                sys.exit()
            numero_compte = random.choice(num_compte_dispo)
            print(
                'Bienvenu chez la banque ARGA. Nous sommes très heureux de commencer cette aventure avec vous.'
            )
            print("Votre numéro de compte sera {}".format(numero_compte))
            while conf_mdp_true_false == False:
                mdp = input(
                    "Choisissez votre mot de passe de 3 caractères et appuyez sur Entrer: "
                )
                conf_mdp = input(
                    "Confirmer votre mot de passe de 3 caractères et appuyez sur Entrer: "
                )
                if mdp != conf_mdp or len(mdp) != 3:
                    print("Mot de passe invalide. Veuillez réessayez...")
                else:
                    conf_mdp_true_false = True
                    phrase_mdp = input(
                        "Indiquez une phrase pour vous rappeler du mot de passe et appuyez sur ENTRÉE: "
                    )
            argent = random.randint(100, 500)
            print(
                "Pour vous souhaiter la bienvenu, on vous offre un fond de départ de {}$"
                .format(argent))

            requete = """INSERT INTO banque(num_compte, mdp, conf_mdp, phrase, argent, nb_virement)
            VALUES
            (?,?,?,?,?,?)"""
            nb_virement = 0
            cursor.execute(requete, (numero_compte, mdp, conf_mdp, phrase_mdp,
                                     argent, nb_virement))
            connexion.commit()
            connexion.close()

        elif touche == "A":
            touche_valide = True
            fenetre_connexion()


# fenetre_connexion()
connexion = sqlite3.connect('base.db')
cursor = connexion.cursor()

cursor.execute("SELECT * FROM banque")
lignes = cursor.fetchall()


connexion.close()
interface_console()
