import pymysql
import numpy as np

def DB_AI_store (instanceID ,coor):
    # 資料庫設定
    db_settings = {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "password": "fghfgh0904",
        "db": "ai_coordinate",
    }
    #coor_srt = str(coor)
    try:
        # 建立Connection物件
        conn   = pymysql.connect(**db_settings)
        cursor = conn.cursor()
        
        for i in range(len(instanceID)):
            coor_list = []
            for j in range(len(coor[i])):
                coor_t = coor[i][j].tolist()
                coor_list.append(coor_t)
                
            sql = (
            "INSERT INTO coordinate (SOPinstanceID, coor) VALUES ('"+instanceID[i]+"', '"+str(coor_list)+"') "
            "ON DUPLICATE KEY UPDATE coor = '"+str(coor_list)+"'"
            )
            cursor.execute(sql)
            
        conn.commit()

        print("connect finish.")
    except Exception as ex:
        print(ex)
    
    return "123"

def DB_AI_get (instanceID):

    db_settings = {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "password": "fghfgh0904",
        "db": "ai_coordinate",
    }
    
    try:
        conn   = pymysql.connect(**db_settings)
        cursor = conn.cursor()
        command = "SELECT coor FROM coordinate where SOPinstanceID='"+instanceID+"'"
        cursor.execute(command)
        result = cursor.fetchall()
        print("result is ",result[0][0])
        print("result type is ",type(result[0][0]))
        print("result eval is ",type(eval(result[0][0])))
        print("result eval is ",len(eval(result[0][0])))
        conn.commit()
        print("connect finish.")
        result = eval(result[0][0])
        
    except Exception as ex:
        result = []
        
    return result
#myNumpyArray = np.array([[7,4],[5,2]])
#DB_AI_0('1.2.840.113619.2.359.3.296505355.597.1531427826.947.3153921',myNumpyArray)