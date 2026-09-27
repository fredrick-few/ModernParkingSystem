from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import sqlite3

from parking_core import SlotManager, FeeCalculator
from payment import PaymentProcessor
import database

app = Flask(__name__)
app.secret_key = 'super_secret_parking_key'

# Initialize Core System Modules
slot_mgr = SlotManager(total_slots=20)
calculator = FeeCalculator()

# Initialize SQLite Schema
database.init_db()

@app.route('/')
def index():
    """Main Entrance View - Slot Availability & Check-in."""
    return render_template('index.html', slots=slot_mgr.slots)

@app.route('/checkin', methods=['POST'])
def checkin():
    """Vehicle Arrival Registration Endpoint."""
    plate = request.form.get('plate_number', '').strip().upper()
    if not plate:
        flash("Please enter a valid license plate number.", "error")
        return redirect(url_for('index'))

    slot_id = slot_mgr.allocate_slot(plate)
    if slot_id is None:
        flash("Parking Lot is FULL! No available slots.", "error")
        return redirect(url_for('index'))

    entry_time = datetime.now()
    ticket_id = database.save_active_ticket(plate, slot_id, entry_time)
    flash(f"Vehicle {plate} Checked-In successfully! Assigned to Slot {slot_id}. Ticket #{ticket_id}", "success")
    return redirect(url_for('index'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    """Vehicle Exit Gateway & Settlement Endpoint."""
    if request.method == 'POST':
        plate = request.form.get('plate_number', '').strip().upper()
        payment_method = request.form.get('payment_method', 'MPESA')

        ticket = database.get_active_ticket(plate)
        if not ticket:
            flash(f"No active parked vehicle found with license plate: {plate}", "error")
            return redirect(url_for('checkout'))

        ticket_id, plate, slot_id, entry_time_str = ticket
        entry_time = datetime.fromisoformat(entry_time_str)
        exit_time = datetime.now()

        # Compute fee and VAT breakdown
        fee, duration, net_amt, vat_amt = calculator.calculate_fee(entry_time, exit_time)

        # --- NEW LOGIC: Bypass payment gateways if the fee is 0 ---
        if fee == 0:
            pay_res = {
                "status": "SUCCESS", 
                "message": "Parking duration under 30 minutes. Free of charge.", 
                "barrier_open": True
            }
            payment_method = "FREE_PASS"  # Log it as a free pass in the database
        else:
            # Process Payment normally for fees > 0
            if payment_method == 'MPESA':
                phone = request.form.get('mpesa_phone', '')
                pay_res = PaymentProcessor.process_mpesa(phone, fee)
            elif payment_method == 'CASH':
                cash_given = float(request.form.get('cash_given', 0))
                pay_res = PaymentProcessor.process_cash(cash_given, fee)
            elif payment_method == 'CARD':
                card_num = request.form.get('card_number', '')
                expiry = request.form.get('card_expiry', '')
                cvv = request.form.get('card_cvv', '')
                pay_res = PaymentProcessor.process_card(card_num, expiry, cvv, fee)
            else:
                pay_res = {"status": "FAILED", "message": "Unknown Payment Method", "barrier_open": False}

        if pay_res["barrier_open"]:
            # Clear active ticket & log completed transaction audit
            database.remove_active_ticket(ticket_id)
            slot_mgr.release_slot(slot_id)
            database.log_transaction(
                plate, slot_id, entry_time_str, exit_time.isoformat(),
                round(duration, 2), fee, payment_method, "PAID"
            )
            flash(f"Success! {pay_res['message']} BARRIER OPEN. Slot {slot_id} is now FREE.", "success")
            return redirect(url_for('index'))
        else:
            flash(f"Payment Failed: {pay_res['message']} BARRIER REMAINS CLOSED.", "error")
            return redirect(url_for('checkout'))

    return render_template('checkout.html')

@app.route('/admin')
def admin():
    """Admin Dashboard - Active Cars, Rates Config & Audit Transactions Log."""
    conn = sqlite3.connect(database.DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM active_tickets')
    active_vehicles = cursor.fetchall()
    
    cursor.execute('SELECT * FROM transactions ORDER BY transaction_id DESC')
    transactions = cursor.fetchall()
    conn.close()
    
    return render_template(
        'admin.html', 
        active=active_vehicles, 
        transactions=transactions,
        tiers=calculator.rate_tiers,
        max_fee=calculator.max_fee
    )

@app.route('/update_rates', methods=['POST'])
def update_rates():
    """Allows admin to update parking rate tariffs dynamically."""
    try:
        t30 = request.form.get('tier_30m', 0)
        t2h = request.form.get('tier_2h', 50)
        t4h = request.form.get('tier_4h', 100)
        t6h = request.form.get('tier_6h', 300)
        max_fee = request.form.get('max_fee', 500)

        calculator.update_rates(t30, t2h, t4h, t6h, max_fee)
        flash("Parking rate tariffs updated successfully!", "success")
    except Exception as e:
        flash(f"Failed to update rates: {str(e)}", "error")

    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)