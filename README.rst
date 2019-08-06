.. image:: https://travis-ci.org/SFB-ELAINE/ckanext-vtkjs.svg?branch=master
    :target: https://travis-ci.org/SFB-ELAINE/ckanext-vtkjs

=============
ckanext-vtkjs
=============

This is a CKAN extension that provides views for STL, VTP, VTI, and VTK PolyData files,
as well as ZIP archives containing OBJ files.

------------
Requirements
------------

Tested with CKAN 2.9.0a.

------------
Installation
------------

.. Add any additional install steps to the list below.
   For example installing any non-Python dependencies or adding any required
   config settings.

To install ckanext-vtkjs:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Install the ckanext-vtkjs Python package into your virtual environment::

     pip install ckanext-vtkjs

3. Add ``vtkjs`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``). Do **not** add ``vtkjs`` to the
   list of default views - the plugin automatically adds itself as a view to
   any resource it can display, and adding it to the list of default views
   causes it to be added to some types of resources that it cannot display.

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload


---------------
Config settings
---------------

None at present.

.. Document any optional config settings here. For example::

.. # The minimum number of hours to wait before re-checking a resource
   # (optional, default: 24).
   ckanext.vtkjs.some_setting = some_default_value


----------------------
Developer installation
----------------------

To install ckanext-vtkjs for development, activate your CKAN virtualenv and
do::

    git clone https://github.com//ckanext-vtkjs.git
    cd ckanext-vtkjs
    python setup.py develop
    pip install -r dev-requirements.txt


-----
Tests
-----

To run the tests, do::

    nosetests --nologcapture --with-pylons=test.ini

To run the tests and produce a coverage report, first make sure you have
coverage installed in your virtualenv (``pip install coverage``) then run::

    nosetests --nologcapture --with-pylons=test.ini --with-coverage --cover-package=ckanext.vtkjs --cover-inclusive --cover-erase --cover-tests
