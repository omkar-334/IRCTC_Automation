import tkinter

from app import BookingApp, messages
from models import BookingData
from script import Booking
from values import values

# same case for backend and frontend
# invalid station error


def book(values=None):
    # If default values are not found, then GUI is provided
    if not values:
        root = tkinter.Tk()
        app = BookingApp(root)
        root.mainloop()

    # Else Booking is started directly.
    else:
        try:
            BookingData(**values)

            booking = Booking(values)
            booking.main()
        except Exception as e:
            errors = "\n".join(messages(e))
            print(errors)


book(values)
