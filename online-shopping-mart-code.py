                                              #IMPORT STATEMENTS
from abc import ABC, abstractmethod
import time as t
import sqlite3
from random import randint

                                      #CLASSES/FUNCTIONALITY OF THE CODE:


class Login:
    all_accounts = []

    def __init__(self, accounts):
        Login.all_accounts = accounts

    def login_choice(self):
        """This method lets the user choose if s/he wants to login as admin or customer"""
        
        print(f"Do you want to login as: \n1.) Admin. \n2.) Customer.")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            return 1
        if choice == 2:
            return 2

    def enter_email(self):
        """This method lets the user input his/her e-mail"""
        
        self.email = input("Enter email: ")

    def enter_password(self):
        """This method lets the user input his/her password"""
        
        self.password = input("Enter password: ")

    def confirm_login(self, choice):              # Have to pass login choice here
        """This method does two things:
            1. Checks if the user confirms and then account already exists and then logs into it
            by printing the respective statement.
            2. If the user doesn't confirm, it asks to change the attributes i.e 'password' and 'e-mail'."""
        print("Enter 'y' to confirm login: ", end=" ")
        confirmation = input()
        if confirmation.lower() == "y":
            flag = 0
            for acc in Login.all_accounts:
                if (self.email == acc[1]) and (self.password == acc[2]):
                    flag += 1

            if flag != 0:
                if choice == 1:
                    print("Admin Login successful.")
                    return True
                if choice == 2:
                    print("Customer Login successful.")
                    return True
            elif flag == 0:
                print("Login unsuccessful, account not found.")
                return False
        else:
            print("Do you want to change your email or password?(Y/N) ", end = "")
            choice_ip = input()
            if choice_ip.lower() == 'y':
                print(f"1.) Change email \n2.) Change password \n3.) Change both")
                choice_no = int(input("Choose choice number: "))
                if choice_no == 1:
                    self.enter_email()
                if choice_no == 2:
                    self.enter_password()
                if choice_no == 3:
                    self.enter_email()
                    self.enter_password()
                self.confirm_login(choice)
            if choice_ip.lower() != 'y':
                return False


class PasswordError(Exception):           # EXCEPTION CLASS
    """This is an exception class which is generated when the user inputs password whic doesn't fit in the
       criteria defined by the programmer."""
    def __init__(self):
        super().__init__("Length should be between 8-10. \nNo special characters allowed. \nPassword must have at least 1 digit.")

class DuplicateError(Exception):        # EXCEPTION CLASS
    """This is an exception class which is generated when the user inputs data which already exists in the
       ".db" files."""
    def __init__(self):
        super().__init__("Input already exists.")


class Signup:
    accounts_data = sqlite3.connect("accounts.db")
    a = accounts_data.cursor()

    @classmethod
    def update_data(cls, self_obj_info):
        """This method updates the list and adds up another entry in 'accounts.db'"""
        with Signup.accounts_data:
            Signup.a.execute("INSERT INTO accounts VALUES (:name, :email,:passw)",
                             {"name": self_obj_info[0], "email": self_obj_info[1], "passw": self_obj_info[2]})

    @classmethod
    def get_all_data(cls):
        """This method fetches all the previous data from 'accounts.db'"""
        Signup.a.execute("SELECT * FROM accounts")
        return Signup.a.fetchall()

    def __init__(self):
        self.info = []

    def input_name(self):
        """This method lets the user to input its name."""
        self.username = input("Enter username: ")

    def input_email(self):
        """This method lets the user to input its e-mail."""
        self.email = input("Enter email: ")

    def input_password(self):
        """The method lets the user input its password."""
        self.password = input("Enter password: ")

    def check_name(self):
        '''This method checks if the current name entered by the user doesn't already exist in "accounts.db"
            if it does, it raises a "DuplicateError"'''
        all_accounts = Signup.get_all_data()
        temp = True
        while temp:
            try:
                flag = 0
                for acc in all_accounts:
                    if self.username == acc[0]:
                        flag += 1
                if flag != 0:
                    raise DuplicateError
                elif flag == 0:
                    self.info.append(self.username)
                    temp = False
            except DuplicateError as De:
                print(De)
                self.input_name()

    def check_email(self):
        '''This method checks if the current e-mail entered by the user doesn't already exist in "accounts.db"
            if it does, it raises a "DuplicateError"'''
        all_accounts = Signup.get_all_data()
        temp = True
        while temp:
            try:
                flag = 0
                for acc in all_accounts:
                    if self.email == acc[1]:
                        flag += 1
                if flag != 0:
                    raise DuplicateError
                elif flag == 0:
                    self.info.append(self.email)
                    temp = False
            except DuplicateError as De:
                print(De)
                self.input_email()

    def check_password(self):
        '''This method checks if the password input by the user fits into a certain criteria, if it does
            not fit in the criteria, it raises a "PasswordError"'''
        temp = True
        while temp:
            try:
                flag = 0
                for i in self.password:
                    if i in "0123456789":
                        flag = 1
                if not(10 >= len(self.password) >= 8) or not(self.password.isalnum()) or flag == 0:
                    raise PasswordError
                else:
                    self.info.append(self.password)
                    temp = False
            except PasswordError as passe:
                print(passe)
                self.input_password()

    def confirmation(self):
        """This method confirms and then updates the data in 'accounts.db'."""
        confirmation = input("Enter 'y' to confirm creating the account: ")
        if confirmation.lower() == 'y':
            Signup.update_data(self.info)
            print("Signup Successful.")
            return True
        else:
            return False



class MainWindow:
    def __init__(self):
        print(f"{' '*17}HELLO")
        print(f"{' '*5}Welcome to the THE MILKY DAIRIES")
        print()

    def login(self, accounts):
        """The method triggers the "Login" class."""
        self.L = Login(accounts)

    def signup(self):
        """This method triggers the "Signup" class."""
        self.S = Signup()

        

class Order:
        def __init__(self):
            self.placement_time = t.time()
            PD = t.localtime(self.placement_time)
            self.placement_date = f"{PD.tm_mday} - {PD.tm_mon} - {PD.tm_year}"

        def get_history_and_balance(self, history, balance):      
            """This method takes the "balance" and "history" from the "Customer" class and
            then initiates the order number of the customer."""
            self.userbalance = balance
            self.customer_history = history
            if len(self.customer_history) == 0:
                self.order_no = 1
            else:
                last_order = self.customer_history[-1]
                self.order_no = last_order[1] + 1
                
        def check_total_price(self, shopping_cart):         
            """This method takes what "get_current_user_cart" in class "ShoppingCart" returns and
            prints the whole cart and its price and also checks if the user balance is sufficient or
            insufficient for this purchase."""
            self.cart = shopping_cart
            self.total_price = 0
            table = []
            for item in self.cart:
                price_of_item = float(item[3])*int(item[4])
                table.append([item[2], item[3], item[4], price_of_item])
                self.total_price += price_of_item
            print(f"Your email is: {self.cart[0][0]}")
            print(f"Your cart id is: {self.cart[0][1]}")
            print(f"Your total price for all the items is: {self.total_price}")
            string = "Item Name" + " " * 16 + "Price" + " " * 5 + "Quantity" + " " * 2 + "Total of Item" + " " * 2
            for item in table:
                string += f"\n{item[0]:25}{item[1]:5}{item[2]:10}{item[3]:15}"
            print(string)


            if self.userbalance >= self.total_price:
                print("Your current balance is sufficient for all the items in your cart")
                return True
            else:                          
                print("Your current balance is insufficient for all the items in your cart")
                return False

        def update_customerHistory(self):
            """This method updates the "customer_history.db" by inputting the respective attributes to
            the respective columns in our database."""
            all_items = []
            email = self.cart[0][0]
            for item in self.cart:
                a = [f"{item[2]};{item[4]}"]
                all_items.append(str(a))
            with Customer.customers_history:
                Customer.c.execute("INSERT INTO History VALUES (?,?,?)",
                                   (email, self.order_no, str(all_items)))

        def update_productList(self):
            """This method updates the quantity of the no. of products that can be purchased after a
            customer had just finished purchasing something."""
            for product in self.cart:
                item = product[2]
                quantity = product[4]
                ProductList.p.execute("SELECT * FROM Products WHERE (Name = :item)", {'item': item})
                results = ProductList.p.fetchall()
                quantity = results[0][2] - quantity
                with ProductList.product_data:
                    ProductList.p.execute("UPDATE Products SET Quantity = :quantity WHERE Name = :item",
                                          {'quantity': quantity, 'item': item})

        def confirm_order(self):
            """This method, if the order is confirmed, triggers the 'update_productList' and
            'update_customerHistory' to do its respective functions and prints the delivery and
            shipping time and date."""
            print(f"Enter 'y' to confirm your order: ", end="")
            confirmation = input()
            if confirmation.lower() == 'y':
                self.update_productList()
                self.update_customerHistory()
                shipping_time = self.placement_time + (86400 * 3)
                delievery_time = self.placement_time + (86400 * 5)
                SD = t.localtime(shipping_time)
                self.shipping_date = f"{SD.tm_mday} - {SD.tm_mon} - {SD.tm_year}"
                DD = t.localtime(delievery_time)
                self.delievery_date = f"{DD.tm_mday} - {DD.tm_mon} - {DD.tm_year}"
                return True
            else:
                return False

            

class Customer:
    customers_history = sqlite3.connect("customer_history.db")
    c = customers_history.cursor()

    @classmethod
    def get_all_data(cls):
        """This method fetches all the data from 'customer_history.db'."""
        Customer.c.execute("SELECT * FROM History")
        return Customer.c.fetchall()

    def __init__(self, email):    # association bw login and customer
        self.current_userEmail = email   # e-mail of "Login" class
        self.current_balance = None
        self.credit_card = None
        self.order = Order()

    def input_balance(self):
        """This method lets the user input their balance in their bank account."""
        self.current_balance = float(input("Enter your balance: "))

    def input_creditCard(self):
        """This method lets the user input their credit card number."""
        self.credit_card = input("Enter your credit card number: ")

    @staticmethod
    def search(productList):                  
        """This method uses the "product list" of class "Admin" and then lets the user search for a
        particular product and if found, then displays its name, price and quantity."""
        item = input("Enter item you want to search: ")
        results = []
        for product in productList:
            if item in product[0]:
                results.append(product)

        if len(results) != 0:
            string = "Item Name" + " " * 16 + "Price" + " " * 5 + "Stock" + " " * 5
            for item in results:
                string += f"\n{item[0]:25}{item[1]:5}{item[2]:10}"
            print(string)
        else:
            print("No items match your search")

    def get_current_user_orders(self):
        """This method lets the user review its past history if s/he ever purchased before."""
        with Customer.customers_history:
            Customer.c.execute("SELECT * FROM History WHERE Customer_email = :email", {'email': self.current_userEmail})
            return Customer.c.fetchall()

    def view_history(self):
        """This method shows the history of the customer in table format."""
        with Customer.customers_history:
            Customer.c.execute("SELECT * FROM History WHERE Customer_email = :email", {'email': self.current_userEmail})
            results = Customer.c.fetchall()

        if len(results) == 0:
            print("You do not have any previous order history.")
        else:
            print(f"Your email is: {results[0][0]}")
            for item in results:
                string = "Item Name" + " " * 16 + "Quantity" + " "
                items_of_order = []
                print(f"ORDER NUMBER: {item[1]}")
                items_ordered = item[2].split(",")

                for one_item in items_ordered:
                    new = ''
                    for char in one_item:
                        if (char == "]") or (char == "[") or (char == "'") or (char == '"') or (char == " "):
                            pass
                        else:
                            new += char
                    items_of_order.append(new)

                for info in items_of_order:
                    info = info.split(";")
                    string += f"\n{info[0]:25}{info[1]:8}"
                print(string)

class ProductList(ABC):
    product_data = sqlite3.connect("products.db")
    p = product_data.cursor()

    @classmethod
    def get_all_data(cls):
        """This class method fetches the data from the 'products.db'."""
        with ProductList.product_data:
            ProductList.p.execute("SELECT * FROM products")
            return ProductList.p.fetchall()


    @abstractmethod
    def add_product(self): # An abstract method whose implementation is in given in class "Admin"
        pass

    @abstractmethod
    def remove_product(self): # An abstract method whose implementation is in given in class "Admin" 
        pass


class ShoppingCart:
    shopping_cart = sqlite3.connect("shopping_cart.db")
    s = shopping_cart.cursor()

    @classmethod
    def delete_cart(cls, email):
        """This method deletes the cart of the customer whose email is passed."""
        with ShoppingCart.shopping_cart:
            ShoppingCart.s.execute("DELETE FROM Customer_cart WHERE Customer_email = :email", {'email': email})

    def __init__(self, email, productList):
        self.current_userEmail = email    #e-mail of "Login" class
        self.strForADD = "-"   # sole purpose to add this as an 'attr' was to use it for operator overloading
        self.products = productList
        self.ID = randint(100, 1000)

    def show_products(self):
        """ This method basically pretty prints our product list/menu items."""
        string = "Item Name"+" "*16+"Price"+" "*5+"Stock"+" "*5
        for item in self.products:
            string += f"\n{item[0]:25}{item[1]:5}{item[2]:10}"
        return string

    def add_product(self):
        """This method lets the user to input item(s) in his/her shopping cart and then returns a list of it."""
        print()
        print("Product List And Information: ")
        print(self.show_products())
        print()
        print(f"Enter product name to add: ", end="")
        product = input()
        print(f"Enter quantity: ", end="")
        quantity = int(input())
        print()
        return [product, quantity]

    def __add__(self, lst):    # list of product and quantity return from add_product()
        """This dunder method is overriden. It basically selects the product from the "products.db" entered
        by the user and adds that in the shopping cart list."""
        ProductList.p.execute("SELECT * FROM Products WHERE name = :item", {'item': lst[0]})
        result = ProductList.p.fetchall()
        price = result[0][1]
        with ShoppingCart.shopping_cart:
            ShoppingCart.s.execute("INSERT INTO Customer_cart VALUES (?,?,?,?,?)", (self.current_userEmail, self.ID, lst[0], price, lst[1]))
        return f"Item Name: \n{self.strForADD}{lst[0]} \nItem Quantity: \n{self.strForADD}{lst[1]} \n\tItem Added Successfully."

    def remove_product(self):
        """This method lets the user remove item(s) from a shopping cart and returns that product as a str."""
        print("Shopping Cart And Information: ")
        self.show_cart()
        print(f"Enter product name to remove: ", end="")
        product = input()
        return product

    def __sub__(self, product_name):        # product name from remove_product()
        """This dunder method is overidden. It basically deletes the product from the "products.db" entered\
        by the user and removes that from the shopping cart."""
        with ShoppingCart.shopping_cart:
            ShoppingCart.s.execute("DELETE FROM Customer_cart WHERE Item_name = :name", {'name': product_name})
        return f"{self.strForADD}{product_name} has been successfully removed from your cart."

    def get_current_user_cart(self):
        """This method takes the e-mail of the user and then searches it in the "shopping_cart.db" and
        fetches all the data of the shopping cart of the current user."""
        ShoppingCart.s.execute("SELECT * FROM Customer_cart WHERE Customer_email = :email", {'email': self.current_userEmail})
        return ShoppingCart.s.fetchall()

    def show_cart(self):
        """This method shows the cart in a table format."""
        with Customer.customers_history:
            ShoppingCart.s.execute("SELECT * FROM Customer_cart WHERE Customer_email = :email", {'email': self.current_userEmail})
            results = ShoppingCart.s.fetchall()
        email = results[0][0]
        cart_no = results[0][1]
        string = "Item Name" + " " * 16 + "Price" + " " * 5 + "Quantity" + " " * 2
        for item in results:
            string += f"\n{item[2]:25}{item[3]:5}{item[4]:10}"
        print(string)


class Admin(ProductList):
    customer_history = ""
    customer_accounts = ""

    def __init__(self): 
        with Signup.accounts_data:
            Signup.a.execute("SELECT * FROM accounts")
            accounts = Signup.a.fetchall()

        string = "Username" + " " * 17 + "Email" + " " * 30 + "Password" + " " * 12
        for acc in accounts:
            string += f"\n{acc[0]:25}{acc[1]:35}{acc[2]:20}"
        Admin.customer_accounts += string

        with Customer.customers_history:
            Customer.c.execute("SELECT * FROM History")
            history = Customer.c.fetchall()
        string = "Email" + " " * 30 + "Order" + " " * 5 + "Items;Quantity" + " " * 100
        for record in history:
            string += f"\n{record[0]:35}{str(record[1]):10}{record[2]:200}"
        Admin.customer_history += string

    def add_product(self):
        """This method lets the admin user to add more products in "products.db" by taking input from the
        admin user of "name","quantity", and "price" of the product."""
        while True:
            print(f"Enter product name to add, press 'e' to exit: ", end="")
            product = input()
            if product.lower() == 'e':
                break
            else:
                print(f"Enter quantity available for {product}: ", end="")
                quantity = int(input())
                print(f"Enter price for {product}: ", end="")
                price = float(input())

                with ProductList.product_data:
                    ProductList.p.execute("INSERT INTO products VALUES (?,?,?)", (product, price, quantity))

    def remove_product(self):
        """This method lets the admin user by entering the name of the specific item and the code itself
        accesses the "products.db" and searches the name and deletes the record of that specific item."""
        while True:
            print(f"Enter product name to remove, press 'e' to exit: ", end="")
            product = input()
            if product.lower() == 'e':
                break
            else:
                with ProductList.product_data:
                    ProductList.p.execute("DELETE FROM products WHERE Name = :name", {'name': product})

    @classmethod
    def get_accounts(cls):
        """This method lets the admin user to access all the older accounts that are stored in the
        database 'accounts.db'."""
        accounts_data = sqlite3.connect("accounts.db")
        a = accounts_data.cursor()
        Signup.a.execute("SELECT * FROM accounts")
        return Signup.a.fetchall()

    @classmethod
    def get_history(cls):
        """This method lets the admin user to access all the customer info and history that are stored in
        the database 'customer_history.db'."""
        customers_history = sqlite3.connect("customer_history.db")
        c = customers_history.cursor()
        Customer.c.execute("SELECT * FROM History")
        return Customer.c.fetchall()

    def view_products(self, productList):
        """This method shows products in table format."""
        string = "Item Name"+" "*16+"Price"+" "*5+"Stock"+" "*5
        for item in productList:
            string += f"\n{item[0]:25}{item[1]:5}{item[2]:10}"
        return string


                         #DRIVER CODE/CREATION OF OBJECTS AND CALLING OF FUNCTIONS:
Main = MainWindow()
Main.signup()                   
all_accounts = Signup.get_all_data()      
products = ProductList.get_all_data()

while True:
    print(f"Do you want to: \n1.) Login. \n2.) Signup. \n3.) Exit.")
    print()
    choice = int(input("Enter your choice: "))
    print()
    if choice == 1:
        Main.login(all_accounts)
        login_choice = Main.L.login_choice()

        if login_choice == 1:
            print()
            Main.L.enter_email()
            Main.L.enter_password()
            Main.L.confirm_login(login_choice)
            A = Admin()

            while True:
                print()
                print(f'''You have the following options as an Admin
                            1.) See all the registered accounts.
                            2.) See all customers history.
                            3.) See all products.
                            4.) Add a product.
                            5.) Remove a product.
                            6.) Logout.''')
                choice = int(input("Enter your choice: "))
                print()
                if choice == 6:
                    break
                if choice == 1:
                    print(Admin.customer_accounts)
                if choice == 2:
                    print(Admin.customer_history)
                if choice == 3:
                    results = Admin.get_all_data()
                    print(A.view_products(results))
                if choice == 4:
                    A.add_product()
                if choice == 5:
                    A.remove_product()
                if choice == 6:
                    del Main.L

        if login_choice == 2:
            print()
            Main.L.enter_email()
            Main.L.enter_password()
            Main.L.confirm_login(login_choice)
            C = Customer(Main.L.email)
            print()
            print(f'''Please enter the following data:
                        1.) Current Balance.
                        2.) Credit Cart Number.''')
            C.input_balance()
            C.input_creditCard()
            history = C.get_current_user_orders()

            while True:
                print()
                print(f'''You can do the following things:
                            1.) View all the products.
                            2.) Search for a specific product.
                            3.) Add a product in your cart.
                            4.) Remove a product from your cart. (i.e, if you already added at least 1)
                            5.) Show cart.
                            6.) Check total price of your cart.
                            7.) View your previous history.
                            8.) Checkout.''')
                S = ShoppingCart(Main.L.email, products)
                C.order.get_history_and_balance(history, C.current_balance)
                choice = int(input("Enter your choice: "))
                print()
                if choice == 1:
                    print(S.show_products())
                if choice == 2:
                    Customer.search(products)
                if choice == 3:
                    lst = S.add_product()
                    print(S + lst)
                if choice == 4:
                    lst = S.remove_product()
                    print(S - lst)
                if choice == 5:
                    S.show_cart()
                if choice == 6:
                    cart = S.get_current_user_cart()
                    C.order.check_total_price(cart)
                if choice == 7:
                    C.view_history()
                if choice == 8:
                    print(f"Placement Date: {C.order.placement_date}")
                    C.order.confirm_order()
                    ShoppingCart.delete_cart(Main.L.email)
                    print(f"Shipping Date: {C.order.shipping_date}")
                    print(f"Delivery Date: {C.order.delievery_date}")
                    print()
                    break

    if choice == 2:
        Main.S.input_name()
        Main.S.check_name()
        Main.S.input_email()
        Main.S.check_email()
        Main.S.input_password()
        Main.S.check_password()
        Main.S.confirmation()
        print()

    if choice == 3:
        print('''        Thankyou for shopping at THE MILKY DAIRIES.
                 Hope you visit again.''')
        print('x'*100)
        break