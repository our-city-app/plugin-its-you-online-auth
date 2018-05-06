import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { NgModule, Optional, SkipSelf } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatButtonModule, MatChipsModule, MatIconModule, MatInputModule, MatListModule } from '@angular/material';
import { RouterModule } from '@angular/router';
import { EffectsModule } from '@ngrx/effects';
import { Store, StoreModule } from '@ngrx/store';
import { MultilingualModule } from '../../framework/client/i18n/multilingual.module';
import { IAppState } from '../../framework/client/ngrx';
import { AddRoutesAction } from '../../framework/client/sidebar/actions';
import {
  CreateOrganizationComponent,
  ItsYouOnlineAuthComponent,
  OrganizationDetailComponent,
  OrganizationSettingsComponent,
  SelectedOrganizationComponent,
  ViewOrganizationComponent,
} from './components';
import { OrganizationsEffects } from './effects';
import { ItsYouOnlineAuthRoutes } from './its-you-online-auth.routes';
import { organizationsReducer } from './reducers';
import { ItsYouOnlineConfig, OrganizationsService } from './services';

/**
 * Do not specify providers for modules that might be imported by a lazy loaded module.
 */

const MATERIAL_IMPORTS = [
  MatButtonModule, MatChipsModule, MatIconModule, MatInputModule, MatListModule,
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
    HttpClientModule,
    RouterModule,
    MultilingualModule,
    RouterModule.forChild(ItsYouOnlineAuthRoutes),
    StoreModule.forFeature('organizations', organizationsReducer),
    EffectsModule.forFeature([ OrganizationsEffects ]),
    MATERIAL_IMPORTS,
  ],
  declarations: [
    ...ITS_YOU_ONLINE_COMPONENTS,
  ],
  providers: [
    ITSYOU_ONLINE_PROVIDERS,
  ],
  exports: [
    ...ITS_YOU_ONLINE_COMPONENTS,
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
