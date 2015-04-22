from split_settings.tools import optional, include

include(
    'settings_base.py',
    'settings_database.py',
    scope=locals() )
