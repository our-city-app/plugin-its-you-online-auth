import { MetaGuard } from '@ngx-meta/core';
import { Route } from '../../framework/client/app.routes';
import { CreateOrganizationComponent, ItsYouOnlineAuthComponent, ViewOrganizationComponent } from './components/index';

export const ItsYouOnlineAuthRoutes: Route[] = [
  {
    path: 'itsyouonlinesettings',
    canActivate: [ MetaGuard ],
    data: {
      icon: 'perm_identity',
      id: 'its_you_online_settings',
      meta: {
        title: 'iyo.itsyouonline_settings',
      }
    },
    component: ItsYouOnlineAuthComponent
  },
  {
    path: 'itsyouonlinesettings/organizations/create',
    canActivate: [ MetaGuard ],
    data: {
      meta: {
        title: 'iyo.add_organization',
      }
    },
    component: CreateOrganizationComponent
  },
  {
    path: 'itsyouonlinesettings/organizations/:organization_id',
    canActivate: [ MetaGuard ],
    data: {
      meta: {
        title: 'iyo.update_organization',
      }
    },
    component: ViewOrganizationComponent
  }
];
