// angular
import { Injectable } from '@angular/core';
import { Actions, Effect } from '@ngrx/effects';
// libs
import { Action } from '@ngrx/store';
import { Observable } from 'rxjs/Observable';
import * as organizationActions from '../actions/organizations.action';
import { Organization } from '../index';
// module
import { OrganizationsService } from '../services/organizations.service';

@Injectable()
export class OrganizationsEffects {

  @Effect() getOrganizations$: Observable<Action> = this.actions$
    .ofType(organizationActions.ActionTypes.GET_ORGANIZATIONS)
    .switchMap(() => this.organizationsService.getOrganizations())
    .map(payload => new organizationActions.GetOrganizationsCompleteAction(payload))
    // nothing reacting to failure at moment but you could if you want (here for example)
    .catch(() => Observable.of(new organizationActions.GetOrganizationsFailedAction()));

  @Effect() getOrganization$: Observable<Action> = this.actions$
    .ofType(organizationActions.ActionTypes.GET_ORGANIZATION)
    .switchMap((value: Action) => this.organizationsService.getOrganization(value.payload))
    .map((payload: Organization) => new organizationActions.GetOrganizationCompleteAction(payload))
    // nothing reacting to failure at moment but you could if you want (here for example)
    .catch(() => Observable.of(new organizationActions.GetOrganizationFailedAction()));

  @Effect() add$: Observable<Action> = this.actions$
    .ofType(organizationActions.ActionTypes.ADD)
    .switchMap((value: Action) => this.organizationsService.createOrganization(value.payload))
    .map((payload: Organization) => new organizationActions.OrganizationAddedAction(payload));

  @Effect() edit$: Observable<Action> = this.actions$
    .ofType(organizationActions.ActionTypes.EDIT)
    .switchMap((value: Action) => this.organizationsService.updateOrganization(value.payload))
    .map(organization => new organizationActions.OrganizationEditedAction(organization))
    .catch(() => Observable.of(new organizationActions.EditOrganizationFailedAction()))
    .share();

  @Effect() delete$: Observable<Action> = this.actions$
    .ofType(organizationActions.ActionTypes.DELETE)
    .switchMap((value: Action) => this.organizationsService.deleteOrganization(value.payload))
    .map(organization => new organizationActions.OrganizationRemovedAction(organization))
    .catch((payload: Organization) => Observable.of(new organizationActions.RemoveOrganizationFailedAction(payload)));

  constructor(private actions$: Actions,
              private organizationsService: OrganizationsService) {
  }
}
