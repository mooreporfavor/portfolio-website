export interface UtmOptions {
  source?: string;
  medium?: string;
  campaign?: string;
  content?: string;
  term?: string;
}

export const TNFA_BASE_URL = 'https://thenewforeignassistance.org';
export const DEFAULT_UTM_SOURCE = 'ryanamoore.com';
export const DEFAULT_UTM_MEDIUM = 'referral';
export const DEFAULT_UTM_CAMPAIGN = 'exec_leadership_ryan_moore';

/**
 * Domains where appending UTM query parameters provides no destination analytics value
 * to the site owner and risks breaking mobile Universal Links / deep-link routers.
 */
const EXCLUDED_DOMAINS = new Set([
  'linkedin.com',
  'www.linkedin.com',
  'facebook.com',
  'www.facebook.com',
  'x.com',
  'www.x.com',
  'twitter.com',
  'www.twitter.com',
  'youtube.com',
  'www.youtube.com',
  'youtu.be',
  'github.com',
  'www.github.com',
]);

/**
 * Legacy server script extensions or static file downloads that should not have query strings mutated.
 */
const EXCLUDED_EXTENSIONS = /\.(cfm|aspx|jsp|pdf|docx?|xlsx?|pptx?|zip|png|jpe?g|gif|webp|svg)$/i;

export function isUtmSafeUrl(url: URL): boolean {
  if (url.protocol !== 'http:' && url.protocol !== 'https:') return false;
  const host = url.hostname.toLowerCase();
  if (EXCLUDED_DOMAINS.has(host)) return false;
  if (EXCLUDED_EXTENSIONS.test(url.pathname)) return false;
  return true;
}

/**
 * Safely appends standardized UTM parameters to any external URL while preserving
 * existing query parameters and hashes, skipping excluded domains and fragile extensions.
 */
export function withUtm(rawUrl: string, options: UtmOptions = {}): string {
  try {
    const url = new URL(rawUrl);
    if (!isUtmSafeUrl(url)) {
      return rawUrl;
    }
    url.searchParams.set('utm_source', options.source ?? DEFAULT_UTM_SOURCE);
    url.searchParams.set('utm_medium', options.medium ?? DEFAULT_UTM_MEDIUM);
    url.searchParams.set('utm_campaign', options.campaign ?? DEFAULT_UTM_CAMPAIGN);
    if (options.content) {
      url.searchParams.set('utm_content', options.content);
    }
    if (options.term) {
      url.searchParams.set('utm_term', options.term);
    }
    return url.toString();
  } catch {
    return rawUrl;
  }
}

/**
 * Generates a tracked TNFA outbound URL using the <page>-<section>-<element> content convention.
 */
export function tnfaUrl(content: string, campaign: string = DEFAULT_UTM_CAMPAIGN): string {
  return withUtm(TNFA_BASE_URL, {
    campaign,
    content,
  });
}
