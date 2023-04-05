class Produit: 
    def __init__(self, conn) -> None:
        self.conn = conn
        self.cursor = conn.cursor()

    def create_produit(self, nom, description, prix, quantite, id_categorie):
        sql = "INSERT IGNORE INTO produit (nom, description, prix, quantite, id_categorie) VALUES (%s, %s, %s, %s, %s)"
        val = (nom, description, prix, quantite, id_categorie)
        self.cursor.execute(sql, val)
        self.conn.commit()
        return self.cursor.lastrowid

    def read_produit(self, id):
        sql = "SELECT * FROM produit WHERE id = %s"
        val = (id,)
        self.cursor.execute(sql, val)
        result = self.cursor.fetchone()
        if result is None:
            return None
        else:
            return {'id': result[0], 'nom': result[1], 'description': result[2], 'prix': result[3]}
    
    def read_all_produit(self):
        sql = "SELECT * FROM produit"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        save_produits = []
        if result is None:
            return None
        else:
            for produit in result:
                save_produits.append({'id': produit[0], 'nom': produit[1], 'description': produit[2], 'prix': produit[3], 'quantite': produit[4], 'id_categorie': produit[5]})

            # convertir la liste de dictionnaires en une chaîne de caractères
            save_produits_str = ""
            for produit in save_produits:
                produit_str = ""
                for key, value in produit.items():
                    produit_str += str(key) + ": " + str(value) + ", "
                produit_str = produit_str[:-2] # supprimer la dernière virgule et l'espace
                save_produits_str += produit_str + "\n"

            return save_produits_str


    def update_produit(self, id, nom=None, description=None, prix=None, quantite=None, id_categorie=None):
        sql = "UPDATE produit SET"
        val = []
        if nom is not None:
            sql += " nom = %s,"
            val.append(nom)
        if description is not None:
            sql += " description = %s,"
            val.append(description)
        if prix is not None:
            sql += " prix = %s,"
            val.append(prix)
        if quantite is not None:
            sql += " quantite = %s,"
            val.append(quantite)
        if id_categorie is not None:
            sql += " id_categorie = %s,"
            val.append(id_categorie)
        sql = sql.rstrip(",") + " WHERE id = %s"
        val.append(id)
        self.cursor.execute(sql, tuple(val))
        self.conn.commit()
        return True
 
    def delete_produit(self, id):
        sql = "DELETE FROM produit WHERE id = %s"
        val = (id,)
        self.cursor.execute(sql, val)
        self.conn.commit()
        return self.cursor