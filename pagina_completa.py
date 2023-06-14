from flask import Flask, request, render_template
import psycopg2
import CONT

app = Flask(__name__)

# FORMULARIO 
def formatacao():
    global cpf_formatado, telefone_formatado
    if cpf == None :
        cpf_formatado = 'vazio'
    else:
        cpf_formatado  = cpf[0:3] + '.' + cpf[3:6] + '.' + cpf[6:9] + '-' + cpf[9:12]


    if telefone == None :
        telefone_formatado = 'vazio'
    else:
        telefone_formatado  = telefone[0:2] + ' ' + telefone[2:7] + '-' + telefone[7:11] 


    return cpf_formatado, telefone_formatado


def conexao_bd():
    global sintaxe
    try:
        connect = psycopg2.connect(database='user',user='postgres',password= CONT.password)
        cursor = connect.cursor()
        sintaxe_consulta = """SELECT cpf FROM logins WHERE cpf = ('{}')""".format(cpf_formatado)
        cursor.execute(sintaxe_consulta)
        retorno_consulta = cursor.fetchone()

        try:
            if retorno_consulta[0] == cpf_formatado :
                print('usuario já cadastrado')

        except:        
            sintaxe = """INSERT INTO logins (nome, idade, cidade, rua, cpf, telefone, email, senha)
                                VALUES ('{}','{}','{}','{}','{}','{}','{}','{}')""".format(nome,idade,cidade,rua,cpf_formatado,telefone_formatado, email,senha)
            # sintaxe= """SELECT * FROM logins"""
            cursor.execute(sintaxe)

            connect.commit()
            connect.close()

            print('cadastrado!')

    except:
            print("error no BD")

    return 


@app.route('/formulario', methods=['GET', 'POST'])
def cadastro():

    try:
        global nome, idade, cidade, rua, cpf, telefone, email, senha
        nome = request.form["name"].capitalize()
        idade = request.form["IDADE"]
        cidade = request.form["CIDADE"]
        rua = request.form["RUA"]
        cpf = request.form["CPF"]
        telefone = request.form["TELEFONE"]
        email = request.form['EMAIL']
        senha = request.form['SENHA']

        formatacao()
        conexao_bd()

    except:
        print(KeyError)

    return render_template('formulario_completo.html')
   



#LOGIN

def login_banco():
    global valida_senha
    global valida_usuario

    connect = psycopg2.connect(host='localhost', database='user', user='postgres',password= CONT.password )
    cursor = connect.cursor()
    v_usuario = """SELECT nome FROM logins WHERE nome = '{}'""".format(usuario)
    cursor.execute(v_usuario)  
    valida_usuario = cursor.fetchone()

    v_senha = """SELECT senha FROM logins WHERE nome = '{}'""".format(usuario)
    cursor.execute(v_senha)
    valida_senha = cursor.fetchone()

    connect.close()
    

@app.route('/', methods=['GET','POST'])
def login():
    global usuario, senha, valida_login

    try:
        usuario = request.form['usuario'].capitalize()
        senha = request.form['senha']

        login_banco()

        if usuario == valida_usuario[0] and senha == valida_senha[0] :

            valida_login = 'Login Efetuado com sucesso!'
            print(valida_login)
            

    except:
        print('Usuario/Senha incorreto.')
        valida_login = 'Usuario/Senha incorreto.'

    return render_template('login_completo.html', resposta = '')




#QUEM SOMOS!

@app.route('/WhoWeAre', methods=['GET'])
def apresentação():
    return render_template('quem_somos.html')


#CONTATO

@app.route('/contato_', methods=['GET'])
def contatos():
    return render_template('contato.html')




app.run(host='localhost', port='5000', debug=True)