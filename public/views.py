from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from permatom.thomutils import *
import re
    
def bill(request, congress, bill_type, bill_id, format='html'):
    bill_info = BillInfo(congress, bill_type, bill_id)
    bill_info.oc_url = bill_info.open_congress()
    bill_info.gt_url = bill_info.govtrack()
    bill_info.th_url = bill_info.thomas_handle()
    bill_info.oc_api_url = bill_info.open_congress_api()
    bill_info.uri = "http:/%s/bill/%s-%s-%s/" %\
        (settings.PERMATOM_DOMAIN, bill_info.congress, bill_info.bill_type, bill_info.bill_id)
    
    if format=="xml":
        mime_type = "text/xml"
    elif format=="json":
        mime_type = "application/json"
    else:
        mime_type = "text/html"
        
    return render_to_response('public/bill_info.%s' % format, {'bill_info':bill_info, 'domain':settings.PERMATOM_DOMAIN}, mimetype=mime_type)
    
def handle(request):
    if request.method == 'GET':
        handle_url = None
        if 'congress' in request.GET and 'bill_type' in request.GET and 'bill_id' in request.GET:     
            bill_info = BillInfo(request.GET['congress'], request.GET['bill_type'], request.GET['bill_id'])
            handle_url = bill_info.thomas_handle()
        elif 'bill_num' in request.GET:
            congress = 111 #fix to automate current congress.. see congress_utils.py
            bill_num = request.GET['bill_num'].replace(' ', '').replace('.', '').lower()
            b = re.compile('([a-z]*)([0-9]*)');
            bm = b.match(bill_num)
            if bm:
                if bm.group():
                    bill_type = bm.group(1)
                    bill_id = bm.group(2)
                    bill_info = BillInfo(congress, bill_type, bill_id)
                    handle_url = bill_info.thomas_handle()
        return HttpResponseRedirect('/bill/%s-%s-%s' % (bill_info.congress, bill_info.bill_type, bill_info.bill_id))
        
def shortcut(request, congress, bill_type, bill_id, destination='loc'):
    bill_info = BillInfo(congress, bill_type, bill_id)
    
    url = None
    if destination == 'loc':
        url = bill_info.thomas_handle()
    elif destination == 'oc':
        url = bill_info.open_congress()
    elif destination == 'gt':
        url = bill_info.govtrack()
    
    if url:   
        return HttpResponseRedirect(url)
    else:
        return HttpResponseRedirect('/')