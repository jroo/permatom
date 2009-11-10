import re

#loc handle settings
HANDLE_SERVER = 'hdl.loc.gov'
NAMING_AUTHORITY = 'loc.uscongress'

GOVTRACK_TYPE_MAP = {'hr':'h', 'hres':'hr', 'sres':'sr', 'hconres':'hc', 'sconres':'sc', 
    'hjres':'hj', 'sjres':'sj'}
FRIENDLY_MAP = {'hr':'H.R.', 'hres':'H.RES.', 'sres':'S.R.', 'hconres':'H.CON.RES.', 
    'sconres':'S.CON.RES', 'hjres':'H.J.RES', 'sjres':'S.J.RES.'}

class BillInfo:
    def __init__(self, congress=None, bill_type=None, bill_id=None):
        self.congress = int(congress)
        self.bill_type = bill_type
        self.bill_id = int(bill_id)
        self.friendly_id = "%s%s" % (FRIENDLY_MAP[self.bill_type], self.bill_id)

    def type_map(self):
        map = GOVTRACK_TYPE_MAP
        if self.bill_type in map:
            bill_type = map[self.bill_type]
        else:
            bill_type = self.bill_type
        return bill_type
	
    def thomas_handle(self):
        id_collection = 'legislation'
        id_item = '%s%s%s' % (self.congress, self.bill_type, self.bill_id)
        url = 'http://%s/%s/%s.%s' % (HANDLE_SERVER, NAMING_AUTHORITY, id_collection, id_item)
        return url	
	
    def thomas_direct(self):
        url = 'http://thomas.loc.gov/cgi-bin/query/z?c%i:%s%i:' %\
            (self.congress, self.bill_type, self.bill_id)
        return url
            
    def govtrack(self):
        bill_type = self.type_map()
        url = 'http://www.govtrack.us/congress/bill.xpd?bill=%s%s-%s' %\
            (bill_type, self.congress, self.bill_id)
        return url
        	
    def open_congress(self):
        bill_type = self.type_map()
        url = 'http://www.opencongress.org/bill/%i-%s%i/show' %\
            (self.congress, bill_type, self.bill_id)
        return url
        
    def open_congress_api(self):
        bill_type = self.type_map()
        url = 'http://www.opencongress.org/api/bills_by_ident?ident[]=%s-%s%s&key=' %\
            (self.congress, bill_type, self.bill_id)
        return url

    def shortcut(self):
        url = '/%i-%s-%i/' %\
            (self.congress, self.bill_type, self.bill_id)
        return url