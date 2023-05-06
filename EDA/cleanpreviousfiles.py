import os

# Remove previously saved files
def cleanpreviousfiles():
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for f in files:
        if f.endswith('.csv'):
            os.remove(f)