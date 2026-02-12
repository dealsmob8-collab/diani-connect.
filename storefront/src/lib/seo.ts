export type SeoProps = {
  title: string;
  description: string;
  canonicalPath: string;
  image?: string;
  type?: 'website' | 'product';
};

export function buildCanonical(pathname: string): string {
  const base = 'https://sesicthub.co.ke';
  return new URL(pathname, base).toString();
}

export function productJsonLd(product: {
  name: string;
  description: string;
  image: string;
  url: string;
  price: string;
  stockStatus: string;
}) {
  return {
    '@context': 'https://schema.org',
    '@type': 'Product',
    name: product.name,
    description: product.description,
    image: [product.image],
    offers: {
      '@type': 'Offer',
      priceCurrency: 'KES',
      price: product.price,
      availability:
        product.stockStatus === 'instock'
          ? 'https://schema.org/InStock'
          : 'https://schema.org/OutOfStock',
      url: product.url
    }
  };
}
