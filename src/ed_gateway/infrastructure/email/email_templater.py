from jinja2 import Environment, FileSystemLoader

from ed_gateway.application.contracts.infrastructure.email.abc_email_templater import \
    ABCEmailTemplater


class EmailTemplater(ABCEmailTemplater):
    def __init__(self) -> None:
        self._file_names: dict[str, str] = {
            "welcome_consumer": "welcome_consumer.html",
            "welcome_business": "welcome_business.html",
            "welcome_driver": "welcome_driver.html",
        }
        self._template_env = Environment(
            loader=FileSystemLoader("./email_templates"))

    def welcome_consumer(self, consumer_name: str) -> str:
        template = self._load_template("welcome_consumer")
        return template.render(consumer_name=consumer_name)

    def welcome_business(self, business_name: str) -> str:
        template = self._load_template("welcome_business")
        return template.render(business_name=business_name)

    def welcome_driver(self, driver_name: str) -> str:
        template = self._load_template("welcome_driver")
        return template.render(driver_name=driver_name)

    def _load_template(self, template_key: str):
        file_name = self._file_names.get(template_key)
        if not file_name:
            raise ValueError(f"Template key '{template_key}' not found.")
        return self._template_env.get_template(file_name)
