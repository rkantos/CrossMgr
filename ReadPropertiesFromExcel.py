import re
import Utils
import Model

sheetName = '--CrossMgr-Properties'

HeadersFields = (
	('Event Name',		'name', 			's'),
	('Event Organizer',	'organizer',	 	's'),
	('Event City',		'city',				's'),
	('Event StateProv',	'stateProv',		's'),
	('Event Country',	'country',			's'),
	('Event Date',		'date',				's'),
	('Scheduled Start',	'scheduledStart',	's'),
	('Discipline',		'discipline',		's'),
	('Race Number',		'raceNum',			'n'),
	('Enable RFID',		'enableJChipIntegration',	'b'),
	('Distance Unit',	'distanceUnit',		's'),
	('Time Trial',		'isTimeTrial',		'b'),
)

HeadersToFields = dict( (h, p) for h, p, t in HeadersFields )
FieldType = dict( (p, t) for h, p, t in HeadersFields )
HeaderSet = set( h for h, p, t in HeadersFields )

reStartDate = re.compile( '^[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]$' )
reStartTime = re.compile( '^[0-2][0-9]:[0-9][0-9]$' )

def ReadPropertiesFromExcel( reader ):
	race = Model.race
	if not race:
		return False
		
	if sheetName not in reader.sheet_names():
		return False
	
	headerMap = {}
	for r, row in enumerate(reader.iter_list(sheetName)):
		# Since this is machine generated, assume the headers are in the first row.
		if not headerMap:
			for c, v in enumerate(row):
				if v in HeaderSet:
					headerMap[v] = c
			continue
		
		for h, c in headerMap.iteritems():
			p = HeadersToFields[h]
			if p is None:
				continue
			
			v = row[c]
			t = FieldType[p]
			if t == 's':
				v = unicode(v)
			elif t == 'b':
				v = bool(v)
			elif t == 'n':
				try:
					v = int(v)
				except ValueError:
					v = 1
					
			if p == 'distanceUnit':
				v = 1 if v and v.lower().startswith('m') else 0
			elif p == 'date':
				if not reStartDate.match(v or ''):
					v = None
			elif p == 'scheduledStart':
				if not reStartTime.match(v or ''):
					v = None
			
			if v is not u'' and v is not None:
				setattr( race, p, v )
		
		return True
		
	return False