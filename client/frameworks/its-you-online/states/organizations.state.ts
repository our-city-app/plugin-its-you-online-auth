import { Observable } from 'rxjs/Observable';
import { Organization } from '../types/organization.types';

export interface IOrganizationsState {
  organizations: Array<Organization>;
  selectedOrganization: string;
  organizationStatus: string;
}

export const initialState: IOrganizationsState = {
  organizations: [],
  selectedOrganization: null,
  organizationStatus: null
};

export function getOrganizations(state$: Observable<IOrganizationsState>) {
  return state$.select(state => state.organizations);
}

export function getOrganization(state$: Observable<IOrganizationsState>) {
  return state$.select(state => state.organizations.filter(o => o.id === state.selectedOrganization)[ 0 ] || {
    id: '',
    name: '',
    auto_connected_services: [],
    roles: [],
    modules: [],
  });
}

export function getOrganizationStatus(state$: Observable<IOrganizationsState>) {
  return state$.select(state => state.organizationStatus);
}
