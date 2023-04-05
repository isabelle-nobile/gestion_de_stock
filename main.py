# from connexion import conn
# from categories import Categorie
# from produit import Produit
# from tkinter import Tkinter

# # create a connection
# conn = conn()

# # create a database
# cursor = conn.cursor()
# cursor.execute("CREATE DATABASE IF NOT EXISTS boutique")

# # create the categorie table
# cursor.execute("USE boutique")
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS categorie (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     nom VARCHAR(255)
# )
# """)

# # insert some categories
# categorie = Categorie(conn)
# categorie.create_categorie("Vêtements")
# categorie.create_categorie("Chaussure")

# # create the produit table
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS produit (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     nom VARCHAR(255),
#     description TEXT,
#     prix INT,
#     quantite INT,
#     id_categorie INT,
#     FOREIGN KEY (id_categorie) REFERENCES categorie(id)
# )
# """)

# # insert some products
# produit = Produit(conn)
# produit.create_produit("Chemise", "Chemise en coton", 50, 10, 1)
# produit.create_produit("Pantalon", "Pantalon en jean", 70, 5, 1)
# produit.create_produit("Chaussures de sport", "Chaussures de sport légères", 80, 20, 2)
# produit.create_produit("Chaussures de ville", "Chaussures de ville élégantes", 100, 15, 2)


#TABLEAU de bord : 
# categorie.delete_categorie(7)
# print(categorie.read_categorie(1))
# print(categorie.read_all_categorie())
# print(produit.read_all_produit())

# # close the connection
# conn.close()


from interface import Application


Application()

