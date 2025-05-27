import os
import json
import logging
from pathlib import Path
from typing import Any
from services.translator import WorkorderTranslator
from repositories.workorder_repository import TracOSWorkorderRepository


class FileExporter:
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export(self, filename: str, data: dict[str, Any]) -> Path:
        file_path = self.output_dir / f"{filename}.json"
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2, default=str)
        return file_path


class OutboundService:
    def __init__(
        self,
        repo: TracOSWorkorderRepository,
        exporter: FileExporter,
        translator: WorkorderTranslator = WorkorderTranslator(),
    ):
        self.repo = repo
        self.exporter = exporter
        self.translator = translator
        self.logger = logging.getLogger(__name__)

    async def export_unsynced_workorders(self):
        workorders = await self.repo.get_unsynced()
        self.logger.info(f"Found {len(workorders)} unsynced records.")

        for wo in workorders:
            number = wo.get("number")
            try:
                client_wo = self.translator.tracos_to_client(wo)
                file_path = self.exporter.export(str(client_wo["orderNo"]), client_wo)
                await self.repo.mark_as_synced(number)
                self.logger.info(f"Exported {file_path.name} successfully.")

            except (KeyError, IOError, ValueError) as e:
                self.logger.error(f"Error exporting workorder {number}: {e}")
