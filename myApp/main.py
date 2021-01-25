
import kivy
from kivy.app import App
#from kivy.uix.label import Label
#from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen,ScreenManager,SwapTransition,SlideTransition

from datetime import date
import pickle as pk

current_user = []

class LoginScreen(Screen):
    user = ObjectProperty(None)
    passw = ObjectProperty(None)

    def login_btn(self):
        f = open('user_data.txt', 'rb')
        user_dic = pk.load(f)
        f.close()
        if self.passw.text in user_dic:
            dic_part = user_dic[self.passw.text]
            for i in range(len(dic_part)):
                if self.user.text in dic_part[i]:
                    global current_user
                    current_user = [self.passw.text,self.user.text]
                    sm.current = "main"
                    self.user.text = ""
                    self.passw.text = ""

    def new_btn(self):
        sm.current = "register"

class RegisterScreen(Screen):
    username = ObjectProperty(None)
    passw = ObjectProperty(None)
    email = ObjectProperty(None)
    name_error = ObjectProperty(None)
    email_error = ObjectProperty(None)
    passw_error = ObjectProperty(None)
    reg_button = ObjectProperty(None)
    name_bool = False
    email_bool = False
    passw_bool = False

    def on_enter(self, *args):
        self.username.bind(text=self.user_text)
        self.passw.bind(text=self.passw_text)
        self.email.bind(text=self.email_text)

    def user_text(self, value,*args):
        self.name_bool = False
        if len(list(str(value.text))) < 4:
            self.name_error.color = 1, 0, 0, 1
            self.name_error.text = "Your Username is too short"
        elif len(list(str(value.text))) > 20:
            self.name_error.color = 1, 0, 0, 1
            self.name_error.text = "Your Username is too long"
        elif ' ' in list(str(value.text)):
            self.name_error.color = 1, 0, 0, 1
            self.name_error.text = "Username can't contain spaces"
        else:
            f = open('user_data.txt', 'rb')
            user_dic = pk.load(f)
            f.close()
            user_values = list(user_dic.values())
            name_used = False
            for i in range(len(user_values)):
                for j in range(len(user_values[i])):
                    if value.text == user_values[i][j][1]:
                        self.name_error.color = 1, 0, 0, 1
                        self.name_error.text = "Username in use"
                        name_used = True
            if not name_used:
                self.name_error.color = 0,1,0,1
                self.name_error.text = "Valid Username"
                self.name_bool = True
                self.check_register()

    def email_text(self, value,*args):
        self.email_bool = False
        if len(list(str(value.text))) < 4:
            self.email_error.color = 1, 0, 0, 1
            self.email_error.text = "Your adress is too short"
        elif len(list(str(value.text))) > 50:
            self.email_error.color = 1, 0, 0, 1
            self.email_error.text = "Your adress is too long"
        elif ' ' in list(str(value.text)):
            self.email_error.color = 1, 0, 0, 1
            self.email_error.text = "Adress can't contain spaces"
        elif value.text.count("@")!=1 or value.text.count(".")==0:
            self.email_error.color = 1, 0, 0, 1
            self.email_error.text = "Not a valid adress"
        else:
            f = open('user_data.txt', 'rb')
            user_dic = pk.load(f)
            f.close()
            user_values = list(user_dic.values())
            adress_used = False
            for i in range(len(user_values)):
                for j in range(len(user_values[i])):
                    if value.text == user_values[i][j][0]:
                        self.email_error.color = 1, 0, 0, 1
                        self.email_error.text = "Adress in use"
                        adress_used = True
            if not adress_used:
                self.email_error.color = 0, 1, 0, 1
                self.email_error.text = "Valid Email"
                self.email_bool = True
                self.check_register()


    def passw_text(self, value,*args):
        self.passw_bool = False
        if len(list(str(value.text))) < 4:
            self.passw_error.color = 1, 0, 0, 1
            self.passw_error.text = "Your Password is too short"
        elif len(list(str(value.text))) > 20:
            self.passw_error.color = 1, 0, 0, 1
            self.passw_error.text = "Your Password is too long"
        elif ' ' in list(str(value.text)):
            self.passw_error.color = 1, 0, 0, 1
            self.passw_error.text = "Password can't contain spaces"
        else:
            self.passw_error.color = 0,1,0,1
            self.passw_error.text = "Valid Password"
            self.passw_bool = True
            self.check_register()

    def check_register(self):
        if self.passw_bool and self.name_bool and self.email_bool:
            self.reg_button.text = "Register new acoount"
            self.reg_button.background_color = 0.15, 0.78, 0.15, 1
        else:
            self.reg_button.text = "Go back to login"
            self.reg_button.background_color = 0.9,0.9,0.9, 1

    def register_btn(self):
        f = open('user_data.txt', 'rb')
        user_dic = pk.load(f)
        f.close()
        # saved as: dict{ passw:[[email,username,date],...,[email,username,date]]}
        # multiple users to one password
        if self.passw_bool and self.name_bool and self.email_bool:
            if self.passw.text in user_dic:
                l = user_dic[self.passw.text]
                for i in range(len(l)):
                    if l[i][0]!=self.email.text and l[i][1]!=self.username.text:
                        l += [[self.email.text,self.username.text,date.today().strftime("%d/%m/%Y")]]
                user_dic[self.passw.text] = l
            else:
                user_dic[self.passw.text]=[[self.email.text,self.username.text,date.today().strftime("%d/%m/%Y")]]
            f = open('user_data.txt', 'wb')
            pk.dump(user_dic, f)
            f.close()
            self.passw.text = ""
            self.username.text = ""
            self.email.text = ""
            sm.current = "login"
            self.reg_button.text = "Go back to login"
            self.reg_button.background_color = 0.9, 0.9, 0.9, 1
        else:
            sm.current = "login"

class MainScreen(Screen):
    n = ObjectProperty(None)
    created = ObjectProperty(None)
    email = ObjectProperty(None)
    passw = ObjectProperty(None)
    passw_error = ObjectProperty(None)
    global current_user

    def on_enter(self, *args):
        self.passw.bind(text=self.passw_text)

    def passw_text(self,value,*args):
        self.passw_bool = False
        if len(list(str(value.text))) < 4:
            self.passw_error.color = 1, 0, 0, 1
            self.passw_error.text = "Your Password is too short"
        elif len(list(str(value.text))) > 20:
            self.passw_error.color = 1, 0, 0, 1
            self.passw_error.text = "Your Password is too long"
        elif ' ' in list(str(value.text)):
            self.passw_error.color = 1, 0, 0, 1
            self.passw_error.text = "Password can't contain spaces"
        else:
            self.passw_error.color = 0, 1, 0, 1
            self.passw_error.text = "Valid Password - Saved"
            f = open('user_data.txt', 'rb')
            user_dic = pk.load(f)
            f.close()
            #changing the password
            rest_data = []
            for i in range(len(user_dic[current_user[0]])):
                if current_user[1] in user_dic[current_user[0]][i]:
                    user_data = user_dic[current_user[0]][i]
                else:
                    rest_data.append(user_dic[current_user[0]][i])
            if len(rest_data)>0:
                user_dic[current_user[0]]=rest_data
            else:
                user_dic.pop(current_user[0])
            user_dic[value.text]=[user_data]
            current_user[0] = value.text
            print(user_dic)
            f = open('user_data.txt', 'wb')
            pk.dump(user_dic, f)
            f.close()




    def on_pre_enter(self, *args):
        f = open('user_data.txt', 'rb')
        user_dic = pk.load(f)
        f.close()
        for i in range(len(user_dic[current_user[0]])):
            if current_user[1] in user_dic[current_user[0]][i]:
                email, name, created = user_dic[current_user[0]][i]
                self.n.text = name
                self.email.text = email
                self.created.text = created
                self.passw.text = current_user[0]

    def exit_btn(self):
        sm.current = "login"


class WindowManager(ScreenManager):
    transition = SwapTransition()

class P(FloatLayout):
    pass

def show_popup():
    show = P()
    popup_w = Popup(title="Popup",content=show,size_hint=(None,None),size=(400,400))
    popup_w.open()

Builder.load_file('my.kv')

sm = WindowManager()
screens = [LoginScreen(name="login"),RegisterScreen(name="register"),MainScreen(name="main")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"



class MyApp(App):
    def build(self):
        return sm


if __name__ == '__main__':
    MyApp().run()

