
import sys
import os

from django.core.management import execute_from_command_line


project_dir = os.path.dirname(os.path.abspath(__file__))


sys.path.insert(0, os.path.join(project_dir, 'src'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "salinasite.settings_dev")


print "Removing dev db"
dbfile = os.path.join(project_dir, 'tmp', 'dev.db')
if os.path.exists(dbfile):
    os.remove(dbfile)


execute_from_command_line([__file__, 'syncdb', '--noinput'])

execute_from_command_line([__file__, 'loaddata', 'salina/user.json'])
