from src.domain.models import TracOSWorkorder, CustomerWorkorder
from datetime import datetime
from typing import Literal, Dict



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
        status = WorkorderTranslator._map_status(data)

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
            orderNo=data['number'],
            summary=data['title'],
            creationDate=data['createdAt'],
            lastUpdateDate=data['updatedAt'],
            isCanceled=data['status'] == "cancelled",
            isDeleted=data['deleted'],
            isDone=data['status'] == "completed",
            isOnHold=data['status'] == "on_hold",
            isPending=data['status'] == "pending",
            deletedDate=data['deletedAt'],
        )

    @staticmethod
    def _map_status(data: CustomerWorkorder) -> Literal["pending", "in_progress", "completed", "on_hold", "cancelled"]:
        if data.isPending:
            return "pending"
        elif data.isOnHold:
            return "on_hold"
        elif data.isDone:
            return "completed"
        elif data.isCanceled:
            return "cancelled"
        else:
            return "in_progress"
