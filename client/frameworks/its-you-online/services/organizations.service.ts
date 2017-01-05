// angular
import { Injectable } from '@angular/core';
import { Http } from '@angular/http';
// libs
import { Observable } from 'rxjs/Observable';
// app
import { Config } from '../../core/index';
import { Analytics, AnalyticsService } from '../../analytics/index';
import { ITS_YOU_ONLINE_CATEGORY } from '../common/category.common';
// module
import { Organization } from '../types/organization.types';
import { ItsYouOnlineConfig } from './its-you-online-config';

@Injectable()
export class OrganizationsService extends Analytics {

  constructor(public analytics: AnalyticsService, private http: Http) {
    super(analytics);
    this.category = ITS_YOU_ONLINE_CATEGORY;
  }

  getOrganizations(): Observable<Array<Organization>> {
    return this.http.get(`${ItsYouOnlineConfig.API_URL}/organizations`)
      .map(res => res.json());
  }

  getOrganization(id: string): Observable<Organization> {
    return this.http.get(`${ItsYouOnlineConfig.API_URL}/organizations/${encodeURIComponent(id)}`)
      .map(res => res.json());
  }

  createOrganization(organization: Organization): Observable<Organization> {
    return this.http.post(`${ItsYouOnlineConfig.API_URL}/organizations`, organization)
      .map(res => res.json());
  }

  updateOrganization(organization: Organization): Observable<Organization> {
    const url = `${ItsYouOnlineConfig.API_URL}/organizations/${encodeURIComponent(organization.id)}`;
    return this.http.put(url, organization)
      .map(res => res.json());
  }

  deleteOrganization(organization: Organization): Observable<Organization> {
    return this.http.delete(`${ItsYouOnlineConfig.API_URL}/organizations/${encodeURIComponent(organization.id)}`)
      .map(res => organization);
  }
}
