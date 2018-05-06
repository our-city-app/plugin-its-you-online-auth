import { ChangeDetectionStrategy, Component, OnDestroy, ViewEncapsulation } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Store } from '@ngrx/store';
import { Subscription } from 'rxjs';
import { map } from 'rxjs/operators';
import * as organizationActions from '../actions/organizations.action';
import { IOrganizationsState } from '../states';

@Component({
  selector: 'view-organization',
  encapsulation: ViewEncapsulation.None,
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <selected-organization [isNewOrganization]="false"></selected-organization>`,
})
export class ViewOrganizationComponent implements OnDestroy {
  actionsSubscription: Subscription;

  constructor(private store: Store<IOrganizationsState>, route: ActivatedRoute) {
    this.actionsSubscription = route.params
      .pipe(map(params => new organizationActions.GetOrganizationAction(params.organization_id)))
      .subscribe(store);
  }

  ngOnDestroy() {
    this.actionsSubscription.unsubscribe();
  }
}
