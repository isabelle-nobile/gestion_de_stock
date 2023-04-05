import tkinter as tk
from tkinter import ttk
from categories import Categorie
from produit import Produit
from connexion import conn

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Gestion de stocks")
        self.pack()
        self.create_widgets()
        self.conn = conn()
        self.produit = Produit(self.conn)
        self.categorie = Categorie(self.conn)

    def create_widgets(self):
        # Créer un cadre pour la classe Categorie
        self.categorie_frame = tk.LabelFrame(self, text="Categories")
        self.categorie_frame.pack(side="left", padx=10, pady=10)

        # Ajouter une étiquette pour afficher toutes les catégories
        self.categories_label = tk.Label(self.categorie_frame, text="Toutes les categories :")
        self.categories_label.pack()

        # Ajouter un bouton pour ajouter une nouvelle catégorie
        self.add_categorie_button = tk.Button(self.categorie_frame, text="Ajouter une categorie", command=self.add_categorie)
        self.add_categorie_button.pack()

        # Ajouter une étiquette pour afficher les produits d'une catégorie
        self.produits_label = tk.Label(self.categorie_frame, text="Produits dans cette categorie :")
        self.produits_label.pack()

        # Créer un cadre pour la classe Produit
        self.produit_frame = tk.LabelFrame(self, text="Produits")
        self.produit_frame.pack(side="left", padx=10, pady=10)

        # Ajouter une étiquette pour afficher tous les produits
        self.produits_label = tk.Label(self.produit_frame, text="Tous les produits :")
        self.produits_label.pack()
        # Créer une zone d'affichage pour les produits
        self.produits_listbox = tk.Listbox(self)
        self.produits_listbox.pack()

        # Récupérer la liste de tous les produits
        liste_produits = self.produit.read_all_produit()

        # Ajouter les produits à la zone d'affichage
        for p in liste_produits:
            self.produits_listbox.insert(tk.END, p.nom)
        
        # Ajouter un bouton pour ajouter un nouveau produit
        self.add_produit_button = tk.Button(self.produit_frame, text="Ajouter un produit", command=self.add_produit)
        self.add_produit_button.pack()

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
    
    def add_produit(self):
        # Créer une fenêtre de dialogue pour ajouter un nouveau produit
        self.produit_window = tk.Toplevel(self.master)
        self.produit_window.title("Ajouter un produit")
        self.produit_window.geometry("400x200")

        # Ajouter une étiquette et un champ de saisie pour le nom du produit
        self.produit_nom_label = tk.Label(self.produit_window, text="Nom du produit : ")
        self.produit_nom_label.pack()

        self.produit_nom_entry = tk.Entry(self.produit_window)
        self.produit_nom_entry.pack()

        # Ajouter un bouton pour ajouter la catégorie
        self.add_produit_button = tk.Button(self.produit_window, text="Ajouter", command=self.save_produit)
        self.add_produit_button.pack()

    def save_categorie(self):
        # Enregistrer la nouvelle catégorie dans la base de données
        self.categorie.create_categorie(self.categorie_nom_entry.get())
        conn.close()

    def save_produit(self):
        # Enregistrer la nouvelle catégorie dans la base de données
        self.produit.creatproduit(self.produit_nom_entry.get())
        conn.close()
    
    def delete_produit(self):
        # Créer une fenêtre de dialogue pour supprimer un produit
        self.categorie_window = tk.Toplevel(self.master)
        self.categorie_window.title("Supprimer un produit")
        self.categorie_window.geometry("400x200")

        # Ajouter une étiquette et un champ de saisie pour le nom du produit
        self.categorie_nom_label = tk.Label(self.categorie_window, text=" Supprimer le produit  : ")
        self.categorie_nom_label.pack()

        self.categorie_nom_entry = tk.Entry(self.categorie_window)
        self.categorie_nom_entry.pack()

        # Ajouter un bouton pour supprimer le produit
        self.add_categorie_button = tk.Button(self.categorie_window, text="Supprimer", command=self.save_produit)
        self.add_categorie_button.pack()
    


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()