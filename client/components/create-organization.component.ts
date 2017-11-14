import { ChangeDetectionStrategy, Component, OnInit, ViewEncapsulation } from '@angular/core';
import { Store } from '@ngrx/store';
import * as organizationActions from '../actions/organizations.action';
import { IOrganizationsState } from '../states/organizations.state';

@Component({
  selector: 'create-organization',
  encapsulation: ViewEncapsulation.None,
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <selected-organization [isNewOrganization]="true"></selected-organization>`
})
export class CreateOrganizationComponent implements OnInit {
  constructor(private store: Store<IOrganizationsState>) {
  }

  ngOnInit() {
    this.store.dispatch(new organizationActions.CreateAction());
  }
}
