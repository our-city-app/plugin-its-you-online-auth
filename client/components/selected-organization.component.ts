import { ChangeDetectionStrategy, Component, Input } from '@angular/core';
import { Store } from '@ngrx/store';
import { Observable } from 'rxjs/Observable';
import { AddOrganizationAction, EditOrganizationAction, RemoveOrganizationAction } from '../actions/index';
import { Organization } from '../interfaces/organization.interfaces';
import { getOrganizationStatus, getSelectedOrganization } from '../its-you-online-auth.state';
import { IOrganizationsState } from '../states/organizations.state';

@Component({
  moduleId: module.id,
  selector: 'selected-organization',
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <organization-detail
      [organization]="organization$ | async"
      [isNew]="isNewOrganization"
      (onAdd)="addOrganization($event)"
      (onUpdate)="updateOrganization($event)"
      (onRemove)="removeOrganization($event)">
    </organization-detail>
  `
})
export class SelectedOrganizationComponent {
  organization$: Observable<Organization>;
  status$: Observable<string>;

  @Input() isNewOrganization: boolean;

  constructor(private store: Store<IOrganizationsState>) {
    this.organization$ = store.let(getSelectedOrganization);
    this.status$ = store.let(getOrganizationStatus);
  }

  addOrganization(organization: Organization) {
    this.store.dispatch(new AddOrganizationAction(organization));
  }

  updateOrganization(organization: Organization) {
    this.store.dispatch(new EditOrganizationAction(organization));
  }

  removeOrganization(organization: Organization) {
    this.store.dispatch(new RemoveOrganizationAction(organization));
  }
}
