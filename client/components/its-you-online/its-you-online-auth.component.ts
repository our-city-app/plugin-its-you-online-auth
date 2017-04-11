// libs
import { Component, OnInit } from '@angular/core';
// app
import { RouterExtensions } from '../../frameworks/core/index';
import { IAppState } from '../../frameworks/ngrx/index';
import { AuthenticationService, Identity } from '../../frameworks/sample/index';

@Component({
  moduleId: module.id,
  selector: 'settings-component',
  template: `
    <organization-settings *ngIf="isAdmin"></organization-settings>`
})
export class ItsYouOnlineAuthComponent implements OnInit {
  isAdmin: boolean = false;

  constructor(private routerext: RouterExtensions,
              private auth: AuthenticationService) {
  }

  ngOnInit(): void {
    let identity: Identity = this.auth.identity;
    if (identity.scopes.includes('admin')) {
      this.isAdmin = true;
    } else {
      let organization = identity.scopes.filter((s: string) => {
        return s.startsWith('memberof:') && s.endsWith(':admin');
      })[ 0 ];
      let route: string = '';
      if (organization) {
        route = '/itsyouonlinesettings/organizations/' + organization
            .replace('memberof:', '')
            .replace(':admin', '');
      }
      this.routerext.navigateByUrl(route);
    }
  }
}
