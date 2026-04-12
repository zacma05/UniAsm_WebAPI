CREATE DATABASE Fruitables;

USE Fruitables;

-- 1. Tạo bảng tblAccount
CREATE TABLE tblAccount (
    AccountID INT PRIMARY KEY,
    Name VARCHAR(255),
    Password VARCHAR(255),
    Address VARCHAR(255),
    Phone VARCHAR(20),
    Role VARCHAR(50)
);

-- 2. Tạo bảng tblProduct
CREATE TABLE tblProduct (
    ProductID INT PRIMARY KEY,
    Name VARCHAR(255),
    Category VARCHAR(100),
    Price FLOAT,
    Stock INT,
    DueDate DATE,
    Description TEXT,
    Discount INT,
    Image VARCHAR(255)
);

-- 3. Tạo bảng tblInvoice
CREATE TABLE tblInvoice (
    InvoiceID INT PRIMARY KEY,
    AccountID INT,
    TotalPayment FLOAT,
    State VARCHAR(50),
    CONSTRAINT FK_Invoice_Account FOREIGN KEY (AccountID) REFERENCES tblAccount(AccountID)
);

-- 4. Tạo bảng tblPayment
CREATE TABLE tblPayment (
    PaymentID INT PRIMARY KEY,
    InvoiceID INT,
    Paying_method VARCHAR(100),
    Paying_date DATE,
    CONSTRAINT FK_Payment_Invoice FOREIGN KEY (InvoiceID) REFERENCES tblInvoice(InvoiceID)
);

-- 5. Tạo bảng tblOrder
-- Khi đã thêm tiền tố 'tbl', bạn không còn lo bị trùng với từ khóa 'Order' nữa
CREATE TABLE tblOrder (
    OrderID INT PRIMARY KEY,
    DeliveryMethod VARCHAR(100),
    InvoiceID INT,
    Address VARCHAR(255),
    Phone VARCHAR(20),
    CONSTRAINT FK_Order_Invoice FOREIGN KEY (InvoiceID) REFERENCES tblInvoice(InvoiceID)
);

-- 6. Tạo bảng tblInvoiceDetail
CREATE TABLE tblInvoiceDetail (
    InvoiceDetailID INT PRIMARY KEY,
    InvoiceID INT,
    ProductID INT,
    Quantity INT,
    CONSTRAINT FK_Detail_Invoice FOREIGN KEY (InvoiceID) REFERENCES tblInvoice(InvoiceID),
    CONSTRAINT FK_Detail_Product FOREIGN KEY (ProductID) REFERENCES tblProduct(ProductID)
);

-- 7. Tạo bảng tblCart
CREATE TABLE tblCart (
    AccountID INT,
    ProductID INT,
    Quantity INT,
    PRIMARY KEY (AccountID, ProductID),
    CONSTRAINT FK_Cart_Account FOREIGN KEY (AccountID) REFERENCES tblAccount(AccountID),
    CONSTRAINT FK_Cart_Product FOREIGN KEY (ProductID) REFERENCES tblProduct(ProductID)
);