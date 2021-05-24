from typing import Optional

from pydantic.main import BaseModel


class Response(BaseModel):
    user_id: str
    session_id: str
    message_id: str
    version: float
    text: Optional[str]
    dialogue: Optional[int]
    speech: Optional[int]

    def to_json(self) -> dict:
        return {
            "response": {
                "text": self.text,
                "end_session": False
            },
            "session": {
                "message_id": self.message_id,
                "session_id": self.session_id,
                "user_id": self.user_id
            },
            "version": self.version
        }


class Request(BaseModel):
    user_id: str
    session_id: str
    message_id: str
    version: float
    text: str
    tokens: list
    dialogue: Optional[int]
    speech: Optional[int]
