import { ChangeDetectionStrategy, Component, OnInit, ViewEncapsulation } from '@angular/core';
import { Store } from '@ngrx/store';
import { Observable } from 'rxjs/Observable';
import { GetOrganizationsAction, RemoveOrganizationAction } from '../actions/index';
import { Organization } from '../interfaces/organization.interfaces';
import { getOrganizations } from '../its-you-online-auth.state';
import { IOrganizationsState } from '../states/organizations.state';

@Component({
  selector: 'organization-settings',
  encapsulation: ViewEncapsulation.None,
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: 'organization-settings.component.html'
})
export class OrganizationSettingsComponent implements OnInit {
  public organizations$: Observable<Organization[]>;

  constructor(private store: Store<IOrganizationsState>) {
  }

  ngOnInit() {
    this.store.dispatch(new GetOrganizationsAction());
    this.organizations$ = this.store.select(getOrganizations);
  }

  public organizationId(organization: Organization) {
    return organization.id;
  }

  public deleteOrganization(organization: Organization) {
    this.store.dispatch(new RemoveOrganizationAction(organization));
  }
}
