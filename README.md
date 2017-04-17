# LSVLM GUI

## Dear Software Engineering Course Evaluators

You do not need to install anything in order to evaluate our software.  The official version of what we have written is hosted at https://lm.lsv.uni-saarland.de.  You may use the username 'antonyan' and the password '123456789' in order to log in to the system.  The section below is for developers who wish to have a local, offline version of the site.

## How to install

1. Install django and django related dependencies:
    
    In order to uninstall any conflicting django installations:

        pip uninstall django
    
    To avoid database problems, please use the older version of django in which the original project was written.
    
        pip install django==1.7.7
        
    Then install the following django apps:

        pip install django-jsonify
        pip install django-sslserver
        pip install django-jsonfield

2. Install mod-wsgi:
    
    The following command is specific to ubuntu. One can install these packages in any nix platform using appropriate commands. Also, python-dev may come pre-installed on the system.
    
        sudo apt-get install -y python-dev apache2-dev 
    
    Then, install the python wrapper:
    
        pip install mod_wsgi

3. Install LDAP:

    The following command is specific to ubuntu. One can install these packages in any nix platform using appropriate commands.

        sudo apt-get install -y libldap2-dev libsasl2-dev libssl-dev

    Then, install the python wrapper for ldap and ldap authentication:

        pip install python-ldap
        pip install django-auth-ldap

4. Build the django database:
    
    Make sure you have the latest db.sqlite3 file as this is not always included in the version control.
    
        python manage.py migrate

5. Run server:
    
    You can run the server using python, which will server the website on http://127.0.0.1:8000, or you can configure apache.
    
        python manage.py runserver

## Notes

This configuration has been tested with Python version 2.7

