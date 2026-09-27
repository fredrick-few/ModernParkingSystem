from datetime import datetime, timedelta

class FeeCalculator:
    """
    Module: Fee Computation Engine
    Data Structure: Dynamic Rule List / Interval Lookup
    Time Complexity: O(1) constant time lookup
    """
    def __init__(self, rate_tiers=None, max_fee=500):
        # Default tariff rates: (max_minutes, fee)
        self.rate_tiers = rate_tiers or [
            (30, 0),      # 0-30 mins: Free
            (120, 50),    # 30m-2h: 50 Kshs
            (240, 100),   # 2h-4h: 100 Kshs
            (360, 300)    # 4h-6h: 300 Kshs
        ]
        self.max_fee = max_fee

    def update_rates(self, tier_30m, tier_2h, tier_4h, tier_6h, max_daily_fee):
        """Allows management to change rates dynamically at runtime without altering code."""
        self.rate_tiers = [
            (30, float(tier_30m)),
            (120, float(tier_2h)),
            (240, float(tier_4h)),
            (360, float(tier_6h))
        ]
        self.max_fee = float(max_daily_fee)

    def calculate_fee(self, entry_time: datetime, exit_time: datetime):
        time_difference: timedelta = exit_time - entry_time
        duration_minutes = time_difference.total_seconds() / 60.0

        fee = self.max_fee
        for max_minutes, tier_fee in self.rate_tiers:
            if duration_minutes <= max_minutes:
                fee = tier_fee
                break

        vat_amount = round(fee * 0.16, 2)  # 16% Statutory VAT calculation
        net_amount = round(fee - vat_amount, 2)

        return fee, duration_minutes, net_amount, vat_amount


class SlotManager:
    """
    Module: Parking Slot & Vehicle Allocation Manager
    Data Structure: Dictionary (Hash Map) for O(1) slot lookups
    """
    def __init__(self, total_slots: int = 20):
        self.total_slots = total_slots
        self.slots = {slot_id: None for slot_id in range(1, total_slots + 1)}

    def allocate_slot(self, plate_number: str) -> int | None:
        for slot_id, occupied_by in self.slots.items():
            if occupied_by is None:
                self.slots[slot_id] = plate_number
                return slot_id
        return None

    def release_slot(self, slot_id: int) -> bool:
        if slot_id in self.slots:
            self.slots[slot_id] = None
            return True
        return False