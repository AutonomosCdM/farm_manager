import uuid
from datetime import datetime
from typing import List, Dict, Optional, Any


class Machinery:
    """Class representing agricultural machinery resources."""

    def __init__(
        self,
        name: str,
        type: str,
        status: str = "available",
        last_maintenance_date: Optional[str] = None,
        purchase_date: Optional[str] = None,
        id: Optional[str] = None,
    ):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.type = type
        self.status = status
        self.last_maintenance_date = last_maintenance_date
        self.purchase_date = purchase_date

    def to_dict(self) -> Dict[str, Any]:
        """Convert machinery object to dictionary for serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "status": self.status,
            "last_maintenance_date": self.last_maintenance_date,
            "purchase_date": self.purchase_date,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Machinery":
        """Create machinery object from dictionary."""
        return cls(
            id=data.get("id"),
            name=data["name"],
            type=data["type"],
            status=data["status"],
            last_maintenance_date=data.get("last_maintenance_date"),
            purchase_date=data.get("purchase_date"),
        )


class Personnel:
    """Class representing agricultural personnel resources."""

    def __init__(
        self,
        name: str,
        role: str,
        department: str,
        status: str = "available",
        skills: List[str] = None,
        id: Optional[str] = None,
    ):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.role = role
        self.department = department
        self.status = status
        self.skills = skills or []

    def to_dict(self) -> Dict[str, Any]:
        """Convert personnel object to dictionary for serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "department": self.department,
            "status": self.status,
            "skills": self.skills,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Personnel":
        """Create personnel object from dictionary."""
        return cls(
            id=data.get("id"),
            name=data["name"],
            role=data["role"],
            department=data["department"],
            status=data["status"],
            skills=data.get("skills", []),
        )
