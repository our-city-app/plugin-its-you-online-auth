export interface Profile {
  username: string;
  language: string;
  info: ProfileInfo | null;
}

export interface ProfileInfo {
  addresses: ProfileInfoAddress[];
  avatar: ProfileInfoAvatar[];
  bankaccounts: ProfileInfoBankAccount[];
  digitalwallet: ProfileInfoDigitalAssetAddress[];
  emailaddresses: ProfileInfoEmailAddress[];
  facebook: ProfileInfoFacebook;
  firstname: string;
  github: ProfileInfoGithubAccount;
  lastname: string;
  ownerof: ProfileInfoOwnerOf;
  phonenumbers: ProfileInfoPhoneNumber[];
  publicKeys: ProfileInfoPublicKey[];
  username: string;
  validatedemailaddresses: ProfileInfoEmailAddress[];
  validatedphonenumbers: ProfileInfoPhoneNumber[];
}

export interface ProfileInfoAddress {
  city: string;
  country: string;
  label: string;
  nr: string;
  other: string;
  postalcode: string;
  street: string;
}

export interface ProfileInfoAvatar {
  label: string;
  source: string;
}

export interface ProfileInfoBankAccount {
  bic: string;
  country: string;
  iban: string;
  label: string;
}

export interface ProfileInfoDigitalAssetAddress {
  address: string;
  currencysymbol: string;
  expire: string;
  label: string;
  noexpiration: boolean;
}

export interface ProfileInfoEmailAddress {
  emailaddress: string;
  label: string;
}

export interface ProfileInfoFacebook {
  id: string;
  link: string;
  name: string;
  picture: string;
}

export interface ProfileInfoGithubAccount {
  avatar_url: string;
  html_url: string;
  id: string;
  login: string;
  name: string;
}

export interface ProfileInfoOwnerOf {
  emailaddresses: ProfileInfoEmailAddress[];
}

export interface ProfileInfoPhoneNumber {
  label: string;
  phonenumber: string;
}

export interface ProfileInfoPublicKey {
  label: string;
  publickey: string;
}
