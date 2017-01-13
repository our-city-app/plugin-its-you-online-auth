// libs
import { Component, OnInit } from '@angular/core';
import { Subscription } from 'rxjs/Subscription';
import { Store } from '@ngrx/store';
// app
import { RouterExtensions } from '../../frameworks/core/index';
import { IAppState, getIdentity } from '../../frameworks/ngrx/index';
import { Identity } from '../../frameworks/sample/index';

@Component({
  moduleId: module.id,
  selector: 'settings-component',
  templateUrl: 'its-you-online-auth.component.html'
})
export class ItsYouOnlineAuthComponent implements OnInit {
  isAdmin: boolean = false;
  identitySubscription: Subscription;

  constructor(private routerext: RouterExtensions, private store: Store<IAppState>) {
  }

  ngOnInit(): void {
    this.identitySubscription = this.store.let(getIdentity).subscribe((identity: Identity) => {
        if (!identity.user_id) {
          return;
        }
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
    );
  }

  ngOnDestroy(): void {
    this.identitySubscription.unsubscribe();
  }
}
