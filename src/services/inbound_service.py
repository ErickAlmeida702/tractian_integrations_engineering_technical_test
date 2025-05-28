import os
import json
from pathlib import Path
from typing import Any

from src.domain.models import CustomerWorkorder
from src.services.translator import WorkorderTranslator
from src.repositories.workorder_repository import TracOSWorkorderRepository
import logging
from pydantic import ValidationError

REQUIRED_FIELDS = ['id', 'status', 'createdAt']


class InboundService:
    def __init__(self, repo: TracOSWorkorderRepository, inbound_dir: str):
        self.repo = repo
        self.inbound_dir = Path(inbound_dir)
        self.logger = logging.getLogger(__name__)

    async def process_inbound_files(self) -> None:
        files = list(self.inbound_dir.glob("*.json"))
        self.logger.info(f"Found {len(files)} files to process.")
        for file_path in files:
            await self._process_file(file_path)


    async def _process_file(self, path: Path) -> None:
        try:
            with open(path, "r") as f:
                raw: dict[str, Any] = json.load(f)

            missing = [field for field in REQUIRED_FIELDS if field not in raw]
            if missing:
                self.logger.error(f"{path.name} is missing required fields: {', '.join(missing)}")
                return

            customer_data = CustomerWorkorder(**raw)
            tracos_data = WorkorderTranslator.client_to_tracos(customer_data)
            await self.repo.upsert(tracos_data)

            self.logger.info(f"Processed {path.name} successfully.")

        except json.JSONDecodeError as e:
            self.logger.error(f"{path.name} contains invalid JSON: {e}")
        except ValidationError as e:
            self.logger.error(f"Validation error in {path.name}: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error processing {path.name}: {e}")
