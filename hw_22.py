import sqlite3
from tkinter import *
from datetime import datetime

with sqlite3.connect('hw_21.db') as connection: # считываем из базы
    cur = connection.cursor()
    cur.execute(f"SELECT code, name FROM hotels")
    hotels = cur.fetchall()

    cur.execute(f"SELECT code, (last_name || ' ' || first_name) FROM guests")
    guests = cur.fetchall()

hotels_options = dict(hotels)
guests_options = dict(guests)
ariv_year_options = ['2019', '2020', '2021']
ariv_month_options = list([m for m in range(1, 13)])
ariv_day_options = list([d for d in range(1, 32)])
now = datetime.now().date()

def get_hotel_code(value):  # считываем выбор отеля
    global hotel_code
    for k, v in hotels_options.items():
        if v == str(value):
            hotel_code = k


def get_guest_code(value):  # считываем выбор гостя
    global guest_code
    for k, v in guests_options.items():
        if v == str(value):
            guest_code = k


def get_year(value):    # считываем выбор года
    global year
    year = value


def get_month(value):   # считываем выбор месяца
    global month
    month = value


def get_day(value): # считываем выбор дня
    global day
    day = value


# def print_values():
#     date = f"{year}-{month:02}-{day:02}"
#     print(now, guest_code, hotel_code, date, dayz.get())

def add_order():    # записываем ордер в базу
    with sqlite3.connect('hw_21.db') as connection:
        cur = connection.cursor()
        query = """
        INSERT INTO orders (order_date, guest_code, hotel_code, arival_date, days)
        VALUES (?, ?, ?, ?, ?);
        """
        date = f"{year}-{month:02}-{day:02}"
        cur.execute(query, (now, guest_code, hotel_code, date, dayz.get()))
        text.insert(1.0, 'Odrer added!')


def show_orders():  # показываем заказы гостя, выбранного в форме
    text.delete('1.0', END)
    with sqlite3.connect('hw_21.db') as connection:
        cur = connection.cursor()
        query = """
        SELECT guests.last_name, guests.first_name, hotels.name, orders.order_date, orders.arival_date, orders.days 
        FROM orders
        INNER JOIN guests ON orders.guest_code = guests.code
        INNER JOIN hotels ON orders.hotel_code = hotels.code
        WHERE orders.guest_code = ?;
        """
        cur.execute(query, (guest_code,))
        result = cur.fetchall()
        for line in result:
            var = f"Guest - {line[0]} {line[1]}: Hotel - {line[2]}, order date - {line[3]:10}, arival date - {line[4]:10}, days - {line[5]:3} \n"
            text.insert(1.0, var)


def show_hotel_info():  # показываем инфо отеля, выбранного в базе
    text.delete('1.0', END)
    with sqlite3.connect('hw_21.db') as connection:
        cur = connection.cursor()
        query = """
        SELECT name, stars, rooms, price 
        FROM hotels
        WHERE code = ?;
        """
        cur.execute(query, (hotel_code,))
        result = cur.fetchall()
        # print(result[0][1])
        # for line in range(len(result)):
        var = f"Hotel - {result[0][0]} has {result[0][1]} stars, {result[0][2]} rooms, each costs {result[0][3]} \n"
        text.insert(1.0, var)
            # print(line[0] line[1])


root = Tk()
root.title('Order form')
root.geometry('800x600')


slogan = Label(root, text="Adding orders", font="Arial 24")
slogan.grid(row=0, column=3, columnspan=2)


hotels_label = Label(root, text='Select hotel')
hotels_label.grid(row=1, column=1)

hotel_var = StringVar(root)
hotel_option = OptionMenu(root, hotel_var, *hotels_options.values(), command=get_hotel_code)
hotel_option.config(width=16)
hotel_option.grid(row=2, column=1, padx=10)


guests_label = Label(root, text='Select guest')
guests_label.grid(row=1, column=2)

guest_var = StringVar(root)
guest_option = OptionMenu(root, guest_var, *guests_options.values(), command=get_guest_code)
guest_option.config(width=16)
guest_option.grid(row=2, column=2)


ariv_year_label = Label(root, text='Select year')
ariv_year_label.grid(row=1, column=3)

ariv_year = StringVar(root)
ariv_year_option = OptionMenu(root, ariv_year, *ariv_year_options, command=get_year)
ariv_year_option.config(width=5)
ariv_year_option.grid(row=2, column=3)


ariv_month_label = Label(root, text='Select month')
ariv_month_label.grid(row=1, column=4)

ariv_month = StringVar(root)
ariv_month_option = OptionMenu(root, ariv_month, *ariv_month_options, command=get_month)
ariv_month_option.config(width=5)
ariv_month_option.grid(row=2, column=4)


ariv_day_label = Label(root, text='Select day')
ariv_day_label.grid(row=1, column=5)

ariv_day = StringVar(root)
ariv_day_option = OptionMenu(root, ariv_day, *ariv_day_options, command=get_day)
ariv_day_option.config(width=5)
ariv_day_option.grid(row=2, column=5)


days_label = Label(root, text='Quantity days')
days_label.grid(row=1, column=6)

dayz = IntVar(root)
dayz_entry = Entry(root, textvariable=dayz, width=4, font="Arial 12")
dayz_entry.grid(row=2, column=6)


add_order_button = Button(root, text="Add order", width=15, height=1, command=add_order)
add_order_button.grid(row=2, column=7, pady=10)


orders_by_guest_button = Button(root, text='Show orders', width=15, height=1, command=show_orders)
orders_by_guest_button.grid(row=4, column=2, pady=10, padx=20)


hotel_info_button = Button(root, text='Show hotel info', width=15, height=1, command=show_hotel_info)
hotel_info_button.grid(row=4, column=4, columnspan=2)


text = Text(root, height=20, width=70, wrap=WORD)
text.grid(row=6, column=1, columnspan=7, pady=10)

root.mainloop()

