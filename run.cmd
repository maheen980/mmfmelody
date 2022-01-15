@REM # redis-server
@REM # virtualenv env
@REM python manage.py makemigrations core
@REM python manage.py migrate
@REM python manage.py createsuperuser
@REM python manage.py collectstatic
python manage.py runserver
@REM # pip freeze > requirements.txt
@REM # pip install -r requirements.txt

@REM # npm i -g loadtest
@REM # loadtest -n 100 -k  https://localhost:8000/

@REM # Themes 
@REM # python manage.py loaddata admin_interface_theme_bootstrap.json
@REM # python manage.py loaddata admin_interface_theme_foundation.json
@REM # python manage.py loaddata admin_interface_theme_uswds.json