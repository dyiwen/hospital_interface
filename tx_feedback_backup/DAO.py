from config import config


class Mysql(object):
    def __init__(self):
        import MySQLdb    
        try:
            connjson = {}
            connjson["host"] = config.TXDB.ip
            connjson["port"] = int(config.TXDB.port)
            connjson["user"] = config.TXDB.user
            connjson["passwd"] =  config.TXDB.pwd          
            connjson["db"] = config.TXDB.database
            connjson["charset"] = "utf8"
            self._conn = MySQLdb.connect(**connjson)
            self._conn.autocommit(1)
            self._cursor = self._conn.cursor()
        except:
            print("Mysql connect error")
            
    def execute(self, sql):
        
        return self._cursor.execute(sql),self._cursor.fetchall()
    
    def commit(self):
        self._conn.commit()    
        
    def db_close(self):
        self._cursor.close
        self._conn.close()  
