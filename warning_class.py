import sqlite3

class Warning:
    def __init__(self):
        self.conn = sqlite3.connect('users.db')

        c = self.conn.cursor()

        try:
            c.execute("""
                        CREATE TABLE warnings (
                            id text PRIMARY KEY,
                            warnings int
                        )
                    """)
            self.conn.commit()

        except:
            print("Warnings Table already exists")

        c.close()

    def insertWarning(self, id):
        c = self.conn.cursor()
        try:
            c.execute("INSERT INTO warnings VALUES (?, 1)", (id,))
            self.conn.commit()
            c.close()
            return 1
        except:
            c.execute("UPDATE warnings SET warnings = warnings + 1 WHERE id = ?", (id,))
            c.execute("SELECT warnings FROM warnings WHERE id = ?", (id,))
            warnings = c.fetchone()[0]
            self.conn.commit()
            c.close()
            return warnings
    
    def deleteWarning(self, id):
        try:
            c = self.conn.cursor()
            c.execute("DELETE FROM warnings WHERE id = ?", (id,))
            self.conn.commit()
            c.close()
            return True
        except:
            return False
