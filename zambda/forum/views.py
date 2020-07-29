import ast

import celery
from django import http as django_http
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import exceptions
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views import generic
from django.views.decorators import http
from django.views.decorators.csrf import csrf_exempt

from forum import models, serializers, tasks, utilities

MYUSER = get_user_model()


# def test_tasks_view(request):
#     tasks.send_new_email.delay(
#         'silede5221@retqio.com',
#         'This is a message'
#     )
#     return django_http.HttpResponse(
#         '<h1>Task was accomplished</h1>'
#     )


class ForumView(LoginRequiredMixin, generic.View):
    """
    Main entrypoint to access the forum
    """
    def get(self, request, *args, **kwargs):
        # TODO: The queryset does not return threads where the
        # user has been specifically added by another user
        threads = models.Thread.custom_manager.mythreads(request)
        context = {
            'users': MYUSER.objects.exclude(username__iexact=request.user.username),
        }
        if threads:
            has_already_selected_thread = request.session.get('current_thread', None)
            if has_already_selected_thread:
                try:
                    # We use this try catch in case there is a stale reference
                    # in the session of a thread which the status has changed
                    # e.g. the user is not part of anymore.
                    first_thread = threads.get(reference=has_already_selected_thread)
                except exceptions.ObjectDoesNotExist:
                    first_thread = threads.first()
            else:
                first_thread = threads.first()

            messages = first_thread.message_set.all()

            serialized_threads = serializers.ThreadSerializer(instance=threads, many=True)
            serialized_messages = serializers.MessageSerializer(instance=messages, many=True)

            context.update({'vue_threads': serialized_threads.data})
            context.update({'vue_messages': serialized_messages.data})
            context.update({'first_thread_reference': first_thread.reference})
        context.update({'user_has_threads': True if threads else False})
        return render(request, 'pages/messages.html', context=context) 


class PrivateMessageView(LoginRequiredMixin, generic.ListView):
    """
    Private messages or DM view
    """
    model = models.PrivateMessage
    queryset = models.PrivateMessage.objects.all()
    template_name = 'pages/private.html'
    context_object_name = 'messages'


@csrf_exempt
@login_required
@http.require_POST
def delete_message(request, **kwargs):
    """
    Delete a message from a thread
    """
    thread = get_object_or_404(models.Message, reference=kwargs['reference'])
    if thread:
        message_id = request.POST.get('messageid')
        try:
            message = thread.message_set.get(id=message_id)
        except:
            messages.error(request, "The action could not be performed", extra_tags='alert-warning')
            return django_http.JsonResponse(data={'state': False}, status=400)
        else:
            if message:
                message.delete()
                return django_http.JsonResponse(data={'message': message.id}, status=200)
    messages.error(request, "The action could not be performed", extra_tags='alert-warning')
    return redirect(reverse('forum'))


@csrf_exempt
@login_required
@http.require_POST
def create_thread(request, **kwargs):
    user_creating = request.user
    thread_name  = request.POST.get('name')
    private_or_public = request.POST.get('public')

    thread = models.Thread.objects.create(name=thread_name, sender=user_creating)
    if private_or_public:
        thread.public = True
        thread.save()
        
    messages.success(request, "New thread created", extra_tags='alert-success')
    return redirect('forum:forum')

@csrf_exempt
@login_required
@http.require_POST
def report_thread(request, **kwargs):
    thread = get_object_or_404(models.Message, reference=kwargs['reference'])

    if thread:
        thread.reported = True
        thread.save()
        messages.success(request, "Thread was reported", extra_tags='alert-success')
        return django_http.JsonResponse(data={'message': thread.reference}, status=200)

    messages.error(request, "The action could not be performed", extra_tags='alert-warning')
    return django_http.JsonResponse(data={}, status=400)


@login_required
@http.require_GET
def change_thread(request, **kwargs):
    reference = request.GET.get('q')
    if not reference:
        messages.error(request, 'Could not find the given thread')
        return django_http.JsonResponse(data={'state': False})
    thread = get_object_or_404(models.Thread, reference__iexact=reference)
    # Store the currently selected thread
    # so that when the user refreshes the
    # page, he can fall on that exact same one
    request.session.update({'current_thread': thread.reference})
    thread_messages = thread.message_set.all()
    serialized_messages = serializers.MessageSerializer(instance=thread_messages, many=True)
    data = {
        'messages': serialized_messages.data,
        'current_thread': thread.reference,
        'is_reported': thread.reported
    }
    return django_http.JsonResponse(data=data)

@csrf_exempt
@login_required
@http.require_POST
def add_user_to_thread(request):
    # BUG: With materialize checkbox,
    # can only retrieve one user from
    # the list of users
    reference = request.POST.get('reference')
    users_to_link = request.POST.get('user')

    if not users_to_link:
        messages.error(request, "An error occured USE-NO")
        return redirect('forum:forum')

    if isinstance(users_to_link, str):
        users_to_link = [users_to_link]

    users = MYUSER.objects.filter(username__in=users_to_link)
    if users.exists():
        thread = models.Thread.objects.get(reference=reference)
        thread.receivers.set(users, clear=True)

    return redirect('forum:forum')
