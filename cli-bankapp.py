import json
class Register_bank:
    def __init__(self,):
        with open("go.json","r") as file:
            self.user = json.load(file)
    def check_username(self, username):
            if username in self.user:
                print("username already used")
            else:
                return True
    def check_password(self,password):
            if len(password) < 12:
                print("password must have at least 12 characters")
                return False
            if not any(c.isalpha() for c in password):
                print("password must have an alphabeth")
                return False
            if not any(c.isdigit() for c in password):
                print("password must have a digit")
                return False
            else:
                return True
    def check_user(self,username,password):
        if self.check_username(username) and self.check_password(password) is True:
            return True
        else:
            return False
    def save_user(self,username,password,full_name,balance):
        if self.check_user(username,password) is True:
            name,data = username,{"Name":full_name, "Password":password, "Balance":balance}
            self.user[name]=data
            with open("go.json","w") as file:
                    json.dump(self.user,file, indent=4) 
                    return "user saved successfully"
        else:
            return "user not saved"
            
class Bank_server:
    def __init__(self):
        self.login_status = False
    def login(self,username,password):
        if username in users.user and users.user[username]["Password"]==password:
            self.login_status = True
            return True
        else:
            self.login_status= False
            return False
    def user_status(self):
        if self.login is True:
            return "User is active"
        else:
            return "user not active"
            
class Account:
    def __init__(self,customer):
        self.customer = customer
        self.balance = users.user[self.customer]["Balance"]
    def deposit(self,amount):
             self.balance+=amount
             users.user[self.customer]["Balance"]=self.balance
             with open("go.json","w") as file:
                 json.dump(users.user,file)
             return f"you deposited {amount}"
    def withdraw(self,amount):
         if amount > self.balance:
              print("insufficient funds")
              return False
         else:
             self.balance-=amount
             users.user[self.customer]["Balance"]=self.balance
             with open("go.json","w") as file:
                 json.dump(users.user,file)
                 print(f"{amount} withdrawn successfully")
             return True
    def transfer(self,recipient,amount):
          if recipient in users.user:
              if self.withdraw(amount) is True:
                  users.user[recipient]["Balance"]+=amount
                  with open("go.json","w") as file:
                      json.dump(users.user,file)
                  return "Transfer successful"
              else:
                  return "unable to make transfer"
          else:
              return "user not found"
    def check_balance(self):
         return f"your balance is {self.balance}"

users = Register_bank()


def full_name():
    name = input("Enter your fullname: ").title()
    return name
    
def bal():
    while True:
        try:
            balance = float(input("Enter your balance: "))
            return balance
        except ValueError:
            print("Balance must be in figures")
            
def amount():
    while True:
        try:
            amount = float(input("Enter amount: "))
            return amount
        except ValueError:
            print("Amount must be in figures")
            
def recipient():
    recipient = input("Enter beneficiary username: ")
    return recipient
def exit():
    return "Thank you for banking with us"
    
def sign_up():
    for attempts in range(5):
        username = input("username: ")
        password = input("password: ")
        if users.check_user(username,password) is True:
            print(users.save_user(username,password,full_name(),bal()))
            break 
        else:
            print("try again")
user = Bank_server()
def sign_in():
    max_attempts = 3
    attempts = 0
    while attempts < max_attempts:
        username = input("username: ")
        password = input("password: ")
        if user.login(username,password) is True:
            customer = username
            print("login in successful")
            return customer
            break
        else:
            attempts+=1
            print(f"invalid username or password. {max_attempts-attempts} attempts left")
    return "thanks"
    
def menu():
   try:
       banker = Account(sign_in())
       while True:
           menu = input("1.Deposit/2.Withdraw/3.Transfer/4.Balance/5.Exit: ")
           if menu=='1':
               print(banker.deposit(amount()))
           elif menu=='2':
               print(banker.withdraw(amount()))
           elif menu=='3':
               print(banker.transfer(recipient(),amount()))
           elif menu=='4':
               print(banker.check_balance())
           elif menu=='5':
               break
           else:
               print("invalid option")
   except KeyError:
           return "Locked out"
  
def main_menu():
    print("WELCOME TO PROTOTYPE BANK")
    while True:
        ask = { '1':sign_up, '2':menu, '3':exit}
        select = input("1.Register/2.Login/3.exit: ")
        ask.get(select,"invalid option")()
    
print(main_menu())

    


    