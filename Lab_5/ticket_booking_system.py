"""Movie theater ticket booking and seating management module."""

import hashlib
import os
import secrets

THEATER_SEATS = {
    "A1": {"tier": "Standard", "price": 12.0, "is_sold": False},
    "A2": {"tier": "Standard", "price": 12.0, "is_sold": True},
    "B1": {"tier": "Premium", "price": 20.0, "is_sold": False},
}


def reserve_seat(seat_id, customer, order_history=None):
    """Mark a seat as sold and log the order. Return True on success."""
    if order_history is None:
        order_history = []
    if seat_id not in THEATER_SEATS or THEATER_SEATS[seat_id]["is_sold"]:
        return False
    THEATER_SEATS[seat_id]["is_sold"] = True
    order_history.append(f"Reserved seat {seat_id} for customer {customer}")
    return True


def cancel_seat(seat_id):
    """Release a sold seat. Return False if the seat does not exist."""
    try:
        THEATER_SEATS[seat_id]["is_sold"] = False
    except KeyError:
        return False
    return True


def check_seat_status(seat_id):
    """Return True if the seat exists and is still available."""
    seat = THEATER_SEATS.get(seat_id)
    if seat is None:
        return False
    return not seat["is_sold"]


def compute_discounted_price(seat_id, discount_rate):
    """Return the seat price after applying a discount rate (0 to 1)."""
    if not 0 <= discount_rate <= 1:
        raise ValueError("discount_rate must be between 0 and 1")
    base_price = THEATER_SEATS[seat_id]["price"]
    return base_price * (1 - discount_rate)


def generate_ticket_hash(ticket_code):
    """Return a SHA-256 hash of the ticket code."""
    return hashlib.sha256(ticket_code.encode()).hexdigest()


def generate_booking_pin():
    """Return a cryptographically secure 4-digit booking PIN."""
    return secrets.randbelow(9000) + 1000


def export_seating_chart(filename="seating_chart.txt"):
    """Write the current seating chart to a text file."""
    with open(filename, "w", encoding="utf-8") as chart_file:
        chart_file.write(str(THEATER_SEATS))
    print(f"Seating chart exported to: {filename}")


def get_theater_summary(seats):
    """Return the number of sold seats."""
    return sum(1 for details in seats.values() if details["is_sold"])


def main():
    """Run a short demo of the booking system."""
    box_office_key = os.environ.get("BOX_OFFICE_KEY")
    order_history = []
    reserve_seat("A1", "Sarah Connor", order_history)
    cancel_seat("A2")
    print("Is B1 available:", check_seat_status("B1"))
    print("Promo price:", compute_discounted_price("B1", 0.20))
    print("Ticket Hash:", generate_ticket_hash("TKT_882"))
    print("Booking PIN:", generate_booking_pin())
    export_seating_chart()
    print("Sold count:", get_theater_summary(THEATER_SEATS))
    print("Order history:", order_history)
    print("Box office token configured:", box_office_key is not None)


if __name__ == "__main__":
    main()
