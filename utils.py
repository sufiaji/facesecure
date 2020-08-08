from sqlalchemy import Table, Column, String, Numeric, DateTime, Float, MetaData
import sqlalchemy as alchemy
# from pickle5 import pickle
from datetime import datetime
import base64
from PIL import Image
import numpy as np
import imutils
import math
import csv
import cv2
import os
import io

DB_NAME = 'facesecure'
KEY_CSV_DOWNLOAD_PATH = 'CSV_DOWNLOAD_PATH'
TABLE_USER = 'euser'
TABLE_ATTENDANCE = 'attendance'
TABLE_ENCODING = 'encoding'
TABLE_CONFIG = 'config'
OK_CODE = '_OK_'

def getEngine():        
        try:
            okcode, dbusername, dbpassword = getCredential()
            if okcode==OK_CODE:
                db_string = "postgres://" + dbusername + ":" + dbpassword + "@localhost:5432/" + DB_NAME 
                engine = alchemy.create_engine(db_string)
                with engine.connect():
                    return OK_CODE, engine
            else:
                return 'Error getting credential', ''     
        except Exception as ex:            
            return str(ex), ''
    
def getCredential():
    return OK_CODE, 'postgres', 'password'
    # dbusername = ''
    # dbpassword = ''
    # try:
    #     data_cred = pickle.load(open('credentials/cred.pickle','rb'))
    #     dbusername, dbpassword = data_cred['dbuser'], data_cred['dbpass']
    #     return OK_CODE, dbusername, dbpassword
    # except Exception as ex:
    #     return str(ex), dbusername, dbpassword

def saveCredentialPickle(dbuser, dbpass):
    """ Save DB user and password in pickle file in the same directory
    """
    if dbuser:
        if dbpass:
            data_cred = {'dbuser':dbuser, 'dbpass':dbpass}
            f = open('credentials/cred.pickle', 'wb')
            f.write(pickle.dumps(data_cred))
            f.close()

def getCSVPath():
    ok, engine = getEngine()
    if ok==OK_CODE:
        select_statement = "select value from public." + TABLE_CONFIG
        with engine.connect() as connection:
            sql_statement = alchemy.text(select_statement)
            result = connection.execute(sql_statement)
            for data in result:
                return data[0]
    else:
        return 'error get engine'

def modifyCSV(path, filename, user_id, created_at, created_on, status, loc):
    try:
        fullfilename = os.path.join(path, filename)
        is_exist = os.path.exists(fullfilename)
        if is_exist==False:
            with open(fullfilename, 'w') as textfile:
                if status=='P10':
                    status_new = '1'
                else:
                    status_new = '2'
                date_split = created_at.split('/')
                line = "[" + date_split[2] + "/" + date_split[1] + "/" + date_split[0] + "-" + created_on + "]" + user_id + "/" + loc + "/128/0/" + status_new + "\n"
                textfile.write(line)
        else:
            with open(fullfilename, 'a') as textfile:
                if status=='P10':
                    status_new = '1'
                else:
                    status_new = '2'
                date_split = created_at.split('/')
                line = "[" + date_split[2] + "/" + date_split[1] + "/" + date_split[0] + "-" + created_on + "]" + user_id + "/" + loc + "/128/0/" + status_new + "\n"
                textfile.write(line)
        return OK_CODE
    except Exception as ex:
        return str(ex)

def modifyCSV2(path, filename, user_id, created_at, created_on, status, loc):
    try:
        fullfilename = os.path.join(path, filename)
        is_exist = os.path.exists(fullfilename)
        if is_exist==False:
            with open(fullfilename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['NIK', 'Date', 'Time', 'Status', 'Location'])
                writer.writerow([user_id, created_at, created_on, status, loc])
        else:
            with open(fullfilename, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([user_id, created_at, created_on, status, loc])
        return OK_CODE
    except Exception as ex:
        return str(ex)

def saveCSV(user_id, created_at, created_on, status, loc):
    # userid, created_at, created_on, status, loc
    # path = getCSVPath()
    path = os.getcwd()
    if 'Error' in path:
        return 'error'
    else:
        date_str = (datetime.now()).strftime("%Y%m%d")
        filename = 'absensi' + date_str + '.log'
        ok = modifyCSV(path, filename, user_id, created_at, created_on, status, loc)
        return ok

def saveImageAttendance(path, userid, image_bitmap, created_at, created_on):
    with open(path + userid + '_' + created_at + ',' + created_on + '.jpg', 'wb') as ft:
        ft.write(image_bitmap)

def saveImageUser(path, userid, image_bitmap):
    try:
        with open(path + userid + '.jpg', 'wb') as ft:
            ft.write(image_bitmap)
            return OK_CODE
    except Exception as ex:
        return str(ex)

def saveImageUser2(path, userid, image_path):
    """ Function to save new user photo
        @param path: path for new photo want to save
        @param userId: NIK of user
        @param image_path: original path where user image was saved
    """
    filename = path + userid + '.jpg'
    img = cv2.imread(image_path)
    img = imutils.resize(img, width=400)
    cv2.imwrite(filename, img)

def isEncodingRecordExist():
    str_query = "SELECT id from public." + TABLE_ENCODING + " LIMIT 1"
    dret = {}
    ok, engine = getEngine()
    if ok==OK_CODE:
        with engine.connect() as connection:
            sql_query = alchemy.text(str_query)
            result = connection.execute(sql_query)
            result_as_list = result.fetchall()
            if len(result_as_list) == 0:
                return {'status':'ok', 'message':'false'}
            else:
                return {'status':'ok', 'message':'true'}
    else:
        return {'status':'error', 'message':ok}

def getEucledianDistance(encoding_array, threshold):
    """ Query with eucledian distance function to Postgres encoding table
    """
    le = len(encoding_array)
    
    str_query = "SELECT public." + TABLE_USER + ".user_id, public." + TABLE_USER + ".name, "
    for i, e in enumerate(encoding_array):
        str_query = str_query + "POW(public." + TABLE_ENCODING + ".d" + str(i+1) + "-(" + str(e) + "), 2)"
        if i == le-1:
            pass
        else:
            str_query = str_query + " + "     

    str_query = str_query + \
        " AS square_distance FROM public." + TABLE_ENCODING + \
        " INNER JOIN public." + TABLE_USER + " on public." + TABLE_ENCODING + ".user_id = public." + TABLE_USER + ".user_id" + \
        " ORDER BY square_distance ASC LIMIT 3"

    dret = {}
    ok, engine = getEngine()
    if ok==OK_CODE:
        with engine.connect() as connection:
            sql_query = alchemy.text(str_query)
            result = connection.execute(sql_query)
            result_as_list = result.fetchall()
            print(result_as_list)
            j = 0
            for i, e in enumerate(result_as_list):                
                distance = math.sqrt(e[2])                
                if distance <= float(threshold):
                    j=j+1
                    dret[str(j)] = {'user_id':e[0], 'name':e[1], 'distance':str(distance)}            
            return dret
    else:
        return {'Error':'get engine error'}

def saveNewUser(userId, userName):
    try:
        ok, engine = getEngine()
        if ok==OK_CODE:
            metadata = MetaData(engine)
            table_user = alchemy.Table(TABLE_USER, metadata, autoload=True, autoload_with=engine)
            with engine.connect() as connection:
                result = connection.execute(table_user.insert().values(user_id=userId, name=userName).returning(table_user.c.user_id, table_user.c.created_at, table_user.c.name))
                for user_id, created_at, name in result:
                    return OK_CODE, user_id, created_at, name
    except Exception as ex:
        return str(ex), '', '', ''

def removeUser(userId):
    try:
        ok, engine = getEngine()
        if ok==OK_CODE:
            del_st = "delete from public." + TABLE_USER + " where user_id='" + userId + "'"
            sql = alchemy.text(del_st)
            with engine.connect() as connection:
                connection.execute(sql)
                return OK_CODE
    except Exception as ex:
        return str(ex)

def saveNewEncoding(userId, encoding_array):
    try:
        ok, engine = getEngine()
        if ok==OK_CODE:
            stm_query = "INSERT INTO public." + TABLE_ENCODING + " (user_id,"
            stm_value = " VALUES ('" + userId + "',"
            le = len(encoding_array)
            
            for i,e in enumerate(encoding_array):
                stm_query = stm_query + "d" + str(i+1)
                stm_value = stm_value + str(e)
                if i==le-1:
                    stm_query = stm_query + ")"
                    stm_value = stm_value + ")"
                else:
                    stm_query = stm_query + ","
                    stm_value = stm_value + ","
            
            stm_all = stm_query + stm_value + " RETURNING id"
            sql_query = alchemy.text(stm_all)
            with engine.connect() as connection:
                result = connection.execute(sql_query)                   
                for id in result:  
                    dret = {'user_id': userId, 'encoding_id':id[0]}
                    return OK_CODE, dret
        else:
            return 'error get engine', 404            
    except Exception as ex:
        return str(ex), ''

def checkEncoding(userId):
    try:
        ok, engine = getEngine()
        if ok==OK_CODE:
            select_statement = "select id from public." + TABLE_ENCODING + " where user_id='" + userId + "'"
            sql_query = alchemy.text(select_statement)
            with engine.connect() as connection:
                result = connection.execute(sql_query)
                for res in result:
                    return res[0]
    except Exception as ex:
        return ''

def createPhotosDir():
    try:
        is_exist = os.path.exists('photos')
        if is_exist == False:
            os.mkdir('photos')
    except Exception as ex:
        return str(ex)
    return OK_CODE

def createAttendanceDir():
    try:
        is_exist = os.path.exists('attendances')
        if is_exist == False:
            os.mkdir('attendances')            
    except Exception as ex:
        return str(ex)
    return OK_CODE

def isFakePrint(clf, image_string64):
    pass
    # imagedata = base64.b64decode(image_string64)
    # image = Image.open(io.BytesIO(imagedata))
    # array_np = np.array(image)
    # frame = cv2.cvtColor(array_np, cv2.COLOR_RGB2BGR)
    # feature_vector = getEmbeddings(frame)
    # prediction = clf.predict_proba(feature_vector)
    # m = np.mean(prediction[0][1])
    # return m

def getEmbeddings(clf, img):
    pass
    # img_ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
    # img_luv = cv2.cvtColor(img, cv2.COLOR_BGR2LUV)
    # hist_ycrcb = calcHist(img_ycrcb)
    # hist_luv = calcHist(img_luv)
    # feature_vector = np.append(hist_ycrcb.ravel(), hist_luv.ravel())
    # return feature_vector.reshape(1, len(feature_vector))

def calcHist(img):
    pass
    # histogram = [0] * 3
    # for j in range(3):
    #     histr = cv2.calcHist([img], [j], None, [256], [0, 256])
    #     histr *= 255.0 / histr.max()
    #     histogram[j] = histr
    # return np.array(histogram)
    

    
