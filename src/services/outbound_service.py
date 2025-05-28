import os
import json
from pathlib import Path
from src.services.translator import WorkorderTranslator
from src.domain.models import TracOSWorkorder
from src.repositories.workorder_repository import TracOSWorkorderRepository
import logging


class OutboundService:
    def __init__(self, repo: TracOSWorkorderRepository, outbound_dir: str):
        self.repo = repo
        self.outbound_dir = Path(outbound_dir)
        self.outbound_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(__name__)

    async def export_unsynced_workorders(self) -> None:
        unsynced = await self.repo.get_unsynced()
        self.logger.info(f"Found {len(unsynced)} unsynced records.")

        for wo in unsynced:
            try:
                tracos_wo = TracOSWorkorder(**wo)
                client_wo = WorkorderTranslator.tracos_to_client(tracos_wo)
                file_path = self.outbound_dir / f"{client_wo.orderNo}.json"
                with open(file_path, "w") as f:
                    json.dump(client_wo.model_dump(), f, indent=2, default=str)

                await self.repo.mark_as_synced(tracos_wo.number)
                self.logger.info(f"Exported {file_path.name} successfully.")

            except Exception as e:
                self.logger.error(f"Failed to export workorder {wo.get('number')}: {e}")

