# plugin-its-you-online-auth
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/32093039f2484a91b00b0584d6bf58fc)](https://www.codacy.com/app/lucas-vanhalst/plugin-its-you-online-auth?utm_source=github.com&utm_medium=referral&utm_content=rogerthat-platform/plugin-its-you-online-auth&utm_campaign=badger)


## Permissions

The organization structure is expected to look like this:

![Organization structure](docs/images/organization-structure.png)

`root_org` is the name of your main organization in this case.

Members of the top-level organization (`root_org` in this example) have permission to everything.
 
Members of the `root_org.organizations.example.users` organization can only login, and members of `root_org.organizations.example` have admin permissions on that organization.

The organization `root_org.organizations` should never have any members/owners, as that would imply that those users have permission to every organization. Those users should just be added to the top-level organization(`root_org`) if this is what you want.