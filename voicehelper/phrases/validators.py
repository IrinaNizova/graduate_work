from marshmallow import Schema, fields


class Request(Schema):
    user_id = fields.Str(required=True)
    session_id = fields.Str(required=True)
    message_id = fields.Int(required=True)
    skill_id = fields.Str(required=True)
    application_id = fields.Str(required=True)
    version = fields.Str(required=True)
    text = fields.Str()
    tokens = fields.List(fields.Str())
    dialogue = fields.Int(required=False)
    speech = fields.Int(required=False)


