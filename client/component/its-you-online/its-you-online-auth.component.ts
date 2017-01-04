import { Component } from '@angular/core';
// libs
// app
import { RouterExtensions } from '../../frameworks/core/index';

@Component({
  moduleId: module.id,
  selector: 'settings-component',
  templateUrl: 'its-you-online-auth.component.html'
})
export class ItsYouOnlineAuthComponent {

  constructor(public routerext: RouterExtensions) {
  }
}
