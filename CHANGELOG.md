# Changelog

## 0.2.0

Profile pointers

### Bugfixes

profile: A new datastore model has been added: ProfileAppEmailMapping. This provides a mapping between a rogerthat user and an ityou.online username. This is needed because since itsyou.online now generates usernames, the usernames are no longer lowercase-only. This was a problem on rogerthat and has been fixed by taking a hash of the username instead of the username itself

Run this migration when updating:

```python
def iyo_2():
    from plugins.its_you_online_auth.migrations._002_profile_pointers import migrate
    return migrate(dry_run=False)
```

## 0.1.0

Start versioning of ityou-online-auth plugin

### Features

Added 'info' on Profile which is populated every 7 days with up-to-date information of the user via the GetUserInformation api call to itsyou.online.
This is optional and needs to be enabled by adding setting `"fetch_information": true` to the config 

### Breaking changes

'source' has been removed as parent from Profile. Run the following migration to migrate existing profiles:


```python
from plugins.its_you_online_auth.migrations._001_user_profiles import migrate
    migrate(dry_run=False)
```