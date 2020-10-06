from braces import views as braces
from django.conf import settings
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy as reverse
from django.utils.http import is_safe_url
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from api.resources import Admin, OpenExperiments, ValidateToken
from main.mixins import OverrideLanguageMixin
from .forms import ChangePasswordForm, EnterTokenForm, ForgotPasswordForm, \
    ResetPasswordForm


#
# Home
#

class HomeView(OverrideLanguageMixin, generic.TemplateView):
    template_name = 'main/index.html'

    language_override = 'nl'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        experiments = OpenExperiments.client.get()
        admin = Admin.client.get()

        context['experiments'] = experiments
        context['admin'] = admin

        return context


#
# Password related views
#

class ChangePasswordView(braces.LoginRequiredMixin, SuccessMessageMixin,
                         generic.FormView):
    template_name = 'main/change_password.html'
    form_class = ChangePasswordForm
    success_message = _('password:message:updated')
    success_url = reverse('main:change_password')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_ldap_account:
            return HttpResponseRedirect(reverse('main:ldap_password'))

        return super(ChangePasswordView, self).dispatch(
            request,
            *args,
            **kwargs
        )

    def form_valid(self, form):
        self.request.session['force_password_change'] = False

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['forced'] = self.request.session.get('force_password_change',
                                                     False)

        return context


class LDAPPasswordView(generic.TemplateView):
    template_name = 'main/ldap_password.html'


class ForgotPasswordView(braces.AnonymousRequiredMixin, SuccessMessageMixin,
                         generic.FormView):
    template_name = 'main/forgot_password.html'
    form_class = ForgotPasswordForm
    success_message = _('password:message:reset_requested')
    success_url = reverse('main:forgot_password')

    def form_valid(self, form):
        if form.ldap:
            return HttpResponseRedirect(reverse('main:ldap_password'))

        return super(ForgotPasswordView, self).form_valid(form)


class EnterTokenView(braces.AnonymousRequiredMixin, generic.FormView):
    template_name = 'main/enter_reset_token.html'
    form_class = EnterTokenForm

    def form_valid(self, form):
        args = [form.cleaned_data['token']]
        return HttpResponseRedirect(reverse('main:reset_password', args=args))


class ResetPasswordView(braces.AnonymousRequiredMixin, SuccessMessageMixin,
                        generic.FormView):
    template_name = 'main/reset_password.html'
    form_class = ResetPasswordForm
    success_message = _('password:message:reset_successful')
    success_url = reverse('main:login')

    def get_initial(self):
        initial = super(ResetPasswordView, self).get_initial()

        initial['token'] = self.kwargs.get('token')

        return initial

    def get_context_data(self, **kwargs):
        context = super(ResetPasswordView, self).get_context_data(**kwargs)
        token = self.kwargs.get('token')

        req = ValidateToken()
        req.token = token

        response = req.put()

        context['valid'] = response.success

        return context


#
# Login View
#

class CustomLoginView(LoginView):
    redirect_authenticated_user = True

    def get_success_url(self):
        # HACK
        # Because we force the language to dutch on the frontpage, the language
        # can stay Dutch even if the logging in user has Accept-Language set to
        # english. This solves that problem.
        if '_language' in self.request.session:
            del self.request.session['_language']

        redirect_to = self.request.POST.get(
            'next',
            self.request.GET.get('next', None)
        )

        if redirect_to:
            url_is_safe = is_safe_url(
                url=redirect_to,
                allowed_hosts=self.get_success_url_allowed_hosts(),
                require_https=self.request.is_secure(),
            )

            if url_is_safe:
                return redirect_to

        if self.request.user.is_leader:
            return reverse('leader:experiments')

        else:
            return reverse('main:home')


#
#  Error pages
#

def handler403(request, exception):
    return render(request, 'base/403.html', status=404)


def handler404(request, exception):
    return render(request, 'base/404.html', status=404)


def handler500(request, exception=None):
    context = {
        'technician_contact': settings.TECHNICIAN_CONTACT
    }
    return render(request, 'base/500.html', status=500, context=context)
