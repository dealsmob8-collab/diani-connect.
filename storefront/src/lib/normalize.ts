export type ProductAttribute = {
  name: string;
  slug?: string;
  options: string[];
};

export type ProductImage = {
  src: string;
  alt: string;
};

export type Product = {
  id: number;
  name: string;
  slug: string;
  permalink: string;
  description: string;
  shortDescription: string;
  regularPrice: number | null;
  salePrice: number | null;
  displayPrice: number | null;
  onSale: boolean;
  priceLabel: string;
  stockStatus: 'instock' | 'outofstock' | 'onbackorder';
  stockQuantity: number | null;
  images: ProductImage[];
  categories: { id: number; name: string; slug: string }[];
  attributes: ProductAttribute[];
  featured: boolean;
  dateCreated: string;
};

const currencyFormatter = new Intl.NumberFormat('en-KE', {
  style: 'currency',
  currency: 'KES',
  maximumFractionDigits: 0
});

export const formatKES = (value: number | null): string => {
  if (value === null || Number.isNaN(value)) return 'Contact for price';
  return currencyFormatter.format(value);
};

const parsePrice = (price?: string): number | null => {
  if (!price) return null;
  const parsed = Number(price);
  return Number.isFinite(parsed) ? parsed : null;
};

export const normalizeProduct = (raw: any): Product => {
  const regularPrice = parsePrice(raw.regular_price);
  const salePrice = parsePrice(raw.sale_price);
  const currentPrice = parsePrice(raw.price);

  return {
    id: raw.id,
    name: raw.name,
    slug: raw.slug,
    permalink: raw.permalink,
    description: raw.description ?? '',
    shortDescription: raw.short_description ?? '',
    regularPrice,
    salePrice,
    displayPrice: currentPrice,
    onSale: Boolean(raw.on_sale),
    priceLabel: formatKES(currentPrice),
    stockStatus: raw.stock_status ?? 'outofstock',
    stockQuantity: raw.stock_quantity ?? null,
    images: (raw.images ?? []).map((image: any) => ({
      src: image.src,
      alt: image.alt || raw.name
    })),
    categories: (raw.categories ?? []).map((category: any) => ({
      id: category.id,
      name: category.name,
      slug: category.slug
    })),
    attributes: (raw.attributes ?? []).map((attribute: any) => ({
      name: attribute.name,
      slug: attribute.slug,
      options: attribute.options ?? []
    })),
    featured: Boolean(raw.featured),
    dateCreated: raw.date_created
  };
};

export const attributeValue = (product: Product, keywords: string[]): string | null => {
  const lowered = keywords.map((keyword) => keyword.toLowerCase());
  const match = product.attributes.find((attribute) =>
    lowered.some((keyword) => attribute.name.toLowerCase().includes(keyword))
  );

  if (!match || match.options.length === 0) return null;
  return match.options.join(', ');
};
