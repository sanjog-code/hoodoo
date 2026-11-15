export interface Swatch {
  name: string;
  color: string;
  image?: string;
  backImage?: string;
}

export interface Product {
  id: string;
  name: string;
  subtitle?: string;
  quote?: string;
  price: number;
  originalPrice?: number;
  category: 'hoodie' | 'tee' | 'kicks' | 'all';
  image: string;
  backImage?: string;
  thumbnails?: string[];
  swatches?: Swatch[];
  description: string;
  fabricSpecs: string[];
  sizes: string[];
  inStock: boolean;
  featured?: boolean;
  edition?: string;
  model3d?: string;
}

export interface CartItem {
  product: Product;
  selectedSize: string;
  selectedColor: string;
  quantity: number;
}
