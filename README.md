Brief description or introduction of this project.

1. Create the virtual environment:
python -m venv venv
linux => source/bin/activate
windows => venv/Scripts/activate

2. Install dependencies:
python -m pip install --upgrade pip
pip install -r requirements.txt

3. Apply database migrations:
python manage.py makemigrations
python manage.py migrate

4. Create a superuser
python manage.py createsuperuser

5. Apply the seeder - for Payment structures - apps/client/fixtures/payment_struct.json
python manage.py loaddata payment_struct

6. Run the server 
python manage.py runserver
