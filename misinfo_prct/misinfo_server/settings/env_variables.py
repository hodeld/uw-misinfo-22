import os
import io
import configparser


var_names = ['EARTH_DB_PASSWORD', 'SECRET_KEY', 'DB_HOST', 'DB_USER', 'DB_PASSWORD', 'DB_PORT',]


def set_env_variables(base_dir):
    """
    Get the environment variables
    """
    if os.getenv('DB_HOST') is None:
        root_path = os.path.dirname(os.path.dirname(base_dir))
        file_path = os.path.join(root_path, '.env')
        env_file = os.environ.get('PROJECT_ENV_FILE', file_path)
        for var_name in var_names:
            try:
                return os.environ[var_name]
            except KeyError:
                try:
                    config = io.StringIO()
                    config.write("[DATA]\n")
                    config.write(open(env_file).read())
                    config.seek(0, os.SEEK_SET)
                    cp = configparser.ConfigParser()
                    cp.readfp(config)
                    value = dict(cp.items('DATA'))[var_name.lower()]
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    os.environ.setdefault(var_name, value)
                except (KeyError, IOError):
                    from django.core.exceptions import ImproperlyConfigured
                    error_msg = "Either set the env variable '{var}' or place it in your " \
                                "{env_file} file as '{var} = VALUE'"
                    raise ImproperlyConfigured(error_msg.format(var=var_name, env_file=env_file))

