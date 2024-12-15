import tk

from app import BookingApp
from script import Booking
from values import values


def book(values=None):
    if not values:
        while True:
            root = tk.Tk()
            app = BookingApp(root)
            root.mainloop()

            values = app.handle_booking()

            if values:
                break

    booking = Booking(values)
    booking.main()


book(values)
