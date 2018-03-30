#   Save this anywhere... I just saved it in the /etc folder
#   This will make the pi discoverable on boot

import os
os.system('sudo hciconfig hci0 piscan')

#I don't yet know if we'll need this line, but I'm adding it in for now
#   os.system('sudo bluetooth-agent 1234')

#TODO
#   Now that this has been done, go to the file /etc/rc.local and add the following just before the exit 0 line:
#
#       sudo python /etc/superscript.py &
#
#   in place of /etc/superscript.py, make sure it's the full path name to your script.  The & tells the program
#   to terminate in case it hangs up.
