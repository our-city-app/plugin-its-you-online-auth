import '@ngrx/core/add/operator/select';
import { compose } from '@ngrx/core/compose';
import { Observable } from 'rxjs/Observable';
import * as fromItsyouonline from './index';
import { IOrganizationsState } from './states/organizations.state';

export function getOrganizationsState(state$: Observable<IOrganizationsState>) {
  return state$.select(s => s.organizations);
}


export const getOrganizations: any = compose(fromItsyouonline.getOrganizations, getOrganizationsState);

export const getSelectedOrganization: any = compose(fromItsyouonline.getOrganization, getOrganizationsState);

export const getOrganizationStatus: any = compose(fromItsyouonline.getOrganizationStatus, getOrganizationsState);
