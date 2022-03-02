from cryptography.fernet import Fernet

class PasswordManager:

    """
    Password Manager is a functionality that helps to encrypt a password
    in file system(it can be extended in database as well).

    For below when using for first time, the first 2 inputs must be 2 and 4

    """
    
    def __init__(self):
        self.key = None
        self.password_file = None
        self.password_dic = {}
    def create_key(self, path):

        """
        Creates a key file. It is not meant to store your information.
        Just a password maintaince key file.
        """

        self.key = Fernet.generate_key()
        print(self.key)
        with open(path, 'wb') as f:
            f.write(self.key)
    def load_key(self, path):

        """
        Loads the key in your system
        """

        with open(path, 'rb') as f:
            self.key = f.read()
            # here path valic=dation is not being done, and correc path provided by user 
            # are not present. Can use os module for that
    def create_password_file(self, path, initial_values=None):

        """
        Create a new password file which is managed by your key file.
        This password file is the main file which stores your encrypted
        data.
        """
        self.password_file = path 
        if initial_values!=None:
            for key, value in initial_values.items():
                self.add_password(key, value)
    def load_password_file(self, path):

        """
        Loads password file for your particular key file.
        If you are creating key1.key and pass3.pass and have loaded key1.key
        then always load pass3.pass otherwise it will not work.
        """

        self.password_file = path 
        with open(path, 'r') as f:
            for line in f:
                # for each line we will decrypt the password
                # site:password form
                site, encrypted = line.split(":")
                self.password_dic[site] = Fernet(self.key).decrypt(encrypted.encode()).decode()
    def add_password(self, site, password):

        """
        Adds new site:password in your password file
        """
        
        self.password_dic[site] = password 
        if self.password_file!=None:
            with open(self.password_file, 'a+') as f:
                encrypted = Fernet(self.key).encrypt(password.encode())
                f.write(site + ":" + encrypted.decode() + "\n")
    def get_password(self, site):

        """
        Gets Password for your particular site.
        """
        
        return self.password_dic[site]

def main():
    password = {
                    "email":"1234567",
                    "facebook":"myfbpass",
                    "youtube":'asd',
                    "something":'12345sdfsd'
                }
    pm = PasswordManager()

    print(""" 
    What Do You Want to DO ? 
    
    (1) Create a new Key
    (2) Load an existing key
    (3) Create new password file
    (4) Load Existing Password File
    (5) Add a new Password
    (6) Get a Password
    (q) Quit

    """)

    done = False

    while not done:
        choice = input("Enter Your Choice")
        if choice=="1":
            path = input("Enter Path: ")
            pm.create_key(path)
        elif choice=="2":
            path = input("Enter Path: ")
            pm.load_key(path)
        elif choice=="3":
            path = input("Enter Path: ")
            pm.create_password_file(path, password)
        elif choice=="4":
            path = input("Enter Path: ")
            pm.load_password_file(path)
        elif choice=="5":
            site = input("Enter site: ")
            password = input("Enter Password: ")
            pm.add_password(site, password)
        elif choice=="6":
            site = input("What site do you want: ")
            print(f"Password for {site} is {pm.get_password(site)}")
        elif choice=="q":
            done = True
            print("Bye")
        else:
            print("Invalid choice")

if __name__=="__main__":
    main()