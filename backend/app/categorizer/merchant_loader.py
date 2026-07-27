import json
from pathlib import Path


class MerchantLoader:

    _cache = None

    @classmethod
    def load(cls):

        if cls._cache is None:

            file_path = (
                Path(__file__).resolve()
                .parent.parent
                / "data"
                / "merchants.json"
            )

            with open(file_path, "r", encoding="utf-8") as f:

                cls._cache = json.load(f)

        return cls._cache