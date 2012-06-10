Test Reports
============

XML Reports
-----------
Test results are written into xUnit XML test reports. Report is generated for each test executed under file name `<testname>.result.xml`. XML result files are placed into bunch results directory. The results of common dependency fixtures are placed into `setup.result.xml` and `teardown.result.xml`.

HTML reports
____________

Just use::

bunch --output-plugin="checklist_layout" --plugin-params="dst_dir=/var/www/" test_bunch ./result_dir

And you get static HTML site with test reports.  All further results are linked by this index and are kept together.

