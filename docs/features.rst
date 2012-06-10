========
Features
========

Implemented features
====================

* Test parameterization via Jinja2 templates and YAML configs
* Test fixture separation
* Fixture grouping by test configuration. That will help writing environment agnostic tests which require different fixture versions for each environment
* Dependencies for test fixtures: setup and teardown scripts associated with test may be shared within test bunch and between different bunches
* xUnit XML reports. This is handy for using Bunch with CI tools
* HTML reports feature. Test reports are stored as static Web site
* MustFail feature. Create exemptions for your failing steps, scenarios and features. Get reports without failure while keeping notified about bug presence and bug status.

Planned features
================
* Parallel test scenario execution
