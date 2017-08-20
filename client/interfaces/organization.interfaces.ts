export interface RegistrationResultRoles {
  service: string;
  identity: string;
  ids: number[];
}

export interface Organization {
  name: string;
  id: string;
  auto_connected_services: string[];
  roles: RegistrationResultRoles[];
  modules: string[];
}
