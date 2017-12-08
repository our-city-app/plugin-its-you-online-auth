import { insertItem, removeItem, updateItem } from '../../../framework/client/ngrx/redux-utils';
import * as actions from '../actions/organizations.action';
import { initialState, IOrganizationsState } from '../states/index';

export function organizationsReducer(state: IOrganizationsState = initialState,
                                     action: actions.Actions): IOrganizationsState {
  switch (action.type) {
    case actions.ActionTypes.GET_ORGANIZATIONS_COMPLETE:
      return {
        ...state,
        selectedOrganization: state.selectedOrganization,
        organizationStatus: action.type,
      };
    case actions.ActionTypes.GET_ORGANIZATION:
      return {
        ...state,
        selectedOrganization: action.payload,
        organizationStatus: action.type
      };
    case actions.ActionTypes.CREATE:
      return {
        ...state,
        selectedOrganization: '',
        organizationStatus: action.type
      };
    case actions.ActionTypes.EDITED:
      return {
        ...state,
        organizations: updateItem(state.organizations, action.payload, 'id'),
        organizationStatus: action.type
      };
    case actions.ActionTypes.GET_ORGANIZATION_COMPLETE:
      if (state.organizations.find(organization => organization.id === action.payload.id)) {
        // already present in the state
        return { ...state, organizationStatus: action.type };
      }
      return {
        ...state,
        organizations: insertItem(state.organizations, action.payload),
        selectedOrganization: action.payload.id,
        organizationStatus: action.type,
      };
    case actions.ActionTypes.ORGANIZATION_ADDED:
      return {
        ...state,
        organizations: [ ...state.organizations, action.payload ],
        selectedOrganization: state.selectedOrganization,
        organizationStatus: action.type
      };
    case actions.ActionTypes.DELETED:
      return {
        ...state,
        organizations: removeItem(state.organizations, action.payload, 'id'),
        organizationStatus: action.type
      };
    case actions.ActionTypes.ADD:
    case actions.ActionTypes.GET_ORGANIZATIONS:
    case actions.ActionTypes.GET_ORGANIZATIONS_FAILED:
    case actions.ActionTypes.GET_ORGANIZATION_FAILED:
    case actions.ActionTypes.EDIT:
    case actions.ActionTypes.EDIT_FAILED:
    case actions.ActionTypes.DELETE:
      return { ...state, organizationStatus: action.type };
    default:
      return state;
  }
}
