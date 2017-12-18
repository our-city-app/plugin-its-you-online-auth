import { ChangeDetectionStrategy, Component, OnDestroy, OnInit, ViewEncapsulation } from '@angular/core';
import { Store } from '@ngrx/store';
import { filter } from 'rxjs/operators/filter';
import { Subscription } from 'rxjs/Subscription';
import { getIdentity } from '../../../framework/client/identity/identity.state';
import { Identity } from '../../../framework/client/identity/index';
import { IAppState } from '../../../framework/client/ngrx/index';
import { Router } from '@angular/router';

@Component({
  selector: 'settings-component',
  encapsulation: ViewEncapsulation.None,
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <organization-settings *ngIf='isAdmin'></organization-settings>`,
})
export class ItsYouOnlineAuthComponent implements OnInit, OnDestroy {
  isAdmin: boolean = false;
  private sub: Subscription;

  constructor(private router: Router,
              private store: Store<IAppState>) {
  }

  ngOnInit(): void {
    this.sub = this.store.select(getIdentity).pipe(filter(i => i !== null)).subscribe((identity: Identity) => {
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
        this.router.navigateByUrl(route);
      }
    });
  }

  ngOnDestroy() {
    this.sub.unsubscribe();
  }
}
