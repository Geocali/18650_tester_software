import tester
import pytest
import json

def atest():
    test_state = {1: 0, 2: 0, 3: 0, 4: 0}
    jsons = json.dumps(test_state)
    f = open("test_state.json","w")
    f.write(jsons)
    f.close()
    tester.main_function()


if __name__ == "__main__":
    atest()
