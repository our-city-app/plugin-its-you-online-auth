import '@ngrx/core/add/operator/select';
import 'rxjs/add/operator/map';
import { Component, OnDestroy, ChangeDetectionStrategy } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Store } from '@ngrx/store';
import { Subscription } from 'rxjs/Subscription';

import * as organizationActions from '../actions/organizations.action';
import { IOrganizationsState } from '../states/organizations.state';
@Component({
  moduleId: module.id,
  selector: 'view-organization',
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `<selected-organization [isNewOrganization]="false"></selected-organization>`
})
export class ViewOrganizationComponent implements OnDestroy {
  actionsSubscription: Subscription;

  constructor(private store: Store<IOrganizationsState>, route: ActivatedRoute) {
    this.actionsSubscription = route.params
      .select<string>('organization_id')
      .map(organizationId => new organizationActions.GetOrganizationAction(organizationId))
      .subscribe(store);
  }

  ngOnDestroy() {
    this.actionsSubscription.unsubscribe();
  }
}
