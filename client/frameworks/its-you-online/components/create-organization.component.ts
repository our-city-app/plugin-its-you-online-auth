import { Component, ChangeDetectionStrategy } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Store } from '@ngrx/store';
import * as organizationActions from '../actions/organizations.action';
import { IOrganizationsState } from '../states/organizations.state';


@Component({
  moduleId: module.id,
  selector: 'create-organization',
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `<selected-organization [isNewOrganization]="true"></selected-organization>`
})
export class CreateOrganizationComponent {
  constructor(private store: Store<IOrganizationsState>, route: ActivatedRoute) {
    this.store.dispatch(new organizationActions.CreateAction());
  }
}
