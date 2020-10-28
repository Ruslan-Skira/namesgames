# import sys
# sys.path.append('..')
#
# from django.contrib.auth.models import User
# from django.contrib import messages
# from django.views.generic import CreateView
#
# from django.views.generic.edit import FormView
# from django.views.generic.list import ListView
# from django.shortcuts import redirect
#
#
#
# from .forms import RegistrationForm, NewslettersForm
# from .models import Contact
# # from .service import send
# # from namesgames.tasks import create_random_user_accounts, send_spam_email
# from namesgames.tasks import create_random_user_accounts, send_beat_email, send_spam_email
#
# import logging
#
#
# logger = logging.getLogger(__name__)
#
#
#
#
# class UsersListView(ListView):
#
#
#     template_name = 'user/users_list.html'
#     model = User
#
#
#
#
#
# class UserRegistrationView(FormView):
#     template_name = 'user/registration_form.html'
#     form_class = RegistrationForm
#
#     def form_valid(self, form):
#
#
#
#         total = form.cleaned_data.get('total')
#         # create_random_user_accounts.delay(total)
#         messages.success(self.request, 'Rundom users generated')
#         return redirect('registration')
#
#
# class GetNewsletterView(CreateView):
#     model = Contact
#     model = Contact
#     form_class = NewslettersForm
#     success_url = '/'
#     template_name = 'user/registration_form.html'
#
#     def form_valid(self, form):
#         form.save()
#         # send(form.instance.email)
#         logger.info('request is done')
#         send_spam_email.delay(form.instance.email)
#         # send_beat_email.delay(form.instance.email)
#         return super().form_valid(form)
