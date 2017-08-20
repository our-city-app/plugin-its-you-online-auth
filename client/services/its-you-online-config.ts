import { Config, PluginConfig } from '../../../framework/client/core/utils/config';

export class ItsYouOnlineConfig extends PluginConfig {
  public static NAME: string = 'its_you_online_auth';
  public static VERSION: string = 'v1.0';
  public static API_URL: string = `${Config.API_URL}/plugins/${ItsYouOnlineConfig.NAME}/${ItsYouOnlineConfig.VERSION}`;
}
