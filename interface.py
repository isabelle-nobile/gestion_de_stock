import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.messagebox import askyesno
from categories import Categorie
from produit import Produit
from connexion import conn

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.conn = conn()
        self.create_database()
        self.create_tables_categories()
        self.create_tables_produit()
        self.produit = Produit(self.conn)
        self.categorie = Categorie(self.conn)
        self.categorie_id_dict = {}

        self.master = master
        self.master.title("Gestion de stocks")
        self.master.iconbitmap('gestiondesstocksicon.ico')
        self.pack()
        self.create_widgets()
    
    def create_database(self):
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS boutique")

        # create the categorie table
        return self.cursor.execute("USE boutique")

    def create_tables_produit(self):
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS produit (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nom VARCHAR(255),
            description TEXT,
            prix INT,
            quantite INT,
            id_categorie INT,
            FOREIGN KEY (id_categorie) REFERENCES categorie(id)
        )
        """)
    
    def create_tables_categories(self):
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS categorie (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nom VARCHAR(255)
        )
        """)

    def create_widgets(self):
        # Créer un cadre pour la classe Categorie
        self.categorie_frame = tk.LabelFrame(self, text="Categories")
        self.categorie_frame.pack(side="left", padx=10, pady=10)

        # Ajouter une étiquette pour afficher toutes les catégories
        self.categories_label = tk.Label(self.categorie_frame, text="Toutes les categories :")
        self.categories_label.pack()

        # Créer un cadre pour la liste des catégories
        self.categorie_frame = tk.Frame(self.categorie_frame)
        self.categorie_frame.pack()

        # Créer une zone d'affichage pour les produits
        self.categories_listbox = tk.Listbox(self.categorie_frame, height=10, width=50)
        self.categories_listbox.pack()

        # Récupérer la liste de tous les produits
        liste_categories = self.categorie.read_all_categorie()

        # Ajouter les produits à la zone d'affichage
        for categorie in liste_categories:
            self.categories_listbox.insert(tk.END, f"Nom: {categorie[1]}")

        # Ajouter un bouton pour ajouter une nouvelle catégorie
        self.add_categorie_button = tk.Button(self.categorie_frame, text="Ajouter une categorie", command=self.add_categorie)
        self.add_categorie_button.pack()

        # Ajouter une étiquette pour afficher les produits d'une catégorie
        self.produits_label = tk.Label(self.categorie_frame, text="Produits dans cette categorie :")
        self.produits_label.pack()

        # Ajouter une zone d'affichage pour les produits de la catégorie sélectionnée
        self.produits_cat_listbox = tk.Listbox(self.categorie_frame, height=10, width=50)
        self.produits_cat_listbox.pack()

        # Créer un cadre pour la classe Produit
        self.produit_frame = tk.LabelFrame(self, text="Produits")
        self.produit_frame.pack(side="left", padx=10, pady=10)

        # Ajouter une étiquette pour afficher tous les produits
        self.produits_label = tk.Label(self.produit_frame, text="Tous les produits :")
        self.produits_label.pack()

        # Créer un cadre pour la liste des produits
        self.produits_frame = tk.Frame(self.produit_frame)
        self.produits_frame.pack()

        # Créer une zone d'affichage pour les produits
        self.produits_listbox = tk.Listbox(self.produits_frame, height=10, width=100)
        self.produits_listbox.pack()

        # Récupérer la liste de tous les produits
        liste_produits = self.produit.read_all_produit()

        # Ajouter les produits à la zone d'affichage
        for produit in liste_produits:
            self.produits_listbox.insert(tk.END, f"ID: {produit[0]}, Nom: {produit[1]}, Description: {produit[2]}, Prix: {produit[3]}, Quantité: {produit[4]}, Catégorie: {produit[5]}")

        # Ajouter un bouton pour ajouter un nouveau produit
        self.add_produit_button = tk.Button(self.produit_frame, text="Ajouter un produit", command=self.add_produit)
        self.add_produit_button.pack()

        # Ajouter un bouton pour modifier un nouveau produit
        self.modify_produit_button = tk.Button(self.produit_frame, text="Mofidier un produit", command=self.modify_produit)
        self.modify_produit_button.pack()

        # Ajouter un bouton pour supprimer un produit
        self.delete_produit_button = tk.Button(self.produit_frame, text="Supprimer un produit", command=self.delete_produit)
        self.delete_produit_button.pack()

    def add_categorie(self):
        # Créer une fenêtre de dialogue pour ajouter une nouvelle catégorie
        self.categorie_window = tk.Toplevel(self.master)
        self.categorie_window.title("Ajouter une categorie")
        self.categorie_window.geometry("400x200")

        # Ajouter une étiquette et un champ de saisie pour le nom de la catégorie
        self.categorie_nom_label = tk.Label(self.categorie_window, text="Nom de la categorie : ")
        self.categorie_nom_label.pack()

        self.categorie_nom_entry = tk.Entry(self.categorie_window)
        self.categorie_nom_entry.pack()

        # Ajouter un bouton pour ajouter la catégorie
        self.add_categorie_button = tk.Button(self.categorie_window, text="Ajouter", command=self.save_categorie)
        self.add_categorie_button.pack()
    

    def modify_produit(self):
        # Vérifier si un produit est sélectionné
        selected_produit = self.produits_listbox.curselection()
        if not selected_produit:
            return

        # Récupérer l'ID du produit sélectionné
        selected_produit_id = self.produit.read_all_produit()[selected_produit[0]][0]

        # Créer une fenêtre de dialogue pour modifier le produit
        self.produit_window = tk.Toplevel(self.master)
        self.produit_window.title("Modifier un produit")
        self.produit_window.geometry("400x300")

        # Récupérer les informations du produit
        produit_infos = self.produit.read_produit(selected_produit_id)

        # Ajouter une étiquette et un champ de saisie pour le nom du produit
        self.produit_nom_label = tk.Label(self.produit_window, text="Nom du produit : ")
        self.produit_nom_label.pack()

        self.nom_produit_entry = tk.Entry(self.produit_window)
        self.nom_produit_entry.insert(tk.END, produit_infos['nom'])
        self.nom_produit_entry.pack()


        # Ajouter une étiquette et un champ de saisie pour la description du produit
        self.produit_desc_label = tk.Label(self.produit_window, text="Description du produit : ")
        self.produit_desc_label.pack()

        self.produit_desc_entry = tk.Entry(self.produit_window)
        self.produit_desc_entry.insert(tk.END, produit_infos["description"])
        self.produit_desc_entry.pack()

        # Ajouter une étiquette et un champ de saisie pour le prix du produit
        self.produit_prix_label = tk.Label(self.produit_window, text="Prix du produit : ")
        self.produit_prix_label.pack()

        self.produit_prix_entry = tk.Entry(self.produit_window)
        self.produit_prix_entry.insert(tk.END, produit_infos["prix"])
        self.produit_prix_entry.pack()

        # Ajouter une étiquette et un champ de saisie pour la quantité du produit
        self.produit_quantite_label = tk.Label(self.produit_window, text="Quantité du produit : ")
        self.produit_quantite_label.pack()

        self.produit_quantite_entry = tk.Entry(self.produit_window)
        self.produit_quantite_entry.insert(tk.END, produit_infos["quantite"])
        self.produit_quantite_entry.pack()

        # Ajouter une étiquette et une liste déroulante pour la catégorie du produit
        self.produit_categorie_label = tk.Label(self.produit_window, text="Catégorie du produit : ")
        self.produit_categorie_label.pack()

        # Récupérer la liste de toutes les catégories
        categories = self.categorie.read_all_categorie()
        for cat in categories:
                self.categorie_id_dict[cat[1]] = cat[0]

        print(self.categorie_id_dict)

        self.produit_categorie_combobox = ttk.Combobox(self.produit_window, values=[cat[1] for cat in categories])
        self.produit_categorie_combobox.set(list(self.categorie_id_dict.keys())[list(self.categorie_id_dict.values()).index(int(produit_infos["id_categorie"]))])
        self.produit_categorie_combobox.pack()

        # Ajouter un bouton pour modifier le produit
        self.produit_modifier_button = tk.Button(self.produit_window, text="Modifier le produit", command=lambda: self.update_produit(selected_produit_id))
        self.produit_modifier_button.pack()

    def update_produit(self, produit_id):
        # Récupérer les nouvelles valeurs des champs de saisie
        nom = self.nom_produit_entry.get()
        description = self.produit_desc_entry.get()
        prix = self.produit_prix_entry.get()
        quantite = self.produit_quantite_entry.get()
        categorie = self.produit_categorie_combobox.get()

        # Récupérer l'ID de la catégorie à partir du dictionnaire
        categorie_id = self.categorie_id_dict[categorie]

        # Mettre à jour le produit dans la base de données
        self.produit.update_produit(produit_id, nom, description, prix, quantite, categorie_id)

         # Mettre à jour l'affichage de la liste des produits
        self.produits_listbox.delete(0, tk.END)
        liste_produits = self.produit.read_all_produit()
        for produit in liste_produits:
            categorie = self.categorie.read_categorie(produit[5])
            if categorie:
                self.produits_listbox.insert(tk.END, f"Nom: {produit[1]}, Description: {produit[2]}, Prix: {produit[3]}, Quantité: {produit[4]}, Catégorie: {categorie['nom']}")

        # Fermer la fenêtre de dialogue pour modifier le produit
        self.produit_window.destroy()

    def add_produit(self):
        # Créer une fenêtre de dialogue pour ajouter un nouveau produit
        self.produit_window = tk.Toplevel(self.master)
        self.produit_window.title("Ajouter un produit")
        self.produit_window.geometry("400x400")

        # Ajouter une étiquette et un champ de saisie pour le nom du produit
        self.produit_nom_label = tk.Label(self.produit_window, text="Nom du produit : ")
        self.produit_nom_label.pack()

        self.produit_nom_entry = tk.Entry(self.produit_window)
        self.produit_nom_entry.pack()

        # Ajouter une étiquette et un champ de saisie pour la description du produit
        self.produit_description_label = tk.Label(self.produit_window, text="Description : ")
        self.produit_description_label.pack()

        self.produit_description_entry = tk.Entry(self.produit_window)
        self.produit_description_entry.pack()

        # Ajouter une étiquette et un champ de saisie pour le prix du produit
        self.produit_prix_label = tk.Label(self.produit_window, text="Prix : ")
        self.produit_prix_label.pack()

        self.produit_prix_entry = tk.Entry(self.produit_window)
        self.produit_prix_entry.pack()

        # Ajouter une étiquette et un champ de saisie pour la quantité du produit
        self.produit_quantite_label = tk.Label(self.produit_window, text="Quantité : ")
        self.produit_quantite_label.pack()

        self.produit_quantite_entry = tk.Entry(self.produit_window)
        self.produit_quantite_entry.pack()

        # Ajouter une étiquette pour la liste des catégories
        self.produit_categorie_label = tk.Label(self.produit_window, text="Catégorie: ")
        self.produit_categorie_label.pack()

        # Ajouter une liste déroulante pour sélectionner la catégorie
        self.produit_categorie_combobox = ttk.Combobox(self.produit_window, state="readonly")
        self.produit_categorie_combobox.pack()

        # Ajouter un bouton pour ajouter le produit
        self.add_produit_button = tk.Button(self.produit_window, text="Ajouter", command=self.save_produit)
        self.add_produit_button.pack()

        # Récupérer la liste de toutes les catégories
        liste_categories = self.categorie.read_all_categorie()

        # Ajouter les catégories à la liste déroulante
        self.produit_categorie_combobox['values'] = [categorie[1] for categorie in liste_categories]

        # Sélectionner la première catégorie par défaut
        if len(liste_categories) > 0:
            self.produit_categorie_combobox.current(0)

    def save_categorie(self):
        # Enregistrer la nouvelle catégorie dans la base de données
        self.categorie.create_categorie(self.categorie_nom_entry.get())
        self.conn.close()

    def save_produit(self):
        nom = self.produit_nom_entry.get()
        description = self.produit_description_entry.get()
        prix = float(self.produit_prix_entry.get())
        quantite = int(self.produit_quantite_entry.get())
        categorie_id = self.produit_categorie_combobox.current() + 1
        categorie_nom = self.produit_categorie_combobox.get()

        # Ajouter le nouveau produit à la base de données
        self.produit.create_produit(nom, description, prix, quantite, categorie_id)

        # Mettre à jour l'affichage de la liste des produits
        self.produits_listbox.delete(0, tk.END)
        liste_produits = self.produit.read_all_produit()
        for produit in liste_produits:
            categorie = self.categorie.read_categorie(produit[5])
            if categorie:
                self.produits_listbox.insert(tk.END, f"Nom: {produit[1]}, Description: {produit[2]}, Prix: {produit[3]}, Quantité: {produit[4]}, Catégorie: {categorie['nom']}")

        # Fermer la fenêtre d'ajout de produit
        self.produit_window.destroy()

    def delete_produit(self):
        # Récupérer l'indice du produit sélectionné dans la zone d'affichage
        selection = self.produits_listbox.curselection()

        if len(selection) > 0:
            index = int(selection[0])
            produit = self.produits_listbox.get(index)
            produit_id = produit.split(",")[0].split(":")[1].strip() 
            self.produit.delete_produit(produit_id) 
            self.produits_listbox.delete(index) 
        else:
            messagebox.showwarning("Aucun produit sélectionné", "Veuillez sélectionner un produit à supprimer.")


    def on_select(self):
        # Récupérer le nom de la catégorie sélectionnée
        categorie_nom = self.categories_listbox.get(self.categories_listbox.curselection())

        # Effacer la liste des produits de la catégorie précédente
        self.produits_cat_listbox.delete(0, tk.END)

        # Récupérer la liste des produits de la catégorie sélectionnée
        produits = self.produit.read_produit_by_categorie(categorie_nom)

        # Ajouter les produits à la zone d'affichage
        for produit in produits:
            self.produits_cat_listbox.insert(tk.END, f"ID: {produit[0]}, Nom: {produit[1]}, Description: {produit[2]}, Prix: {produit[3]}, Quantité: {produit[4]}, Catégorie: {produit[5]}")

        # Ajouter la fonction de rappel à la méthode bind du widget categories_listbox
        self.categories_listbox.bind("<<ListboxSelect>>", self.on_select)



if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

