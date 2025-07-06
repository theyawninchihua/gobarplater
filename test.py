import json
from pathlib import Path

from llm_tools import *

if __name__ == "__main__":

    for spec_name in ["ScorecardSpec"]:

        test_file = Path(f"tests/{spec_name}.json")

        if not test_file.exists():
            print(f"Testing tool {spec_name}: testcases file not found")
            continue

        with test_file.open() as f:
            testcases = json.load(f)

        for testcase in testcases:
            spec = eval(spec_name)(**testcase["args"])
            scorecard(spec)