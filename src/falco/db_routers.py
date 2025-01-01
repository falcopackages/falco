from django.conf import settings


class DBTaskRouter:
    """
    A router to control all database operations on models in the django_tasks application.
    """

    route_app_labels = {"django_tasks_database", "django_tasks", "django.tasks"}

    def db_for_read(self, model, **hints):
        """
        Attempts to read django_tasks models go to the tasks database.
        """
        if model._meta.app_label in self.route_app_labels:  # noqa
            return self.get_db()
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write django_tasks models go to the tasks database.
        """
        if model._meta.app_label in self.route_app_labels:  # noqa
            return self.get_db()
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):  # noqa
        """
        Make sure the django_tasks app only appears in the tasks database.
        """
        if app_label in self.route_app_labels:
            return db == self.get_db()
        return None

    @classmethod
    def get_db(cls):
        try:
            return settings.TASKS["default"]["OPTIONS"]["database"]
        except (AttributeError, KeyError):
            return "tasks_db"
