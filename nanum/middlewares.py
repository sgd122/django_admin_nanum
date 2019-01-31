def json_middleware(get_response):
    def middleware(request, *args):
        response = get_response(request, *args)
        response['Content-Language'] = 'ko'

        if not request.path.startswith('/admin'):
            response['Access-Control-Allow-Origin'] = request.META.get('HTTP_ORIGIN', '*')
            response['Access-Control-Allow-Headers'] = 'ACCEPT,ACCEPT-ENCODING,CONTENT-TYPE,ORIGIN,' \
                                                       'USER-AGENT,X-REQUESTED-WITH'
            response['Access-Control-Allow-Methods'] = "*"
            response['Access-Control-Allow-Credentials'] = 'true'
        return response

    return middleware
