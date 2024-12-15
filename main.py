import tkinter

from app import BookingApp, messages
from models import BookingData
from script import Booking
from values import values

# same case for backend and frontend
# invalid station error


def book(values=None):
    # Entry Loop
    if not values:
        while True:
            root = tkinter.Tk()
            app = BookingApp(root)
            root.mainloop()

            values = app.handle_booking()

            if values:
                break

    # Final validation
    if values:
        try:
            BookingData(**values)
        except Exception as e:
            errors = "\n".join(messages(e))
            print(errors)
            return

    print("values successfully filled")

    # Ticket booking
    booking = Booking(values)
    booking.main()


book(values)
