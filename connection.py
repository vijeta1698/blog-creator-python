import mysql.connector as cn


config = {
  'user': 'ur5pawj8aubnd9ff',
  'password': 'hMCghUesQHHFS0XQqE4d',
  'host': 'bod1djqf7pu6dyeccowc-mysql.services.clever-cloud.com',
  'database': 'bod1djqf7pu6dyeccowc',
  'raise_on_warnings': True
}

class connection():
    def __init__(self):
        self.connection = cn.connect(**config)
        self.mycursor = self.connection.cursor()


    def create_table(self):
        self.mycursor().execute('create table blog(id int primary key auto_increment,author varchar(200),'
                         'title varchar(200), subtitle varchar(200),content nvarchar(5000),date_posted datetime, user_parent_id int)')
        return "table created successfully"


    def insert_data(self,author,title,subtitle,content,upi):
         self.mycursor.execute("insert into  blog(title,subtitle,author,content,date_posted,user_parent_id) values('{}','{}','{}','{}',now(),'{}')".format(author,title,subtitle,content,upi))
         self.connection.commit()
         return "data inserted successfully"


    def retrievedata(self):
        self.mycursor.execute('select id,author,title,subtitle,content,date_posted from  blog order by date_posted desc')
        return self.mycursor.fetchall()


    def read_data(self,id):
        self.mycursor.execute('select * from  blog where user_parent_id = {}'.format(id))
        return self.mycursor.fetchall()


    def read_blog_data(self, id):
        self.mycursor.execute('select * from  blog where id = {}'.format(id))
        return self.mycursor.fetchone()


    def create_user_table(self):
         self.mycursor.execute('create table  user_login(user_id int primary key auto_increment ,username varchar(50),password varchar(32))')
         return "table created "


    def user_credentials(self, username,password):
        self.mycursor.execute("insert into  user_login(username,password) values('{}','{}')".format(username,password))
        self.connection.commit()
        return "signed up successfully"


    def retrieve_user_credential(self,username,password):
         self.mycursor.execute('select user_id ,username , password from  user_login where username = "{}" and password = "{}" '.format(username,password))
         cred = self.mycursor.fetchone()
         if cred == None:
                return None
         else:
                return cred


    def update(self,title,subtile,author,content,b_id):
        self.mycursor.execute("update  blog set title = '{}',subtitle = '{}',author = '{}',content = '{}' where id = '{}'". format(title,subtile,author,content,b_id))
        self.connection.commit()
        return "updated successfully"


    def get_blog_by_id(self,id):
         self.mycursor.execute("select id, title, subtitle, author, content from  blog where id = '{}'".format(id))
         data = self.mycursor.fetchone()
         return data


    def delete(self,id):
        self.mycursor.execute("delete from  blog where id ='{}'".format(id))
        self.connection.commit()
        return "deleted successfully"


    def fetch_by_email(self,username):
         self.mycursor.execute("select * from  user_login where username = '{}'".format(username))
         return self.mycursor.fetchone()


    def update_by_username(self, username, password):
        self.mycursor.execute("update  user_login set password = '{}' where username = '{}'".format(password, username))
        self.connection.commit()
        return "Password Updated"







