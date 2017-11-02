// angular
import { Injectable } from '@angular/core';
import { Actions, Effect } from '@ngrx/effects';
import { Observable } from 'rxjs/Observable';
import * as actions from '../actions/organizations.action';
import { OrganizationsService } from '../services/organizations.service';
import { Organization } from '../interfaces/organization.interfaces';

@Injectable()
export class OrganizationsEffects {

  @Effect() getOrganizations$ = this.actions$
    .ofType<actions.GetOrganizationsAction>(actions.ActionTypes.GET_ORGANIZATIONS)
    .switchMap(() => this.organizationsService.getOrganizations()
      .map(payload => new actions.GetOrganizationsCompleteAction(payload))
      .catch(() => Observable.of(new actions.GetOrganizationsFailedAction())));

  @Effect() getOrganization$ = this.actions$
    .ofType<actions.GetOrganizationAction>(actions.ActionTypes.GET_ORGANIZATION)
    .switchMap(action => this.organizationsService.getOrganization(action.payload)
      .map((payload: Organization) => new actions.GetOrganizationCompleteAction(payload))
      .catch(() => Observable.of(new actions.GetOrganizationFailedAction())));

  @Effect() add$ = this.actions$
    .ofType<actions.AddOrganizationAction>(actions.ActionTypes.ADD)
    .switchMap(action => this.organizationsService.createOrganization(action.payload)
      .map((payload: Organization) => new actions.OrganizationAddedAction(payload)));

  @Effect() edit$ = this.actions$
    .ofType<actions.EditOrganizationAction>(actions.ActionTypes.EDIT)
    .switchMap(action => this.organizationsService.updateOrganization(action.payload)
      .map(organization => new actions.OrganizationEditedAction(organization))
      .catch(() => Observable.of(new actions.EditOrganizationFailedAction())));

  @Effect() delete$ = this.actions$
    .ofType<actions.RemoveOrganizationAction>(actions.ActionTypes.DELETE)
    .switchMap(action => this.organizationsService.deleteOrganization(action.payload)
      .map(organization => new actions.OrganizationRemovedAction(organization))
      .catch((payload: Organization) => Observable.of(new actions.RemoveOrganizationFailedAction(payload))));

  constructor(private actions$: Actions,
              private organizationsService: OrganizationsService) {
  }
}
