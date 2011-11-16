===============================
Bunch Test Organizer and Runner
===============================

Bunch is tool for grouping, managing and running Lettuce scenarios. It offers explicit separation of test fixtures from test scenarios by dividing it into setup, teardown and test scripts. Bunch encourages writing clean, self-sufficient and multi-environment tests, which can be executed in parallel. It also provides more flexibility for test parameterization - test scenarios are treated as templates, which get parameterized upon execution.

Features
========

.. include:: features.rst


Installation
============

Just do the following::

        user@machine:~/projects$ git clone  git.griddynamics.net:~skosyrev/repos/bunch
        user@machine:~/projects$cd bunch
        user@machine:~/projects/bunch$  python setup.py install


Writing Tests
=============

Bunch test scenarios are basically ``Lettuce`` feature files which are organized in special order.


Organizing Test Scenarios
-------------------------

Tests are grouped into bunches. All tests in a bunch are considered to be independent and may be executed in any order or even in parallel.

``Test`` is a group of Lettuce scenarios of three types located in the same directory. These types are differentiated by file extensions:

* `<name>.test` is main scenario for test `<name>`
* `<name>.<configuration_name>.setup` is setup fixture for test `<name>` intended for test configuration `<configuration_name>`
* `<name>.<configuration_name>.teardown` is teardown fixture for test `<name>` intended for test configuration `<configuration_name>`

``Bunch`` consists  of ``tests`` and ``config.yaml`` file. All bunch items are located in the same directory, i.e. all Lettuce scenarios, Python files and configuration data.

``config.yaml`` is bunch-wide configuration file containing parameter values for scenario templates.

Test parameterization
---------------------

Every Lettuce scenarios in a bunch is considered as template. That means that scenarios may contain ``Jinja2`` template expressions. The template expression are expanded with values taken from ``config.yaml`` file. See examples below.

If we have user item in the ``config.yaml``::

        user:
          name: admin1

Then we can use it in the ``sample_test.setup``::

        Feature: Make preparations for sample test
                Scenario: Create admin user
                        Create admin user "{{user.name}}"
                        Check user "{{user.name}}" exist

The presence of bunch config and templates is not necessary. If ommitted then no parameterization is performed. It is also possible to use some global config file for each bunch execution::

        >>>bunch -c /pathto/config  bunch_sourec results_dir

The global config file can be used along with local per-bunch configs. In that case global variables are loaded first then local variables are loaded on bunch execution. The variables with the same names get overriden with local values.


Test Fixtures and Dependencies
------------------------------

By default all tests are dependent from their fixtures of any. But it is possible to specify that test requires extra setup performed prior its execution. The dependency spefication is performed via special Lettuce steps in \*.test scenario::
        
        Requires setup: "<list of setup fixtures required>"
And ::

        Requires external setup: "<list of setup fixtures from other bunches>"

The `<list of setup fixtures required>` is the white-space or newline separated list of fixture names which should be executed and return successful result before test run. Setup scripts may be executed in parrallel and started in the order specified in the "Requires setup:" statement. Often setup actions rely on each other and so should be executed sequentially. For that reason syncronization quantifier may be used. Just put exclamation mark between fixture names, to specify the point of syncronization::

        setup1 ! setup2 setup3 ! setup_final

This splits fixtures into groups. All fixtures within single group are executed in parallel. Also it is possible to make it run sequentially in specific order::

        setup1 ! setup2 ! setup3! setup_final

The corresponding teardown scripts are executed after test is finished, so there is no need to specify that particular teardown is required.


Running Tests
=============

Tests may be executed via `bunch` console script or via `bunch.cli.main()` function::

        >>>bunch  samples/dummy results

The `results` directory will contain parameterized scenarios and test results.


Execution parallellism
----------------------

The `-b` command option controls bunch execution concurrency. It may have the following values:

* `serial` - tests are executed in single thread
* `unlimited` - all tests may be executed in parallel if possible
* `limited<n>` - tests are executed within <n> threads
* `auto` - tests are executed according to machine capabilities and the common sense

Test Results
============

Test results are written into xUnit XML test reports. Report is generated for each test which was executed as `<testname>.result.xml`
