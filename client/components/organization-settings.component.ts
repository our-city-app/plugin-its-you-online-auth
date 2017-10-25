import { ChangeDetectionStrategy, Component } from '@angular/core';
// libs
import { Store } from '@ngrx/store';
import { Observable } from 'rxjs/Observable';
// app
import { GetOrganizationsAction, RemoveOrganizationAction } from '../actions/index';
import { Organization } from '../interfaces/organization.interfaces';
import { getOrganizations } from '../its-you-online-auth.state';
import { IOrganizationsState } from '../states/organizations.state';

@Component({
  moduleId: module.id,
  selector: 'organization-settings',
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: 'organization-settings.component.html'
})
export class OrganizationSettingsComponent {
  public organizations$: Observable<Organization[]>;

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
