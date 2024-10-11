from pathlib import Path
from typing import TypedDict

import parso
from django.apps import AppConfig
from django.apps import apps
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import CommandError
from django.template import Context
from django.template import Template
from falco.management.base import CleanRepoOnlyCommand
from falco.utils import run_html_formatters
from falco.utils import run_python_formatters
from falco.utils import simple_progress

from .copy_template import get_template_absolute_path

IMPORT_START_COMMENT = "# IMPORTS:START"
IMPORT_END_COMMENT = "# IMPORTS:END"
CODE_START_COMMENT = "# CODE:START"
CODE_END_COMMENT = "# CODE:END"


class DjangoField(TypedDict):
    verbose_name: str
    editable: bool
    class_name: str
    accessor: str  # e.g: {{product.name}}


class DjangoModel(TypedDict):
    name: str
    name_plural: str
    verbose_name: str
    verbose_name_plural: str
    fields: dict[str, DjangoField]
    has_file_field: bool
    has_editable_date_field: bool


class PythonBlueprintContext(TypedDict):
    login_required: bool
    app_label: str
    model_name: str
    model_name_plural: str
    model_verbose_name_plural: str
    model_has_file_fields: bool
    model_has_editable_date_fields: bool
    model_fields: dict[str, DjangoField]
    entry_point: bool


class HtmlBlueprintContext(TypedDict):
    app_label: str
    model_name: str
    model_name_plural: str
    model_verbose_name: str
    model_obj_accessor: str
    model_verbose_name_plural: str
    model_has_file_fields: bool
    model_fields: dict[str, DjangoField]
    list_view_url: str
    create_view_url: str
    detail_view_url: str
    update_view_url: str
    delete_view_url: str


class Command(CleanRepoOnlyCommand):
    help = "Generate CRUD (Create, Read, Update, Delete) views for a model."

    def add_arguments(self, parser):
        parser.add_argument("model_path", type=str,
                            help="The path (<app_label>.<model_name>) of the model to generate CRUD views for. Ex: myapp.product")
        parser.add_argument("-e", "--exclude", action='append',
                            help="Fields to exclude from the views, forms and templates.")
        parser.add_argument("--only-python", action="store_true", help="Generate only python code.")
        parser.add_argument("--only-html", action="store_true", help="Generate only html code.")
        parser.add_argument("--entry-point", action="store_true",
                            help="Use the specified model as the entry point of the app.")
        parser.add_argument("--login-required", "-l", action="store_true",
                            help="Add the login_required decorator to all views.")
        parser.add_argument("--migrate", "-m", action="store_true", help="Run makemigrations and migrate beforehand")

    def handle(self, *args, **options):
        model_path = options["model_path"]
        excluded_fields = options["exclude"] or []
        only_python = options["only_python"]
        only_html = options["only_html"]
        entry_point = options["entry_point"]
        login_required = options["login_required"]
        migrate = options["migrate"]

        app_label, model_name = self.parse_model_path(model_path)

        if entry_point and not model_name:
            raise CommandError("The --entry-point option requires a full model path.")

        if migrate:
            with simple_progress("Running migrations"):
                call_command("makemigrations", app_label)
                call_command("migrate")

        app: AppConfig = apps.get_app_config(app_label)
        with simple_progress("Getting models info"):
            all_django_models = self.get_models_data(
                app_label=app_label,
                excluded_fields=excluded_fields,
                entry_point=entry_point,
            )
            dirs = settings.TEMPLATES[0].get("DIRS", [])
            templates_dir = Path(dirs[0]) / app_label if dirs else Path(app.path) / "templates"

        django_models = (
            [m for m in all_django_models if
             m["name"].lower() == model_name.lower()] if model_name else all_django_models
        )
        if model_name and not django_models:
            msg = f"Model {model_name} not found in app {app_label}"
            raise CommandError(msg)

        python_blueprint_context: list[PythonBlueprintContext] = []
        html_blueprint_context: list[HtmlBlueprintContext] = []

        for django_model in django_models:
            python_blueprint_context.append(
                get_python_blueprint_context(
                    app_label=app_label,
                    django_model=django_model,
                    login_required=login_required,
                    entry_point=entry_point,
                )
            )
            html_blueprint_context.append(get_html_blueprint_context(app_label=app_label, django_model=django_model))

        updated_python_files = set()

        if not only_html:
            python_blueprints = ("crud/forms.py.dtl", "crud/views.py.dtl")
            updated_python_files.update(
                self.generate_python_code(
                    app=app,
                    blueprints=[Path(get_template_absolute_path(p)) for p in python_blueprints],
                    contexts=python_blueprint_context,
                    entry_point=entry_point,
                )
            )

            updated_python_files.update(
                self.generating_urls(
                    app=app,
                    django_models=django_models,
                    entry_point=entry_point,
                )
            )

        updated_html_files = set()
        if not only_python:
            html_blueprints = ("crud/list.html", "crud/create.html", "crud/update.html", "crud/detail.html")
            updated_html_files.update(
                self.generate_html_templates(
                    contexts=html_blueprint_context,
                    entry_point=entry_point,
                    blueprints=[Path(get_template_absolute_path(p)) for p in html_blueprints],
                    templates_dir=templates_dir,
                )
            )

        for file in updated_python_files:
            run_python_formatters(str(file))

        for file in updated_html_files:
            run_html_formatters(str(file))

        display_names = ", ".join(m.get("name") for m in django_models)
        self.stdout.write(self.style.SUCCESS(f"CRUD views generated for: {display_names}"))

    @classmethod
    def parse_model_path(cls, model_path: str):
        model_path_parts = model_path.split(".")
        if len(model_path_parts) == 1:
            model_name = None
            app_label = model_path_parts[0]
        else:
            model_name = model_path_parts.pop()
            app_label = ".".join(model_path_parts)
        return app_label, model_name

    @classmethod
    def get_models_data(cls, app_label: str, excluded_fields: list[str], *, entry_point: bool) -> "list[DjangoModel]":
        models = apps.get_app_config(app_label).get_models()
        file_fields = ("ImageField", "FileField")
        dates_fields = ("DateField", "DateTimeField", "TimeField")

        def get_model_dict(model) -> "DjangoModel":
            name = model.__name__
            name_lower = name.lower()
            if entry_point:
                name_plural = app_label.lower()
            else:
                name_plural = f"{name.replace('y', 'ies')}" if name.endswith("y") else f"{name}s"

            verbose_name = model._meta.verbose_name
            verbose_name_plural = model._meta.verbose_name_plural
            fields: dict[str, DjangoField] = {
                field.name: {
                    "verbose_name": field.verbose_name,
                    "editable": field.editable,
                    "class_name": field.__class__.__name__,
                    "accessor": "{{"
                                f"{name_lower}.{field.name}" + (
                                    ".url }}" if field.__class__.__name__ in file_fields else "}}"),
                }
                for field in model._meta.fields
                if field.name not in excluded_fields
            }
            return {
                "name": name,
                "name_plural": name_plural,
                "fields": fields,
                "verbose_name": verbose_name,
                "verbose_name_plural": verbose_name_plural,
                "has_file_field": any(f["class_name"] in file_fields for f in fields.values()),
                "has_editable_date_field": any(
                    f["class_name"] in dates_fields and f["editable"] for f in fields.values()),
            }

        return [get_model_dict(model) for model in models]

    @simple_progress("Generating python code")
    def generate_python_code(
        self,
        app: AppConfig,
        blueprints: list[Path],
        contexts: list["PythonBlueprintContext"],
        *,
        entry_point: bool,
    ) -> list[Path]:
        updated_files = []

        for blueprint in blueprints:
            imports_template, code_template = extract_python_file_templates(blueprint.read_text())
            # blueprints python files end in .py.dtl
            file_name_without_jinja = ".".join(blueprint.name.split(".")[:-1])
            file_to_write_to = Path(app.path) / file_name_without_jinja
            file_to_write_to.touch(exist_ok=True)

            imports_content, code_content = "", ""

            for context in contexts:
                model_name_lower = context["model_name"].lower()
                imports_content += render_from_string(imports_template, context)
                code_content += render_from_string(code_template, context)

                if entry_point:
                    code_content = code_content.replace(f"{model_name_lower}_", "")
                    code_content = code_content.replace("list", "index")

            file_to_write_to.write_text(imports_content + file_to_write_to.read_text() + code_content)
            updated_files.append(file_to_write_to)

        model_name = contexts[0]["model_name"] if len(contexts) == 1 else None
        updated_files.append(
            self.register_models_in_admin(
                app=app,
                model_name=model_name
            )
        )
        return updated_files

    @simple_progress("Generating urls")
    def generating_urls(
        self,
        app: AppConfig,
        django_models: list["DjangoModel"],
        *,
        entry_point: bool,
    ) -> list[Path]:
        urls_content = ""
        for django_model in django_models:
            model_name_lower = django_model["name"].lower()
            urlsafe_model_verbose_name_plural = django_model["verbose_name_plural"].lower().replace(" ", "-")
            urls_content += get_urls(
                model_name_lower=model_name_lower,
                urlsafe_model_verbose_name_plural=urlsafe_model_verbose_name_plural,
            )
            if entry_point:
                urls_content = urls_content.replace(f"{urlsafe_model_verbose_name_plural}/", "")
                urls_content = urls_content.replace("list", "index")
                urls_content = urls_content.replace(f"{model_name_lower}_", "")

        app_urls = Path(app.path) / "urls.py"
        updated_files = [app_urls]
        if app_urls.exists() and app_urls.read_text().strip() != "":
            urlpatterns = f"\nurlpatterns +=[{urls_content}]"
            app_urls.write_text(app_urls.read_text() + urlpatterns)
        else:
            app_urls.touch()
            app_urls.write_text(initial_urls_content(app.label, urls_content))
            updated_files.append(register_app_urls(app=app))
        return updated_files

    @simple_progress("Generating html templates")
    def generate_html_templates(
        self,
        templates_dir: Path,
        blueprints: list[Path],
        contexts: list["HtmlBlueprintContext"],
        *,
        entry_point: bool,
    ) -> list[Path]:
        updated_files = []
        templates_dir.mkdir(exist_ok=True, parents=True)
        for blueprint in blueprints:
            filecontent = blueprint.read_text()

            for context in contexts:
                model_name_lower = context["model_name"].lower()
                new_filename = f"{model_name_lower}_{blueprint.name}"
                if entry_point:
                    new_filename = blueprint.name.replace(".jinja", "")
                if new_filename.startswith("list"):
                    new_filename = new_filename.replace("list", "index")
                file_to_write_to = templates_dir / new_filename
                file_to_write_to.touch(exist_ok=True)
                views_content = render_from_string(filecontent, context=context)

                if entry_point:
                    views_content = views_content.replace(f"{model_name_lower}_", "")
                    views_content = views_content.replace("list", "index")
                file_to_write_to.write_text(views_content)
                updated_files.append(file_to_write_to)

        return updated_files

    def register_models_in_admin(self, app: AppConfig, model_name: str | None = None) -> Path:
        admin_file = Path(app.path) / "admin.py"

        # Skip further processing if model_name is not specified and file is non-empty
        if not model_name and admin_file.exists() and admin_file.stat().st_size > 0:
            self.stdout.write(self.style.WARNING("Skipping admin registration as the file is not empty."))
            return admin_file

        admin_file.touch(exist_ok=True)
        cmd_args = [app.label]
        if model_name:
            cmd_args.append(model_name)

        try:
            output = call_command("admin_generator", *cmd_args)
        except CommandError as e:
            self.stdout.write(self.style.WARNING(f"Admin failed to generate: {e}"))
            return admin_file

        # the first line of the generated code set the encoding, it is useless for python 3
        admin_code = output.stdout.split("\n", 1)[1]
        existing_code = admin_file.read_text()

        if model_name and model_name.title() in existing_code:
            self.stdout.write(self.style.WARNING(f"Model {model_name} is already registered."))
            return admin_file

        admin_file.write_text(existing_code + admin_code)

        if not model_name:
            # we probably don't need to reorder the imports if the admin code is being generated for all models
            return admin_file

        # if this is not the first time running this, the imports will be messed up, move all
        # of them to the top
        admin_lines = admin_file.read_text().split("\n")
        _imports = []
        _code = []
        for line in admin_lines:
            if line.startswith("from"):
                _imports.append(line)
            else:
                _code.append(line)
        admin_file.write_text("\n" + "\n".join(_imports) + "\n" + "\n".join(_code))

        return admin_file


def render_from_string(template_string: str, context: dict) -> str:
    return Template(template_string).render(Context(context))


def get_urls(model_name_lower: str, urlsafe_model_verbose_name_plural: str) -> str:
    prefix = urlsafe_model_verbose_name_plural
    return f"""
        path('{prefix}/', views.{model_name_lower}_list, name='{model_name_lower}_list'),
        path('{prefix}/create/', views.{model_name_lower}_create, name='{model_name_lower}_create'),
        path('{prefix}/<int:pk>/', views.{model_name_lower}_detail, name='{model_name_lower}_detail'),
        path('{prefix}/<int:pk>/update/', views.{model_name_lower}_update, name='{model_name_lower}_update'),
        path('{prefix}/<int:pk>/delete/', views.{model_name_lower}_delete, name='{model_name_lower}_delete'),
    """


def extract_python_file_templates(file_content: str) -> tuple[str, str]:
    imports_template = extract_content_from(file_content, IMPORT_START_COMMENT, IMPORT_END_COMMENT)
    code_template = extract_content_from(file_content, CODE_START_COMMENT, CODE_END_COMMENT)
    return imports_template, code_template


def extract_content_from(text: str, start_comment: str, end_comment: str):
    start_index = text.find(start_comment) + len(start_comment)
    end_index = text.find(end_comment)
    return text[start_index:end_index]


def initial_urls_content(app_label: str, urls_content: str) -> str:
    return f"""
from django.urls import path
from . import views

app_name = "{app_label}"

urlpatterns = [
{urls_content}
]
        """


def register_app_urls(app: AppConfig) -> Path:
    root_url = settings.ROOT_URLCONF
    root_url = root_url.strip().replace(".", "/")
    root_url_path = Path(f"{root_url}.py")
    module = parso.parse(root_url_path.read_text())
    new_path = parso.parse(f"path('{app.label}/', include('{app.name}.urls', namespace='{app.label}'))")

    for node in module.children:
        try:
            if (
                node.children[0].type == parso.python.tree.ExprStmt.type
                and node.children[0].children[0].value == "urlpatterns"
            ):
                patterns = node.children[0].children[2]
                elements = patterns.children[1]
                elements.children.append(new_path)
                new_content = module.get_code()
                new_content = "from django.urls import include\n" + new_content
                root_url_path.write_text(new_content)
                break
        except AttributeError:
            continue

    return root_url_path


def get_python_blueprint_context(
    app_label: str,
    django_model: DjangoModel,
    *,
    login_required: bool,
    entry_point: bool,
) -> PythonBlueprintContext:
    model_fields = django_model["fields"]
    model_name = django_model["name"]
    return {
        "app_label": app_label,
        "login_required": login_required,
        "model_name": model_name,
        "model_name_plural": django_model["name_plural"],
        "model_verbose_name_plural": django_model["verbose_name_plural"],
        "model_fields": model_fields,
        "model_has_editable_date_fields": django_model["has_editable_date_field"],
        "model_has_file_fields": django_model["has_file_field"],
        "entry_point": entry_point
    }


def get_html_blueprint_context(app_label: str, django_model: DjangoModel) -> HtmlBlueprintContext:
    model_name_lower = django_model["name"].lower()
    return {
        "app_label": app_label,
        "model_name": django_model["name"],
        "model_name_plural": django_model["name_plural"],
        "model_verbose_name": django_model["verbose_name"],
        "model_verbose_name_plural": django_model["verbose_name_plural"],
        "model_has_file_fields": django_model["has_file_field"],
        "model_fields": django_model["fields"],
        "model_obj_accessor": "{{" + model_name_lower + "}}",
        "list_view_url": f"{{% url '{app_label}:{model_name_lower}_list' %}}",
        "create_view_url": f"{{% url '{app_label}:{model_name_lower}_create' %}}",
        "detail_view_url": f"{{% url '{app_label}:{model_name_lower}_detail' {model_name_lower}.pk %}}",
        "update_view_url": f"{{% url '{app_label}:{model_name_lower}_update' {model_name_lower}.pk %}}",
        "delete_view_url": f"{{% url '{app_label}:{model_name_lower}_delete' {model_name_lower}.pk %}}",
    }
