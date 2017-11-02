import { Organization } from '../index';

export interface IOrganizationsState {
  organizations: Organization[];
  selectedOrganization: string;
  organizationStatus: string;
}

export const initialState: IOrganizationsState = {
  organizations: [],
  selectedOrganization: null,
  organizationStatus: null
};
