from rest_framework.views import APIView
from rest_framework.response import Response
from shortener.models import Urls
from urllib.parse import urlparse
import base64
import hashlib


class ShortenerView(APIView):
    def post(self, request):
        if is_valid_url(request.data.get('url')):
            link = it_is_a_known_url(request.data.get('url'))
            if not link:
                short_url = generate_short_url(request.data.get('url'))
                Urls.objects.create(long_url= request.data.get('url'),
                                            short_url= short_url,)
                return Response({'msg': 'Link was copied to Clipboard',
                                'short_url': short_url},
                                content_type='application/json')
            else:
                return Response({'msg': 'A known URL', 'url': link})
        else:
        	return Response({'msg': 'Invalid URL'})

class ForwardingView(APIView):
    def post(self, request):
        link = forwarding_exist(request.data.get('url'))
        if link:
            return Response({'url': link})
        return Response({'url': None})

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def generate_short_url(long_url):
    hash_object = hashlib.sha1(long_url.encode())
    hex_dig = hash_object.hexdigest()
    decimal_hash = int(hex_dig, 16)
    short_url = base64.b64encode(str(decimal_hash).encode()).decode()
    return f'{short_url[:8]}'

def it_is_a_known_url(long_url):
    all_urls = Urls.objects.all()
    for url in all_urls:
        if long_url == url.long_url:
            return url.short_url
    return False

def forwarding_exist(hex_code):
    all_urls = Urls.objects.all()
    for url in all_urls:
        if hex_code == url.short_url:
            return url.long_url
    return False

