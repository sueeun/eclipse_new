from flask import Flask, render_template, request, redirect, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql


app = Flask(__name__)
app.secret_key = 'secret_key'

def get_db_connection():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='admin',
            password='password',
            db='eclipse',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except Exception as e:
        return None


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/AnomalyDetection')
def AnomalyDetection():
    return render_template('AnomalyDetection.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/goaccess')
def goaccess():
    return render_template('goAccess.html')

@app.route('/ml_dashboard')
def ml_dashboard():
    return render_template('Flask.html')

@app.route('/cloudwatch')
def cloudwatch():
    return render_template('Cloudwatch.html')

@app.route('/member1')
def member1():
    return render_template('member1.html')

@app.route('/member2')
def member2():
    return render_template('member2.html')

@app.route('/member3')
def member3():
    return render_template('member3.html')

@app.route('/member4')
def member4():
    return render_template('member4.html')

# 로그인
@app.route('/login', methods=['GET', 'POST'])
def login():
    id = request.values.get('id')
    password = request.values.get('pw')
    
    if(id is None):
        return render_template('login.html')

    else: 
        conn = get_db_connection()

        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM members WHERE id=%s", (id))
                    user = cursor.fetchone()

                    if check_password_hash(user['pw'], password):
                        return render_template('dashboard.html')
                        
                    else:
                        message = '아이디와 비밀번호가 일치하지 않습니다.'
                        return render_template('login.html', message=message)
            except Exception as e:
                return jsonify({'error': str(e)})
            finally:
                conn.close()
        else: 
            return "Failed to connect to the database"

# 회원가입
@app.route('/join', methods=['GET', 'POST'])
def join():
    id = request.values.get('id')
    password = request.values.get('pw')
    name = request.values.get('name')
    birth = request.values.get('birth')

    if(id is None):
        return render_template('createAccount.html')
    
    else:
        conn = get_db_connection()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("insert into members (id, pw, name, birth) values (%s, %s, %s, %s)", (id, generate_password_hash(password), name, birth))
                conn.commit()
                return render_template('login.html', message="계정이 생성되었습니다.")


            except Exception as e:
                return jsonify({'error': str(e)})
            finally:
                conn.close()


        else:
            return "Failed to connect to the database"

# 회원가입 아이디 중복체크
@app.route('/get_id', methods=['GET', 'POST'])
def get_id():
    id = request.values.get('id')

    conn = get_db_connection()

    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM members WHERE id=%s", (id))
                user = cursor.fetchone()
                
                if id=='':
                    message = '아이디를 입력해주세요.'
                    return message

                if user:
                    message = '이미 생성된 아이디 입니다.'
                    return message
                    # return render_template('login_check.html', message=message)
                    
                else:
                    message = '사용 가능한 아이디입니다.'
                    return message
                    # return render_template('login.html', message=message)
        except Exception as e:
            return jsonify({'error': str(e)})
        finally:
            conn.close()
    else: 
        return "Failed to connect to the database"

# 아이디 찾기
@app.route('/findId',  methods=['GET', 'POST'])
def findId():
    name = request.values.get('name')
    birth = request.values.get('birth')

    if(name is None):
        return render_template('findId.html')

    # if (name is not None):
    #     return render_template('findId.html', message='')

    # if (birth is not None):
    else:
        conn = get_db_connection()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM members WHERE name=%s and birth=%s", (name, birth))
                    user = cursor.fetchone()

                    if user:
                        message = "귀하의 아이디는 {finded_id} 입니다.".format(finded_id=user['id'])
                        return render_template('findId.html', message=message)
                    else:
                        message = "입력한 정보가 유효하지 않습니다."
                        return render_template('findId.html', message=message)

            except Exception as e:
                return jsonify({'error': str(e)})
            finally:
                conn.close()

        else:
            return "Failed to connect to the database"


# 비밀번호 찾기
@app.route('/findPw',  methods=['GET', 'POST'])
def findPw():
    id = request.values.get('id')
    name = request.values.get('name')
    birth = request.values.get('birth')

    if(id is None):
        return render_template('findPw.html')

    # if (name is not None):
    #     return render_template('findId.html', message='')

    # if (birth is not None):
    else:
        conn = get_db_connection()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM members WHERE id=%s and name=%s and birth=%s", (id, name, birth))
                    user = cursor.fetchone()

                    if user:
                        message = "귀하의 비밀번호는 {finded_pw} 입니다.".format(finded_pw=user['pw'])
                        return render_template('findPw.html', message=message)
                    else:
                        message = "입력한 정보가 유효하지 않습니다."
                        return render_template('findPw.html', message=message)

            except Exception as e:
                return jsonify({'error': str(e)})
            finally:
                conn.close()

        else:
            return "Failed to connect to the database"


# 새 비밀번호 설정 
@app.route('/newPwConfig',  methods=['POST'])
def newConfig():
    id = request.values.get('id')
    newPw = request.values.get('newPw')
    newPw_confirm = request.values.get('newPw_confirm')
   
    if(newPw is None):
        session['id'] = id
        return render_template('newPwConfig.html')
    
    else:
        if(newPw != newPw_confirm):
            return render_template('newPwConfig.html', message="비밀번호가 서로 일치하지 않습니다.")
        else:
            conn = get_db_connection()
            if conn:
                try:
                    with conn.cursor() as cursor:
                        cursor.execute("update members set pw=%s where id=%s", (generate_password_hash(newPw), session['id']))
            
                    # try:
                    conn.commit()
                    return render_template('login.html')
                    # except Exception as e:
                    #     return jsonify({"커밋 실패: {str(e)"})


                except Exception as e:
                    return jsonify({'error': str(e)})
                finally:
                    conn.close()


            else:
                return "Failed to connect to the database"


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
