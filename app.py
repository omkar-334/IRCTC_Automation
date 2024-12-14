from tkinter import Button, Entry, Frame, Label


class BookingGui(Frame):
    def __init__(self, master, labels):
        """
        For Creating interactive GUI for IRCTC automation
        :param master:
        :param labels:
        """
        super().__init__(master)
        self.label = labels
        self.passenger = ["PassengersDetail:", "Psg:One", "Psg:Two", "Psg:Three", "Psg:Four"]
        self.entry = {}
        self.values = {}

    def main_gui(self):
        """
        For creating interactive GUI for IRCTC Automation
        """
        for label_index, label_value in enumerate(self.label):
            Label(self, text=label_value).grid(row=label_index + 1, column=0)
            self.entry[label_value] = Entry(self, show="*") if label_value == "Password" else Entry(self)
            self.entry[label_value].grid(row=label_index + 1, column=1)

        for passenger_index, passenger_label in enumerate(self.passenger):
            Label(self, text=passenger_label).grid(row=10, column=passenger_index)

        for index, value in enumerate(self.label[10:], start=12):
            Label(self, text=value).grid(row=index, column=0)
            for extra_index in range(4):
                self.entry[value + str(extra_index)] = Entry(self)
                self.entry[value + str(extra_index)].grid(row=index, column=extra_index + 1)

        Button(self, text="Book Tatkal Ticket", command=self._login_btn_clicked).grid(row=5, column=3)

    def _login_btn_clicked(self):
        """
        It will start the portal with provided value
        """
        for label in self.label[:10]:
            self.values[label] = self.entry[label].get()

        for temp_index in self.label[10:]:
            for extra_index in range(4):
                self.values[temp_index + str(extra_index)] = self.entry[temp_index + str(extra_index)].get()
