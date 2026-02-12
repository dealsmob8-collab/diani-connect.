import fs from 'node:fs/promises';
import path from 'node:path';
import { normalizeProduct, type Product } from './normalize';

type WooCategory = { id: number; name: string; slug: string; parent: number };

type Snapshot = {
  fetchedAt: string;
  products: Product[];
  categories: WooCategory[];
};

const CACHE_FILE = path.join(process.cwd(), '.cache', 'woo-snapshot.json');
const CACHE_TTL_MS = 1000 * 60 * 10;

const env = {
  baseUrl: import.meta.env.WC_BASE_URL,
  consumerKey: import.meta.env.WC_CONSUMER_KEY,
  consumerSecret: import.meta.env.WC_CONSUMER_SECRET
};

const hasAuth = Boolean(env.baseUrl && env.consumerKey && env.consumerSecret);

const wait = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

async function withRetry<T>(fn: () => Promise<T>, retries = 3): Promise<T> {
  let lastError: unknown;
  for (let attempt = 1; attempt <= retries; attempt += 1) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;
      if (attempt < retries) await wait(250 * attempt);
    }
  }
  throw lastError;
}

function buildUrl(endpoint: string, page: number): string {
  if (!env.baseUrl || !env.consumerKey || !env.consumerSecret) {
    throw new Error('Missing WooCommerce credentials in environment variables.');
  }

  const url = new URL(`/wp-json/wc/v3/${endpoint}`, env.baseUrl);
  url.searchParams.set('consumer_key', env.consumerKey);
  url.searchParams.set('consumer_secret', env.consumerSecret);
  url.searchParams.set('per_page', '100');
  url.searchParams.set('page', String(page));
  if (endpoint === 'products') url.searchParams.set('status', 'publish');
  return url.toString();
}

async function fetchPaged<T>(endpoint: string): Promise<T[]> {
  const rows: T[] = [];

  for (let page = 1; ; page += 1) {
    const url = buildUrl(endpoint, page);
    const response = await withRetry(() => fetch(url));

    if (!response.ok) {
      throw new Error(`Failed ${endpoint} page ${page}: ${response.status}`);
    }

    const data = (await response.json()) as T[];
    rows.push(...data);
    if (data.length < 100) break;
  }

  return rows;
}

async function readSnapshot(): Promise<Snapshot | null> {
  try {
    const raw = await fs.readFile(CACHE_FILE, 'utf8');
    const parsed = JSON.parse(raw) as Snapshot;
    const age = Date.now() - new Date(parsed.fetchedAt).getTime();
    return age < CACHE_TTL_MS ? parsed : null;
  } catch {
    return null;
  }
}

async function writeSnapshot(snapshot: Snapshot): Promise<void> {
  await fs.mkdir(path.dirname(CACHE_FILE), { recursive: true });
  await fs.writeFile(CACHE_FILE, JSON.stringify(snapshot, null, 2), 'utf8');
}

const sampleData = {
  categories: [
    { id: 1, name: 'Laptops', slug: 'laptops', parent: 0 },
    { id: 2, name: 'Desktops', slug: 'desktops', parent: 0 },
    { id: 3, name: 'Printers', slug: 'printers', parent: 0 },
    { id: 4, name: 'Smartphones', slug: 'smartphones', parent: 0 },
    { id: 5, name: 'Accessories', slug: 'accessories', parent: 0 }
  ],
  products: [] as Product[]
};

export async function getStoreData(): Promise<{ products: Product[]; categories: WooCategory[] }> {
  const cached = await readSnapshot();
  if (cached) return { products: cached.products, categories: cached.categories };

  if (!hasAuth) return sampleData;

  const [rawProducts, categories] = await Promise.all([
    fetchPaged<any>('products'),
    fetchPaged<WooCategory>('products/categories')
  ]);

  const products = rawProducts.map(normalizeProduct);
  await writeSnapshot({ fetchedAt: new Date().toISOString(), products, categories });
  return { products, categories };
}

export async function getAttributes() {
  if (!hasAuth) return [];
  return fetchPaged<any>('products/attributes');
}
