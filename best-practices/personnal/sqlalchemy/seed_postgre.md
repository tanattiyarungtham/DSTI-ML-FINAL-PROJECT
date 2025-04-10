**📘 seed_postgres.py — Seeding Your PostgreSQL Reference Tables with SQLAlchemy**

  

**📦 Fichier : back_end/database/seed_postgres.py**

---

**🔁 1. Importations et dépendances**

```
from back_end.database.connect import get_db, engine
```

• 🔁 **Import de get_db et engine** depuis le fichier connect.py

• engine: C’est l’objet central de SQLAlchemy pour établir une **connexion bas niveau** avec la base de données.

• get_db: Une fonction génératrice qui **fournit une session (SessionLocal)** — pratique dans FastAPI ou les scripts réutilisables.

```
from sqlalchemy.orm import Session
```

• 📚 **Import du type Session**

• Utilisé ici pour **annoter** (typer) les arguments de fonction — bonne pratique pour l’autocomplétion, la lisibilité et les vérifications statiques.

```
from sqlalchemy import text
```

• 📜 text() permet d’écrire des **requêtes SQL brutes** mais sécurisées (avec protection contre l’injection SQL).

• Ex. : text("SELECT * FROM table WHERE label = :val")

---

**🧩 2. Données de référence à insérer**

```
GENDERS = ["male", "female", "other"]
DIET_TYPES = ["vegetarian", "vegan", "keto", "none"]
FITNESS_LEVELS = ["beginner", "intermediate", "advanced"]
GOALS = ["Lose weight", "Gain muscle", "Improve endurance", "Tone muscles"]
```

Ces listes contiennent les **valeurs d’enumération** que l’on souhaite insérer **une seule fois** dans des tables de référence (genders, goals, etc.).

---

**🔄 3. Fonction d’insertion unique**

```
def insert_unique_values(db: Session, table: str, values: list[str], label_col="label"):
```

• 💡 Fonction générique pour **insérer des données dans n’importe quelle table de référence** si elles n’existent pas encore.

• 🔤 **Arguments :**

• db: Une instance SQLAlchemy Session (connexion active).

• table: Le nom de la table cible (str).

• values: Une liste de chaînes à insérer.

• label_col: Le nom de la colonne de texte (par défaut "label").

---

```
    for value in values:
```

• Boucle sur chaque valeur dans la liste (ex. "male", "female"…).

```
        exists = db.execute(
            text(f"SELECT 1 FROM {table} WHERE {label_col} = :val"),
            {"val": value}
        ).fetchone()
```

• ⚠️ Vérifie si la valeur existe déjà :

• text(...): Requête SQL brute paramétrée (anti-injection).

• :val est un **paramètre nommé** remplacé par value.

• fetchone() récupère un seul résultat, ou None.

---

```
        if not exists:
            db.execute(
                text(f"INSERT INTO {table} ({label_col}) VALUES (:val)"),
                {"val": value}
            )
```

• Si aucune ligne n’est trouvée, on insère la nouvelle valeur dans la table concernée.

---

**🚀 4. Fonction principale run_seed()**

```
def run_seed():
    """
    Seeds PostgreSQL with reference data for genders, diet types, fitness levels, and goals.
    """
    print("🌱 Seeding PostgreSQL reference tables...")
```

• Affiche une ligne de log pour indiquer que le **peuplement des tables est en cours**.

---

```
    with engine.begin() as connection:
```

• Ouvre une **transaction** avec le moteur SQLAlchemy :

• engine.begin() garantit que toutes les requêtes dans ce bloc seront **validées ensemble** (COMMIT) ou annulées si erreur (ROLLBACK).

---

```
        db = Session(bind=connection)
```

• Crée une session SQLAlchemy liée à la connexion ouverte.

• Cette db est passée à la fonction insert_unique_values.

---

```
        insert_unique_values(db, "genders", GENDERS)
        insert_unique_values(db, "diet_types", DIET_TYPES)
        insert_unique_values(db, "fitness_levels", FITNESS_LEVELS)
        insert_unique_values(db, "goals", GOALS, label_col="label")
```

• Appelle la fonction générique pour chaque table.

• label_col="label" est explicite pour goals car la colonne d’ID s’appelle ici goal_id, mais la **colonne de texte** reste "label".

---

```
    print("✅ Seeding complete.")
```

• Confirmation dans la console que tout a été inséré avec succès.

---

**🚨 5. Point d’entrée du script**

```
if __name__ == "__main__":
    run_seed()
```

• Si le fichier est exécuté directement, on **lance le peuplement** de la base (run_seed()).

• Cela permet de l’utiliser aussi bien en script CLI qu’en module importable.

---

**✅ Résumé pédagogique**

|**Élément**|**Rôle**|
|---|---|
|Session(bind=connection)|Crée une session liée à une transaction.|
|text(...)|Écrit une requête SQL sécurisée (paramétrée).|
|fetchone()|Récupère une seule ligne si elle existe.|
|insert_unique_values(...)|Remplit une table de référence de manière idempotente.|
|run_seed()|Lance le remplissage des tables avec des valeurs de base.|

  

---

Souhaites-tu que je t’écrive un fichier .md formaté avec tout ça dedans ?

Tu veux aussi qu’on ajoute un modèle ORM (avec Base) ou que je t’explique la partie models.py ensuite ?