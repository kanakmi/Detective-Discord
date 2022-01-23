import re
import sqlite3

conn = sqlite3.connect('users.db')

c = conn.cursor()

try:
    c.execute("""CREATE TABLE warnings (
                    id text PRIMARY KEY,
                    warnings int
    )""")
    conn.commit()

except:
    print("Table already exists")

def insert_warning(id):
    try:
        c.execute("INSERT INTO warnings VALUES (?, 1)", (id,))
    except:
        c.execute("UPDATE warnings SET warnings = warnings + 1 WHERE id = ?", (id,))
        c.execute("SELECT warnings FROM warnings WHERE id = ?", (id,))
        if c.fetchone()[0] >= 3:
            print("User has been banned")

    conn.commit()

def delete_warning(id):
    try:
        c.execute("DELETE FROM warnings WHERE id = ?", (id,))
        print("Warnings for user {} have been deleted".format(id))
    except:
        print("User {} has no warnings".format(id))

    conn.commit()

string = '''@everyone
            Discord is giving away nitro!
            https://dissord.gift/xGCs7cGt2sdFOf84'''

# function to check if the string contains a url and return the url
def contains_url(string):
    return re.findall(r'(https?://\S+)', string)

# function to check the number of insertions/deletions have to be done to make two strings identical
# lesser the number, more similar the strings are
def similarity(string1):
    string2 = "discord"
    m = len(string1)
    n = 7
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n+1):
            if string1[i-1] == string2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return (m+n)-(2*dp[m][n])

def main(string):
    url = contains_url(string)

    if(len(url) > 0):
        splitted = url[0].split("/")
        domain = splitted[2]

        if(domain == "discord.gift" or domain == "discord.gg"):
            return False

        domainName = domain.split(".")[0]

        if(len(domainName)>6):
            sim = similarity(domainName[:7])
        else:
            sim = similarity(domainName)

        if sim < 4:
            return True
        else:
            trigger_words = ["nitro", "discord"]
            if any(word in string for word in trigger_words):
                return True
            else:
                return False
    else:
        return False

if main(string):
    print("Nitro scam detected")
    insert_warning("123456789")
    c.execute("SELECT warnings FROM warnings WHERE id = ?", ("123456789",))
    print(c.fetchone()[0])
    conn.commit()
    delete_warning("123456789")
    conn.commit()
