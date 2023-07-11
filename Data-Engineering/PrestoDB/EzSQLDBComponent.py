import urllib3
import uuid
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import warnings
warnings.filterwarnings('ignore')  #this will ignore the warnings.it wont display warnings in notebook
import prestodb
import getpass


class DBComponentEzsql(object):
    def __init__(self, **args):
        self._db_version = str
        self._http_scheme = args['http_scheme']
        self._schema = args['schema']
        self._catelog = args['catelog']
        self._host = args['host']
        self._user = args['user']
        self._pwd = args['password']
        self._port = args['port']
        self._test_query= "select database();"
        self._cursor = object
        self._connection = object
        self._err = "Exception while connecting to PrestoDB, there, check with your Administrator !!!"
    
    # this is the prestodb connect component user defined function.
    def _connect(self)->object:
        try:
            with prestodb.dbapi.connect(host=self._host, port=self._port, user=self._user, catalog=self._catelog, schema= self._schema, http_scheme=self._http_scheme, auth=prestodb.auth.BasicAuthentication(self._user, self._pwd)) as self._connection:
                self._connection._http_session.verify = False

            if self._connection:
                return self._connection

        except Exception as e:
            print(self._err, e)
            exit(0)

        finally:
            if self._connection:
                self._connection.close()
    
    # this is the prestodb connect component user defined function.
    def _old_connect(self)->object:
        try:
            with prestodb.dbapi.connect(host=self._host, port=self._port, user=self._user, 
                                        catalog=self._catelog, schema=self._schema, http_scheme=self._http_scheme, 
                                        auth=prestodb.auth.BasicAuthentication(self._user, self._pwd)) as self._connection:
                self._connection._http_session.verify = False

            if self._connection:
                return self._connection

        except Exception as e:
            print(self._err, e)
            exit(0)

        finally:
            if self._connection:
                self._connection.close()
    
    #returns sql schema consisted table details                
    def _get_sql_schema(self, **args)->list:
        try:
            self._cursor = self._connection.cursor()
            # self._cursor.execute('show catalogs')
            self._cursor.execute('SHOW SCHEMAS')
            _db_list = self._cursor.fetchall()
            return _db_list
        except Exception as e:
            print(self._err, e)
        finally:
            if self._connection:
                self._connection.close()
                self._cursor.close()

    #returns sql schema consisted table details                
    def _get_sql_tables(self, **args)->list:
        try:
            self._connection.close()
            if self._schema != None and args["run_schema"] != None:
                self._schema = args["run_schema"]
                self._connection = self._connect()
                self._cursor = self._connection.cursor()
                self._cursor.execute('show tables')
                _table_list = self._cursor.fetchall()
                return _table_list
        except Exception as e:
            print(self._err, e)
        finally:
            if self._connection:
                self._connection.close()
                self._cursor.close()
    
    #returns sql table persisted data
    def _get_data(self,**args)->list:
        try:
            if args['table_name']!= None:
                ''' This generalized sql query we must need to extend '''
                str_query = f"SELECT * FROM {args['table_name']}"
                self._cursor = self._connection.cursor()
                self._cursor.execute(str_query)
                res_data = self._cursor.fetchall()
                return res_data
        except Exception as e:
            print(self._err, e)
        finally:
            if self._connection:
                self._connection.close()
                self._cursor.close()

if __name__ == "__main__":
    try:
        # config to validate the schema name:
        config = {
            #"host":"ezsql.hpe-qa1-ezaf.com", 
            "host":"ezpresto.hpe-staging-ezaf.com",
            "catelog":"mysql",
            "user":"hpedemo-user01", 
            "password":"Hpepoc@123", 
            "schema":"retailstore",
            "http_scheme":"https",
            "port":443,
            "table": "call_center"
        }
        
        ezobj = DBComponentEzsql(
            host=config.get("host"), 
            catelog=config.get("catelog"),
            schema="default",
            user= config.get("user"),
            password=config.get("password"), 
            http_scheme = config.get("http_scheme"),
            port=config.get("port"))
        conn = ezobj._connect()
        print("-"*100, conn)
        
        ''' How we can use the developed core Ezmeral unified analytics Ezsql component explained bellow !!!'''
        if conn:
            print("-"*100," print list of schams ", ezobj._get_sql_schema())
            for item in range(0, len(ezobj._get_sql_schema())):
                # validate desired scema:
                if config.get("schema") in ezobj._get_sql_schema()[item]:
                    print(ezobj._get_sql_tables(run_schema=config.get("schema")))
                    print(ezobj._get_data(table_name=config.get("table")))
                    
    except Exception as e:
        print(ezobj._err, e)
