import { Component } from '@angular/core';
// libs
import { Store } from '@ngrx/store';
import { Observable } from 'rxjs/Observable';
// app
import * as states from '../its-you-online.state';
import { IOrganizationsState } from '../states';
import { RouterExtensions, LogService } from '../../core/index';
import * as itsyouonline from '../index';
import { Organization } from '../types/organization.types';

@Component({
  moduleId: module.id,
  selector: 'organization-settings',
  templateUrl: 'organization-settings.component.html'
})
export class OrganizationSettingsComponent {
  public organizations$: Observable<any>;

  constructor(private log: LogService, private store: Store<IOrganizationsState>, public routerext: RouterExtensions) {
    this.store.dispatch(new itsyouonline.GetOrganizationsAction());
    this.organizations$ = store.let(states.getOrganizations);
  }

  public clientId(organization: Organization) {
    return organization.client_id;
  }

  public deleteOrganization(organization: Organization) {
    this.store.dispatch(new itsyouonline.RemoveOrganizationAction(organization));
  }
}
