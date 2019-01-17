from django.utils.translation import activate as activate_language


class OverrideLanguageMixin:
    """This mixin can be used to force a page to always display in a
    specified language. It will also add a context variable
    `language_override` with the language that's been specified.

    You can set the language to be used with the `language_override` class
    variable. If this is left to none, this mixin will not change anything.

    Alternatively, one can override the get_language_override method for the
    same effect.
    """

    language_override = None

    def dispatch(self, request, *args, **kwargs):
        override = self.get_language_override(request)
        if override:

            activate_language(self.language_override)

        return super(OverrideLanguageMixin, self).dispatch(request, *args,
                                                           **kwargs)

    def get_language_override(self, request):
        return self.language_override

    def get_context_data(self, **kwargs):
        context = super(OverrideLanguageMixin, self).get_context_data(**kwargs)

        override = self.get_language_override(self.request)
        if override:
            context['language_override'] = override

        return context
