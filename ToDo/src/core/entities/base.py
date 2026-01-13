
from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
import uuid

@dataclass(kw_only=True)
class BaseEntity(ABC):
    uuid: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


    def validate(self):
        pass

    def __post_init__(self):
        self.validate()