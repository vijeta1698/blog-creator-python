import mysql.connector as cn
from log_class import getLog,StreamHandler

logger = getLog('blog.py')
StreamHandler(logger)
config = {
  'user': 'ur5pawj8aubnd9ff',
  'password': 'hMCghUesQHHFS0XQqE4d',
  'host': 'bod1djqf7pu6dyeccowc-mysql.services.clever-cloud.com',
  'database': 'bod1djqf7pu6dyeccowc',
  'raise_on_warnings': True
}

class connection():
    try:
        def __init__(self):
            self.connection = cn.connect(**config)
            self.mycursor = self.connection.cursor()
    except Exception as e:
        logger.error('error in connection '+str(e))


    def create_table(self):
        try:
            self.mycursor().execute('create table blog(id int primary key auto_increment,author varchar(200),'
                             'title varchar(200), subtitle varchar(200),content nvarchar(5000),date_posted datetime, user_parent_id int)')
            return "table created successfully"
        except Exception as e:
            logger.error('error in creating table ' + str(e))


    def insert_data(self,author,title,subtitle,content,upi):
        try:
             self.mycursor.execute("insert into  blog(title,subtitle,author,content,date_posted,user_parent_id) values('{}','{}','{}','{}',now(),'{}')".format(author,title,subtitle,content,upi))
             self.connection.commit()
             return "data inserted successfully"
        except Exception as e:
            logger.error('error in inserting data to the table ' + str(e))

    def retrievedata(self):
        try:
            self.mycursor.execute('select id,author,title,subtitle,content,date_posted from  blog order by date_posted desc')
            return self.mycursor.fetchall()
        except Exception as e:
            logger.error('error in retrieving data ' +str(e))


    def read_data(self,id):
        try:
            self.mycursor.execute('select * from  blog where user_parent_id = {}'.format(id))
            return self.mycursor.fetchall()
        except Exception as e:
            logger.error('error in reading data ' +str(e))

    def read_blog_data(self, id):
        try:
            self.mycursor.execute('select * from  blog where id = {}'.format(id))
            return self.mycursor.fetchone()
        except Exception as e:
            logger.error('error in reading blog data ' +str(e))


    def create_user_table(self):
        try:
             self.mycursor.execute('create table  user_login(user_id int primary key auto_increment ,username varchar(50),password varchar(32))')
             return "table created "
        except Exception as e:
            logger.error('error in creating user table ' + str(e))


    def user_credentials(self, username,password):
        try:
            self.mycursor.execute("insert into  user_login(username,password) values('{}','{}')".format(username,password))
            self.connection.commit()
            return "signed up successfully"
        except Exception as e:
            logger.error('error in inserting user credential' + str(e))


    def retrieve_user_credential(self,username,password):
        try:
             self.mycursor.execute('select user_id ,username , password from  user_login where username = "{}" and password = "{}" '.format(username,password))
             cred = self.mycursor.fetchone()
             if cred == None:
                    return None
             else:
                    return cred
        except Exception as e:
            logger.error('error in fetching user credential' + str(e))


    def update(self,title,subtile,author,content,b_id):
        try:
            self.mycursor.execute("update  blog set title = '{}',subtitle = '{}',author = '{}',content = '{}' where id = '{}'". format(title,subtile,author,content,b_id))
            self.connection.commit()
            return "updated successfully"
        except Exception as e:
            logger.error('error in updating user credential' + str(e))



    def get_blog_by_id(self,id):
        try:
             self.mycursor.execute("select id, title, subtitle, author, content from  blog where id = '{}'".format(id))
             data = self.mycursor.fetchone()
             return data
        except Exception as e:
            logger.error('error in getting blog by id user credential'+str(e))


    def delete(self,id):
        try:
            self.mycursor.execute("delete from  blog where id ='{}'".format(id))
            self.connection.commit()
            return "deleted successfully"
        except Exception as e:
            logger.error('error in deleting blog ' + str(e))


    def fetch_by_email(self,username):
        try:
             self.mycursor.execute("select * from  user_login where username = '{}'".format(username))
             return self.mycursor.fetchone()
        except Exception as e:
            logger.error('error in fetching data by email  ' + str(e))


    def update_by_username(self, username, password):
        try:
            self.mycursor.execute("update  user_login set password = '{}' where username = '{}'".format(password, username))
            self.connection.commit()
            return "Password Updated"
        except Exception as e:
            logger.error('error in updating user password ' + str(e))








