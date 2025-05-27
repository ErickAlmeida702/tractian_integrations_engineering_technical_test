from domain.models import TracOSWorkorder
from datetime import datetime


class WorkorderTranslator:

    STATUS_MAPPING = {
        "isPending": "pending",
        "isOnHold": "on_hold",
        "isDone": "completed",
        "isCanceled": "cancelled",
        "isDeleted": "cancelled",
    }

    @staticmethod
    def client_to_tracos(data: CustomerWorkorder) -> TracOSWorkorder:
        status = WorkorderTranslator._resolve_status(data)

        return TracOSWorkorder(
            number=data.orderNo,
            status=status,
            title=data.summary,
            description=f"{data.summary} description",
            createdAt=data.creationDate,
            updatedAt=data.lastUpdateDate,
            deleted=data.isDeleted,
            deletedAt=data.deletedDate,
        )

    @staticmethod
    def tracos_to_client(data: TracOSWorkorder) -> CustomerWorkorder:
        return CustomerWorkorder(
            orderNo=data.number,
            summary=data.title,
            creationDate=data.createdAt,
            lastUpdateDate=data.updatedAt,
            isCanceled=data.status == "cancelled",
            isDeleted=data.deleted,
            isDone=data.status == "completed",
            isOnHold=data.status == "on_hold",
            isPending=data.status == "pending",
            deletedDate=data.deletedAt,
        )

    @staticmethod
    def _resolve_status(data: CustomerWorkorder) -> str:
        for key, value in data.dict().items():
            if key in WorkorderTranslator.STATUS_MAPPING and value:
                return WorkorderTranslator.STATUS_MAPPING[key]
        return "pending"
