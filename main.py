from customtkinter import *
from os import path, system
import csv

LINK = ""


class App:
    def __init__(self, root):
        super().__init__()
        absolute_path = path.dirname(path.abspath(__file__))
        self.file_path = absolute_path + "/database/"

        # root
        root.title("my app")

        width = 1250
        height = 700
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = "%dx%d+%d+%d" % (
            width,
            height,
            (screenwidth - width) / 2,
            (screenheight - height) / 2,
        )
        root.geometry(alignstr)
        # root.grid_columnconfigure(0, weight=1)
        # root.grid_rowconfigure((0, 1), weight=1)

        # init
        self.login_root = CTkFrame(root)
        self.user_entry_var = StringVar()
        self.key_entry_var = StringVar()
        self.user_entry = CTkEntry(self.login_root, width=200, textvariable=self.user_entry_var)
        self.key_entry = CTkEntry(self.login_root, width=200, textvariable=self.key_entry_var, show="*")
        self.Error_label = CTkLabel(self.login_root, text="\n", width=2000)

        # config
        self.user_entry.focus_set()

        # binds
        self.user_entry.bind(
            "<Return>",
            lambda event: self.login(self.user_entry_var.get(), self.key_entry_var.get()),
        )
        self.key_entry.bind(
            "<Return>",
            lambda event: self.login(self.user_entry_var.get(), self.key_entry_var.get()),
        )

        # place and pack
        self.login_root.pack(side=LEFT, fill=BOTH)
        CTkLabel(self.login_root, text="\n\n\n\n\n\n\n\n").pack()
        CTkLabel(self.login_root, text="Introduzca el nombre de usuario y la contraseña\n", font=("Roboto", 24)).pack()
        CTkLabel(self.login_root, text="Nombre de usuario *").pack()
        self.user_entry.pack()
        CTkLabel(self.login_root, text="Contraseña *").pack()
        self.key_entry.pack()
        CTkLabel(self.login_root, text="").pack()
        CTkButton(
            self.login_root,
            text="Login",
            command=lambda: self.login(self.user_entry_var.get(), self.key_entry_var.get()),
        ).pack()
        CTkLabel(self.login_root, text="").pack()
        CTkButton(
            self.login_root,
            text="Register",
            command=lambda: self.register(self.user_entry_var.get(), self.key_entry_var.get()),
        ).pack()
        self.Error_label.pack()

        while True:
            try:
                with open(self.file_path + "data.csv", "r", encoding="utf8") as file:
                    self.data = []
                    r = csv.reader(file)
                    self.users = []

                    for row in r:
                        self.data.append(row)
                break
            except FileNotFoundError:
                open(self.file_path + "data.csv", "x", encoding="utf8")

        for i in self.data:
            if not (i[0] in self.users):
                self.users.append(i[0])
                print(self.users)
                print(self.data)

    def login(self, user: str, key: str, *args):
        self.username = user

        if (len(user) or len(key)) > 20:
            self.login_error(1)
        elif not (user and key):
            self.login_error(0)
        else:
            self.username = user
            self.password = key
            try:
                with open(self.file_path + "data.csv", "r+", encoding="utf8", newline="") as file:
                    self.data = []
                    r = csv.reader(file)
                    login_state = 0

                    for row in r:
                        self.data.append(row)

                    for i in self.data:
                        if not (i[0] in self.users):
                            self.users.append(i[0])

                    if not self.data:
                        login_state = 3
                    else:
                        for i in self.data:
                            if i[0] == self.username:
                                if i[1] == self.password:
                                    login_state = 1
                                    break
                                else:
                                    login_state = 2
                                    break
                            else:
                                login_state = 3

                    if login_state == 1:
                        system(f"start {LINK}")
                    elif login_state == 2:
                        self.login_error(3)
                    elif login_state == 3:
                        self.login_error(2)
                        print("1")
            except FileNotFoundError as e:
                self.login_error(2)
                print("2")

    def register(self, user: str, key: str):
        self.username = user
        self.register_complete = False
        if (len(user) or len(key)) > 20:
            self.login_error(1)
        elif not (user and key):
            self.login_error(0)
        else:
            self.username = user
            self.password = key
            try:
                x = open(self.file_path + "data.csv", "x")
                x.close()
            except FileExistsError:
                pass

            with open(self.file_path + "data.csv", "r+", encoding="utf8", newline="") as file:
                self.data = []
                w = csv.writer(file)
                r = csv.reader(file)
                user_in_use = bool()

                for row in r:
                    self.data.append(row)

                if not self.data:
                    w.writerow([self.username, self.password])
                    self.register_complete = True
                else:
                    for i in self.data:
                        if i[0] == self.username:
                            user_in_use = True
                            self.login_error(4)
                            break
                    if not user_in_use:
                        w.writerow([self.username, self.password])
                        self.register_complete = True
            if self.register_complete:
                self.login(self.user_entry_var.get(), self.key_entry_var.get())

    def login_error(self, x: int):
        if x == 0:
            self.Error_label.configure(text="\nEl usuario y/o la contraseña no pueden estar en blanco.")
        elif x == 1:
            self.Error_label.configure(text="\nEl usuario y la contraseña deben ser inferiores a 20 carácteres.")
        elif x == 2:
            self.Error_label.configure(text="\nUsuario no encontrado.")
        elif x == 3:
            self.Error_label.configure(text="\nContraseña incorrecta.")
        elif x == 4:
            self.Error_label.configure(text="\nEste nombre de usuario y/o contraseña no están disponibles")


if __name__ == "__main__":
    root = CTk()
    app = App(root)
    root.mainloop()
