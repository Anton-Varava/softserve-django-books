import json

from rest_framework.renderers import JSONRenderer


class UserJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        errors = data.get('errors', None)

        if errors:
            return super(UserJSONRenderer, self).render(data)

        # token = data.get('token', None)

        # if token and isinstance(token, bytes):
        #     data['token'] = token.decode('utf-8')
        # else:
        #     data['token'] = token

        return json.dumps({
            'user': data
        })


