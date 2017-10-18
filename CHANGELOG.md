# Changelog

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