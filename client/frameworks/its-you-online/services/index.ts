import { OrganizationsService } from './organizations.service';
import { ItsYouOnlineConfig } from './its-you-online-config';
import {
  CreateOrganizationComponent,
  OrganizationDetailComponent,
  SelectedOrganizationComponent,
  OrganizationSettingsComponent,
  ViewOrganizationComponent
} from '../components/index';
export const ITSYOU_ONLINE_PROVIDERS: any[] = [
  OrganizationsService,
  ItsYouOnlineConfig
];

export const ITS_YOU_ONLINE_COMPONENTS: any[] = [
  CreateOrganizationComponent,
  OrganizationDetailComponent,
  SelectedOrganizationComponent,
  ViewOrganizationComponent,
  OrganizationSettingsComponent
];

export * from './organizations.service';
export * from './its-you-online-config';
