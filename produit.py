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

    def read_all_produit(self):
        sql = "SELECT * FROM produit"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        save_produits = []
        try:
            for produit in result:
                save_produits.append(produit)
        except IndexError:
            return None

        return save_produits

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