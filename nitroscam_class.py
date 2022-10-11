import re
import sqlite3

class NitroScam:
    def __init__(self):
        self.conn = sqlite3.connect('domains.db')
        c = self.conn.cursor()
        # fetch all the safe domains from the database
        self.safe_domains = [domain[0] for domain in c.execute("SELECT * FROM safe_domains").fetchall()]
        c.close()
    
    # function to check if the string contains a url and return the url
    def __contains_url__(self, message):
        return re.findall(r'(https?://\S+)', message)
    
    # Levenstien Distance
    # function to check the number of insertions/deletions have to be done to make two strings identical
    # lesser the number, more similar the strings are
    def __similarity__(self, domain):
        string2 = "discord"
        m = len(domain)
        n = 7
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(1, m + 1):
            for j in range(1, n+1):
                if domain[i-1] == string2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        return (m+n)-(2*dp[m][n])
    
    def checkNitroScam(self, message):
        url = self.__contains_url__(message)

        # check if the string contains a url
        if(len(url) == 0):
            return 0

        splitted = url[0].split("/")
        domain = splitted[2]

        # domain is safe
        if domain in self.safe_domains:
            return 0

        domainName = domain.split(".")[0]

        if(len(domainName)>6):
            sim = self.__similarity__(domainName[:7])
        else:
            sim = self.__similarity__(domainName)

        if sim < 5:
            return 1
        # if message contains a url and words discord and nitro, then it could be a scam
        message = message.split()
        if "discord" in message and "nitro" in message:
            return 2
    
    def addSafeDomain(self, domain):
        if domain not in self.safe_domains:
            self.safe_domains.append(domain)
            c = self.conn.cursor()
            c.execute("INSERT INTO safe_domains VALUES (?)", (domain,))
            self.conn.commit()
            c.close()
    
    def removeSafeDomain(self, domain):
        if domain in self.safe_domains:    
            self.safe_domains.remove(domain)
            c = self.conn.cursor()
            c.execute("DELETE FROM safe_domains WHERE domain=?", (domain,))
            self.conn.commit()
            c.close()
