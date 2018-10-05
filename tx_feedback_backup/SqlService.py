import DAO
from config import config


def ct_feedback():
    db = DAO.Mysql()
    sql = "select pid,feedback_type from {}.CT_feedback".format(config.TXDB.database)
    
    i,result = db.execute(sql)
    db.db_close()
       
    return result

