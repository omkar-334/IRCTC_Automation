# IRCTC Ticket Automation

This is not an application for exploring trains or tickets. You must know all details of the train and passengers beforehand.

A Tkinter GUI is provided for data entry. However, you can choose to enter default values in `values.py` beforehand to save time. For filling the default values - refer to `dropdowns.py` . Any wrong entry will result in an error.

Note - For **FromStation** & **ToStation** - Check https://www.irctc.co.in/nget/train-search for exact station names and paste.

### Process
1. Enter the train details form
2. Select ticket
3. Sign in 
4. Add passengers
5. Start Payment

From here on , you have to continue the payment process manually.

Note - During Step 3 (Sign in) - There is a captcha which you have to fill manually. The script will wait for 10 seconds then continue.