from django import http as django_http
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views.decorators import http
from django.views.generic import View

from forum import models, serializers
from forum import utilities


class ForumView(View):
    def get(self, request, *args, **kwargs):
        qfunctions = Q(from_user__exact=request.user.id) | Q(to_user__exact=request.user.id)
        threads = models.MessagesThread.objects.filter(qfunctions)
        if threads:
            has_already_selected_thread = request.session.get('current_thread')
            if has_already_selected_thread:
                first_thread = threads.get(reference=has_already_selected_thread)
            else:
                # When the user reaches on the forum,
                # we assume from the get go that he
                # is watching the first thread
                first_thread = threads.first()
            messages = first_thread.message_set.all()

            serialized_threads = serializers.ThreadSerializer(instance=threads, many=True)
            serialized_messages = serializers.MessageSerializer(instance=messages, many=True)
        
            context = {
                'threads': serialized_threads.data,
                'first_thread_reference': first_thread.reference,
                'forum_messages': serialized_messages.data
            }
        else:
            context = {
                'threads': [],
                'first_thread_reference': False,
                'forum_messages': []
            }

        return render(request, 'pages/messages.html', context=context)

    def post(self, request, **kwargs):
        method = request.POST.get('method')
        reference = request.POST.get('reference')

        if method == 'viewthread':
            thread = get_object_or_404(models.MessagesThread, reference__iexact=reference)
            # Store the currently selected thread
            # so that when the user refreshes the
            # page, he can fall on that exact same one
            request.session.update({'current_thread': thread.reference})
            if thread:
                messages = thread.message_set.all()
                serialized_messages = serializers.MessageSerializer(instance=messages, many=True)
                data = {
                    'messages': serialized_messages.data,
                    'current_thread': thread.reference
                }
                return django_http.JsonResponse(data=data)

        if method == 'createthread':
            user = request.user
            thread = models.MessagesThread.objects.create(reference=utilities.create_thread_reference(), from_user=user)
            return django_http.JsonResponse(data={'thread': thread})

@http.require_http_methods(['POST'])
def new_message(request, **kwargs):
    message = request.POST.get('message')
    selected_thread = models.MessagesThread.objects.get(reference=kwargs['reference'])
    new_message = selected_thread.message_set.create(message=message)
    serialized_message = serializers.MessageSerializer(new_message)
    return django_http.JsonResponse(data=serialized_message.data)


@http.require_http_methods(['POST'])
def delete_message(request, **kwargs):
        thread = get_object_or_404(models.MessagesThread, reference=kwargs['reference'])
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

@http.require_http_methods(['POST'])
def report_thread(request):
    # selected_thread = MessagesThread.objects.get(reference=kwargs['reference'])
    # selected_thread.reported = True
    # selected_thread.save()
    # serialized_thread = serializers.ThreadSerializer(selected_thread)
    # return Response(data=serialized_thread.data)
    pass
