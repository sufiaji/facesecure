# List of API to get face distance, get and set attendance, get and set user
# Pradhono R Aji @ merkaba.co.id
# 24/05/2020

from sqlalchemy import Table, Column, String, Numeric, DateTime, Float, MetaData
from flask_restful import Resource, Api, reqparse
from flask import Flask, request
from base64 import decodestring
from datetime import datetime
import sqlalchemy as alchemy
# from pickle5 import pickle
import face_recognition
from PIL import Image
import numpy as np
import pickle as pk
import utils
import base64, os
import math
import io

app = Flask(__name__)
api = Api(app)

DEBUG = True
OUT_OF_RANGE = '999999'
TABLE_USER = utils.TABLE_USER
TABLE_ENCODING = utils.TABLE_ENCODING
TABLE_ATTENDANCE = utils.TABLE_ATTENDANCE
TABLE_CONFIG = utils.TABLE_CONFIG
# parser
parser = reqparse.RequestParser()
# clf = pk.load(open('liveness_models/pickle_print.pickle','rb'))
# d = clf

def printDebug(msg):
    if DEBUG:
        print(msg)

class Liveness(Resource):
    def get(self):
        # parser.add_argument('thumb')
        # args = parser.parse_args()
        # thumb = args['thumb']
        # ret = utils.isFakePrint(clf, thumb)
        # dret = {'score':str(ret)}
        dret = {'score':str(999)}
        return dret, 200

class Recognize(Resource):
    def get(self):
        """ get vector distance between a face and faces stored in pickle
            @param thumb: cropped & aligned face image, in base64 String
            @param threshold: threshold distance
            @return dict: 2 level dict, level1: no, level2: name & distance
        """ 
        try:
            # check encoding table
            ret = utils.isEncodingRecordExist()
            if ret['status']=='ok' and ret['message']=='false':
                return 'empty encoding', 200
            elif ret['status']=='error':
                return ret, 404
            # get argument
            parser.add_argument('thumb')
            parser.add_argument('threshold') 
            args = parser.parse_args()
            thumb = args['thumb']
            threshold = args['threshold']
            if thumb==None or threshold==None:
                return 'empty argument', 404
            # convert arg to image
            imagedata = base64.b64decode(thumb)
            image = Image.open(io.BytesIO(imagedata))
            array_np = np.array(image)
            ####
            # import cv2
            # cv2.imshow('Thumb', cv2.cvtColor(array_np, cv2.COLOR_RGB2BGR))
            # cv2.waitKey(0)
            #### 
            # generate encoding for incoming image         
            h = array_np.shape[0]-1
            w = array_np.shape[1]-1
            encoding = face_recognition.face_encodings(array_np, known_face_locations=[[0,w-1,h-1,0]])[0]
            # compare with existing encodings
            return_distance = utils.getEucledianDistance(encoding_array=encoding, threshold=threshold)
            printDebug(return_distance)
            return return_distance, 200
        except Exception as ex:
            printDebug(ex)
            return str(ex), 404

class Attendance(Resource):
    def get(self):
        """ get last attendance of specific user
            @param user_id: NIK of user 
            @return attendance_id: id of attendence record
            @return user_id: ID of user (same with param)
            @return created_at: last attendance creation record
            @return status: IN/OUT
            @return name: name of user
        """        
        parser.add_argument('user_id')
        args = parser.parse_args()
        userid = args['user_id']
        if userid is None:
            return 'error empty argument', 404
        try:
            select_statement = "select public." + TABLE_ATTENDANCE + ".id," \
                + " public." + TABLE_ATTENDANCE + ".user_id," \
                + " public." + TABLE_ATTENDANCE + ".created_at," \
                + " public." + TABLE_ATTENDANCE + ".created_on," \
                + " public." + TABLE_ATTENDANCE + ".status," \
                + " public." + TABLE_USER + ".name" \
                + " from public." + TABLE_ATTENDANCE \
                + " inner join public." + TABLE_USER + " on public." + TABLE_ATTENDANCE + ".user_id=public." + TABLE_USER + ".user_id" \
                + " where public." + TABLE_ATTENDANCE + ".user_id='" + userid + "' order by created_at desc, created_on desc limit 1"
            ok, engine = utils.getEngine()
            if ok==utils.OK_CODE:
                with engine.connect() as connection:
                    sql_query = alchemy.text(select_statement)
                    result = connection.execute(sql_query)
                    result_as_list = result.fetchall()
                    if not result_as_list:
                        return 'NA', 200
                    for data in result_as_list:
                        # id, user_id, created_at, status, name
                        return {'attendance_id':data[0],  
                            'user_id':data[1], 
                            'created_at':(data[2]).strftime('%d/%m/%Y'), 
                            'created_on':(data[3]).strftime('%H:%M:%S'), 
                            'status':data[4], 
                            'name':data[5]}, 200
            else:
                return 'error get engine', 404
        except Exception as ex:
            printDebug(ex)
            return str(ex), 404

    def post(self):
        """ post attendance of specific user
            This time, we save it into Postgres and respective CSV file
            @param user_id: NIK of user who do clock in/out
            @param status: P10(in) or P20(out)
            @param location: 2 digit string location
            @param thumb: image of one doing attendance, encoded in base64 string
            @param created_at: date of attendance, string
            @param created_on: time of attendance, string
        """
        parser.add_argument("user_id")
        parser.add_argument("status")
        parser.add_argument("location")
        parser.add_argument("thumb")
        parser.add_argument("created_at")
        parser.add_argument("created_on")
        args = parser.parse_args()
        userId = args["user_id"]
        status = args["status"]
        loc = args["location"]
        thumb = args["thumb"] # base64 encoded String
        createdAt = args["created_at"]        
        createdOn = args["created_on"]        
        if userId is None or status is None or thumb is None or loc is None or createdOn is None or createdAt is None:
            return 'error empty argument', 404
        try:
            ok = utils.createAttendanceDir()
            if ok!=utils.OK_CODE:
                return 'cannot create attendances dir', 404
            ok, engine = utils.getEngine()
            if ok==utils.OK_CODE:
                createdAt = datetime.strptime(createdAt, "%d-%m-%Y")
                createdOn = datetime.strptime(createdOn, "%H:%M:%S.%f")
                metadata= MetaData(engine)
                table_attendance = alchemy.Table(TABLE_ATTENDANCE, metadata, autoload=True, autoload_with=engine)
                with engine.connect() as connection:
                    result = connection. \
                        execute(table_attendance.insert(). \
                            values(user_id=userId, status=status, location=loc, created_at=createdAt, created_on=createdOn). \
                                returning(table_attendance.c.id, table_attendance.c.created_at, table_attendance.c.created_on))
                    for id, created_at, created_on in result:
                        stm = "select user_id, name from public.euser where user_id='" + userId + "'"
                        sql_query = alchemy.text(stm)
                        result2 = connection.execute(sql_query)
                        result_as_list = result2.fetchall()
                        for data in result_as_list:
                            utils.saveCSV(userId, created_at.strftime('%d/%m/%Y'), created_on.strftime('%H:%M:%S'), status, loc)
                            thumb_bitmap = base64.b64decode(thumb)
                            utils.saveImageAttendance('attendances/', userId, thumb_bitmap, created_at.strftime('%d-%m-%Y'), created_on.strftime('%H-%M-%S'))                            
                            return {'attendance_id':id, 'user_id':userId, 'name':data[1], 'status':status}
            else:
                return 'error get engine', 404
        except Exception as ex:
            printDebug(ex)
            return str(ex), 404

class DataAttendance(Resource):
    def post(self):
        """ Save mass attendance into table Postgres
            @param attendances: list of attendances in json string 
        """
        import json
        try:
            if utils.createAttendanceDir()!=utils.OK_CODE:
                return 'cannot create attendance dir', 404
            parser.add_argument('attendances')
            args = parser.parse_args()
            attendances_json = args['attendances']
            if attendances_json is None:
                return 'error empty argument', 404
            attendances = json.loads(attendances_json)
            attendances_data = []
            attendances_data2 = []
            for at in attendances:
                attendances_data.append({'user_id':at['userId'], 
                    'created_at':at['createdAt'], 
                    'created_on':at['createdOn'], 
                    'status':at['status'], 
                    'location':at['location']})
                attendances_data2.append({'user_id':at['userId'], 
                    'created_at':at['createdAt'], 
                    'created_on':at['createdOn'], 
                    'status':at['status'], 
                    'location':at['location'],
                    'base64Image':at['base64Image']})
            ok, engine = utils.getEngine()
            if ok==utils.OK_CODE:
                metadata = MetaData(engine)
                table_attendance = alchemy.Table(TABLE_ATTENDANCE, metadata, autoload=True, autoload_with=engine)
                with engine.connect() as connection:
                    sql_query = table_attendance.insert().values(attendances_data).returning(table_attendance.c.id)
                    result = connection.execute(sql_query)
                    for id in result:
                        for at in attendances_data2:
                            createDate = datetime.strptime(at['created_at'], '%d-%m-%Y')
                            createdDateCsv = createDate.strftime('%d/%m/%Y')
                            createTime = datetime.strptime(at['created_on'], '%H:%M:%S.%f')
                            createdTimeCsv = createTime.strftime('%H:%M:%S')
                            createdTimeImg = createTime.strftime('%H-%M-%S')
                            utils.saveCSV(at['user_id'], createdDateCsv, createdTimeCsv, at['status'], at['location'])
                            bitmap = base64.b64decode(at['base64Image'])
                            utils.saveImageAttendance('attendances/', at['user_id'], bitmap, at['created_at'], createdTimeImg)                            
                        return 'OK', 200
            # print(attendances)
        except Exception as ex:
            return str(ex), 404

class User(Resource):
    def post(self):
        """ save new NIK, name and it's encoding into Postgres
            @param user_id: NIK of user
            @param name: name of user
            @param thumb: base64 thumb string
            @param image: base64 image string
            @return OK, 200
        """
        dret = {}
        parser.add_argument('user_id')
        parser.add_argument('name')
        parser.add_argument('thumb')
        parser.add_argument('image')
        args = parser.parse_args()
        userid = args['user_id']
        name = args['name']
        thumb = args['thumb']
        image_big = args['image']
        if userid is None or name is None or thumb is None:
            return 'error empty argument', 404
        try:
            ok = utils.createPhotosDir()
            if ok!=utils.OK_CODE:
                return 'cannot create photos dir', 404
            okcode, user_id, _, _ = utils.saveNewUser(userId=userid, userName=name)
            if okcode==utils.OK_CODE:
                # extract image
                thumb_bitmap = base64.b64decode(thumb)
                thumb_image = Image.open(io.BytesIO(thumb_bitmap))
                array_np_thumb = np.array(thumb_image)   
                # generate encoding for incoming image thumb         
                h = array_np_thumb.shape[0]-1
                w = array_np_thumb.shape[1]-1
                encoding = face_recognition.face_encodings(array_np_thumb, known_face_locations=[[0,w-1,h-1,0]])[0]
                okcode, dret = utils.saveNewEncoding(userId=user_id, encoding_array=encoding)
                if okcode==utils.OK_CODE:
                    # save_image = 'error'
                    if image_big is not None:
                        image_big_bitmap = base64.b64decode(image_big)
                        save_image = utils.saveImageUser('photos/', user_id, image_big_bitmap)
                    else:
                        save_image = utils.saveImageUser('photos/', user_id, thumb_bitmap)
                    return dret, 200
                    # if 'error' in save_image:
                        # utils.removeUserById(user_id)
                        # utils.removeUserById(no_id)         
                    # else:
                        # return dret, 200
                else:
                    utils.removeUser(userid)
                    printDebug(okcode)
                    return okcode, 404
            else:
                printDebug(okcode)
                return okcode, 404
        except Exception as ex:
            printDebug(ex)
            return str(ex), 404

class DataUser(Resource):    
    def get(self):
        """ select all user
        """
        try:
            data_all = {}        
            select_statement = "select * from public." + utils.TABLE_USER 
            ok, engine = utils.getEngine()
            if ok==utils.OK_CODE:
                sql = alchemy.text(select_statement)
                with engine.connect() as connection:
                    result = connection.execute(sql)
                    result_as_list = result.fetchall()
                    len_list = len(result_as_list)
                    data_all['0'] = {'length':str(len_list)}
                    for i,data in enumerate(result_as_list):
                        data_all[str(i+1)] = {'user_id':data[0], 'created_at':(data[1]).strftime('%d-%m-%Y %H:%M:%S'), 'name':data[2]}
                return data_all, 200
            else:
                return 'error get engine', 404
        except Exception as ex:
            return str(ex), 404
        

class DataEncoding(Resource):
    """ get all active record of encoding
        0 Column('id', Integer, primary_key=True),
        1 Column('user_id', alchemy.VARCHAR(length=8)),
        2 Column('created_at', DateTime),
        3 Column('deleted', alchemy.VARCHAR(length=1)),
        4 ~ *(Column(f, Float(precision=18, decimal_return_scal
    """
    # TO-DO: Should be one-by-one insertion into database, not all in once
    def get(self):
        try:
            data_all = {}
            select_statement = "select * from public." + utils.TABLE_ENCODING 
            ok, engine = utils.getEngine()
            if ok==utils.OK_CODE:
                sql = alchemy.text(select_statement)
                with engine.connect() as connection:
                    result = connection.execute(sql)
                    result_as_list = result.fetchall()
                    len_list = len(result_as_list)
                    # the first item is the number of encoding record available in database
                    data_all['0'] = {'length':str(len_list)}
                    # send encoding value in string format separated by comma
                    for i, data in enumerate(result_as_list):
                        start = 2
                        encoding_string = ''
                        for j in range(128):
                            start = start+1
                            if j==127:
                                encoding_string = encoding_string + str(data[start])
                            else:
                                encoding_string = encoding_string + str(data[start]) + ','
                        data_all[str(i+1)] = {'user_id':data[2], 'created_at':(data[1]).strftime('%d-%m-%Y %H:%M:%S'), 'encodings':encoding_string}
                return data_all, 200
            else:
                return 'error get engine', 404
        except Exception as ex:
            return str(ex), 404
        
class Ping(Resource):
    def get(self):
        return 'OK', 200

api.add_resource(Recognize, '/api/v1/facesecure/recognize/')
api.add_resource(Liveness, '/api/v1/facesecure/liveness/')
api.add_resource(User, '/api/v1/facesecure/user/')
api.add_resource(Attendance, '/api/v1/facesecure/attendance/')
api.add_resource(DataUser, '/api/v1/facesecure/user/all/')
api.add_resource(DataEncoding, '/api/v1/facesecure/encoding/all/')
api.add_resource(DataAttendance, '/api/v1/facesecure/attendances/')
api.add_resource(Ping, '/api/v1/facesecure/ping/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)

