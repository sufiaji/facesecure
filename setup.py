import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import Table, Column
from sqlalchemy import String, Numeric, DateTime, Float
from sqlalchemy import MetaData, Sequence, Integer, Time, Date
import sqlalchemy as alchemy
import argparse
from pickle5 import pickle
import os
import utils
import datetime

DB_NAME = 'facesecure'

def createDB(dbuser, dbpass, dbname):
    """ Create DB FaceSecure
        @param dbuser: username Postgres DB FaceSecure
        @param dbpass: password Postgres DB FaceSecure
        @param dbname: default: FaceSecure
    """
    # Connect to PostgreSQL DBMS
    str_con = ("user=" + dbuser + " password='" + dbpass + "'")
    con = psycopg2.connect(str_con)
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    # Obtain a DB Cursor
    cursor          = con.cursor()

    # Create table statement
    sqlCreateDatabase = "create database "+ dbname + ";"

    # Create a table in PostgreSQL database
    cursor.execute(sqlCreateDatabase)

def createTable(dbuser, dbpass, dbname):
    """ Generate 3 table inside FaceSecure database: euser, encoding & attendance
        @param dbuser: username Postgres DB FaceSecure
        @param dbpass: password Postgres DB FaceSecure
        @param dbname: default: FaceSecure
    """
    # create table
    db_string = "postgres://" + dbuser + ":" + dbpass + "@localhost:5432/" + dbname
    engine = alchemy.create_engine(db_string)
    metadata = MetaData(engine)

    # for creating a table USER
    # no auto run on field Date since it's possible to create offline
    table_user = Table(
        'euser',
        metadata,
        Column('user_id', alchemy.VARCHAR(length=8), primary_key=True, nullable=False),
        Column('created_at', alchemy.DateTime, server_default=alchemy.func.now()),
        Column('name', String(60)),
        # Column('deleted', alchemy.VARCHAR(length=1))
    )

    # for creating a table ENCODING
    # no auto run on field Date since it's possible to create offline
    fieldnames = []
    for i in range(128):
        fieldname = 'd' + str(i+1)
        fieldnames.append(fieldname)

    table_encoding = Table(
        'encoding', 
        metadata,
        Column('id', Integer, primary_key=True),
        Column('created_at', alchemy.DateTime, server_default=alchemy.func.now()),
        Column('user_id', alchemy.VARCHAR(length=8)),        
        # Column('deleted', alchemy.VARCHAR(length=1)),
        *(Column(f, Float(precision=18, decimal_return_scale=9)) for f in fieldnames)
    )

    # for creating table ATTENDANCE
    # no auto run on field Date & Time since it's possible to create offline
    table_attendance = Table(
        'attendance',
        metadata,
        Column('id', Integer, primary_key=True),
        Column('user_id', alchemy.VARCHAR(8)),
        Column('created_at', Date),
        Column('created_on', Time),      
        Column('status', alchemy.VARCHAR(3)),
        Column('location', alchemy.VARCHAR(2)),
        # Column('deleted', alchemy.VARCHAR(length=1))
    )

    # for creating table CONFIG
    table_config = Table(
        'config',
        metadata,
        Column('key', alchemy.VARCHAR(32), primary_key=True),
        Column('value', alchemy.VARCHAR(128)),
        Column('changed_at', alchemy.DateTime, server_default=alchemy.func.now())
    )

    with engine.connect() as conn:   
        table_user.create()
        table_encoding.create()
        table_attendance.create()
        table_config.create()

def UpdateCSVDownloadPath(dbuser, dbpass, dbname):
    """ Save path of CSV download in config table
        default path is the same directory where setup.py is run
    """
    db_string = "postgres://" + dbuser + ":" + dbpass + "@localhost:5432/" + dbname
    engine = alchemy.create_engine(db_string)
    with engine.connect as connection:
        cdir = os.getcwd()
        insert_config = "insert into public.config (key,value) values ('CSV_DOWNLOAD_PATH','" + cdir + "')"
        sql_query = alchemy.text(insert_config)
        connection.execute(sql_query)

def createDirs():
    """ Create photos and attendances dir in the directory where setup.py is run
    """
    os.mkdir('photos')
    os.mkdir('attendances')

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-u", "--user", required=True, help="postgres username")
    args = vars(ap.parse_args())

    if args["user"]:
        import getpass
        pwd = getpass.getpass("Enter password:")
        if pwd:
            pass
        else: 
            print("Password cannot be empty")
            exit()

    name_Database = DB_NAME
    # if args["dbname"]:        
    #     name_Database   = args["dbname"]    
    try:
        createDB(args["user"], pwd, name_Database)
        print("DB created...")
        createTable(args["user"], pwd, name_Database)
        print("Tables created...")
        UpdateCSVDownloadPath(args["user"], pwd, name_Database)
        print('Config updated...')
        utils.saveCredentialPickle(args["user"], pwd)
        print('Credential saved...')
        # createDirs()
        # print('New directory created for photos and attendances...')
        print("Done.")
    except Exception as ex:
        if 'password authentication failed' in str(ex):
            print("Wrong credential, process terminated.")
        else:
            print('Unknown error occured')