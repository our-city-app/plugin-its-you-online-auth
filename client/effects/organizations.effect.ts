// angular
import { Injectable } from '@angular/core';
import { Actions, Effect } from '@ngrx/effects';
// libs
import { Action } from '@ngrx/store';
import { Observable } from 'rxjs/Observable';
import * as actions from '../actions/organizations.action';
import { Organization } from '../index';
// module
import { OrganizationsService } from '../services/organizations.service';

@Injectable()
export class OrganizationsEffects {

  @Effect() getOrganizations$: Observable<Action> = this.actions$
    .ofType(actions.ActionTypes.GET_ORGANIZATIONS)
    .switchMap(() => this.organizationsService.getOrganizations()
      .map(payload => new actions.GetOrganizationsCompleteAction(payload))
      .catch(() => Observable.of(new actions.GetOrganizationsFailedAction())));

  @Effect() getOrganization$: Observable<Action> = this.actions$
    .ofType(actions.ActionTypes.GET_ORGANIZATION)
    .switchMap((value: Action) => this.organizationsService.getOrganization(value.payload)
      .map((payload: Organization) => new actions.GetOrganizationCompleteAction(payload))
      .catch(() => Observable.of(new actions.GetOrganizationFailedAction())));

  @Effect() add$: Observable<Action> = this.actions$
    .ofType(actions.ActionTypes.ADD)
    .switchMap((value: Action) => this.organizationsService.createOrganization(value.payload)
      .map((payload: Organization) => new actions.OrganizationAddedAction(payload)));

  @Effect() edit$: Observable<Action> = this.actions$
    .ofType(actions.ActionTypes.EDIT)
    .switchMap((value: Action) => this.organizationsService.updateOrganization(value.payload)
      .map(organization => new actions.OrganizationEditedAction(organization))
      .catch(() => Observable.of(new actions.EditOrganizationFailedAction())));

  @Effect() delete$: Observable<Action> = this.actions$
    .ofType(actions.ActionTypes.DELETE)
    .switchMap((value: Action) => this.organizationsService.deleteOrganization(value.payload)
      .map(organization => new actions.OrganizationRemovedAction(organization))
      .catch((payload: Organization) => Observable.of(new actions.RemoveOrganizationFailedAction(payload))));

  constructor(private actions$: Actions,
              private organizationsService: OrganizationsService) {
  }
}
