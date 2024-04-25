import sqlite3
import os


database_name = "salon_database.db"
database_path = f"databases/{database_name}"

if os.path.exists(database_path):
    os.remove(database_path)

# Создание соединения с базой данных
conn = sqlite3.connect(database_path)
cursor = conn.cursor()

# Создание таблиц
cursor.execute(
    """
CREATE TABLE Customer (
    customer_id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    phone_number TEXT,
    birthdate DATE
)
"""
)

cursor.execute(
    """
CREATE TABLE Employee (
    employee_id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    phone_number TEXT,
    role_id INTEGER,
    FOREIGN KEY (role_id) REFERENCES Role(role_id)
)
"""
)

cursor.execute(
    """
CREATE TABLE Role (
    role_id INTEGER PRIMARY KEY,
    role_name TEXT
)
"""
)

cursor.execute(
    """
CREATE TABLE ServiceCategory (
    category_id INTEGER PRIMARY KEY,
    category_name TEXT
)
"""
)

cursor.execute(
    """
CREATE TABLE Service (
    service_id INTEGER PRIMARY KEY,
    category_id INTEGER,
    service_name TEXT,
    description TEXT,
    price REAL,
    FOREIGN KEY (category_id) REFERENCES ServiceCategory(category_id)
)
"""
)

cursor.execute(
    """
CREATE TABLE Appointment (
    appointment_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    employee_id INTEGER,
    service_id INTEGER,
    appointment_date DATE,
    appointment_time TIME,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    FOREIGN KEY (employee_id) REFERENCES Employee(employee_id),
    FOREIGN KEY (service_id) REFERENCES Service(service_id)
)
"""
)

cursor.execute(
    """
CREATE TABLE Payment (
    payment_id INTEGER PRIMARY KEY,
    appointment_id INTEGER,
    amount REAL,
    payment_date DATE,
    FOREIGN KEY (appointment_id) REFERENCES Appointment(appointment_id)
)
"""
)

cursor.execute(
    """
CREATE TABLE Feedback (
    feedback_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    employee_id INTEGER,
    service_id INTEGER,
    rating INTEGER,
    comments TEXT,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    FOREIGN KEY (employee_id) REFERENCES Employee(employee_id),
    FOREIGN KEY (service_id) REFERENCES Service(service_id)
)
"""
)

cursor.execute(
    """
CREATE TABLE Inventory (
    inventory_id INTEGER PRIMARY KEY,
    item_name TEXT,
    quantity_available INTEGER,
    price_per_unit REAL
)
"""
)

cursor.execute(
    """
CREATE TABLE InventoryTransaction (
    transaction_id INTEGER PRIMARY KEY,
    inventory_id INTEGER,
    employee_id INTEGER,
    transaction_date DATE,
    transaction_type TEXT,
    quantity INTEGER,
    total_cost REAL,
    FOREIGN KEY (inventory_id) REFERENCES Inventory(inventory_id),
    FOREIGN KEY (employee_id) REFERENCES Employee(employee_id)
)
"""
)

cursor.execute(
    """
CREATE TABLE Discount (
    discount_id INTEGER PRIMARY KEY,
    service_id INTEGER,
    discount_percentage REAL,
    FOREIGN KEY (service_id) REFERENCES Service(service_id)
)
"""
)

cursor.execute(
    """
CREATE TABLE Promotion (
    promotion_id INTEGER PRIMARY KEY,
    promotion_name TEXT,
    start_date DATE,
    end_date DATE,
    description TEXT
)
"""
)

cursor.execute(
    """
CREATE TABLE Reservation (
    reservation_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    appointment_id INTEGER,
    reservation_date DATE,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    FOREIGN KEY (appointment_id) REFERENCES Appointment(appointment_id)
)
"""
)

cursor.execute(
    """
CREATE TABLE Attendance (
    attendance_id INTEGER PRIMARY KEY,
    employee_id INTEGER,
    date DATE,
    time_in TIME,
    time_out TIME,
    FOREIGN KEY (employee_id) REFERENCES Employee(employee_id)
)
"""
)

cursor.execute(
    """
CREATE TABLE SalonLocation (
    location_id INTEGER PRIMARY KEY,
    location_name TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT
)
"""
)

cursor.execute(
    """
CREATE TABLE Transactions (
    transaction_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    transaction_date DATE,
    transaction_type TEXT,
    amount REAL
)
"""
)

cursor.execute(
    """
CREATE TABLE Expense (
    expense_id INTEGER PRIMARY KEY,
    expense_date DATE,
    expense_category TEXT,
    amount REAL,
    description TEXT
)
"""
)

cursor.execute(
    """
CREATE TABLE Commission (
    commission_id INTEGER PRIMARY KEY,
    employee_id INTEGER,
    appointment_id INTEGER,
    commission_amount REAL,
    commission_date DATE,
    FOREIGN KEY (employee_id) REFERENCES Employee(employee_id),
    FOREIGN KEY (appointment_id) REFERENCES Appointment(appointment_id)
)
"""
)

# Заполнение таблиц данными
# Customer
cursor.execute(
    "INSERT INTO Customer (name, email, phone_number, birthdate) VALUES ('Alice', 'alice@example.com', '1234567890', '1990-05-15')"
)
cursor.execute(
    "INSERT INTO Customer (name, email, phone_number, birthdate) VALUES ('Bob', 'bob@example.com', '9876543210', '1985-08-22')"
)
cursor.execute(
    "INSERT INTO Customer (name, email, phone_number, birthdate) VALUES ('Charlie', 'charlie@example.com', '5556667777', '1998-02-10')"
)
cursor.execute(
    "INSERT INTO Customer (name, email, phone_number, birthdate) VALUES ('David', 'david@example.com', '3332221111', '1976-11-30')"
)
cursor.execute(
    "INSERT INTO Customer (name, email, phone_number, birthdate) VALUES ('Eve', 'eve@example.com', '4445556666', '2000-07-07')"
)

# Employee
cursor.execute(
    "INSERT INTO Employee (name, email, phone_number, role_id) VALUES ('Employee1', 'employee1@example.com', '1112223333', 1)"
)
cursor.execute(
    "INSERT INTO Employee (name, email, phone_number, role_id) VALUES ('Employee2', 'employee2@example.com', '4445556666', 2)"
)
cursor.execute(
    "INSERT INTO Employee (name, email, phone_number, role_id) VALUES ('Employee3', 'employee3@example.com', '7778889999', 1)"
)
cursor.execute(
    "INSERT INTO Employee (name, email, phone_number, role_id) VALUES ('Employee4', 'employee4@example.com', '1231231234', 3)"
)
cursor.execute(
    "INSERT INTO Employee (name, email, phone_number, role_id) VALUES ('Employee5', 'employee5@example.com', '9998887777', 2)"
)

# Role
cursor.execute("INSERT INTO Role (role_name) VALUES ('Manager')")
cursor.execute("INSERT INTO Role (role_name) VALUES ('Stylist')")
cursor.execute("INSERT INTO Role (role_name) VALUES ('Receptionist')")

# ServiceCategory
cursor.execute("INSERT INTO ServiceCategory (category_name) VALUES ('Hair')")
cursor.execute("INSERT INTO ServiceCategory (category_name) VALUES ('Nails')")
cursor.execute("INSERT INTO ServiceCategory (category_name) VALUES ('Spa')")
cursor.execute("INSERT INTO ServiceCategory (category_name) VALUES ('Makeup')")
cursor.execute("INSERT INTO ServiceCategory (category_name) VALUES ('Massage')")

# Service
cursor.execute(
    "INSERT INTO Service (category_id, service_name, description, price) VALUES (1, 'Haircut', 'Basic haircut', 30.0)"
)
cursor.execute(
    "INSERT INTO Service (category_id, service_name, description, price) VALUES (2, 'Manicure', 'Nail grooming', 20.0)"
)
cursor.execute(
    "INSERT INTO Service (category_id, service_name, description, price) VALUES (3, 'Facial', 'Skin treatment', 50.0)"
)
cursor.execute(
    "INSERT INTO Service (category_id, service_name, description, price) VALUES (4, 'Makeup Application', 'Event makeup', 40.0)"
)
cursor.execute(
    "INSERT INTO Service (category_id, service_name, description, price) VALUES (5, 'Swedish Massage', 'Relaxing massage', 60.0)"
)

# Appointment
cursor.execute(
    "INSERT INTO Appointment (customer_id, employee_id, service_id, appointment_date, appointment_time) VALUES (1, 1, 1, '2022-10-15', '10:00')"
)
cursor.execute(
    "INSERT INTO Appointment (customer_id, employee_id, service_id, appointment_date, appointment_time) VALUES (2, 2, 2, '2022-10-16', '11:30')"
)
cursor.execute(
    "INSERT INTO Appointment (customer_id, employee_id, service_id, appointment_date, appointment_time) VALUES (3, 3, 3, '2022-10-17', '13:00')"
)
cursor.execute(
    "INSERT INTO Appointment (customer_id, employee_id, service_id, appointment_date, appointment_time) VALUES (4, 4, 4, '2022-10-18', '15:30')"
)
cursor.execute(
    "INSERT INTO Appointment (customer_id, employee_id, service_id, appointment_date, appointment_time) VALUES (5, 5, 5, '2022-10-19', '17:00')"
)

# Payment
cursor.execute(
    "INSERT INTO Payment (appointment_id, amount, payment_date) VALUES (1, 30.0, '2022-10-15')"
)
cursor.execute(
    "INSERT INTO Payment (appointment_id, amount, payment_date) VALUES (2, 20.0, '2022-10-16')"
)
cursor.execute(
    "INSERT INTO Payment (appointment_id, amount, payment_date) VALUES (3, 50.0, '2022-10-17')"
)
cursor.execute(
    "INSERT INTO Payment (appointment_id, amount, payment_date) VALUES (4, 40.0, '2022-10-18')"
)
cursor.execute(
    "INSERT INTO Payment (appointment_id, amount, payment_date) VALUES (5, 60.0, '2022-10-19')"
)

# Feedback
cursor.execute(
    "INSERT INTO Feedback (customer_id, employee_id, service_id, rating, comments) VALUES (1, 1, 1, 4, 'Great haircut!')"
)
cursor.execute(
    "INSERT INTO Feedback (customer_id, employee_id, service_id, rating, comments) VALUES (2, 2, 2, 5, 'Amazing manicure!')"
)
cursor.execute(
    "INSERT INTO Feedback (customer_id, employee_id, service_id, rating, comments) VALUES (3, 3, 3, 4, 'Very relaxing facial.')"
)
cursor.execute(
    "INSERT INTO Feedback (customer_id, employee_id, service_id, rating, comments) VALUES (4, 4, 4, 3, 'Makeup was okay.')"
)
cursor.execute(
    "INSERT INTO Feedback (customer_id, employee_id, service_id, rating, comments) VALUES (5, 5, 5, 5, 'Best massage ever!')"
)

# Inventory
cursor.execute(
    "INSERT INTO Inventory (item_name, quantity_available, price_per_unit) VALUES ('Shampoo', 20, 10.0)"
)
cursor.execute(
    "INSERT INTO Inventory (item_name, quantity_available, price_per_unit) VALUES ('Nail Polish', 30, 5.0)"
)
cursor.execute(
    "INSERT INTO Inventory (item_name, quantity_available, price_per_unit) VALUES ('Facial Mask', 15, 8.0)"
)
cursor.execute(
    "INSERT INTO Inventory (item_name, quantity_available, price_per_unit) VALUES ('Makeup Brushes', 25, 12.0)"
)
cursor.execute(
    "INSERT INTO Inventory (item_name, quantity_available, price_per_unit) VALUES ('Massage Oil', 10, 15.0)"
)

# InventoryTransaction
cursor.execute(
    "INSERT INTO InventoryTransaction (inventory_id, employee_id, transaction_date, transaction_type, quantity, total_cost) VALUES (1, 1, '2022-10-01', 'In', 10, 100.0)"
)
cursor.execute(
    "INSERT INTO InventoryTransaction (inventory_id, employee_id, transaction_date, transaction_type, quantity, total_cost) VALUES (2, 2, '2022-10-02', 'Out', 5, 25.0)"
)
cursor.execute(
    "INSERT INTO InventoryTransaction (inventory_id, employee_id, transaction_date, transaction_type, quantity, total_cost) VALUES (3, 3, '2022-10-03', 'In', 20, 160.0)"
)
cursor.execute(
    "INSERT INTO InventoryTransaction (inventory_id, employee_id, transaction_date, transaction_type, quantity, total_cost) VALUES (4, 4, '2022-10-04', 'Out', 2, 24.0)"
)
cursor.execute(
    "INSERT INTO InventoryTransaction (inventory_id, employee_id, transaction_date, transaction_type, quantity, total_cost) VALUES (5, 5, '2022-10-05', 'In', 15, 120.0)"
)

# Discount
cursor.execute("INSERT INTO Discount (service_id, discount_percentage) VALUES (1, 10)")
cursor.execute("INSERT INTO Discount (service_id, discount_percentage) VALUES (2, 15)")
cursor.execute("INSERT INTO Discount (service_id, discount_percentage) VALUES (3, 20)")
cursor.execute("INSERT INTO Discount (service_id, discount_percentage) VALUES (4, 25)")
cursor.execute("INSERT INTO Discount (service_id, discount_percentage) VALUES (5, 30)")

# Promotion
cursor.execute(
    "INSERT INTO Promotion (promotion_name, start_date, end_date, description) VALUES ('Summer Sale', '2022-06-01', '2022-08-31', 'Discounts on selected services')"
)
cursor.execute(
    "INSERT INTO Promotion (promotion_name, start_date, end_date, description) VALUES ('Holiday Special', '2022-12-01', '2022-12-31', 'Gift cards available')"
)
cursor.execute(
    "INSERT INTO Promotion (promotion_name, start_date, end_date, description) VALUES ('New Year Promotion', '2023-01-01', '2023-01-31', 'Free makeup with any service')"
)
cursor.execute(
    "INSERT INTO Promotion (promotion_name, start_date, end_date, description) VALUES ('Spring Refresh', '2023-03-01', '2023-03-31', 'Discounts on skincare products')"
)
cursor.execute(
    "INSERT INTO Promotion (promotion_name, start_date, end_date, description) VALUES ('Back to School', '2023-08-01', '2023-08-31', 'Haircut specials')"
)

# Reservation
cursor.execute(
    "INSERT INTO Reservation (customer_id, appointment_id, reservation_date) VALUES (1, 1, '2022-10-15')"
)
cursor.execute(
    "INSERT INTO Reservation (customer_id, appointment_id, reservation_date) VALUES (2, 2, '2022-10-16')"
)
cursor.execute(
    "INSERT INTO Reservation (customer_id, appointment_id, reservation_date) VALUES (3, 3, '2022-10-17')"
)
cursor.execute(
    "INSERT INTO Reservation (customer_id, appointment_id, reservation_date) VALUES (4, 4, '2022-10-18')"
)
cursor.execute(
    "INSERT INTO Reservation (customer_id, appointment_id, reservation_date) VALUES (5, 5, '2022-10-19')"
)

# Attendance
cursor.execute(
    "INSERT INTO Attendance (employee_id, date, time_in, time_out) VALUES (1, '2022-10-01', '09:00', '18:00')"
)
cursor.execute(
    "INSERT INTO Attendance (employee_id, date, time_in, time_out) VALUES (2, '2022-10-02', '10:00', '19:00')"
)
cursor.execute(
    "INSERT INTO Attendance (employee_id, date, time_in, time_out) VALUES (3, '2022-10-03', '11:00', '20:00')"
)
cursor.execute(
    "INSERT INTO Attendance (employee_id, date, time_in, time_out) VALUES (4, '2022-10-04', '12:00', '21:00')"
)
cursor.execute(
    "INSERT INTO Attendance (employee_id, date, time_in, time_out) VALUES (5, '2022-10-05', '13:00', '22:00')"
)

# SalonLocation
cursor.execute(
    "INSERT INTO SalonLocation (location_name, address, city, state, zip_code) VALUES ('Main Salon', '123 Main St', 'City', 'State', '12345')"
)
cursor.execute(
    "INSERT INTO SalonLocation (location_name, address, city, state, zip_code) VALUES ('Downtown Salon', '456 Elm St', 'City', 'State', '23456')"
)
cursor.execute(
    "INSERT INTO SalonLocation (location_name, address, city, state, zip_code) VALUES ('Westside Salon', '789 Oak St', 'City', 'State', '34567')"
)
cursor.execute(
    "INSERT INTO SalonLocation (location_name, address, city, state, zip_code) VALUES ('Eastside Salon', '101 Pine St', 'City', 'State', '45678')"
)
cursor.execute(
    "INSERT INTO SalonLocation (location_name, address, city, state, zip_code) VALUES ('Northside Salon', '202 Maple St', 'City', 'State', '56789')"
)

# Transactions
cursor.execute(
    "INSERT INTO Transactions (customer_id, transaction_date, transaction_type, amount) VALUES (1, '2022-10-01', 'Sale', 50.0)"
)
cursor.execute(
    "INSERT INTO Transactions (customer_id, transaction_date, transaction_type, amount) VALUES (2, '2022-10-02', 'Sale', 75.0)"
)
cursor.execute(
    "INSERT INTO Transactions (customer_id, transaction_date, transaction_type, amount) VALUES (3, '2022-10-03', 'Refund', -20.0)"
)
cursor.execute(
    "INSERT INTO Transactions (customer_id, transaction_date, transaction_type, amount) VALUES (4, '2022-10-04', 'Sale', 100.0)"
)
cursor.execute(
    "INSERT INTO Transactions (customer_id, transaction_date, transaction_type, amount) VALUES (5, '2022-10-05', 'Sale', 120.0)"
)

# Expense
cursor.execute(
    "INSERT INTO Expense (expense_date, expense_category, amount, description) VALUES ('2022-10-01', 'Supplies', 100.0, 'Hair products')"
)
cursor.execute(
    "INSERT INTO Expense (expense_date, expense_category, amount, description) VALUES ('2022-10-05', 'Utilities', 50.0, 'Electricity bill')"
)
cursor.execute(
    "INSERT INTO Expense (expense_date, expense_category, amount, description) VALUES ('2022-10-10', 'Rent', 500.0, 'Monthly rent payment')"
)
cursor.execute(
    "INSERT INTO Expense (expense_date, expense_category, amount, description) VALUES ('2022-10-15', 'Marketing', 200.0, 'Social media ads')"
)
cursor.execute(
    "INSERT INTO Expense (expense_date, expense_category, amount, description) VALUES ('2022-10-20', 'Miscellaneous', 50.0, 'Office supplies')"
)

# Commission
cursor.execute(
    "INSERT INTO Commission (employee_id, appointment_id, commission_amount, commission_date) VALUES (1, 1, 5.0, '2022-10-15')"
)
cursor.execute(
    "INSERT INTO Commission (employee_id, appointment_id, commission_amount, commission_date) VALUES (2, 2, 4.0, '2022-10-16')"
)
cursor.execute(
    "INSERT INTO Commission (employee_id, appointment_id, commission_amount, commission_date) VALUES (3, 3, 6.0, '2022-10-17')"
)
cursor.execute(
    "INSERT INTO Commission (employee_id, appointment_id, commission_amount, commission_date) VALUES (4, 4, 3.0, '2022-10-18')"
)
cursor.execute(
    "INSERT INTO Commission (employee_id, appointment_id, commission_amount, commission_date) VALUES (5, 5, 7.0, '2022-10-19')"
)

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()

print("База данных и таблицы успешно созданы и заполнены.")
