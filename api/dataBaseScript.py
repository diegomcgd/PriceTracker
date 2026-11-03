import sqlite3

conexion = sqlite3.connect("productsHistory.db")
cur = conexion.cursor()

# Activate foreign keys
cur.execute("PRAGMA foreign_keys = ON;")

cur.execute("DROP TABLE IF EXISTS price;")
cur.execute("DROP TABLE IF EXISTS product;")

cur.execute("""
    CREATE TABLE IF NOT EXISTS product (
        name TEXT PRIMARY KEY,
        url TEXT,
        description TEXT
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS price (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product TEXT NOT NULL,
        price REAL NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY (product) REFERENCES product(name) ON DELETE CASCADE
    )
""")

conexion.commit()
print("Data base created correctly")
