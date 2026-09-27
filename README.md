# Autonomous Parking Management and Barrier Control System

A full-stack, web-based Parking Management System developed in Python using Flask and SQLite[cite: 1, 2]. The system handles real-time vehicle slot allocation, dynamic fee computation, multi-channel payment verification (M-Pesa, Card, Cash), automated exit barrier signaling, live rate management, and financial audit logging with statutory VAT calculations[cite: 1, 2].

---

## 1. Executive Summary & System Features

- **Live Entrance Monitor**: Displays slot availability in real time using a dynamic visual grid where green slots represent free bays and red slots represent occupied bays[cite: 1, 2].
- **Automated Check-In**: Registers arriving vehicles by license plate, logs the exact entry timestamp, and automatically assigns the next available parking slot[cite: 1, 2].
- **Dynamic Fee Engine**: Automatically computes parking duration and applies dynamic rate tiers, grace periods, and daily maximum caps[cite: 1, 2].
- **Multi-Channel Payment Verification**:
  - **M-Pesa**: Validates phone numbers and simulates STK Push network prompts[cite: 1, 2].
  - **Card**: Validates full credentials including 16-digit card numbers, MM/YY expiry dates, and 3-digit CVV codes[cite: 1, 2].
  - **Cash**: Accepts cash amounts, verifies sufficient payment, and calculates change due[cite: 1, 2].
  - **Grace Period Bypass**: Automatically opens the exit barrier without payment prompts if the parking duration is under 30 minutes[cite: 1, 2].
- **Administrative Management Dashboard**:
  - **Live Rate Configuration**: Allows management to update tariff rates dynamically through the web interface without modifying underlying code[cite: 1, 2].
  - **Active Parking View**: Tracks all vehicles currently parked in the facility[cite: 1, 2].
  - **Financial Audit Log**: Maintains a complete record of completed transactions, payment channels, total fees, net amounts, and statutory VAT breakdowns[cite: 1, 2].

---

## 2. Algorithms and Data Structures by Module

### Module 1: Vehicle Check-In and Slot Management (SlotManager)
- **Data Structure Used**: Python Dictionary (Hash Map)[cite: 1, 2].
- **Reason for Use**: A Hash Map provides constant-time average lookup, insertion, and deletion speeds[cite: 1, 2]. Key-value mapping allows direct association between slot numbers and vehicle plate strings without scanning arrays sequentially[cite: 1, 2].
- **Allocation Algorithm**:
  1. Receive vehicle plate number upon arrival[cite: 1, 2].
  2. Iterate through slot dictionary keys from 1 to 20[cite: 1, 2].
  3. Assign the vehicle to the first key where the value is empty (None)[cite: 1, 2].
  4. If all slots contain active vehicle plates, display a "Parking Lot Full" notification[cite: 1, 2].
- **Release Algorithm**:
  1. Receive the assigned slot ID upon confirmed exit payment[cite: 1, 2].
  2. Directly access the key in the dictionary[cite: 1, 2].
  3. Reset the slot value back to empty (None) in constant O(1) time[cite: 1, 2].

---

### Module 2: Dynamic Fee Computation Engine (FeeCalculator)
- **Data Structure Used**: Ordered List of Tuples (Rule List)[cite: 1, 2].
- **Reason for Use**: Parking tariffs are based on duration buckets[cite: 1, 2]. An ordered list of tuples allows continuous evaluation of duration intervals while supporting live updates from the admin page without changing code[cite: 1, 2].
- **Calculation Algorithm**:
  1. Calculate total duration in minutes by subtracting entry timestamp from exit timestamp[cite: 1, 2].
  2. Check for Grace Period: If duration is 30 minutes or less, set fee to 0 and trigger automatic barrier bypass[cite: 1, 2].
  3. Evaluate Rate Tiers: Sequential check across defined rate buckets (30m to 2h, 2h to 4h, 4h to 6h)[cite: 1, 2].
  4. Apply Daily Cap: If duration exceeds 6 hours, apply the maximum daily rate cap (Kshs 500 default)[cite: 1, 2].
  5. Calculate VAT Split: Compute 16% statutory VAT and net revenue for financial reporting[cite: 1, 2].

---

### Module 3: Payment Gateway and Barrier Control (PaymentProcessor)
- **Data Structure Used**: Response Payload Dictionary[cite: 1, 2].
- **Reason for Use**: Passing structured dictionaries isolates payment status metadata, cleanly separating backend validation results from front-end barrier signaling[cite: 1, 2].
- **Payment Algorithms**:
  1. **M-Pesa**: Validates phone string length and formatting, simulates gateway network response delay, generates a reference code, and returns a successful barrier open signal[cite: 1, 2].
  2. **Card**: Validates that card number is 16 digits, expiry matches MM/YY format, and CVV is 3 digits[cite: 1, 2]. Returns authorization confirmation and barrier open signal[cite: 1, 2].
  3. **Cash**: Compares cash handed over against fee due[cite: 1, 2]. If insufficient, reports remaining balance and keeps barrier closed[cite: 1, 2]. If sufficient, computes change due and opens barrier[cite: 1, 2].

---

### Module 4: Relational Persistence and Audit Logging (database.py)
- **Data Structure Used**: Relational SQL Tables (SQLite)[cite: 1, 2].
- **Reason for Use**: Relational database tables ensure ACID compliance (Atomicity, Consistency, Isolation, Durability) and ensure transaction records survive system restarts[cite: 1, 2].
- **Audit Logging Algorithm**:
  1. When payment is confirmed, query and retrieve the active vehicle entry by license plate[cite: 1, 2].
  2. Execute SQL DELETE statement on active_tickets table to clear vehicle from live view[cite: 1, 2].
  3. Execute SQL INSERT statement to record the completed transaction into the transactions ledger[cite: 1, 2].
  4. Commit changes to disk storage[cite: 1, 2].

---

## 3. Data Structures Complexity Summary

| Module | Data Structure | Time Complexity | Primary Rationale |
| :--- | :--- | :--- | :--- |
| **Slot Manager** | Hash Map / Dictionary | O(1) Average | Instant slot assignment, lookup, and release in memory[cite: 1, 2]. |
| **Fee Calculator** | Ordered Tuple List | O(1) Constant | Fast interval matching and dynamic administrative updates[cite: 1, 2]. |
| **Payment Processor** | Response Dictionary | O(1) Constant | Decouples payment status logic from physical barrier control[cite: 1, 2]. |
| **Database** | Relational SQL Tables | O(1) Write | Guarantees data persistence, integrity, and audit compliance[cite: 1, 2]. |

---

## 4. Default Rate Tariff Breakdown

- **0 to 30 minutes**: Free (Kshs 0) — *Automatic Exit Barrier Bypass*[cite: 1, 2]
- **30 minutes to 2 hours**: Kshs 50[cite: 1, 2]
- **2 hours to 4 hours**: Kshs 100[cite: 1, 2]
- **4 hours to 6 hours**: Kshs 300[cite: 1, 2]
- **6+ hours (Max Daily Rate)**: Kshs 500[cite: 1, 2]

*(Note: Tariff rates can be dynamically updated at runtime via the Admin Dashboard)[cite: 1, 2].*

---

## 5. System Scope and Compliance

- **In Scope**: Vehicle arrival entry, slot allocation, live display grid, duration calculation, dynamic tariff computation, multi-channel payment verification, exit barrier control, administrative rate updates, and financial audit logs[cite: 1, 2].
- **Out of Scope**: Advance online bay reservations, valet management, third-party loyalty programs, and license plate blacklisting[cite: 1, 2].

---

## 6. Directory Layout and Local Setup Instructions

### Directory Structure
```text
ParkingSystem/
├── app.py              # Flask Application Controller & Route Handlers
├── database.py         # SQLite Persistence Layer & Table Schemas
├── parking_core.py     # Slot Manager & Dynamic Fee Calculator Modules
├── payment.py          # Payment Processor & Barrier Control Logic
├── parking_system.db   # SQLite Database File
└── templates/          # Responsive Jinja2 HTML Templates

### Step-by-Step Guide to Run Locally

1. **Clone the Repository**:
   Download the project source code from GitHub to your local machine:
   ```bash
   git clone [https://github.com/fredrick-were/ModernParkingSystem.git](https://github.com/fredrick-were/ModernParkingSystem.git)
   cd ModernParkingSystem

2. **Install dependencies**:
   Install the required Web Framework(Flask):
   ```bash
   pip install flask

3. **Start The Application**:
   Launch the backend web server and database controller:
   ```bash
   python app.py

4. **Access the Web Interface**:
   Open any web browser and navigate to:
   ```Plaintext
   [http://127.0.0.1:5000](http://127.0.0.1:5000)
   Alternatively, in your VS Code terminal, hold Ctrl (or Cmd on macOS) and click the http://127.0.0.1:5000 link that appears when Flask     starts to open it directly in your browser. 
    ├── index.html      # Entrance View & Live Slot Grid Monitor
    ├── checkout.html   # Exit Gateway & Payment Settlement View
    └── admin.html      # Admin Dashboard & Live Rate Configuration
