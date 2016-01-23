KAYAK flight scanner
----

This tool uses splinter to open a firefox window and hit kayak website
based on dates and airports.

At the moment tries a multi city search:

Origin/Destination: From and To where the trip starts and ends.
Airport A: Arrival's airport
Airport B: Departure's airport

Installation:

`pip install -i requirements.txt`


Setup:

`python setup_db.py`


Run:

`python main.py`

Note: Kayak limits the number of requests so every ~30mins or so it will ask you to
verify you are not a boot, you need to pass that verification otherwise this tool
won't catch anything.
