from marshmallow import Schema, fields


class EventSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    description = fields.String()
    start_time = fields.DateTime(dump_to='startTime', format='iso')
    end_time = fields.DateTime(dump_to='endTime', format='iso')
    total = fields.Integer()
    taken = fields.Integer()
    available = fields.Integer()
