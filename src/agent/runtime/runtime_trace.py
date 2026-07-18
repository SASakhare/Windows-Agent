from pathlib import Path
from pprint import pformat
from datetime import datetime


class RuntimeTracer:

    def __init__(self, file_name: str = "runtime_trace.log") -> None:
        self._file = Path(file_name)

    def start_run(self):

        with open(self._file, "a", encoding="utf-8") as f:

            f.write("\n")
            f.write("=" * 140)
            f.write("\n")
            f.write(f"NEW RUNTIME : {datetime.now()}")
            f.write("\n")
            f.write("=" * 140)
            f.write("\n\n")

    def iteration(self, iteration: int):

        with open(self._file, "a", encoding="utf-8") as f:

            f.write("\n")
            f.write("#" * 140)
            f.write("\n")
            f.write(f"ITERATION : {iteration}")
            f.write("\n")
            f.write("#" * 140)
            f.write("\n\n")

    def stage(self, name: str, data):

        with open(self._file, "a", encoding="utf-8") as f:

            f.write("=" * 120)
            f.write("\n")
            f.write(f"{name.upper()}")
            f.write("\n")
            f.write("=" * 120)
            f.write("\n")

            f.write(pformat(data))
            f.write("\n\n")