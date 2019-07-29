# Flask-API
- To run the application, with elasticsearch running locally, run api.py from the command line and enter your host and port when prompted (e.g. localhost, 9200)
- Same process to run the tests: with elasticsearch running locally, run tests.py from the command line and enter your host and port when prompted (e.g. localhost, 9200)
- Names are converted to ID's by replacing spaces with dashes and lowering the case. When querying name from URLs, make sure the names are in the ID format
- The data is refreshed every time the application starts and everytime the tests are run