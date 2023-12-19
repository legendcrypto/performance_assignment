# performance_assignment
Developed APIs for a Vendor Management System comprising three core models: Vendor, Purchase Order, and Historical Performance. The project's primary objective was to assess performance metrics associated with vendors, gauging the efficiency in managing the procurement and delivery processes.

Steps to run the project:
1. Clone the repo using the HTTPS link inside a folder.
2. Install the virtual environment using python -m venv venv_name. (If you are using windows)
3. Once installed, activate it using venv/Scripts/activate.
4. Go to the performance_assignment folder and install the dependancies using the requirements file with the command: pip install -r requirements.txt.
5. Run the makemigrations command: python manage.py makemigrations
6. Run the migrate command: python manage.py migrate.
7. Also create a superuser: python manage.py createsuperuser. And then follow the steps coming on the prompt.
8. Then as suggested, test the APIs with the endpoints mentioned in the doc: https://drive.google.com/file/d/1hLWc35hpLQ0EPDAZjZloomeAxgn3V7g9/view. The id in the url should be the one present in the database of a corresponding instance.
9. For testing the performance API, create two or three purchase order corresponding to vendor with the status as default i.e. pending and fill all the required fields.
10. Then mark or update the status to "completed" from the admin panel or the patch api for a purchase order, if the expected delivery date you have assigned is greater than the time you are making the change. The on_time_delivery_rate for that vendor will be shown as 1.0 as expected and the fullfillment rate should be 1/3 i.e. 0.33.
11. Same can be checked for other metrics i.e. avergae quality rate and the average_response_time using the doc mentioned above.

Steps to run the test cases:
1. From the directory performance_assignment run the command: python manage.py test and can see that the tests so written will run successfully.
