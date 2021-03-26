# Assignment 4: A sensor driver website

1. It should work as cloned from git, after venv and pip install -r requirements.txt.
2. You should install your software on your itwot server using the /opg4a/ or /opg4b/ redirects
3. Your system should have the functionality described above, reflecting your level of ambition with regards to the level of functionality.
4. Your Python code should adher to the Pylint (or PEP-8) standard, and your JavaScript code should adher to the Semi-Standard JS coding style
5. Your program must create the necessary tables in the database, if they do not already exist.
6. You should only store valid data in your database.
7. Your system should be able to handle an empty measurement set gracefully
8. Your code should be well structured and well, but not excessively, commented
9. Your overall folder structure should be neat
10. The Web pages should be readable and usable
11. A more ambitious solution will earn more points. A well executed solution will earn more points than a 
poorly executed one, regardless of ambition level, so start at the basic level and work up to the level, 
you desire.

## A basic solution
- The M5SC+ uses request (from MicroPython or UIFlow) to send measurements to the server.
- The server generates the Web pages wholly on the server.
- If the user desires the latest measurements, they reload the pages.

## A medium solution
- The M5SC+ also displays minimum/maximum values (since it was turned on).
- XMLHttpRequest is used to update the front page without the need of reloading the page.
- The measurements are paged (for example, 20 rows of measurements per page) with links to go back and forth between pages of measurements.

## An advanced solution
- MQTT (from MicroPython or UIFlow) is used to transfer measurements from M5SC+ to the server and the front page.
- The measurements are paged, but without requiring loading new pages.