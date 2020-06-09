from flask import Flask, session, abort, url_for, redirect, request, render_template, redirect
import logdb

app = Flask(__name__)
app.secret_key = b'aaa!111/'

#메인 페이지 (로그인하기 전)
@app.route('/')
def index():
    return render_template('main.html')

#로그인
@app.route('/login')
def login():
    return render_template('login.html')

    
@app.route('/method', methods=['GET', 'POST'])
def method():
    if request.method == 'GET':
        return 'GET으로 전송이다'
    else:
        id = request.form['id']
        pw = request.form['pw']
        ret = logdb.select_users(id,pw)
        if ret != None:
            session['users'] = id
            return '''<script>alert("로그인 성공!");
        location.href="/sub"
        </script>
        '''

        else:
            return "아이디나 패스워드가 틀렸습니다."

# 회원가입
@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'GET':
        return render_template('join.html')
    else:
        id = request.form['id']
        pw = request.form['pw']
        name = request.form['name']
        logdb.insert_data(id,pw,name)
        return '''<script>alert("회원가입을 축하드립니다!");
        location.href="/"
        </script>
        '''
     
#서브 페이지(로그인을 한 후)
@app.route('/sub')
def sub():
    return render_template("sub.html")

#회원된 유저정보들(로그인된 유저들에 한에서)
@app.route('/member')
def member():
    if 'users' in session:
        info = logdb.select_all()
        return render_template("showlog.html", data=info)
    else:
        return '''
        <script>alert("로그인을 해야합니다!");
        location.href="/login"
        </script>
        '''
   
#로그 아웃(session 제거)
@app.route('/logout')
def logout():
    session.pop('users', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
