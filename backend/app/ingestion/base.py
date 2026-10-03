from abc import ABC, abstractmethod
from pathlib import Path
from typing import Tuple
import pandas as pd
from app.core.contracts import DatasetMetadata


class BaseLoader(ABC):
    """Abstract base class for format-specific dataset loaders."""

    @abstractmethod
    def load(self, file_path: Path) -> Tuple[pd.DataFrame, DatasetMetadata]:
        """Load a dataset file into a pandas DataFrame and return metadata."""
        pass
