from marshmallow import Schema, fields


class EventSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    description = fields.String()
    start_time = fields.DateTime(dump_to='startTime', load_from='startTime', format='iso', required=True)
    end_time = fields.DateTime(dump_to='endTime', load_from='endTime', format='iso')
    total = fields.Integer()
    taken = fields.Integer(dump_only=True)
    available = fields.Integer(dump_only=True)


class EventBookSchema(Schema):
    number = fields.Integer(load_only=True)
