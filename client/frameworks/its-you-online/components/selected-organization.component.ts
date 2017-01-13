import { Component, ChangeDetectionStrategy, Input } from '@angular/core';
import { Store } from '@ngrx/store';
import { Observable } from 'rxjs/Observable';
import * as states from '../its-you-online.state';
import * as actions from '../actions/organizations.action';
import { Organization, IOrganizationsState } from '../index';

@Component({
  moduleId: module.id,
  selector: 'selected-organization',
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <organization-detail
      [organization]="organization$ | async"
      [isNew]="isNewOrganization"
      (add)="addOrganization($event)"
      (update)="updateOrganization($event)"
      (remove)="removeOrganization($event)">
    </organization-detail>
  `
})
export class SelectedOrganizationComponent {
  organization$: Observable<any>;
  status$: Observable<any>;

  @Input() isNewOrganization: boolean;

  constructor(private store: Store<IOrganizationsState>) {
    this.organization$ = store.let(states.getSelectedOrganization);
    this.status$ = store.let(states.getOrganizationStatus);
  }

  addOrganization(organization: Organization) {
    this.store.dispatch(new actions.AddOrganizationAction(organization));
  }

  updateOrganization(organization: Organization) {
    this.store.dispatch(new actions.EditOrganizationAction(organization));
  }

  removeOrganization(organization: Organization) {
    this.store.dispatch(new actions.RemoveOrganizationAction(organization));
  }
}
