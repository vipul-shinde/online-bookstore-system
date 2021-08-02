# online-bookstore-system

```
# Emails will be sent from this email
email = kushaj123456@gmail.com
email_password = kushaj12345678

# To login to admin goto localhost:8000/admin
admin_password = 12345678
admin_email = kushaj@gmail.com
```

## Run website on local
- python = 3.8.8

Use [miniconda](https://docs.conda.io/en/latest/miniconda.html) to download python 3.8 and then

```
pip install -r requirements.txt
```

To run the website, navigate to "genlib" folder
```
cd genlib
python manage.py runserver
```

The server will be at "localhost:8000".

Goto "localhost:8000/admin" and enter credentials to access admin page. Here you can check all the values stored in the database.