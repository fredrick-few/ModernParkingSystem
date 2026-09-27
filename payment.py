import time

class PaymentProcessor:
    """
    Module: Payment Gateway Interface & Barrier Control Signal Generator
    """

    @staticmethod
    def process_mpesa(phone_number: str, amount: float) -> dict:
        """Simulates Safaricom M-Pesa STK Push Payment verification."""
        clean_phone = phone_number.replace("+", "").replace(" ", "")
        
        if len(clean_phone) < 10 or not clean_phone.isdigit():
            return {
                "status": "FAILED",
                "message": "Invalid M-Pesa phone number format.",
                "barrier_open": False
            }

        print(f"\n[M-PESA GATEWAY] STK Push sent to {clean_phone} for Kshs {amount:.2f}...")
        time.sleep(1)  # Simulate network latency

        return {
            "status": "SUCCESS",
            "transaction_id": f"MP{int(time.time())}",
            "message": "Payment confirmed via M-Pesa.",
            "barrier_open": True
        }

    @staticmethod
    def process_cash(amount_given: float, fee_due: float) -> dict:
        """Validates cash transaction and computes required change."""
        if amount_given < fee_due:
            return {
                "status": "FAILED",
                "message": f"Insufficient Cash. Kshs {fee_due - amount_given:.2f} balance remaining.",
                "barrier_open": False
            }

        change = amount_given - fee_due
        return {
            "status": "SUCCESS",
            "transaction_id": f"CSH{int(time.time())}",
            "message": f"Cash Payment Verified. Change Due: Kshs {change:.2f}",
            "barrier_open": True
        }

    @staticmethod
    def process_card(card_number: str, expiry: str, cvv: str, amount: float) -> dict:
        """Simulates credit/debit card authorization with full credentials."""
        clean_card = card_number.replace(" ", "").replace("-", "")
        clean_cvv = cvv.strip()
        clean_expiry = expiry.strip()

        # 1. Validate Card Number (16 digits)
        if len(clean_card) != 16 or not clean_card.isdigit():
            return {
                "status": "FAILED",
                "message": "Invalid card number. Must be 16 digits.",
                "barrier_open": False
            }

        # 2. Validate CVV (3 digits)
        if len(clean_cvv) != 3 or not clean_cvv.isdigit():
            return {
                "status": "FAILED",
                "message": "Invalid CVV. Must be 3 digits.",
                "barrier_open": False
            }

        # 3. Validate Expiry Format (MM/YY)
        if len(clean_expiry) != 5 or "/" not in clean_expiry:
            return {
                "status": "FAILED",
                "message": "Invalid expiry date format. Use MM/YY.",
                "barrier_open": False
            }

        print(f"\n[CARD GATEWAY] Contacting issuing bank for Kshs {amount:.2f}...")
        time.sleep(1)

        return {
            "status": "SUCCESS",
            "transaction_id": f"TXN{int(time.time())}",
            "message": "Card authorized successfully.",
            "barrier_open": True
        }