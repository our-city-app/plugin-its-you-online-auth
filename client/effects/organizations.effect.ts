import { Injectable } from '@angular/core';
import { Actions, Effect, ofType } from '@ngrx/effects';
import { of as observableOf } from 'rxjs';
import { catchError, map, switchMap } from 'rxjs/operators';
import * as actions from '../actions/organizations.action';
import { OrganizationsService } from '../services';

@Injectable()
export class OrganizationsEffects {

  @Effect() getOrganizations$ = this.actions$.pipe(
      ofType<actions.GetOrganizationsAction>(actions.ActionTypes.GET_ORGANIZATIONS),
      switchMap(() => this.organizationsService.getOrganizations().pipe(
        map(payload => new actions.GetOrganizationsCompleteAction(payload)),
        catchError(() => observableOf(new actions.GetOrganizationsFailedAction())),
      )));

  @Effect() getOrganization$ = this.actions$.pipe(
      ofType<actions.GetOrganizationAction>(actions.ActionTypes.GET_ORGANIZATION),
      switchMap(action => this.organizationsService.getOrganization(action.payload).pipe(
        map(payload => new actions.GetOrganizationCompleteAction(payload)),
        catchError(() => observableOf(new actions.GetOrganizationFailedAction())),
      )));

  @Effect() add$ = this.actions$.pipe(
      ofType<actions.AddOrganizationAction>(actions.ActionTypes.ADD),
      switchMap(action => this.organizationsService.createOrganization(action.payload).pipe(
        map(payload => new actions.OrganizationAddedAction(payload)),
      )));

  @Effect() edit$ = this.actions$.pipe(
      ofType<actions.EditOrganizationAction>(actions.ActionTypes.EDIT),
      switchMap(action => this.organizationsService.updateOrganization(action.payload).pipe(
        map(organization => new actions.OrganizationEditedAction(organization)),
        catchError(() => observableOf(new actions.EditOrganizationFailedAction())),
      )));

  @Effect() delete$ = this.actions$.pipe(
      ofType<actions.RemoveOrganizationAction>(actions.ActionTypes.DELETE),
      switchMap(action => this.organizationsService.deleteOrganization(action.payload).pipe(
        map(organization => new actions.OrganizationRemovedAction(organization)),
        catchError(payload => observableOf(new actions.RemoveOrganizationFailedAction(payload))),
      )));

  constructor(private actions$: Actions,
              private organizationsService: OrganizationsService) {
  }
}
