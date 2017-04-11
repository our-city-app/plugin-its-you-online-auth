import { Component } from '@angular/core';
// libs
import { Store } from '@ngrx/store';
import { Observable } from 'rxjs/Observable';
// app
import { GetOrganizationsAction, IOrganizationsState, Organization, RemoveOrganizationAction } from '../index';
import { getOrganizations } from '../its-you-online.state';

@Component({
  moduleId: module.id,
  selector: 'organization-settings',
  templateUrl: 'organization-settings.component.html'
})
export class OrganizationSettingsComponent {
  public organizations$: Observable<any>;

  constructor(private store: Store<IOrganizationsState>) {
    this.store.dispatch(new GetOrganizationsAction());
    this.organizations$ = store.let(getOrganizations);
  }

  public organizationId(organization: Organization) {
    return organization.id;
  }

  public deleteOrganization(organization: Organization) {
    this.store.dispatch(new RemoveOrganizationAction(organization));
  }
}
