import sys, os, django
from django.core import serializers

sys.path.append("../nycCivilServiceJobs")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nycCivilServiceJobs.settings")
django.setup()
from register.models import User
from django.core.exceptions import ObjectDoesNotExist

job_seekers = [
    {
        "username": "prof_test",
        "first_name": "Gennadiy",
        "last_name": "Civil",
        "email": "prof@domain.com",
        "password": "FjmJpdz45",
        "dob": "1994-10-02",
        "is_hiring_manager": False,
    },
    {
        "username": "ta_test",
        "first_name": "Jack",
        "last_name": "Xu",
        "email": "ta@domain.com",
        "password": "jBUC99AJQ",
        "dob": "1994-10-02",
        "is_hiring_manager": False,
    },
    {
        "username": "test1",
        "first_name": "John",
        "last_name": "Doe",
        "email": "johndoe@domain.com",
        "password": "RbxEb9vhU",
        "dob": "1994-11-02",
        "is_hiring_manager": False,
    },
    {
        "username": "test2",
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "janedoe@domain.com",
        "password": "N2SeetrRn",
        "dob": "1987-03-25",
        "is_hiring_manager": False,
    },
    {
        "username": "test3",
        "first_name": "Mary",
        "last_name": "Jane",
        "email": "maryjane@domain.com",
        "password": "D3dn3tb2n",
        "dob": "1999-12-02",
        "is_hiring_manager": False,
    },
    {
        "username": "test4",
        "first_name": "John",
        "last_name": "Adams",
        "email": "johnadams@domain.com",
        "password": "T6Wyzjv7X",
        "dob": "1990-11-02",
        "is_hiring_manager": False,
    },
    {
        "username": "test5",
        "first_name": "Jane",
        "last_name": "Adams",
        "email": "janeadams@domain.com",
        "password": "KgqQtE4PR",
        "dob": "1997-10-03",
        "is_hiring_manager": False,
    },
]

for user in job_seekers:

    try:
        u = User.objects.get(username=user["username"])
        newuser = u
        for attr, val in user.items():
            if attr == "password":
                newuser.set_password(val)
            else:
                setattr(newuser, attr, val)
    except ObjectDoesNotExist:
        newuser = User.objects.create_user(**user)
    newuser.save()
