from django.db.models.expressions import Case, F, Q, When
from django.db.models.query import QuerySet
from django.db.models import fields


class ThreadsManager(QuerySet):
    def mythreads(self, request):
        case1 = When(receivers__in=[request.user], then=True)
        case2 = When(sender__exact=request.user, then=True)
        case3 = When(public=True, then=True)
        threads = self.annotate(
            user_threads=Case(
                case1, case2, case3, default=False, output_field=fields.BooleanField()
            )
        )
        return threads.filter(user_threads=True).distinct()

    def messaes(self, reference):
        thread = self.get(reference__exact=reference)
        return thread.messages_set.all()


class MessagesManager(QuerySet):
    def my_messages(self, sender, receiver):
        """
        Return the messages sent between two users
        """
        return self.filter(sender__exact=sender, receiver__exact=receiver)
