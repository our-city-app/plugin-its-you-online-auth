import { Action } from '@ngrx/store';
import { type } from '../../../framework/client/core/utils/type';
import { Organization } from '../index';

export interface IActionTypes {
  GET_ORGANIZATIONS: '[Itsyouonline] Get organizations';
  GET_ORGANIZATIONS_COMPLETE: '[Itsyouonline] Get organizations succeeded';
  GET_ORGANIZATIONS_FAILED: '[Itsyouonline] Get organizations failed';
  GET_ORGANIZATION: '[Itsyouonline] Get organization';
  GET_ORGANIZATION_COMPLETE: '[Itsyouonline] Get organization success';
  GET_ORGANIZATION_FAILED: '[Itsyouonline] Get organization failed';
  CREATE: '[Itsyouonline] Create page';
  ADD: '[Itsyouonline] Add';
  ORGANIZATION_ADDED: '[Itsyouonline] Organization added';
  EDIT: '[Itsyouonline] Edit';
  EDITED: '[Itsyouonline] Edited';
  EDIT_FAILED: '[Itsyouonline] Edit failed';
  DELETE: '[Itsyouonline] Delete';
  DELETED: '[Itsyouonline] Deleted';
}

export const ActionTypes: IActionTypes = {
  GET_ORGANIZATIONS: type('[Itsyouonline] Get organizations'),
  GET_ORGANIZATIONS_COMPLETE: type('[Itsyouonline] Get organizations succeeded'),
  GET_ORGANIZATIONS_FAILED: type('[Itsyouonline] Get organizations failed'),
  GET_ORGANIZATION: type('[Itsyouonline] Get organization'),
  GET_ORGANIZATION_COMPLETE: type('[Itsyouonline] Get organization success'),
  GET_ORGANIZATION_FAILED: type('[Itsyouonline] Get organization failed'),
  CREATE: type('[Itsyouonline] Create page'),
  ADD: type('[Itsyouonline] Add'),
  ORGANIZATION_ADDED: type('[Itsyouonline] Organization added'),
  EDIT: type('[Itsyouonline] Edit'),
  EDITED: type('[Itsyouonline] Edited'),
  EDIT_FAILED: type('[Itsyouonline] Edit failed'),
  DELETE: type('[Itsyouonline] Delete'),
  DELETED: type('[Itsyouonline] Deleted'),
};

/**
 * Every action is comprised of at least a type and an optional
 * payload. Expressing actions as classes enables powerful
 * type checking in reducer functions.
 *
 * See Discriminated Unions: https://www.typescriptlang.org/docs/handbook/advanced-types.html#discriminated-unions
 */
export class GetOrganizationsAction implements Action {
  type = ActionTypes.GET_ORGANIZATIONS;
  payload: null = null;
}

export class GetOrganizationsCompleteAction implements Action {
  type = ActionTypes.GET_ORGANIZATIONS_COMPLETE;

  constructor(public payload: Array<Organization>) {
  }
}

export class GetOrganizationsFailedAction implements Action {
  type = ActionTypes.GET_ORGANIZATIONS_FAILED;
  payload: null = null;
}

export class GetOrganizationAction implements Action {
  type = ActionTypes.GET_ORGANIZATION;

  constructor(public payload: string) {
  }
}

export class CreateAction implements Action {
  type = ActionTypes.CREATE;
}

export class GetOrganizationCompleteAction implements Action {
  type = ActionTypes.GET_ORGANIZATION_COMPLETE;

  constructor(public payload: Organization) {
  }
}

export class GetOrganizationFailedAction implements Action {
  type = ActionTypes.GET_ORGANIZATION_FAILED;
  payload: null = null;
}

export class AddOrganizationAction implements Action {
  type = ActionTypes.ADD;

  constructor(public payload: Organization) {
  }
}

export class OrganizationAddedAction implements Action {
  type = ActionTypes.ORGANIZATION_ADDED;

  constructor(public payload: Organization) {
  }
}

export class EditOrganizationAction implements Action {
  type = ActionTypes.EDIT;

  constructor(public payload: Organization) {
  }
}

export class OrganizationEditedAction implements Action {
  type = ActionTypes.EDITED;

  constructor(public payload: Organization) {
  }
}

export class EditOrganizationFailedAction implements Action {
  type = ActionTypes.EDIT_FAILED;
  payload: null = null;
}

export class RemoveOrganizationAction implements Action {
  type = ActionTypes.DELETE;

  constructor(public payload: Organization) {
  }
}

export class OrganizationRemovedAction implements Action {
  type = ActionTypes.DELETED;

  constructor(public payload: Organization) {
  }
}

export class RemoveOrganizationFailedAction implements Action {
  type = ActionTypes.DELETED;

  constructor(public payload: Organization) {
  }
}

/**
 * Export a type alias of all actions in this action group
 * so that reducers can easily compose action types
 */
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
