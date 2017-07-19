import { CommonModule } from '@angular/common';
// angular
import { NgModule, Optional, SkipSelf } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { MdButtonModule, MdChipsModule, MdIconModule, MdInputModule, MdListModule } from '@angular/material';
import { RouterModule } from '@angular/router';
import { EffectsModule } from '@ngrx/effects';
import { MultilingualModule } from '../i18n/multilingual.module';
import { OrganizationsEffects } from './effects/organizations.effect';
// app
import { ITS_YOU_ONLINE_COMPONENTS, ITSYOU_ONLINE_PROVIDERS } from './services/index';

/**
 * Do not specify providers for modules that might be imported by a lazy loaded module.
 */

const MATERIAL_IMPORTS = [
  MdButtonModule, MdChipsModule, MdIconModule, MdInputModule, MdListModule
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
    ITS_YOU_ONLINE_COMPONENTS
  ],
  providers: [
    ITSYOU_ONLINE_PROVIDERS
  ],
  exports: [
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
