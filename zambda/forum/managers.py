from django.db.models.expressions import Case, F, Q, When
from django.db.models.query import QuerySet


class ThreadsManager(QuerySet):
    def mythreads(self, request):
        filters = Q(sender__exact=request.user) | Q(receiver__exact=request.user) | Q(public=True)
        return self.filter(filters)


class MessagesManager(QuerySet):
    def my_messages(self, sender, receiver):
        """
        Return the messages sent between two users
        """
        return self.filter(sender__exact=sender, receiver__exact=receiver)
