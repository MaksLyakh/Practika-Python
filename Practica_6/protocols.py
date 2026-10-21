from typing import Protocol


class Reportable(Protocol):
    def get_report_data(self) -> str:
        ...
