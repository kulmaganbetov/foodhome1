from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from .models import UserSite

def subdomain_user_site_middleware(get_response):

    def middleware(request):
        if request.resolver_match.url_name == 'client':
            host_parts = request.get_host().split('.')
            if len(host_parts) > 2 and host_parts[0] != 'www':
                # get course for the given subdomain
                user_site = get_object_or_404(UserSite, slug=host_parts[0])
                user_site_url = reverse('course_detail',
                                     args=[user_site.slug])
                # redirect current request to the course_detail view
                url = '{}://{}{}'.format(request.scheme,
                                         '.'.join(host_parts[1:]),
                                         user_site_url)
                return redirect(url)
        response = get_response(request)
        return response
    return middleware