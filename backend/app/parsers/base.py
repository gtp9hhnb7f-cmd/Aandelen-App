from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterable
from app.models import Transaction


class BrokerParser(ABC):
    @abstractmethod
    def parse(self, file_path: Path) -> Iterable[Transaction]:
        raise NotImplementedError
