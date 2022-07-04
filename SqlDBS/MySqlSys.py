import pymysql as mysql

class sqldbs(object) :

    def __init__(self, host = "localhost", password=  "", user = "root",charset = "utf8") :

        self.sql = mysql.connect(host = host, password = password, user = user, charset = charset)

        dataBaseInit(self, 'movieComments')

    def executeSql(self, cmd) :
        try:
            cursor = self.sql.cursor()

            cursor.execute(cmd)

            results = cursor.fetchall()

            return results

        except Exception as e:

            print(e)

            self.sql.rollback()

    def executeManySql(self, cmd, data) :
        try:
            cursor = self.sql.cursor()

            cursor.executemany(cmd, data)

            self.sql.commit()

            results = cursor.fetchall()

            return results

        except Exception as e:

            print(e)

            self.sql.rollback()

def dataBaseInit(SQLDBS, name) :

    exist = isDataBaseExist(SQLDBS, name)

    if(not exist) : SQLDBS.executeSql("create database " + name + ";")

    SQLDBS.executeSql("use " + name + ";")

    if(not exist):

        SQLDBS.executeSql("""
            CREATE TABLE commentsh (
            id INT auto_increment PRIMARY KEY , 
            rating INT NOT NULL, 
            text TEXT NOT NULL
            )
            """)

        SQLDBS.executeSql("""
                    CREATE TABLE commentsl (
                    id INT auto_increment PRIMARY KEY , 
                    rating INT NOT NULL, 
                    text TEXT NOT NULL
                    )
                    """)

        SQLDBS.executeSql("""
                            CREATE TABLE commentsm (
                            id INT auto_increment PRIMARY KEY , 
                            rating INT NOT NULL, 
                            text TEXT NOT NULL
                            )
                            """)


def isDataBaseExist(SQLDBS, name) :

    count = len(SQLDBS.executeSql("show databases like '" + name + "';"))

    return count != 0

def saveComments(SQLDBS, comments, feedback) :

    if(feedback == 1) :
        SQLDBS.executeManySql("""
            INSERT INTO commentsh(rating, text)
            VALUES(%s, %s)
        """, [(i['rating'], i['text']) for i in comments])

    elif (feedback == -1):
        SQLDBS.executeManySql("""
                INSERT INTO commentsl(rating, text)
                VALUES(%s, %s)
            """, [(i['rating'], i['text']) for i in comments])

    elif (feedback == 0):
        SQLDBS.executeManySql("""
                INSERT INTO commentsm(rating, text)
                VALUES(%s, %s)
            """, [(i['rating'], i['text']) for i in comments])

def loadComments(SQLDBS, feedback) :

    if(feedback == 1) :

        resulth = SQLDBS.executeSql('SELECT * FROM commentsm WHERE rating >= 30;')

        return resulth

    elif (feedback == -1):
        resultl = SQLDBS.executeSql('SELECT * FROM commentsm WHERE rating <= 30;')

        return resultl

    elif (feedback == 0):
        resultm = SQLDBS.executeSql('SELECT * FROM commentsm;')

        return resultm

def searchComments(SQLDBS, id) :

    if(len(id) == 0) : return []

    searchText = 'SELECT * FROM commentsm where id in({0}) order by field(id,{0}) limit 0,{1} ;'.format(str(id)[1:-1], len(id))

    result = SQLDBS.executeSql(searchText)

    return result





