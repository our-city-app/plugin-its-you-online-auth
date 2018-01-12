import { Injectable } from '@angular/core';
import { Actions, Effect } from '@ngrx/effects';
import { of as observableOf } from 'rxjs/observable/of';
import { catchError } from 'rxjs/operators/catchError';
import { map } from 'rxjs/operators/map';
import { switchMap } from 'rxjs/operators/switchMap';
import * as actions from '../actions/organizations.action';
import { OrganizationsService } from '../services';

@Injectable()
export class OrganizationsEffects {

  @Effect() getOrganizations$ = this.actions$
    .ofType<actions.GetOrganizationsAction>(actions.ActionTypes.GET_ORGANIZATIONS).pipe(
      switchMap(() => this.organizationsService.getOrganizations().pipe(
        map(payload => new actions.GetOrganizationsCompleteAction(payload)),
        catchError(() => observableOf(new actions.GetOrganizationsFailedAction())),
      )));

  @Effect() getOrganization$ = this.actions$
    .ofType<actions.GetOrganizationAction>(actions.ActionTypes.GET_ORGANIZATION).pipe(
      switchMap(action => this.organizationsService.getOrganization(action.payload).pipe(
        map(payload => new actions.GetOrganizationCompleteAction(payload)),
        catchError(() => observableOf(new actions.GetOrganizationFailedAction())),
      )));

  @Effect() add$ = this.actions$
    .ofType<actions.AddOrganizationAction>(actions.ActionTypes.ADD).pipe(
      switchMap(action => this.organizationsService.createOrganization(action.payload).pipe(
        map(payload => new actions.OrganizationAddedAction(payload)),
      )));

  @Effect() edit$ = this.actions$
    .ofType<actions.EditOrganizationAction>(actions.ActionTypes.EDIT).pipe(
      switchMap(action => this.organizationsService.updateOrganization(action.payload).pipe(
        map(organization => new actions.OrganizationEditedAction(organization)),
        catchError(() => observableOf(new actions.EditOrganizationFailedAction())),
      )));

  @Effect() delete$ = this.actions$
    .ofType<actions.RemoveOrganizationAction>(actions.ActionTypes.DELETE).pipe(
      switchMap(action => this.organizationsService.deleteOrganization(action.payload).pipe(
        map(organization => new actions.OrganizationRemovedAction(organization)),
        catchError(payload => observableOf(new actions.RemoveOrganizationFailedAction(payload))),
      )));

  constructor(private actions$: Actions,
              private organizationsService: OrganizationsService) {
  }
}
