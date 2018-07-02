import os

with open(os.path.join(os.path.dirname(__file__), 'test_blocklist_sigmaprojects.data'), 'rb') as handle:
    REPORT_DATA = handle.read()
print(REPORT_DATA)
