from django.db.models.query import QuerySet


class MessagesManager(QuerySet):
    def my_messages(self, to_user, from_user):
        """Return the messages sent between two users"""
        return self.filter(to_user__exact=to_user, from_user__exact=from_user)