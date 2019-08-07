from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .server import server
from django.shortcuts import render
import re
from django.contrib.auth.decorators import login_required

def dispatcher(request):
    '''
    Main function
    @param request: Request object
    '''

    params = {
        'data': request.body,
        'method': request.method,
        'content_type': request.content_type
    }
    with server.test_request_context(request.path, **params):
        server.preprocess_request()
        try:
            response = server.full_dispatch_request()
        except Exception as e:
            response = server.make_response(server.handle_exception(e))
        return response.get_data()

def clean_dash_content(dash_content):
    ''' This is a hack to get rid of carriage returns in the html returned by the call to dash_dispatcher'''
    print("Function: clean_dash_content")

    string_content = str(dash_content)
    string_content = string_content.replace("\n", "")
    string_content = string_content.replace("\n ", "")
    string_content = string_content.replace("\n  ", "")
    string_content = string_content.replace("\n    ", "")
    string_content = string_content.replace("\n   ", "")
    string_content = string_content.replace("\\n   ", "")
    string_content = string_content.replace("\\\\n", "")
    string_content = string_content.replace("\\\'", "")
    string_content = string_content.replace(">\\n<", "><")
    string_content = string_content[:-6]
    string_content = string_content[1:]
    string_content = re.sub(r'\s+',' ', string_content)
    string_content = string_content[1:]
    cleaned_dash_content = string_content

    return cleaned_dash_content

@login_required(login_url='/login')
def dash_index(request):
    dash_content = HttpResponse(dispatcher(request), content_type='application/json').getvalue()
    dash_content = clean_dash_content(dash_content)
    context = {'dash_content': dash_content}
    return render(request, 'dashboard/dash.html', context=context)


@csrf_exempt
def dash_ajax(request):
    ''' '''
    return HttpResponse(dispatcher(request), content_type='application/json')


