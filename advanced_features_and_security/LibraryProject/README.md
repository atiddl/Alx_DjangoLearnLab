# Library Project

This is a Django project for the "Introduction to Django" ALX project.

# 🔐 Permissions & Groups Setup

## 👥 User Groups

We use three main user groups to control access:

- **Admins**
  - Can view, create, edit, and delete books.
- **Editors**
  - Can view, create, and edit books (cannot delete).
- **Viewers**
  - Can only view books.

---

## 🛡️ Custom Permissions

The following permissions were added to the `Book` model in `bookshelf/models.py`:

| Permission Codename | Description        |
|---------------------|--------------------|
| `can_view`          | Can view books     |
| `can_create`        | Can add new books  |
| `can_edit`          | Can change books   |
| `can_delete`        | Can delete books   |

---

## ⚙️ How Permissions Are Enforced

Views are protected using the `@permission_required` decorator:

```python
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    ...
