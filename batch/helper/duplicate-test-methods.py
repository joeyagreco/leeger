import os
import collections
import sys

"""
Checks for duplicate test method names.
"""

dirPath = "test"

testMethods = collections.defaultdict(list)
currentClass = None

for root, dirs, files in os.walk(dirPath):
    for file in files:
        if file.endswith(".py"):
            with open(os.path.join(root, file), "r") as f:
                lines = f.readlines()
                for i, line in enumerate(lines, start=1):
                    line = line.strip()
                    if line.startswith("class Test"):
                        currentClass = line.split()[1].split("(")[0]
                    elif currentClass and line.startswith("def test_"):
                        method_name = line.split()[1].split("(")[0]
                        key = f"{currentClass}.{method_name}"
                        testMethods[key].append(f"{os.path.join(root, file)}: Line {i}")

duplicateMethods = {
    method: locations for method, locations in testMethods.items() if len(locations) > 1
}

if duplicateMethods:
    print("Duplicate Test Methods:")
    for method, locations in duplicateMethods.items():
        print(f"{method} found at:")
        for location in locations:
            print(location)
    sys.exit(1)
