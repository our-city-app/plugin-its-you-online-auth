import { Route } from '@angular/router';
import { ViewOrganizationComponent } from '../../frameworks/its-you-online/components/view-organization.component';
import { CreateOrganizationComponent } from '../../frameworks/its-you-online/components/create-organization.component';
import { ItsYouOnlineAuthComponent } from './its-you-online-auth.component';
import { MetadataResolve } from '../../frameworks/i18n/index';

export const ItsYouOnlineAuthRoutes: Array<Route> = [
  {
    path: 'itsyouonlinesettings',
    data: {
      label: 'iyo.itsyouonline_settings',
      id: 'its_you_online_settings',
      meta: {
        title: 'iyo.itsyouonline_settings',
      }
    },
    component: ItsYouOnlineAuthComponent,
    resolve: { metadata: MetadataResolve }
  },
  {
    path: 'itsyouonlinesettings/organizations/create',
    data: {
      meta: {
        title: 'iyo.add_organization',
      }
    },
    component: CreateOrganizationComponent,
    resolve: { metadata: MetadataResolve }
  },
  {
    path: 'itsyouonlinesettings/organizations/:organization_id',
    data: {
      meta: {
        title: 'iyo.update_organization',
      }
    },
    component: ViewOrganizationComponent,
    resolve: { metadata: MetadataResolve }
  }
];
