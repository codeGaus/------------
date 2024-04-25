import sqlite3
import os


sql = '''
-- Создание таблиц
CREATE TABLE Customer (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255),
    email VARCHAR(255),
    phone_number VARCHAR(20),
    birthdate TEXT,
    tg_id TEXT
);

CREATE TABLE Employee (
    employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255),
    email VARCHAR(255),
    phone_number VARCHAR(20),
    role_id INT,
    FOREIGN KEY (role_id) REFERENCES Role(role_id)
);

CREATE TABLE Role (
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_name VARCHAR(50)
);

CREATE TABLE ServiceCategory (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name VARCHAR(100)
);

CREATE TABLE Service (
    service_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INT,
    service_name VARCHAR(255),
    description TEXT,
    price DECIMAL(10, 2),
    FOREIGN KEY (category_id) REFERENCES ServiceCategory(category_id)
);

CREATE TABLE Appointment (
    appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INT,
    employee_id INT,
    service_id INT,
    appointment_date TEXT,
    appointment_time TEXT,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    FOREIGN KEY (employee_id) REFERENCES Employee(employee_id),
    FOREIGN KEY (service_id) REFERENCES Service(service_id)
);

CREATE TABLE Payment (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    appointment_id INT,
    amount DECIMAL(10, 2),
    payment_date DATE,
    FOREIGN KEY (appointment_id) REFERENCES Appointment(appointment_id)
);

CREATE TABLE Feedback (
    feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INT,
    employee_id INT,
    service_id INT,
    rating INT,
    comments TEXT,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    FOREIGN KEY (employee_id) REFERENCES Employee(employee_id),
    FOREIGN KEY (service_id) REFERENCES Service(service_id)
);

CREATE TABLE Inventory (
    inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name VARCHAR(255),
    quantity_available INT,
    price_per_unit DECIMAL(10, 2)
);

CREATE TABLE InventoryTransaction (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    inventory_id INT,
    employee_id INT,
    transaction_date DATE,
    transaction_type VARCHAR(50),
    quantity INT,
    total_cost DECIMAL(10, 2),
    FOREIGN KEY (inventory_id) REFERENCES Inventory(inventory_id),
    FOREIGN KEY (employee_id) REFERENCES Employee(employee_id)
);

CREATE TABLE Discount (
    discount_id INTEGER PRIMARY KEY AUTOINCREMENT,
    service_id INT,
    discount_percentage DECIMAL(5, 2),
    FOREIGN KEY (service_id) REFERENCES Service(service_id)
);

CREATE TABLE Promotion (
    promotion_id INTEGER PRIMARY KEY AUTOINCREMENT,
    promotion_name VARCHAR(255),
    start_date DATE,
    end_date DATE,
    description TEXT
);

CREATE TABLE Reservation (
    reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INT,
    appointment_id INT,
    reservation_date DATE,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    FOREIGN KEY (appointment_id) REFERENCES Appointment(appointment_id)
);

CREATE TABLE Attendance (
    attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INT,
    date DATE,
    time_in TIME,
    time_out TIME,
    FOREIGN KEY (employee_id) REFERENCES Employee(employee_id)
);

CREATE TABLE SalonLocation (
    location_id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_name VARCHAR(255),
    address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    zip_code VARCHAR(20)
);

CREATE TABLE Transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INT,
    transaction_date DATE,
    transaction_type VARCHAR(50),
    amount DECIMAL(10, 2),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
);

CREATE TABLE Expense (
    expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
    expense_date DATE,
    expense_category VARCHAR(255),
    amount DECIMAL(10, 2),
    description TEXT
);

CREATE TABLE Commission (
    commission_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INT,
    appointment_id INT,
    commission_amount DECIMAL(10, 2),
    commission_date DATE,
    FOREIGN KEY (employee_id) REFERENCES Employee(employee_id),
    FOREIGN KEY (appointment_id) REFERENCES Appointment(appointment_id)
);

-- Заполнение таблиц данными
-- Customer (Клиенты)
INSERT INTO Customer (customer_id, name, email, phone_number, birthdate, tg_id) VALUES
(1, 'Иванов Иван', 'ivanov@example.com', '+1234567890', '1990-01-01', '3242342'),
(2, 'Петрова Мария', 'petrova@example.com', '+9876543210', '1995-05-15', '234234234');

-- Employee (Сотрудники)
INSERT INTO Employee (employee_id, name, email, phone_number, role_id) VALUES
(1, 'Смирнова Екатерина', 'smirnova@example.com', '+1111111111', 1),
(2, 'Козлов Алексей', 'kozlov@example.com', '+2222222222', 2);

-- Role (Роли сотрудников)
INSERT INTO Role (role_id, role_name) VALUES
(1, 'Администратор'),
(2, 'Мастер по наращиванию');

-- ServiceCategory (Категории услуг)
INSERT INTO ServiceCategory (category_id, category_name) VALUES
(1, 'Стрижка'),
(2, 'Маникюр'),
(3, 'Педикюр');

-- Service (Услуги)
INSERT INTO Service (service_id, category_id, service_name, description, price) VALUES
(1, 1, 'Мужская стрижка', 'Классическая стрижка для мужчин', 30.00),
(2, 2, 'Маникюр с покрытием', 'Маникюр с покрытием гель-лаком', 40.00),
(3, 3, 'Педикюр', 'Комплекс процедур для ног', 50.00);

-- Appointment (Записи на прием)
INSERT INTO Appointment (appointment_id, customer_id, employee_id, service_id, appointment_date, appointment_time) VALUES
(1, 1, 1, 1, '2024-04-15', '10:00:00'),
(2, 2, 2, 2, '2024-04-16', '11:30:00');

-- Payment (Платежи)
INSERT INTO Payment (payment_id, appointment_id, amount, payment_date) VALUES
(1, 1, 30.00, '2024-04-15'),
(2, 2, 40.00, '2024-04-16');

-- Feedback (Отзывы)
INSERT INTO Feedback (feedback_id, customer_id, employee_id, service_id, rating, comments) VALUES
(1, 1, 2, 1, 5, 'Отличная стрижка!'),
(2, 2, 1, 2, 4, 'Хороший маникюр, спасибо!');

-- Inventory (Инвентарь)
INSERT INTO Inventory (inventory_id, item_name, quantity_available, price_per_unit) VALUES
(1, 'Набор для маникюра', 10, 25.00),
(2, 'Гель-лак', 20, 15.00);

-- InventoryTransaction (Транзакции инвентаря)
INSERT INTO InventoryTransaction (transaction_id, inventory_id, employee_id, transaction_date, transaction_type, quantity, total_cost) VALUES
(1, 1, 1, '2024-04-15', 'Приход', 5, 125.00),
(2, 2, 2, '2024-04-16', 'Приход', 10, 150.00);

-- Discount (Скидки)
INSERT INTO Discount (discount_id, service_id, discount_percentage) VALUES
(1, 1, 10),
(2, 2, 5);

-- Promotion (Промо-акции)
INSERT INTO Promotion (promotion_id, promotion_name, start_date, end_date, description) VALUES
(1, 'Летняя распродажа', '2024-06-01', '2024-08-31', 'Скидки на все услуги в течение лета');

-- Reservation (Бронирование)
INSERT INTO Reservation (reservation_id, customer_id, appointment_id, reservation_date) VALUES
(1, 1, 1, '2024-04-14'),
(2, 2, 2, '2024-04-15');

-- Attendance (Посещаемость)
INSERT INTO Attendance (attendance_id, employee_id, date, time_in, time_out) VALUES
(1, 1, '2024-04-15', '09:00:00', '18:00:00'),
(2, 2, '2024-04-16', '10:00:00', '19:00:00');

-- SalonLocation (Локации салона)
INSERT INTO SalonLocation (location_id, location_name, address, city, state, zip_code) VALUES
(1, 'Салон "Красота"', 'ул. Пушкина, д. 10', 'Город', 'Область', '123456');

-- Transactions (Транзакции)
INSERT INTO Transactions (transaction_id, customer_id, transaction_date, transaction_type, amount) VALUES
(1, 1, '2024-04-15', 'Приход', 100.00),
(2, 2, '2024-04-16', 'Расход', 50.00);

-- Expense (Расходы)
INSERT INTO Expense (expense_id, expense_date, expense_category, amount, description) VALUES
(1, '2024-04-15', 'Зарплата сотрудникам', 2000.00, 'Зарплата за месяц апрель'),
(2, '2024-04-16', 'Реклама', 500.00, 'Рекламная кампания в социальных сетях');

-- Commission (Комиссии)
INSERT INTO Commission (commission_id, employee_id, appointment_id, commission_amount, commission_date) VALUES
(1, 2, 1, 5.00, '2024-04-15'),
(2, 1, 2, 7.00, '2024-04-16');
'''

database_name = "salon_database.db"
database_path = f"databases/{database_name}"

if os.path.exists(database_path):
    os.remove(database_path)

# Создание соединения с базой данных
conn = sqlite3.connect(database_path)
cursor = conn.cursor()

# Создание таблиц
cursor.executescript(sql)

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()

print("База данных и таблицы успешно созданы и заполнены.")
