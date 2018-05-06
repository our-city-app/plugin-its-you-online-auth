import { ChangeDetectionStrategy, Component, Input, OnInit, ViewEncapsulation } from '@angular/core';
import { Store } from '@ngrx/store';
import { Observable } from 'rxjs';
import { AddOrganizationAction, EditOrganizationAction, RemoveOrganizationAction } from '../actions/index';
import { Organization } from '../interfaces/organization.interfaces';
import { getOrganizationStatus, getSelectedOrganization } from '../its-you-online-auth.state';
import { IOrganizationsState } from '../states/organizations.state';

@Component({
  selector: 'selected-organization',
  encapsulation: ViewEncapsulation.None,
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <organization-detail
      [organization]="organization$ | async"
      [isNew]="isNewOrganization"
      (onAdd)="addOrganization($event)"
      (onUpdate)="updateOrganization($event)"
      (onRemove)="removeOrganization($event)">
    </organization-detail>
  `,
})
export class SelectedOrganizationComponent implements OnInit {
  organization$: Observable<Organization>;
  status$: Observable<string>;

  @Input() isNewOrganization: boolean;

  constructor(private store: Store<IOrganizationsState>) {
  }

  ngOnInit() {
    this.status$ = this.store.select(getOrganizationStatus);
    this.organization$ = this.store.select(getSelectedOrganization);
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
