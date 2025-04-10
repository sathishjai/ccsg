import os
from importlib import import_module

class TemplateManager:
    def __init__(self):
        self.templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
        self.available_templates = self._load_templates()

    def _load_templates(self):
        templates = {}
        for file in os.listdir(self.templates_dir):
            if file.endswith('.py') and not file.startswith('__'):
                template_name = file[:-3]
                module = import_module(f'pdf_generator.templates.{template_name}')
                templates[template_name] = module.Template()
        return templates

    def get_template(self, bank_name):
        if bank_name not in self.available_templates:
            raise ValueError(f"Template for {bank_name} not found")
        return self.available_templates[bank_name]