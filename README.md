# Squid-Proxy sqlite ACL script
## WARNING
This is a **Hobby project** and has not been tested in an enterprise setting. If you want to test it out anyway, please report your experience in the issues. Thanks!


## What does this do?
If you have a large number of entries for an ACL - for example, a domain block list, this script allows you to query it effectively in squid, without needing to load the whole file at startup and keeping it in RAM.

Note that this is only worth it if your list is HUGE (more than 10000 entries).

## How does it work?
* Entries get imported to an sqlite database
* squid uses the `squid-sqlite-helper` script to query the database
* Performance gain:
    * Often queried destination domains get cached
    * Less often destination domains don't take up memory, which you can use for caching
# Setup
## Clone the repo
```
mkdir -p /usr/local/libexec/squid/
git -C /usr/local/libexec/squid/ clone https://github.com/jauchi/squid-sqlite-helper 
```
## Configure
```
# Create some directory to store files:
mkdir /var/squid
chown -R proxy:proxy /var/squid

# Configure some things
vim /usr/local/libexec/squid/squid-sqlite-helper/settings.py

# put your entries into /var/squid/acl.list (or configure an alternative location in settings.py)

# Import the list to your database
python3 /usr/local/libexec/squid/squid-sqlite-helper/load.py
```
## Configure squid to use the helper script
Add the following configuration:
```
# For blocking DNS, we want to check if the request domain (%>rd) is in the database:
external_acl_type sqlite_blocklist_lookup children-startup=1 %>rd /usr/local/libexec/squid/squid-sqlite-helper/squid-sqlite-helper.py
# Then, define an ACL with our custom type:
acl testacl external sqlite_blocklist_lookup
# And, as usual, perform filtering based on the ACL:
http_access deny testacl
```
## Issues
### Squid does not work anymore!!!
Make sure the lock file does not exist, or the ACL will not be evaluated correctly.
### I want more than one ACL
Copy the script to two locations, and modify the settings.py
### Database is corrupted (Database image is malformed)
If your database becomes corrupted, delete the file, load the ACL again and restart squid.