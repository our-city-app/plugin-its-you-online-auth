import { CommonModule } from '@angular/common';
// angular
import { NgModule, Optional, SkipSelf } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { MdButtonModule, MdChipsModule, MdIconModule, MdInputModule, MdListModule } from '@angular/material';
import { RouterModule } from '@angular/router';
import { EffectsModule } from '@ngrx/effects';
import { OrganizationsEffects } from './effects/organizations.effect';
// app
import { ItsYouOnlineConfig, OrganizationsService } from './services/index';
import { MultilingualModule } from '../../framework/client/i18n/multilingual.module';
import { CreateOrganizationComponent } from './components/create-organization.component';
import {
  ItsYouOnlineAuthComponent,
  OrganizationDetailComponent,
  SelectedOrganizationComponent
} from './components/index';
import { ViewOrganizationComponent } from './components/view-organization.component';
import { OrganizationSettingsComponent } from './components/organization-settings.component';

/**
 * Do not specify providers for modules that might be imported by a lazy loaded module.
 */

const MATERIAL_IMPORTS = [
  MdButtonModule, MdChipsModule, MdIconModule, MdInputModule, MdListModule
];
export const ITS_YOU_ONLINE_COMPONENTS: any[] = [
  CreateOrganizationComponent,
  OrganizationDetailComponent,
  SelectedOrganizationComponent,
  ViewOrganizationComponent,
  OrganizationSettingsComponent,
  ItsYouOnlineAuthComponent
];

export const ITSYOU_ONLINE_PROVIDERS: any[] = [
  OrganizationsService,
  ItsYouOnlineConfig
];


@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    HttpModule,
    RouterModule,
    MultilingualModule,
    EffectsModule.run(OrganizationsEffects),
    MATERIAL_IMPORTS
  ],
  declarations: [
    ...ITS_YOU_ONLINE_COMPONENTS
  ],
  providers: [
    ITSYOU_ONLINE_PROVIDERS
  ],
  exports: [
    ...ITS_YOU_ONLINE_COMPONENTS
  ]
})
export class ItsYouOnlineAuthModule {

  constructor(@Optional() @SkipSelf() parentModule: ItsYouOnlineAuthModule) {
    if (parentModule) {
      throw new Error('ItsYouOnlineAuthModule already loaded; Import in root module only.');
    }
  }
}
