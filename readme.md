
BACS Platform
==================
A super straightforward implementation of Wagtail CMS.

# Installation locally
It should be sufficient to simply run `vagrant up` to load the project.
```
vagrant up
vagrant ssh
python manage.py runserver 0.0.0.0:8000
```

### Loading mock data
Given that it's a content management system it's quite useful to have some data :)

You can load it in by running `python manage.py load_initial_data`.

### Logging in
Once you've run `python manage.py load_initial_data.py` you'll be able to visit [http://localhost:8000/admin/](http://localhost:8000/admin/) and login using
Username: test
Password: password123

### Troubleshooting local installation problems
On the `vagrant up` command the vagrant/provision.sh file will run

```
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
```

Occassionally (because the computer has gone to sleep etc) that process may not run smoothly. In that instance wait for `vagrant up` to complete, then `vagrant ssh` into the VM and run the above commands.

# Apps included
- theplatform
- People
- Skills
- Location


## Initial Work Plan

### Frontend development
1. Add a theme to make sure the BACS website is available

### User registration
1. Add user registration form with discussed fields
2. Create a admin interface to verify/activate users
3. Send confirmation mail to user

### Event Mangement
1. Add new event management section on admin
2. Assign a user to that specific event
3. Under event there will be various pages, forms, gallery

