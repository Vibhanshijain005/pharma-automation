-- SQLite schema for Pharmacy Automation System
CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  role TEXT
);

CREATE TABLE supplier (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  email TEXT,
  phone TEXT,
  address TEXT
);

CREATE TABLE customer (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  email TEXT,
  phone TEXT,
  address TEXT
);

CREATE TABLE medicine (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  category TEXT,
  price REAL,
  quantity INTEGER,
  reorder_level INTEGER,
  expiry_date DATE,
  supplier_id INTEGER
);

CREATE TABLE sale (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  customer_name TEXT,
  total REAL,
  date DATETIME
);

CREATE TABLE purchase (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  supplier_id INTEGER,
  total REAL,
  date DATETIME
);
