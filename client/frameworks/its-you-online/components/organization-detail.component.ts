import {
  ChangeDetectionStrategy,
  ChangeDetectorRef,
  Component,
  EventEmitter,
  Input,
  OnDestroy,
  Output,
} from '@angular/core';
import { FormControl } from '@angular/forms';
import { MdChipInputEvent, MdDialog, MdDialogConfig, MdDialogRef } from '@angular/material';
import { Store } from '@ngrx/store';
import { TranslateService } from '@ngx-translate/core';
import { Observable, Subscription } from 'rxjs';
import { LogService } from '../../core/services/index';
import { RouterExtensions } from '../../core/services/router-extensions.service';
import { IAppState } from '../../ngrx/state/app.state';
import { ConfirmDialogComponent, ConfirmDialogData } from '../../sample/index';
import { ActionTypes } from '../actions/organizations.action';
import { Organization, RegistrationResultRoles } from '../index';

@Component({
  moduleId: module.id,
  selector: 'organization-detail',
  templateUrl: 'organization-detail.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class OrganizationDetailComponent implements OnDestroy {
  addModuleFormControl = new FormControl();
  addAcsFormControl = new FormControl();
  status: string;
  statusSubscription: Subscription;
  dialogRef: MdDialogRef<ConfirmDialogComponent>;
  newRole: RegistrationResultRoles;
  newRoleIds: string;
  emptyRole: RegistrationResultRoles = {
    service: '',
    identity: '+default+',
    ids: [],
  };

  @Input() isNew: boolean;
  @Output() add = new EventEmitter<Organization>();
  @Output() update = new EventEmitter<Organization>();
  @Output() remove = new EventEmitter<Organization>();
  private _organization: Organization;

  constructor(private log: LogService, private store: Store<IAppState>,
              public dialog: MdDialog, public translate: TranslateService, private cdRef: ChangeDetectorRef) {
    this.newRole = Object.assign({}, this.emptyRole);
    this.statusSubscription = store.select((state: any) => state.organizations.organizationStatus)
      .subscribe((status: string) => {
        // We need a better way to do this...
      if (ActionTypes.EDITED === status) {
        this.status = 'iyo.organization_edited';
      } else if (ActionTypes.ORGANIZATION_ADDED === status) {
        this.status = 'iyo.organization_added';
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

  public addModuleInput(event: MdChipInputEvent) {
    if (this.organization.modules.indexOf(event.value) === -1) {
      this.organization.modules = [ ...this.organization.modules, event.value ];
      }
    this.addModuleFormControl.reset();
    }

  public removeModule(module: string) {
    this.organization.modules = this.organization.modules.filter(a => a !== module);
  }

  public addAutoConnectedInput(event: MdChipInputEvent) {
    if (!this.addAcsFormControl.valid) {
      this.addAcsFormControl.markAsTouched();
      return;
    }
    if (this.organization.auto_connected_services.indexOf(event.value) === -1) {
      this.organization.auto_connected_services = [ ...this.organization.auto_connected_services, event.value ];
    }
    this.addAcsFormControl.reset();
  }

  public removeAutoConnectedService(acs: string) {
    this.organization.auto_connected_services = this.organization.auto_connected_services.filter(a => a !== acs);
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

  public showConfirmRemoveModule(module: string) {
    let msg = this.translate.get('iyo.do_you_want_to_delete_module', { m: module });
    this.showConfirmDialog(this.translate.get('iyo.confirmation'), msg)
      .filter(confirmed => confirmed).subscribe(confirmed => this.removeModule(module));
  }

  public showConfirmRemoveACS(acs: string) {
    let msg = this.translate.get('iyo.do_you_want_to_delete_auto_connected_service', { acs: acs });
    this.showConfirmDialog(this.translate.get('iyo.confirmation'), msg)
      .filter(confirmed => confirmed).subscribe(confirmed => this.removeAutoConnectedService(acs));
  }

  public showConfirmDialog(title: Observable<string>, message: Observable<string>) {
    let config: MdDialogConfig = {
      data: <ConfirmDialogData>{
        title: title,
        message: message,
        ok: this.translate.get('iyo.yes'),
        cancel: this.translate.get('iyo.no'),
      },
    };
    return this.dialog.open(ConfirmDialogComponent, config).afterClosed();
  }

  ngOnDestroy(): void {
    this.statusSubscription.unsubscribe();
  }


}
