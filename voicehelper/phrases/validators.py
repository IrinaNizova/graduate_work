from typing import Optional

from pydantic.main import BaseModel


class Response(BaseModel):
    user_id: str
    session_id: str
    message_id: int
    skill_id: str
    application_id: str
    version: str
    text: Optional[str]
    dialogue: Optional[int]
    speech: Optional[int]

    def to_json(self) -> dict:
        return {
            "session": {
                "message_id": self.message_id,
                "session_id": self.session_id,
                "skill_id": self.skill_id,
                "user": {"user_id": self.user_id},
                "application": {"application_id": self.application_id},
                'new': False,
                "user_id": self.application_id,
            },
            "version": self.version,
            "response": {
                "end_session": False,
                "text": self.text
            },
            "session_state": {
                "dialogue": self.dialogue,
                "speech": self.speech
            }
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
