export class RegistrationResultRoles {
  constructor(public service: string, public identity: string, public ids: number[]) {
  }
}
export class Organization {
  constructor(public name: string, public client_id: string, public auto_connected_services: string[],
              public roles: RegistrationResultRoles[]) {
  }
}
