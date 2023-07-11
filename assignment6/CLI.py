import mysql.connector
from sqlalchemy import create_engine
import pandas as pd



mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="Samridh!2qwaszx",
  database="demo1"
)
cursor=mydb.cursor()


def displayMainMenu():
    print( "— — — — MENU — — — -")
    print(" 1. Enter as Admin")
    print(" 2. Enter as customer")
    print(" 3. Exit")
    print( " — — — — — — — — — — " )
    c=int(input("Enter choice : "))
    if c==1:
        adminmenu()
    if c==2:
        customermenu()
    if c==3:
        exit()
    else:
        print("Enter Valid choice!")
        displayMainMenu()
    
def customermenu():
    print("""  1. Sign up
  2. Log in   
  3. back""")
    c=int(input("Enter Choice : "))
    if c==1:
        signup()
    if c==2:
        email=input("Enter email id : ")
        password=input("Enter password: ")
        cursor.execute("select * from customer where customer_email='{a}' and customer_password='{b}';".format(a=email,b=password))
        result=cursor.fetchall()
        if len(result)!=0:
            login(result[0])
        else:
            print("Wrong cridentials")
            customermenu()

    if c==3:
        displayMainMenu()
    else:
        print("Enter valid choice!")
        customermenu()

def signup():
    name=input("Enter Name : ")
    email=input("Enter email : ")
    password=input("Enter password : ")
    address=input("Enter address : ")
    age=input("Enter age : ")
    num=input("Enter number : ")
    paydet=input("Enter payment Details: ")
    query="insert into customer(customer_name, customer_email, customer_address, customer_age, customer_number, customer_paymentDetails, customer_password) values('{a}', '{b}','{c}',{d},'{e}','{f}','{g}')".format(a=name,b=email,c=address,d=age,e=num,f=paydet,g=password)
    cursor.execute(query)
    
    query="select * from customer where customer_name='{a}'".format(a=name)
    a=cursor.execute(query)
    r=cursor.fetchall()
    c_id=r[0]
    print(c_id)
    query="insert into cart(cart_id, customer_id, item_count, total_cost) values({a},{a},0,0)".format(a=r[0][0])
    a=cursor.execute(query)
    mydb.commit()
    login(c_id)

def login(tup):
    print("Welcome {a} !".format(a=tup[1]))
    print(""" 1. view Cart
 2. view products
 3. checkout
 4. logout
    """)
    c=int(input("Enter Choice : "))
    if c==1:
        viewcart(tup[0],tup)
        login(tup)
    if c==2:
        viewproducts(tup)
        login(tup)
    if c==3:
        checkout(tup[0],tup)
        login(tup)
    if c==4:
        customermenu()

def viewcart(customer_id,tup):
    query="select p.product_id, p.product_name from product p JOIN cart_product cp on p.product_id = cp.product_id where cp.cart_id={a};".format(a=customer_id)
    a=cursor.execute(query)
    r=cursor.fetchall()
    for row in r:
        print(row)
    

def viewproducts(tup):
    query="select * from product"
    a=cursor.execute(query)
    result=cursor.fetchall()
    for row in result:
        print(row)
    product_to_cart(tup[0],tup)

def product_to_cart(cart_id,tup):
    print("""
 1. add product to cart with product_id
 2. Back
    """)
    c=int(input("Enter choice: "))
    if c==1:
        p=input("Enter product ID : ")
        query="insert into cart_product(cart_id, product_id) values({a},{b})".format(a=cart_id,b=p)
        a=cursor.execute(query)
        query="select product_price from product where product_id={a}".format(a=p)
        a=cursor.execute(query)
        results=cursor.fetchall()
        price=int(results[0][0])
        query="update cart set item_count=item_count+1, total_cost=total_cost+{a} where cart_id={b}".format(a=price,b=cart_id)
        a=cursor.execute(query)
        mydb.commit()
        product_to_cart(cart_id,tup)
    if c==2:
        login(tup)

def checkout(customer_id,tup):
    viewcart(customer_id,tup)
    query="select total_cost from cart where customer_id={a}".format(a=customer_id)
    a=cursor.execute(query)    
    result=cursor.fetchall()
    total_amount=result[0][0]
    print("Your total cost of the order : ",total_amount)
    choice=input("Do you want to place order (Y/N) : ")
    if choice=='Y':
        method=input("Enter payment method : ")
        query="select delivery_partner_id from delivery_partner where status<>'Unavailable' and status<>'At capacity' limit 1;"
        cursor.execute(query)
        result=cursor.fetchall()
        dp_id=result[0][0]
        query="insert into payment(mode, details, order_id, customer_id, time_date) values('{a}','{b}',NULL, {c},NOW())".format(a=method,b=tup[6],c=customer_id)
        cursor.execute(query)
        
        query="select payment_id from payment where customer_id={a}".format(a=customer_id)
        cursor.execute(query)
        result=cursor.fetchall()
        payment_id=result[0][0]
        query="insert into orders(order_id, delivery_partner_id, customer_id, retailer_id, payment_id, time_date, status, cart_id, total_cost) values ({a},{b},{c},{d},{e},{f},'{g}',{h},{i})".format(a=payment_id,b=dp_id,c=customer_id,d=4,e=payment_id,f="NOW()",g="dispatched",h=customer_id,i=total_amount)
        cursor.execute(query)
        
        query="update cart set item_count=0, total_cost=0 where customer_id={a}".format(a=customer_id)
        cursor.execute(query)
        
        query="delete from cart_product where cart_id={a}".format(a=customer_id)
        cursor.execute(query)
        mydb.commit()
        print("Order placed, Keep checking mail for further details! \n Thank You!")
    login(tup)
    



def adminmenu():
    print("""
  1. All orders 
  2. add delivery agents 
  3. add categories 
  4. add products
  5. change price
  6. back
        """)
    c=int(input("Enter Choice : "))
    if c==1:
        allorders()
    if c==3:
        addCategory()
    if c==4:
        addproduct()
    if c==2:
        addDA()
    if c==5:
        changeprice()
    if c==6:
        displayMainMenu()
    else:
        print("Enter valid choice!")
        adminmenu()

def allorders():
    query="select * from orders"
    cursor.execute(query)
    result=cursor.fetchall()
    for row in result:
        print(row)    

def addDA():
    type=input("Enter type of partner : ")
    retailer=input("enter retailer_ID of partner : ")

    query="insert into delivery_partner (type, status, order_id, retailer_id) values('{t}','available',NULL,{a})".format(a=retailer,t=type)
    cursor.execute(query)
    

def addCategory():
    name=input("Enter name of category : ")
    query="insert into category (catregory_name) values('{t}')".format(t=name)
    cursor.execute(query)
    

def addproduct():
    name=input("Enter name of product : ")
    cat=input("Enter category ID : ")
    price=input("Enter Price : ")
    ret=input("Enter retailer ID : ")
    det=input("Enter details : ")
    query="insert into product(product_name, category_id, product_price, retailer_id, details) values ('{a}',{b},{c},{d},'{e}')".format(a=name,b=cat,c=price,d=ret,e=det)
    cursor.execute(query)

def changeprice():
    product=input("Enter product ID : ")
    newp=input("Enter new price : ")
    query="update product set product_price={a} where product_id={b}".format(a=newp,b=product)
    cursor.execute(query)


displayMainMenu()
# query="select total_cost from cart where customer_id=1"
# a=cursor.execute(query)    
# result=cursor.fetchall()
# total_amount=result[0][0]

# print(total_amount)


mydb.commit()