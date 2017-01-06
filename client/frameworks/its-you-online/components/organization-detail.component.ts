import {
  Component,
  Input,
  Output,
  EventEmitter,
  ChangeDetectionStrategy,
  OnDestroy,
  ChangeDetectorRef
} from '@angular/core';
import { Organization, RegistrationResultRoles } from '../types/organization.types';
import { ActionTypes, IOrganizationsActions } from '../actions/organizations.action';
import { Store } from '@ngrx/store';
import { IOrganizationsState } from '../states/organizations.state';
import { Subscription } from 'rxjs';
import { RouterExtensions } from '../../core/services/router-extensions.service';
import { LogService } from '../../core/services/log.service';
import { ConfirmDialogComponent } from '../../sample/index';
import { MdDialogConfig, MdDialog, MdDialogRef } from '@angular/material';
import { TranslateService } from 'ng2-translate';

@Component({
  moduleId: module.id,
  selector: 'organization-detail',
  templateUrl: 'organization-detail.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class OrganizationDetailComponent implements OnDestroy {
  _organization: Organization;
  status: string;
  ActionTypes: IOrganizationsActions = ActionTypes;
  statusSubscription: Subscription;
  dialogRef: MdDialogRef<ConfirmDialogComponent>;
  newModule: string;
  newACS: string;
  newRole: RegistrationResultRoles;
  newRoleIds: string;
  emptyRole: RegistrationResultRoles = {
    service: '',
    identity: '+default+',
    ids: []
  };

  /**
   * Presentational components receive data through @Input() and communicate events
   * through @Output() but generally maintain no internal state of their
   * own. All decisions are delegated to 'container', or 'smart'
   * components before data updates flow back down.
   *
   * More on 'smart' and 'presentational' components see
   * https://gist.github.com/btroncone/a6e4347326749f938510#utilizing-container-components
   */
  @Input() isNew: boolean;
  @Output() add = new EventEmitter<Organization>();
  @Output() update = new EventEmitter<Organization>();
  @Output() remove = new EventEmitter<Organization>();

  constructor(private log: LogService, private store: Store<IOrganizationsState>, public routerext: RouterExtensions,
              public dialog: MdDialog, public translate: TranslateService, private cdRef: ChangeDetectorRef) {
    this.newRole = Object.assign({}, this.emptyRole);
    this.statusSubscription = store.select((state: any) => state.organizations.organizationStatus)
      .subscribe((status: string) => {
      if (ActionTypes.EDITED === status) {
        this.status = 'organization_edited';
      } else if (ActionTypes.ORGANIZATION_ADDED === status) {
        this.status = 'organization_added';
      } else {
        return;
      }
      setTimeout(() => {
        this.status = null;
        cdRef.markForCheck();
      }, 5000);
    });
  }

  @Input() set organization(value: Organization) {
    this._organization = Object.assign({}, value);
  }

  get organization() {
    return this._organization;
  }


  public save(organization: Organization) {
    if (this.isNew) {
      this.add.emit(organization);
    } else {
      this.update.emit(organization);
    }
  }

  public addModuleInput() {
      if (this.organization.modules.indexOf(this.newModule) === -1) {
        this.organization.modules = [ ...this.organization.modules, this.newModule ];
      }
      this.newModule = '';
    }

  public removeModule(thiz: OrganizationDetailComponent, m: string) {
      thiz.organization.modules = thiz.organization.modules.filter(a => a !== m);
      thiz.cdRef.markForCheck();
  }

  public addAutoConnectedInput() {
    if (this.organization.auto_connected_services.indexOf(this.newACS) === -1) {
      this.organization.auto_connected_services = [ ...this.organization.auto_connected_services, this.newACS ];
    }
    this.newACS = '';
  }

  public removeAutoConnectedService(thiz: OrganizationDetailComponent, acs: string) {
    thiz.organization.auto_connected_services = thiz.organization.auto_connected_services.filter(a => a !== acs);
    thiz.cdRef.markForCheck();
  }

  public addRole() {
    try {
      this.newRole.ids = this.newRoleIds.split(',').map(r => parseInt(r.trim())).filter(r => !isNaN(r));
    } catch (e) {
      this.log.error(e);
      this.status = 'invalid_roles';
      return;
    }
    this.organization.roles = [ ...this.organization.roles, this.newRole ];
    this.newRole = Object.assign({}, this.emptyRole);
    this.newRoleIds = '';
  }

  public removeRole(role: RegistrationResultRoles) {
    this.organization.roles = this.organization.roles.filter(a => a !== role);
  }

  public showConfirmRemoveModule(m: string) {
    let msg = this.translate.get('do_you_want_to_delete_module', {m: m});
    this.showConfirmDialog(this.translate.get('confirmation'), msg, this.removeModule, m);
  }

  public showConfirmRemoveACS(acs: string) {
    let msg = this.translate.get('do_you_want_to_delete_auto_connected_service', {acs: acs});
    this.showConfirmDialog(this.translate.get('confirmation'), msg, this.removeAutoConnectedService, acs);
  }

  public showConfirmDialog(title: any, message: any, callback: any, callback_param: string) {
      let config: MdDialogConfig = {
          disableClose: false,
          width: '',
          height: '',
          position: {
            top: '',
            bottom: '',
            left: '',
            right: ''
          }
      };
      this.dialogRef = this.dialog.open(ConfirmDialogComponent, config);
      // TODO: https://github.com/angular/material2/pull/2266
      this.dialogRef.componentInstance[ 'title' ] = title;
      this.dialogRef.componentInstance[ 'message' ] = message;
      this.dialogRef.afterClosed().subscribe((confirmed: boolean) => {
          this.dialogRef = null;
          if (confirmed) {
              callback(this, callback_param);
          }
      });
  }

  ngOnDestroy(): void {
    this.statusSubscription.unsubscribe();
  }


}
