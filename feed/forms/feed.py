from django import forms

from feed.utils.feed_validators import AbstractValidator
from feed.utils.helpers import get_url_content_type


class FeedForm(forms.Form):
    validator: AbstractValidator
    url = forms.URLField(label='')

    def __init__(self, *args, **kwargs):
        data = kwargs.get('data')

        if data is not None:
            url = data.get('url')
            self.content_type = get_url_content_type(url)
            self.validator = kwargs.pop('validator')

        super().__init__(*args, **kwargs)

    def full_clean(self):
        super().full_clean()
        if not self.is_bound:
            return

        if hasattr(self, 'validator') and self.validator is not None:
            error = self.validator.validate(self.data.get('url'))

            if error is not None:
                self.add_error('url', error)
        else:
            self.add_error('url', 'This URL could not be parsed.')
