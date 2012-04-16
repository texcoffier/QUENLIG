# Version
version = "2.3.6"

# URL Of the Centralized Authentification service
CAS = 'https://cas.univ-lyon1.fr/cas'

# If the student stays with a question displayed longer than this time,
# then we do not count the time as thinking time.
timeout_on_question = 1800 # In seconds

# Once per 10 hour, a new ticket is asked to CAS
timeout = 36000 # in seconds

# Statistics take some time to compute.
# We don't want to compute them every time, so they are cached some time.
statistics_cpu_allocation = 1 # % of time used to compute statistics

# For INPUT / TEXTAREA
nr_columns = 60




