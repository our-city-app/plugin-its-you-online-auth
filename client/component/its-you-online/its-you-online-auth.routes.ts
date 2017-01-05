import { Route } from '@angular/router';
import { ViewOrganizationComponent } from '../../frameworks/its-you-online/components/view-organization.component';
import { CreateOrganizationComponent } from '../../frameworks/its-you-online/components/create-organization.component';
import { ItsYouOnlineAuthComponent } from './its-you-online-auth.component';

export const ItsYouOnlineAuthRoutes: Array<Route> = [
  {
    path: 'itsyouonlinesettings',
    data: {
      label: 'itsyouonline_settings',
      id: 'its_you_online_settings'
    },
    component: ItsYouOnlineAuthComponent,
  },
  {
    path: 'itsyouonlinesettings/organizations/create',
    component: CreateOrganizationComponent
  },
  {
    path: 'itsyouonlinesettings/organizations/:organization_id',
    component: ViewOrganizationComponent
  }
];
