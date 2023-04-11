class Categorie: 
    def __init__(self, conn) -> None:
        self.conn = conn
        self.cursor = conn.cursor()

    def create_categorie(self, nom):
        sql = """
            INSERT INTO categorie (nom)
            SELECT %s
            WHERE NOT EXISTS (
                SELECT * FROM categorie 
                WHERE nom = %s
            )
        """
        val = (nom, nom)
        self.cursor.execute(sql, val)
        self.conn.commit()
        return self.cursor.lastrowid

    def read_categorie(self, id):
        sql = "SELECT * FROM categorie WHERE id = %s"
        val = (id,)
        self.cursor.execute(sql, val)
        result = self.cursor.fetchone()
        if result is None:
            return None
        else:
            return {'id': result[0], 'nom': result[1]}
    
    def read_categorie_by_id(self, categorie_id):
        return self.read_categorie(categorie_id)

    
    # def read_all_categorie(self):
    #     sql = "SELECT * FROM categorie"
    #     self.cursor.execute(sql)
    #     result = self.cursor.fetchall()
    #     save_categories = []
    #     if result is None:
    #         return None
    #     else:
    #         for categorie in result:
    #             save_categories.append(f"Id de la catégorie: {categorie[0]}, Nom de la catégorie: {categorie[1]}")
    #         return '\n'.join(save_categories)
    
    def read_all_categorie(self):
        sql = "SELECT * FROM categorie"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        save_produits = []
        try:
            for produit in result:
                save_produits.append(produit)
        except IndexError:
            return None

        return save_produits
    
    # dans la classe Categorie
    def read_all_categories_modify(self):
        sql = "SELECT * FROM categorie"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        categories = []
        for row in result:
            categories.append(row[1])
        return categories


        
    def update_categorie(self, id, nom):
        sql = "UPDATE categorie SET nom = %s WHERE id = %s"
        val = (nom, id)
        self.cursor.execute(sql, val)
        self.conn.commit()
        return True
    
    def delete_categorie(self, id):
        sql = "DELETE FROM categorie WHERE id = %s"
        val = (id,)
        self.cursor.execute(sql, val)
        self.conn.commit()
        return self.cursor.rowcount