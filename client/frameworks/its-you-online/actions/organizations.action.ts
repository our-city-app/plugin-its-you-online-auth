import { Action } from '@ngrx/store';
import { type } from '../../core/utils/type';
import { ITS_YOU_ONLINE_CATEGORY } from '../common/category.common';
import { Organization } from '../index';

/**
 * For each action type in an action group, make a simple
 * enum object for all of this group's action types.
 *
 * The 'type' utility function coerces strings into string
 * literal types and runs a simple check to guarantee all
 * action types in the application are unique.
 */
export interface IOrganizationsActions {
  GET_ORGANIZATIONS: string;
  GET_ORGANIZATIONS_COMPLETE: string;
  GET_ORGANIZATIONS_FAILED: string;
  GET_ORGANIZATION: string;
  GET_ORGANIZATION_COMPLETE: string;
  GET_ORGANIZATION_FAILED: string;
  CREATE: string;
  ADD: string;
  ORGANIZATION_ADDED: string;
  EDIT: string;
  EDITED: string;
  EDIT_FAILED: string;
  DELETE: string;
  DELETED: string;
}

export const ActionTypes: IOrganizationsActions = {
  GET_ORGANIZATIONS: type(`${ITS_YOU_ONLINE_CATEGORY} Get organizations`),
  GET_ORGANIZATIONS_COMPLETE: type(`${ITS_YOU_ONLINE_CATEGORY} Get organizations succeeded`),
  GET_ORGANIZATIONS_FAILED: type(`${ITS_YOU_ONLINE_CATEGORY} Get organizations failed`),
  GET_ORGANIZATION: type(`${ITS_YOU_ONLINE_CATEGORY} Get organization`),
  GET_ORGANIZATION_COMPLETE: type(`${ITS_YOU_ONLINE_CATEGORY} Get organization success`),
  GET_ORGANIZATION_FAILED: type(`${ITS_YOU_ONLINE_CATEGORY} Get organization failed`),
  CREATE: type(`${ITS_YOU_ONLINE_CATEGORY} Create page`),
  ADD: type(`${ITS_YOU_ONLINE_CATEGORY} Add`),
  ORGANIZATION_ADDED: type(`${ITS_YOU_ONLINE_CATEGORY} Organization added`),
  EDIT: type(`${ITS_YOU_ONLINE_CATEGORY} Edit`),
  EDITED: type(`${ITS_YOU_ONLINE_CATEGORY} Edited`),
  EDIT_FAILED: type(`${ITS_YOU_ONLINE_CATEGORY} Edit failed`),
  DELETE: type(`${ITS_YOU_ONLINE_CATEGORY} Delete`),
  DELETED: type(`${ITS_YOU_ONLINE_CATEGORY} Deleted`),
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
  payload: string = null;
}

export class GetOrganizationsCompleteAction implements Action {
  type = ActionTypes.GET_ORGANIZATIONS_COMPLETE;

  constructor(public payload: Array<Organization>) {
  }
}

export class GetOrganizationsFailedAction implements Action {
  type = ActionTypes.GET_ORGANIZATIONS_FAILED;
  payload: string = null;
}

export class GetOrganizationAction implements Action {
  type = ActionTypes.GET_ORGANIZATION;

  constructor(public payload: string) {
  }
}

export class CreateAction implements Action {
  type = ActionTypes.CREATE;
  payload: string = null;
}

export class GetOrganizationCompleteAction implements Action {
  type = ActionTypes.GET_ORGANIZATION_COMPLETE;

  constructor(public payload: Organization) {
  }
}

export class GetOrganizationFailedAction implements Action {
  type = ActionTypes.GET_ORGANIZATION_FAILED;
  payload: string = null;
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
  payload: string = null;
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
  | AddOrganizationAction
  | EditOrganizationAction
  | OrganizationEditedAction
  | OrganizationAddedAction
  | RemoveOrganizationAction
  | OrganizationRemovedAction;
