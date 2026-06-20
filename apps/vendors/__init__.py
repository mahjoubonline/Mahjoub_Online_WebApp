registry_path = os.path.join(folder_path, 'registry.py')
if os.path.exists(registry_path):
    module = importlib.import_module(f'apps.{folder}.registry')
    if hasattr(module, 'register_app'):
        module.register_app(app)
