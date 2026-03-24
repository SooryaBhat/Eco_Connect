# 🌱 EcoConnect

### Smart Dustbin with Waste Selling & Connecting Platform

EcoConnect is an **IoT-based smart waste management system** combined with a **digital waste-selling platform**. It connects **citizens, collectors, recyclers, and government authorities** into a single ecosystem to improve waste handling efficiency and promote recycling.

---

## 🚀 Live Demo

https://eco-connect-1-cy88.onrender.com

---

## 📌 Problem Statement

Traditional waste management systems face issues like:

* Overflowing bins due to lack of real-time monitoring
* No proper communication between citizens and authorities
* Inefficient collection routes
* Mixing of recyclable and non-recyclable waste
* No system to monetize recyclable waste

---

## 💡 Solution

EcoConnect provides:

* Real-time smart bin monitoring using IoT
* Role-based web application
* Waste selling marketplace
* Complaint management system
* Analytics dashboard for decision making

---

## 🧠 Key Features

### ♻️ Smart Waste Monitoring

* ESP32-based smart bin
* Load cells measure waste weight
* Real-time bin status:

  * Urgent
  * Medium
  * Enough Space

---

### 👥 Multi-User System

#### 👤 User (Citizen)

* Check bin status
* File complaints
* Sell recyclable waste

#### 🚛 Collector

* View regional bins
* Manage complaints
* Optimize collection

#### ♻️ Recycler

* View waste listings
* Purchase recyclable materials

#### 🏛️ Government

* Monitor all bins
* View analytics & reports
* Track complaints

---

### 💰 Waste Marketplace

* Users can list recyclable waste
* Recyclers can buy directly
* Promotes waste-to-wealth concept

---

### 📊 Analytics Dashboard

* Waste distribution charts
* Bin status visualization
* Data-driven insights for authorities

---

### 🌐 Multilingual Support

* English
* Kannada
* Tulu

---

## ⚙️ Tech Stack

### 🔌 Hardware

* ESP32 Microcontroller
* Load Cell
* HX711 Amplifier

### 💻 Software

* Frontend: HTML, CSS, JavaScript
* Backend: Flask (Python)
* Database: MySQL
* Hosting: Render

---

## 🏗️ System Architecture

```
Smart Bin (ESP32 + Sensors)
        ↓
Flask Backend (Cloud Server)
        ↓
MySQL Database
        ↓
Web Application (Role-Based Access)
        ↓
User | Collector | Recycler | Government
```

---

## 🔄 Workflow

1. Waste is disposed into the smart bin
2. Load cell measures weight
3. ESP32 sends data to server via Wi-Fi
4. Backend processes and updates bin status
5. Data is displayed on dashboards
6. Users can sell waste → recyclers can purchase

---

## 📁 Project Structure

```
Eco_Connect/
│── static/              # CSS, JS, Images
│── templates/           # HTML files
│── app.py               # Main Flask application
│── database/            # MySQL schema
│── requirements.txt     # Dependencies
│── README.md            # Project documentation
```

---

## 🛠️ Installation & Setup

### 1️⃣ Clone the repository

```
git clone https://github.com/SooryaBhat/Eco_Connect.git
cd Eco_Connect
```

### 2️⃣ Install dependencies

```
pip install -r requirements.txt
```

### 3️⃣ Setup database

* Create MySQL database
* Import schema (if provided)
* Update DB credentials in app.py

### 4️⃣ Run the app

```
python app.py
```

### 5️⃣ Open in browser

```
http://localhost:5000
```

---

## ⚠️ Limitations

* Automatic waste segregation is partially implemented
* Load cell calibration may not be fully accurate
* Prototype-level hardware implementation

---

## 🔮 Future Enhancements

* AI-based waste classification
* GPS-based route optimization
* Mobile app (Android/iOS)
* Digital payments (UPI integration)
* Push notifications & alerts
* Advanced analytics & forecasting

---

## 🎯 Conclusion

EcoConnect demonstrates how **IoT + Cloud + Digital Marketplace** can transform waste management into a **smart, efficient, and revenue-generating system**. It provides a scalable solution for smart cities and sustainable environments.

---

