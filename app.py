from flask import Flask, render_template, request, url_for, redirect,session
from connection import connection
from flask_session import Session
import re
import random
import smtplib
from log_class import getLog, StreamHandler

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

logger = getLog('blog.py')
StreamHandler(logger)

def sessionchecker():
    try:
        if session.get('id')!= None and session.get('username') != None:
            return 0
        else:
            return 1
    except Exception as e:
        raise Exception(str(e))

@app.route('/')
def index():
    try:
        obj = connection()
        posts = obj.retrievedata()
        loggedUser = ""
        if session.get('id') != None and session.get('username') != None:
            loggedUser = session.get('username')
        logger.info('site opened successfully')
        return render_template('index.html' ,posts = posts, loggedUser=loggedUser)

    except Exception as e:
        logger.error('Error '+str(e))
       # raise Exception(f'something went wrong' + str(e))


@app.route('/about')
def about():
    try:
        logger.info('page fetched')
        return render_template('about.html')
    except Exception as e:
        logger.exception(str(e))
        #raise Exception (f'something is not correct '+str(e))


@app.route('/logout')
def logout():
    try:
        session.clear()
        return redirect(url_for('index'))
    except Exception as e:
        logger.exception('something went wrong here '+str(e))

@app.route('/post/<int:post_id>')
def post(post_id):
    try:
        loggedUser = ""
        if session.get('id') != None and session.get('username') != None:
            loggedUser = session.get('username')
        obj = connection()
        post = [i for i in obj.read_blog_data(post_id)]
        logger.info('post fetched successfully')
        return render_template('post.html',post=post,loggedUser=loggedUser)

    except Exception as e:
        logger.exception('error in fetching post '+str(e))
        raise Exception (f'can not fetch data '+str(e))

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        try:
            x = sessionchecker()
            if (x == 1):
                return redirect(url_for('index'))
            else:
                loggedUser = ""
                if session.get('id') != None and session.get('username') != None:
                    loggedUser = session.get('username')
                    obj = connection()
                    data =  obj.read_data(session.get('id'))
                    if(data != None):
                        print(session.get('id'))
                        logger.info('post added ')
                        return render_template('add.html', loggedUser=loggedUser,data=data)
                    else:
                        return render_template('add.html', loggedUser=loggedUser)
        except Exception as e:
           raise Exception (f'something went wrong '+str(e))


@app.route('/addpost', methods=['GET', 'POST'])
def addpost():
    try:
        x = sessionchecker()
        if x==1:
            logger.info('user is not logged in')
            return redirect(url_for('index'))
        else:
            obj = connection()
            title = request.form['title']
            subtitle = request.form['subtitle']
            author = request.form['author']
            content = request.form['content']
            obj.insert_data(title,subtitle,author,content,session.get('id'))
            logger.info('post added successfully')
            return redirect(url_for('add'))
    except Exception as e:
        logger.exception('error in adding post '+str(e))
       # raise Exception (f'error '+str(e))


@app.route('/log', methods=['GET', 'POST'])
def loadLogin():
    try:
        return render_template('login.html')
    except Exception as e:
        logger.exception(str(e))


@app.route('/signup', methods=['GET', 'POST'])
def loadSignup():
    try:
        return render_template('signup.html')
    except Exception as e:
        logger.error(str(e))


@app.route('/logIn', methods=['GET', 'POST'])
def login():
    try:
        logger.info('in login')
        username = request.form['loginUname'].lower()
        password = request.form['loginUPass']

        obj = connection()
        #cred = list(obj.retrieve_user_credential(username,password))
        cred = obj.retrieve_user_credential(username, password)
        if cred!=None:
            cred = list(cred)
            if cred[2] == password and cred[1] == username:
                session['id'] = cred[0]
                session['username'] = cred[1]
                logger.info('User logged in')
                return redirect(url_for('index'))
        else:
            logger.error('Log in password not matched')
            login_error = "Password not matched. Kindly check again."
            return render_template('login.html', myErrorMsg=login_error, Password=password, username=username)
    except Exception as e:
        logger.error('log in error'+str(e))
        #raise Exception(str(e))


@app.route('/addUser', methods=['GET','POST'])
def sign():
  try:
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    username = request.form['txtNewUsername']
    password = request.form['txtNewPass']
    confirmpassword = request.form['txtConNewPass']
    obj = connection()
    try:
        if (re.fullmatch(regex, username)):
            if (len(password) < 8):
                errmsg = "Password is not strong enough"
                return render_template('signup.html', myErrorMsg=errmsg, fillPass=password, fillEmail=username, fillConPass=confirmpassword)
            else:
                if password == confirmpassword:
                    obj.user_credentials(username.lower(), password)
                    success_msg = "Registered Successfully"
                    logger.info('user added successfully')
                    return render_template('login.html', myErrorMsg=success_msg)
                else:
                    print('In Signup >> Else')
                    signup_error="Password not matched. Kindly check again."
                    logger.error('password not matched')
                    return render_template('signup.html', myErrorMsg=signup_error)
        else:
            logger.error('email format invalid')
            errmsg = "Invalid Email Format !"
            return render_template('signup.html', myErrorMsg=errmsg, fillPass=password, fillEmail=username, fillConPass=confirmpassword)
    except Exception as e:
        logger.error(str(e))
  except Exception as e:
    logger.error(str(e))
    render_template('error.html')


@app.route('/update', methods=['GET','POST'])
def update():
    try:
        id = request.args.get('bid')
        title = request.args.get('title')
        subtitle = request.args.get('subtitle')
        author = request.args.get('author')
        content = request.args.get('content')


        obj = connection()
        obj.update(title, subtitle, author, content, id)
        logger.info('updated successfully')
        return "{\"result\':\"OK\"}"
        # return redirect(url_for('add'))

    except Exception as e:
            logger.error(str(e))


@app.route('/delete', methods=['GET'])
def delete():
    try:
        id = request.args.get('bid')
        obj = connection()
        obj.get_blog_by_id(id)
        obj.delete(id)
        return "{\"Result\":\"Deleted\"}"
    except Exception as e:
        logger.error(str(e))
        #raise Exception(str(e))


@app.route('/get_blog')
def getBlog():
    try:
        id = request.args.get('bid')
        obj = connection()
        data1 = obj.get_blog_by_id(id)
        if data1!=None:
            data = [i for i in obj.get_blog_by_id(id)]
            dictionar = {'id': data[0], 'title': data[1], 'subtitle': data[2], 'content': data[4], 'author': data[3]}
            # print(dictionar)
            return dictionar
        else :
            return render_template('error.html')
    except Exception as e:
        logger.error(str(e))
        #raise Exception(str(e))


def smtpMailSender(rec):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        gmail_user = "developervijeta@gmail.com"
        gmail_pass = "gurukripa@72"
        server.login(gmail_user, gmail_pass)
        print('Login Success')

        receivers = rec

        numbers_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        password = ""
        for i in range(8):
            password += str(random.choice(numbers_list))

        #Update Password at username
        try:
            obj = connection()
            updatePass = obj.update_by_username(receivers,password)
            if updatePass == "Password Updated":
                message = f"Your new password is {password}"
                print(f"Message = {message}")
                server.sendmail(gmail_user, receivers, message)
                server.quit()
                logger.info('password changed')
            else:
                fmessage = "something went wrong"
                return render_template('forgotPassword.html', myErrorMsg=fmessage)
        except Exception as e:
            logger.error(str(e))
    except Exception as e:
        logger.error(str(e))



@app.route('/resetPassword')
def loadForgetPassword():
    try:
        return render_template('forgotPassword.html')
    except Exception as e:
        logger.error(str(e))

@app.route('/forgetpassword', methods=['POST'])
def forgetpassword():
    try:
        email = request.form['fEmail']
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        fmessage = ""
        if (re.fullmatch(regex, email)):
             #Here we need to check if email id exist in records or not.
            obj = connection()
            username = obj.fetch_by_email(email)
            if username!=None:
                  smtpMailSender(email)
                  fmessage = "We have sent you a mail containing your new password."
                  return  render_template('login.html', myErrorMsg=fmessage)
            else:
                fmessage =  "Email Id not registered, Kindly sign up"
                return render_template('forgotPassword.html', myErrorMsg=fmessage)
        else:
            fmessage="Invalid Email Id"
            return render_template('forgotPassword.html', myErrorMsg=fmessage)
    except Exception as e:
        logger.error(str(e))


if __name__ == '__main__':
    app.secret_key = 'vBlog'
    app.debug = True
    app.run()
