import json
import subprocess
# Load database
class Library:
    def __init__(self):
        with open("lib.json","r") as file:
            self.library = json.load(file)
    def get_titles(self):
        titles = [ ]
        for title in self.library:
            titles.append(title)
        return titles
    def save(self):
        with open("lib.json","w") as file:
            json.dump(self.library,file)
# User class
class User:
    def __init__(self,lib):
        self.lib = lib
    def result(self,book):
        results = [ ]
        for title in self.lib.library:
                books = title.strip().lower()
                if book in books:
                    results.append(books)
        return results
    def search(self,book):
        titles = self.result(book)
        if titles == []:
            return None
        books = "\n".join(f"{i} {result}" for i, result in enumerate(titles,1))
        return books
    def select(self,choice,book):
        try:
            choose = self.result(book)[choice-1]
            for a in self.lib.library:
                a = a.strip().lower()
                if choose in a:
                    return self.lib.library.get(a)
        except IndexError:
            return "invalid option"
    def read(self,choice,book):
        read = self.select(choice,book)
        if read["Available"]==True:
            file = read["Path"]
            read["Available"]=False
            self.lib.save()
            run = subprocess.run(["termux-open","--chooser",file])
            return run
        else:
            return "book borrowed, not currently available"
    def replace(self,choice,book):
        try:
            rpl = self.select(choice,book)
            rpl["Available"]=True
            self.lib.save()
            return "Thanks for reading"
        except IndexError:
            return "invalid option"
#admin class
class Admin:
    def __init__(self,lib):
        self.lib = lib
    def catalogue(self):
        catlg = "\n".join(f"{i} {w}" for i,w in enumerate(self.lib.get_titles(),1))
        return catlg
    def available(self):
        avlbks = []
        for books in self.lib.library:
            if self.lib.library[books]["Available"]==True:
                avlbks.append(books)
        return avlbks
    def select_avl(self):
        if self.available() == []:
            return "no books availble"
        else:
            select = "\n".join(f"{i} {w}" for i,w in enumerate(self.available(),1))
            return select
    def unavailable(self):
        unavl = []
        for books in self.lib.library:
            if self.lib.library[books]["Available"]==False:
                unavl.append(books)
        return unavl
    def select_unavl(self):
        if self.unavailable() == []:
            return
        else:
            select = "\n".join(f"{i} {w}" for i,w in enumerate(self.unavailable(),1))
            return select
    def modify(self,choice):
        try:
            choose = self.unavailable()[choice-1]
            modify = self.lib.library.get(choose)
            modify["Available"]=True
            self.lib.save()
            return "admin override successful"
        except IndexError:
            return "invalid option"
    def remove(self,choice):
        try:
            choose = self.lib.get_titles()[choice-1]
            rmbook = self.lib.library.pop(choose)
            self.lib.save()
            return "Done, book removed"
        except IndexError:
            return "invalid option"
    def add_book(self):
       book = input("Enter book title: ").strip().lower()
       for data in self.lib.library:
           if book in data.strip().lower():
               return "book already in library"
       author = input("Author: ")
       path = input("Enter file path: ")
       title, bk_data = book, {"Author": author, "Path": path, "Available": True}
       self.lib.library[title]=bk_data
       self.lib.save()
       return "book added successfully"
# Interface
lib = Library()
user = User(lib)
admin = Admin(lib)
def get_book():
    bk = input("Enter book: ")
    return bk    
def choice():
    while True:
        try:
            choice = int(input("Select book: "))
            return choice
        except ValueError:
            print("Invalid option")
def library():
    while True:
            Ask = input("1.Read book/2.Return book/3.Exit: ")
            if  Ask == '1':
                book = get_book()
                print(user.search(book))
                if user.search(book):
                    print(user.read(choice(),book))
                else:
                    print("book not available")
            elif Ask == '2':
                book = get_book()
                print(user.search(book))
                if user.search(book):
                    print(user.replace(choice(),book))
                else:
                    print("book not found")
            elif Ask == '3':
                return
            else:
                print("invalid option")
def admin_menu():
    while True:
        cut = { '1':admin.catalogue, '2':admin.select_avl, '3':admin.select_unavl, '5':admin.add_book}
        Ask = input("1.Book Catalogue/2.Available books/3.Borrowed books/4.Modify books/5.Add books/6.Remove books/7.Exit: ")
        action = cut.get(Ask)
        if action:
            print(action())
        elif Ask == '4':
           print(admin.select_unavl())
           if admin.select_unavl():
               print(admin.modify(choice()))
           else:
               print("no unavailable books")
        elif Ask == '6':
           print(admin.catalogue())
           print(admin.remove(choice()))
        elif Ask == '7':
           return
        else:
           print("invalid option")   
def main():
    while True:
        print("WELCOME TO PROTOTYPE LIBRARY")
        menu = input("1.Library/2.Admin/3.Exit: ")
        if menu == '1':
            print(library())
        elif menu == '2':
            print(admin_menu())
        elif menu == '3':
            return "Thank you for using our library"
        else:
            print("invalid option")
print(main())