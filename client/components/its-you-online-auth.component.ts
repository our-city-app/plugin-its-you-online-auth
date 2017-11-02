import { ChangeDetectionStrategy, Component, OnDestroy, OnInit, ViewEncapsulation } from '@angular/core';
import { Store } from '@ngrx/store';
import { Subscription } from 'rxjs/Subscription';
import { RouterExtensions } from '../../../framework/client/core/index';
import { getIdentity } from '../../../framework/client/identity/identity.state';
import { Identity } from '../../../framework/client/identity/index';
import { IAppState } from '../../../framework/client/ngrx/index';

@Component({
  moduleId: module.id,
  selector: 'settings-component',
  encapsulation: ViewEncapsulation.None,
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <organization-settings *ngIf='isAdmin'></organization-settings>`,
})
export class ItsYouOnlineAuthComponent implements OnInit, OnDestroy {
  isAdmin: boolean = false;
  private sub: Subscription;

  constructor(private routerext: RouterExtensions,
              private store: Store<IAppState>) {
  }

  ngOnInit(): void {
    this.sub = this.store.select(getIdentity).filter(i => i !== null).subscribe((identity: Identity) => {
      if (identity.scopes.includes('admin')) {
        this.isAdmin = true;
      } else {
        let organization = identity.scopes.filter((s: string) => {
          return s.startsWith('memberof:') && s.endsWith(':admin');
        })[0];
        let route: string = '';
        if (organization) {
          route = '/itsyouonlinesettings/organizations/' + organization
            .replace('memberof:', '')
            .replace(':admin', '');
        }
        this.routerext.navigateByUrl(route);
      }
    });
  }

  ngOnDestroy() {
    this.sub.unsubscribe();
  }
}
