from sqlalchemy import orm
import datetime
from sqlalchemy import schema, types

metadata = schema.MetaData()

def now():
    return datetime.datetime.now()

reading_table = schema.Table('reading', metadata,
    schema.Column('id', types.Integer,
        schema.Sequence('reading_seq_id', optional=True), primary_key=True),
    schema.Column('probeid', types.Integer, schema.ForeignKey('probe.id')),
    schema.Column('created', types.TIMESTAMP(), default=now()),
    schema.Column('content', types.Text(), nullable=False),
)

probe_table = schema.Table('probe', metadata,
    schema.Column('id', types.Integer,
        schema.Sequence('probe_seq_id', optional=True), primary_key=True),
    schema.Column('name', types.Unicode(255)),
    schema.Column('sourceid', types.Integer, schema.ForeignKey('source.id')),
)

source_table = schema.Table('source', metadata,
    schema.Column('id', types.Integer,
        schema.Sequence('source_seq_id', optional=True), primary_key=True),
    schema.Column('name', types.Unicode(255)),
)

class Reading(object):
    pass

class Probe(object):
    def __init__(self, name = None):
        self.name = name

class Source(object):
    pass

orm.mapper(Reading, reading_table, properties={
    'source':orm.relation(Probe, backref='probe'),
})
orm.mapper(Probe, probe_table, properties={
    'source':orm.relation(Source, backref='source'),
})
orm.mapper(Source, source_table)