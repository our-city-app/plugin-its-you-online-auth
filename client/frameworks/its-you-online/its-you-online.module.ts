// angular
import { NgModule, Optional, SkipSelf } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { RouterModule } from '@angular/router';

// app
import { ITSYOU_ONLINE_PROVIDERS, ITS_YOU_ONLINE_COMPONENTS } from './services/index';
import { MultilingualModule } from '../i18n/multilingual.module';
import { MaterialModule } from '@angular/material';
import { EffectsModule } from '@ngrx/effects';
import { OrganizationsEffects } from './effects/organizations.effect';

/**
 * Do not specify providers for modules that might be imported by a lazy loaded module.
 */

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    HttpModule,
    RouterModule,
    MultilingualModule,
    MaterialModule,
    EffectsModule.run(OrganizationsEffects)
  ],
  declarations: [
    ITS_YOU_ONLINE_COMPONENTS
  ],
  providers: [
    ITSYOU_ONLINE_PROVIDERS
  ],
  exports: [
    MultilingualModule,
    ITS_YOU_ONLINE_COMPONENTS
  ]
})
export class ItsYouOnlineModule {

  constructor(@Optional() @SkipSelf() parentModule: ItsYouOnlineModule) {
    if (parentModule) {
      throw new Error('ItsYouOnlineModule already loaded; Import in root module only.');
    }
  }
}
