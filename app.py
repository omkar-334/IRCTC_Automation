import tkinter as tk
from tkinter import ttk

from pydantic import ValidationError

from models import BookingData


class BookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IRCTC Tatkal Ticket Booking")

        self.fields = [
            "UserID",
            "Password",
            "FromStation",
            "ToStation",
            "Class",
            "Quota",
            "MobileNo",
        ]

        self.quotas = [
            "GENERAL",
            "LADIES",
            "LOWER BERTH/SR.CITIZEN",
            "PERSON WITH DISABILITY",
            "DUTY PASS",
            "TATKAL",
            "PREMIUM TATKAL",
        ]

        self.classes = [
            "All Classes",
            "Anubhuti Class (EA)",
            "AC First Class (1A)",
            "Vistadome AC (EV)",
            "Exec. Chair Car (EC)",
            "AC 2 Tier (2A)",
            "First Class (FC)",
            "AC 3 Tier (3A)",
            "AC 3 Economy (3E)",
            "Vistadome Chair Car (VC)",
            "AC Chair car (CC)",
            "Sleeper (SL)",
            "Vistadome Non AC (VS)",
            "Second Sitting (2S)",
        ]

        self.entries = {}
        self.passenger_entries = []

        self.num_passengers = tk.IntVar(value=4)

        self.create_widgets()

    def create_widgets(self):
        """
        Create and layout all widgets for the application.
        """
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        left_frame = ttk.Frame(main_frame, padding="10")
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        right_frame = ttk.Frame(main_frame, padding="10")
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))

        for i, field in enumerate(self.fields):
            if field not in ["Class", "Quota"]:
                ttk.Label(left_frame, text=field).grid(row=i, column=0, sticky=tk.W, pady=5)
                entry = ttk.Entry(left_frame, show="*" if field == "Password" else None)
                entry.grid(row=i, column=1, sticky=(tk.W, tk.E), pady=5)
                self.entries[field] = entry

            elif field == "Class":
                ttk.Label(left_frame, text="Class:").grid(row=i, column=0, sticky=tk.W, pady=5)
                self.class_var = tk.StringVar(value=self.classes[0])
                class_dropdown = ttk.Combobox(
                    left_frame, textvariable=self.class_var, values=self.classes, state="readonly"
                )
                class_dropdown.grid(row=i, column=1, sticky=(tk.W, tk.E), pady=5)
                self.entries["Class"] = self.class_var

            elif field == "Quota":
                ttk.Label(left_frame, text="Quota:").grid(row=i, column=0, sticky=tk.W, pady=5)
                self.quota_var = tk.StringVar(value=self.quotas[0])
                quota_dropdown = ttk.Combobox(
                    left_frame, textvariable=self.quota_var, values=self.quotas, state="readonly"
                )
                quota_dropdown.grid(row=i, column=1, sticky=(tk.W, tk.E), pady=5)
                self.entries["Quota"] = self.quota_var

        ttk.Label(left_frame, text="Number of Passengers:").grid(row=len(self.fields), column=0, sticky=tk.W, pady=5)
        passenger_slider = ttk.Scale(
            left_frame, from_=1, to=10, orient=tk.HORIZONTAL, command=self.update_passenger_fields
        )
        passenger_slider.set(self.num_passengers.get())
        passenger_slider.grid(row=len(self.fields), column=1, sticky=(tk.W, tk.E), pady=5)

        self.passenger_frame = ttk.Frame(right_frame)
        self.passenger_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

        self.update_passenger_fields(self.num_passengers.get())

        submit_button = ttk.Button(left_frame, text="Book Tatkal Ticket", command=self.handle_booking)
        submit_button.grid(row=len(self.fields) + 1, column=0, columnspan=2, pady=10)

        self.status_label = ttk.Label(left_frame, text="", foreground="green")
        self.status_label.grid(row=len(self.fields) + 2, column=0, columnspan=2, pady=5)

    def update_passenger_fields(self, num_passengers):
        """
        Dynamically update the passenger input fields based on the number of passengers.
        """
        num_passengers = int(float(num_passengers))

        for widget in self.passenger_frame.winfo_children():
            widget.destroy()

        self.passenger_entries = []
        row_index = 0
        for i in range(num_passengers):
            ttk.Label(self.passenger_frame, text=f"Passenger {i + 1}").grid(
                row=row_index, column=0, columnspan=2, sticky=tk.W, pady=10
            )
            row_index += 1

            ttk.Label(self.passenger_frame, text="Name:").grid(row=row_index, column=0, sticky=tk.W, pady=5)
            name_entry = ttk.Entry(self.passenger_frame)
            name_entry.grid(row=row_index, column=1, sticky=(tk.W, tk.E), pady=5)
            row_index += 1

            ttk.Label(self.passenger_frame, text="Age:").grid(row=row_index, column=0, sticky=tk.W, pady=5)
            age_entry = ttk.Entry(self.passenger_frame)
            age_entry.grid(row=row_index, column=1, sticky=(tk.W, tk.E), pady=5)
            row_index += 1

            ttk.Label(self.passenger_frame, text="Gender:").grid(row=row_index, column=0, sticky=tk.W, pady=5)
            gender_entry = ttk.Entry(self.passenger_frame)
            gender_entry.grid(row=row_index, column=1, sticky=(tk.W, tk.E), pady=5)
            row_index += 1

            self.passenger_entries.append({"Name": name_entry, "Age": age_entry, "Gender": gender_entry})

    def handle_booking(self):
        """
        Collect all form data and initiate the booking process.
        """
        values = {field: entry.get() for field, entry in self.entries.items()}

        passenger_details = []
        for entry_set in self.passenger_entries:
            passenger_details.append(
                {
                    "Name": entry_set["Name"].get(),
                    "Age": entry_set["Age"].get(),
                    "Gender": entry_set["Gender"].get(),
                }
            )

        values["Passengers"] = passenger_details

        try:
            print(values)

            booking_data = BookingData(**values)
            self.status_label.config(text="Booking process started successfully!", foreground="green")
        except ValidationError as e:
            error_messages = []
            for error in e.errors():
                field = error.get("loc", ["Unknown field"])[0]
                message = error.get("msg", "Unknown error")
                error_messages.append(f"{field}: {message}")

            if error_messages:
                error_summary = "\n".join(error_messages)
                self.status_label.config(text=f"Errors:\n{error_summary}", foreground="red")
            else:
                self.status_label.config(text="Unknown validation error.", foreground="red")


if __name__ == "__main__":
    root = tk.Tk()
    app = BookingApp(root)
    root.mainloop()
