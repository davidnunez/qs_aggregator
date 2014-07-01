import model
import json
from sqlalchemy import orm
from sqlalchemy import create_engine

import _keys
from moves import MovesClient


# from http://stackoverflow.com/questions/2546207/does-sqlalchemy-have-an-equivalent-of-djangos-get-or-create
def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        return instance

# Create an engine and create all the tables we need
engine = create_engine('sqlite:///:memory:', echo=True)
model.metadata.bind = engine
model.metadata.create_all()

# Set up the session
sm = orm.sessionmaker(bind=engine, autoflush=True, autocommit=False,
    expire_on_commit=True)
session = orm.scoped_session(sm)

#### moves.app

probe_moves_move = get_or_create(session, model.Probe, name='moves_segment_move')
probe_moves_place = get_or_create(session, model.Probe, name='moves_segment_place')

# grab daily segments from moves api
mc = MovesClient() 

response = mc.api('user/storyline/daily', 'GET', params={'pastDays':'3', 'access_token':_keys.moves_token})
response_jsons = json.loads(response.text)

for response_json in response_jsons:
	print '--------------'
	segments = response_json['segments']
	for segment in segments:
		if segment['type'] == 'place':
			reading = model.Reading()
			reading.type = probe_moves_place
			reading.content = json.dumps(segment)
			session.add(reading)
			session.flush()
			session.commit()
			print segment['place']['name']
		if segment['type'] == 'move':
			reading = model.Reading()
			reading.type = probe_moves_move
			reading.content = json.dumps(segment)
			session.add(reading)
			session.flush()
			session.commit()

# TODO: connect to mongodb
# TODO: check for duplicate entries before adding to db (or maybe deal with them as updates)

#### toggl

probe_toggl = get_or_create(session, model.Probe, name='toggl')

