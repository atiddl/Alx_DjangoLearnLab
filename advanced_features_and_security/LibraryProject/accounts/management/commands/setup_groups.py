from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book  # Replace with your actual model name if different

class Command(BaseCommand):
    help = 'Creates user groups and assigns permissions'

    def handle(self, *args, **kwargs):
        groups_permissions = {
            'Viewers': ['can_view'],
            'Editors': ['can_create', 'can_edit'],
            'Admins': ['can_view', 'can_create', 'can_edit', 'can_delete'],
        }

        content_type = ContentType.objects.get_for_model(Book)

        for group_name, perm_codenames in groups_permissions.items():
            group, created = Group.objects.get_or_create(name=group_name)
            permissions = []

            for codename in perm_codenames:
                try:
                    permission = Permission.objects.get(codename=codename, content_type=content_type)
                    permissions.append(permission)
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Permission '{codename}' not found. Did you run makemigrations & migrate?"))
                    continue

            group.permissions.set(permissions)
            group.save()
            self.stdout.write(self.style.SUCCESS(f"Group '{group_name}' updated with permissions: {perm_codenames}"))

        self.stdout.write(self.style.SUCCESS("All groups have been configured successfully."))
