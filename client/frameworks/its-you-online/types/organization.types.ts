export class RegistrationResultRoles {
  constructor(public service: string, public identity: string, public ids: number[]) {
  }
}
export class Organization {
  constructor(public name: string, public id: string, public auto_connected_services: string[],
              public roles: RegistrationResultRoles[], public modules: string[]) {
  }
}
