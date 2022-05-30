from flask import *
from datetime import timedelta, datetime
from flask_nav import Nav
from flask_nav.elements import *
from dominate.tags import img

app = Flask(__name__,template_folder='templates')
app.secret_key="hello"
app.permanent_session_lifetime = timedelta(minutes=1)

logo=img(src='logo.png', height="50", width="50", style="margin-top:-15px") #????

topbar=Navbar(logo,
        View("user board", "user_board"),
        View("Sign in", "login"),
        View("all board", "all_board"),
        View("Create account", "create_account"))

nav=Nav(app)
nav.register_element('top', topbar)

class users():
    def __init__(self, name = " ", password = " ", dog_number = " ", posts = [], friends = []):
        self.name = name
        self.password = password
        self.dog_number = dog_number
        self.friends = self.load_friends()
        tabb = []
        tab = []
        with open("./templates/posts/"+name+".txt") as file:
            x = "s"
            while x != "":
                x = file.readline()
                x = x[:-1]
                if x == "$":
                    tab.append(self.Post(tabb[0],tabb[1])) 
                    tabb = []
                else:
                    tabb.append(x)
        self.posts = tab
        del tabb,tab

    class Post:
        def __init__(self, date = " ", posttext = " "):
            self.date = date
            self.posttext = posttext

    def add_post(self, new_post = "?"):
        tabb = []
        tab = []
        dt_string = datetime.now()
        tabb.append(dt_string)
        tabb.append(new_post)
        tab = self.Post(tabb[0],tabb[1])
        self.posts.insert(0, tab)
        with open(self.name+".txt", "r") as file:
            box = file.read()
            for line in file:
                print(line)
                box = box + file.read()
        with open(self.name+".txt", "w") as file:
            file.write(str(dt_string)+"\n"+new_post+"\n"+"$"+"\n"+box)
        del tabb, tab

    def friends_posts(self, tab = []):
        tabb = []
        tabc = self.friends 
        tabc.append(self.name)
        for x in tabc:
            for y in tab:
                if x == y.name:
                    tabb = tabb + y.posts
        return tabb

    def load_friends(self):
        with open("./templates/friends/"+self.name+"_f.txt", "r") as file:
            tab = []
            for line in file:
                box = file.read()
                tab.append(box)
        del box
        return tab

    def isname(self, person = " " ):
        if str(person) == self.name:
            return True
        else:
            return False
    def isin(self, person = " ", password = " "):
        if str(person) == self.name and str(password) == self.password:
            return True
        else:
            return False

def add_user(filed="users.txt"):
    tabb=[]
    tab=[]
    with open(filed) as file:
        x = "s"
        while x != "":
            x = file.readline()
            x = x[:-1]
            if x == "$":
                tab.append(users(tabb[0],tabb[1],tabb[2]))
                tabb = []
            else:
                tabb.append(x)
    return tab

@app.route('/user_board',methods = ['POST','GET'])
def user_board():
    if "result"  not in session:
        return redirect(url_for("login"))
    else: 
        nickname = session["result"]
        for number, x in enumerate(tab): 
            y = x.isname(nickname)
            if y:
                if request.method == 'POST':
                    new_post = request.form['new_post']
                    x.add_post(new_post)
                    return redirect(url_for("user_board"))
                else:
                    return render_template('user_board.html', name = nickname, tabb = tab[number] )

@app.route('/login',methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        session.permanent = True
        result = request.form['fname']
        resultpass = request.form['password']
        for number,x in enumerate(tab):
            ss=x.isin(result, resultpass)
            if ss:
                session["result"] = result
                return redirect(url_for("all_board"))
        flash("This account doesn't exist or password is wrong!")
        return redirect(url_for("login"))
    else:
        if "result" in session:
            return redirect(url_for("all_board"))
        return render_template('login.html')

@app.route('/all_board',methods = ['POST','GET'])
def all_board():
    if "result"  not in session:
        return redirect(url_for("login"))
    elif request.method=='POST': 
        session.pop("result", None)
        return redirect(url_for("login"))
    else: 
        nickname = session["result"]
        for number, x in enumerate(tab): 
            y = x.isname(nickname)
            if y: 
                tabb = x.friends_posts(tab)

        return render_template('all_board.html', name = session["result"], tabb2 = tabb[number])

@app.route('/create_account',methods = ['POST','GET'])
def create_account():
    if request.method == 'POST':
        session.permanent = True
        result = [0,0,0]
        result[0] = request.form['fname']
        result[1] = request.form['fpassword']
        result[2] = request.form['fmail']
        for number,x in enumerate(tab):
            ss=x.isin(result[0])
            if ss:
                flash("This account already exist!")
                return redirect(url_for("create_account"))
        if len(result[1]) <= 4:
                flash("Too Short or wrong signs")
                return redirect(url_for("create_account"))
        tab.append(users(result[0],result[1],result[2]))
        with open("users.txt",'a',encoding = 'utf-8') as file:
            file.write(f"{result[0]}\n{result[1]}\n{result[2]}\n$\n")
        session["result"] = result[0]
        return redirect(url_for("all_board"))
    else:
        if "result" in session:
            return redirect(url_for("all_board"))
        return render_template('create_account.html')

if __name__ == '__main__':
    tab=[]
    tab=add_user("users.txt")
    app.run(debug=True)
