import { CommonModule } from '@angular/common';
// angular
import { NgModule, Optional, SkipSelf } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { MdButtonModule, MdChipsModule, MdIconModule, MdInputModule, MdListModule } from '@angular/material';
import { RouterModule } from '@angular/router';
import { EffectsModule } from '@ngrx/effects';
import { Store } from '@ngrx/store';
import { MultilingualModule } from '../../framework/client/i18n/multilingual.module';
import { IAppState } from '../../framework/client/ngrx/state/app.state';
import { AddRoutesAction } from '../../framework/client/sidebar/actions/sidebar.action';
import { CreateOrganizationComponent } from './components/create-organization.component';
import {
  ItsYouOnlineAuthComponent,
  OrganizationDetailComponent,
  SelectedOrganizationComponent,
} from './components/index';
import { OrganizationSettingsComponent } from './components/organization-settings.component';
import { ViewOrganizationComponent } from './components/view-organization.component';
import { OrganizationsEffects } from './effects/organizations.effect';
import { ItsYouOnlineAuthRoutes } from './its-you-online-auth.routes';
// app
import { ItsYouOnlineConfig, OrganizationsService } from './services/index';

/**
 * Do not specify providers for modules that might be imported by a lazy loaded module.
 */

const MATERIAL_IMPORTS = [
  MdButtonModule, MdChipsModule, MdIconModule, MdInputModule, MdListModule,
];
export const ITS_YOU_ONLINE_COMPONENTS: any[] = [
  CreateOrganizationComponent,
  OrganizationDetailComponent,
  SelectedOrganizationComponent,
  ViewOrganizationComponent,
  OrganizationSettingsComponent,
  ItsYouOnlineAuthComponent,
];

export const ITSYOU_ONLINE_PROVIDERS: any[] = [
  OrganizationsService,
  ItsYouOnlineConfig,
];


@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    HttpModule,
    RouterModule,
    MultilingualModule,
    RouterModule.forChild(ItsYouOnlineAuthRoutes),
    EffectsModule.run(OrganizationsEffects),
    MATERIAL_IMPORTS,
  ],
  declarations: [
    ...ITS_YOU_ONLINE_COMPONENTS
  ],
  providers: [
    ITSYOU_ONLINE_PROVIDERS,
  ],
  exports: [
    ...ITS_YOU_ONLINE_COMPONENTS
  ],
})
export class ItsYouOnlineAuthModule {

  constructor(@Optional() @SkipSelf() parentModule: ItsYouOnlineAuthModule, private store: Store<IAppState>) {
    if (parentModule) {
      throw new Error('ItsYouOnlineAuthModule already loaded; Import in root module only.');
    }
    this.store.dispatch(new AddRoutesAction(ItsYouOnlineAuthRoutes));
  }
}
