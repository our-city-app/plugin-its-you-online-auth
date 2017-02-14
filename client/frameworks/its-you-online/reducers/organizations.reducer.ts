import { IOrganizationsState, initialState } from '../states/index';
import * as actions from '../actions/organizations.action';
import { Organization } from '../index';

export function organizationsReducer(state: IOrganizationsState = initialState,
                                     action: actions.Actions): IOrganizationsState {
  let organizations: Organization[];
  switch (action.type) {
    case actions.ActionTypes.GET_ORGANIZATIONS_COMPLETE:
      return (<any>Object).assign({}, state, {
        organizations: action.payload,
        selectedOrganization: state.selectedOrganization,
        organizationStatus: action.type
      });
    case actions.ActionTypes.GET_ORGANIZATION:
      return {
        organizations: state.organizations,
        selectedOrganization: <string>action.payload,
        organizationStatus: action.type
      };
    case actions.ActionTypes.CREATE:
      return {
        organizations: state.organizations,
        selectedOrganization: <string>action.payload,
        organizationStatus: action.type
      };
    case actions.ActionTypes.EDITED:
      const org = <Organization>action.payload;
      organizations = state.organizations.filter(o => o.id !== org.id);
      return (<any>Object).assign({}, state, {
        organizations: [ ...organizations, org ],
        selectedOrganization: state.selectedOrganization,
        organizationStatus: action.type
      });
    case actions.ActionTypes.GET_ORGANIZATION_COMPLETE:
      const organization = <Organization>action.payload;

      if (state.organizations.find(organization => organization.id === organization.id)) {
        // already present in the state
        return Object.assign({}, state, {organizationStatus: action.type});
      }

      return Object.assign({}, state, {
        organizations: [ ...state.organizations, organization ],
        selectedOrganization: organization.id,
        organizationStatus: action.type
      });
    case actions.ActionTypes.ORGANIZATION_ADDED:
      return (<any>Object).assign({}, state, {
        organizations: [ ...state.organizations, action.payload ],
        selectedOrganization: state.selectedOrganization,
        organizationStatus: action.type
      });
    case actions.ActionTypes.DELETED:
      organizations = state.organizations.filter(org => {
        return org.id !== (<Organization>action.payload).id;
      });
      return (<any>Object).assign({}, state, {
        organizations: organizations,
        selectedOrganization: state.selectedOrganization,
        organizationStatus: action.type
      });

    case actions.ActionTypes.ADD:
    case actions.ActionTypes.GET_ORGANIZATIONS:
    case actions.ActionTypes.GET_ORGANIZATIONS_FAILED:
    case actions.ActionTypes.GET_ORGANIZATION_FAILED:
    case actions.ActionTypes.EDIT:
    case actions.ActionTypes.EDIT_FAILED:
    case actions.ActionTypes.DELETE:
      return Object.assign({}, state, {organizationStatus: action.type});
    default:
      return state;
  }
}
