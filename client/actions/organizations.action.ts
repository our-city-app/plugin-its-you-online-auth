import { Action } from '@ngrx/store';
import { Organization } from '../index';

export enum ActionTypes {
  GET_ORGANIZATIONS = '[Itsyouonline] Get organizations',
  GET_ORGANIZATIONS_COMPLETE = '[Itsyouonline] Get organizations succeeded',
  GET_ORGANIZATIONS_FAILED = '[Itsyouonline] Get organizations failed',
  GET_ORGANIZATION = '[Itsyouonline] Get organization',
  GET_ORGANIZATION_COMPLETE = '[Itsyouonline] Get organization success',
  GET_ORGANIZATION_FAILED = '[Itsyouonline] Get organization failed',
  CREATE = '[Itsyouonline] Create page',
  ADD = '[Itsyouonline] Add',
  ORGANIZATION_ADDED = '[Itsyouonline] Organization added',
  EDIT = '[Itsyouonline] Edit',
  EDITED = '[Itsyouonline] Edited',
  EDIT_FAILED = '[Itsyouonline] Edit failed',
  DELETE = '[Itsyouonline] Delete',
  DELETED = '[Itsyouonline] Deleted',
}

export class GetOrganizationsAction implements Action {
  readonly type = ActionTypes.GET_ORGANIZATIONS;
}

export class GetOrganizationsCompleteAction implements Action {
  readonly type = ActionTypes.GET_ORGANIZATIONS_COMPLETE;

  constructor(public payload: Array<Organization>) {
  }
}

export class GetOrganizationsFailedAction implements Action {
  readonly type = ActionTypes.GET_ORGANIZATIONS_FAILED;
}

export class GetOrganizationAction implements Action {
  readonly type = ActionTypes.GET_ORGANIZATION;

  constructor(public payload: string) {
  }
}

export class CreateAction implements Action {
  readonly type = ActionTypes.CREATE;
}

export class GetOrganizationCompleteAction implements Action {
  readonly type = ActionTypes.GET_ORGANIZATION_COMPLETE;

  constructor(public payload: Organization) {
  }
}

export class GetOrganizationFailedAction implements Action {
  readonly type = ActionTypes.GET_ORGANIZATION_FAILED;
}

export class AddOrganizationAction implements Action {
  readonly type = ActionTypes.ADD;

  constructor(public payload: Organization) {
  }
}

export class OrganizationAddedAction implements Action {
  readonly type = ActionTypes.ORGANIZATION_ADDED;

  constructor(public payload: Organization) {
  }
}

export class EditOrganizationAction implements Action {
  readonly type = ActionTypes.EDIT;

  constructor(public payload: Organization) {
  }
}

export class OrganizationEditedAction implements Action {
  readonly type = ActionTypes.EDITED;

  constructor(public payload: Organization) {
  }
}

export class EditOrganizationFailedAction implements Action {
  readonly type = ActionTypes.EDIT_FAILED;
}

export class RemoveOrganizationAction implements Action {
  readonly type = ActionTypes.DELETE;

  constructor(public payload: Organization) {
  }
}

export class OrganizationRemovedAction implements Action {
  readonly type = ActionTypes.DELETED;

  constructor(public payload: Organization) {
  }
}

export class RemoveOrganizationFailedAction implements Action {
  readonly type = ActionTypes.DELETED;

  constructor(public payload: Organization) {
  }
}

export type Actions
  = GetOrganizationsAction
  | GetOrganizationsCompleteAction
  | GetOrganizationsFailedAction
  | GetOrganizationAction
  | GetOrganizationCompleteAction
  | GetOrganizationFailedAction
  | CreateAction
  | AddOrganizationAction
  | EditOrganizationAction
  | EditOrganizationFailedAction
  | OrganizationEditedAction
  | OrganizationAddedAction
  | RemoveOrganizationAction
  | OrganizationRemovedAction;
