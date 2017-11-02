import { createFeatureSelector, createSelector } from '@ngrx/store';
import { IOrganizationsState } from './index';

export const selectOrganizationsState = createFeatureSelector<IOrganizationsState>('organizations');

export const getOrganizations = createSelector(selectOrganizationsState, s => s.organizations);
export const getSelectedOrganization = createSelector(selectOrganizationsState, s => s.organizations
  .filter(o => o.id === s.selectedOrganization)[ 0 ] || {
  id: '',
  name: '',
  auto_connected_services: [],
  roles: [],
  modules: [],
});
export const getOrganizationStatus = createSelector(selectOrganizationsState, s => s.organizationStatus);
