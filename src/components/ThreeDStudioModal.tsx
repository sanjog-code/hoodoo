import React, { useEffect, useRef, useState, useMemo } from 'react';
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { X, RotateCw, Camera, Sparkles, Move3d } from 'lucide-react';
import type { Product, Swatch } from '../types';
import { FEATURED_HERO, CATALOG_PRODUCTS } from '../data/products';
import { BrandPalette, PALETTES } from './HoodooLogo';

interface ThreeDStudioModalProps {
  isOpen: boolean;
  onClose: () => void;
  initialProduct: Product;
  initialColor?: string;
  palette?: BrandPalette;
}

export const ThreeDStudioModal: React.FC<ThreeDStudioModalProps> = ({
  isOpen,
  onClose,
  initialProduct,
  initialColor,
  palette = 'silver',
}) => {
  const currentPalette = PALETTES[palette] || PALETTES.silver;
  const mountRef = useRef<HTMLDivElement>(null);
  
  // All products that have 3D models available (Hoodies, Boxy Tees, Skate Sneakers)
  const availableProducts = useMemo(() => {
    const list: Product[] = [];
    if (FEATURED_HERO.model3d) list.push(FEATURED_HERO);
    CATALOG_PRODUCTS.forEach((p) => {
      if (p.model3d && !list.some((item) => item.id === p.id)) {
        list.push(p);
      }
    });
    return list;
  }, []);

  const [activeCategory, setActiveCategory] = useState<'all' | 'hoodie' | 'tee' | 'kicks'>('all');
  const [activeProduct, setActiveProduct] = useState<Product>(initialProduct);
  const [activeColor, setActiveColor] = useState<string>(
    initialColor || initialProduct.swatches?.[0]?.name || 'Standard'
  );
  const [isAutoRotate, setIsAutoRotate] = useState<boolean>(true);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [snapshotTaken, setSnapshotTaken] = useState<boolean>(false);

  // References for live 3D scene manipulation
  const sceneRef = useRef<THREE.Scene | null>(null);
  const cameraRef = useRef<THREE.PerspectiveCamera | null>(null);
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);
  const controlsRef = useRef<OrbitControls | null>(null);
  const currentModelGroupRef = useRef<THREE.Group | null>(null);
  const fabricMeshRef = useRef<THREE.Mesh | null>(null);

  // Sync when initial product opens
  useEffect(() => {
    if (isOpen) {
      setActiveProduct(initialProduct);
      setActiveColor(initialColor || initialProduct.swatches?.[0]?.name || 'Standard');
    }
  }, [isOpen, initialProduct, initialColor]);

  // Main Three.js Scene Setup
  useEffect(() => {
    if (!isOpen || !mountRef.current) return;

    const container = mountRef.current;
    const width = container.clientWidth;
    const height = container.clientHeight;

    // 1. Scene
    const scene = new THREE.Scene();
    sceneRef.current = scene;

    // 2. Camera (50mm telephoto equivalent, FOV 32°)
    const camera = new THREE.PerspectiveCamera(32, width / height, 0.1, 100);
    camera.position.set(0, 0.08, 2.2);
    cameraRef.current = camera;

    // 3. Renderer with ACESFilmic Tone Mapping
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.2;
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    container.innerHTML = '';
    container.appendChild(renderer.domElement);
    rendererRef.current = renderer;

    // 4. OrbitControls
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.minDistance = 1.0;
    controls.maxDistance = 4.0;
    controls.maxPolarAngle = Math.PI / 2 + 0.12;
    controls.target.set(0, -0.05, 0);
    controls.autoRotate = isAutoRotate;
    controls.autoRotateSpeed = 1.8;
    controlsRef.current = controls;

    // 5. Cinematic 4-Light Studio Rig
    // Key Light (Warm 5400K)
    const keyLight = new THREE.DirectionalLight(0xfff6ec, 3.4);
    keyLight.position.set(2.2, 3.0, 2.0);
    keyLight.castShadow = true;
    keyLight.shadow.mapSize.width = 2048;
    keyLight.shadow.mapSize.height = 2048;
    keyLight.shadow.bias = -0.0002;
    scene.add(keyLight);

    // Fill Light (Cool Soft Bounce 7500K)
    const fillLight = new THREE.DirectionalLight(0xdbeafe, 1.3);
    fillLight.position.set(-2.5, 1.5, 1.5);
    scene.add(fillLight);

    // Rim / Kicker Backlight (Contour Separation)
    const rimLight = new THREE.DirectionalLight(0xffffff, 4.2);
    rimLight.position.set(0, 2.8, -2.4);
    scene.add(rimLight);

    // Ground Bounce Ambient
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.85);
    scene.add(ambientLight);

    // Soft Studio Ground Floor with Shadow Contact Falloff
    const floorGeo = new THREE.PlaneGeometry(16, 16);
    const floorMat = new THREE.ShadowMaterial({ opacity: 0.45 });
    const floorMesh = new THREE.Mesh(floorGeo, floorMat);
    floorMesh.rotation.x = -Math.PI / 2;
    floorMesh.position.y = -1.12;
    floorMesh.receiveShadow = true;
    scene.add(floorMesh);

    // Ground Circular Radial Museum Pedestal
    const pedestalGeo = new THREE.CylinderGeometry(0.85, 0.90, 0.03, 64);
    const pedestalMat = new THREE.MeshStandardMaterial({
      color: 0x141416,
      roughness: 0.45,
      metalness: 0.25,
    });
    const pedestal = new THREE.Mesh(pedestalGeo, pedestalMat);
    pedestal.position.y = -1.13;
    pedestal.receiveShadow = true;
    scene.add(pedestal);

    // 6. Animation Loop
    let animationFrameId: number;
    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    };
    animate();

    // 7. Handle Resize
    const handleResize = () => {
      if (!container || !camera || !renderer) return;
      const w = container.clientWidth;
      const h = container.clientHeight;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };
    window.addEventListener('resize', handleResize);

    // 8. 4K Snapshot Hotkey (P)
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'p' || e.key === 'P') {
        take4KSnapshot();
      } else if (e.key === 'Escape') {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);

    return () => {
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('keydown', handleKeyDown);
      cancelAnimationFrame(animationFrameId);
      controls.dispose();
      renderer.dispose();
    };
  }, [isOpen]);

  // Sync Auto-Rotate state
  useEffect(() => {
    if (controlsRef.current) {
      controlsRef.current.autoRotate = isAutoRotate;
    }
  }, [isAutoRotate]);

  // Load / Update 3D Model when activeProduct changes
  useEffect(() => {
    if (!isOpen || !sceneRef.current) return;

    setIsLoading(true);
    const modelPath = activeProduct.model3d || '/assets/models/hoodie_master.glb';
    const isKicks = activeProduct.category === 'kicks' || modelPath.includes('kicks');
    const loader = new GLTFLoader();

    loader.load(
      modelPath,
      (gltf) => {
        // Remove prior model if exists
        if (currentModelGroupRef.current && sceneRef.current) {
          sceneRef.current.remove(currentModelGroupRef.current);
        }

        const model = gltf.scene;
        model.position.set(0, 0, 0);
        model.rotation.y = 0; // Forward facing towards camera at +Z

        if (isKicks) {
          model.scale.set(1.35, 1.35, 1.35);
          if (cameraRef.current && controlsRef.current) {
            cameraRef.current.position.set(0, 0.24, 1.15);
            controlsRef.current.target.set(0, 0.04, 0);
            controlsRef.current.minDistance = 0.5;
            controlsRef.current.maxDistance = 2.5;
            controlsRef.current.update();
          }
        } else {
          model.scale.set(1.15, 1.15, 1.15);
          if (cameraRef.current && controlsRef.current) {
            cameraRef.current.position.set(0, 0.08, 2.2);
            controlsRef.current.target.set(0, -0.05, 0);
            controlsRef.current.minDistance = 0.8;
            controlsRef.current.maxDistance = 4.0;
            controlsRef.current.update();
          }
        }

        // Identify parts
        fabricMeshRef.current = null;

        model.traverse((child) => {
          if ((child as THREE.Mesh).isMesh) {
            const mesh = child as THREE.Mesh;
            mesh.castShadow = true;
            mesh.receiveShadow = true;

            const name = mesh.name.toLowerCase();
            if (
              name.includes('hoodie') ||
              name.includes('tee') ||
              name.includes('sneaker') ||
              name.includes('upper') ||
              name.includes('fabric') ||
              name.includes('body')
            ) {
              fabricMeshRef.current = mesh;
            }
          }
        });

        sceneRef.current?.add(model);
        currentModelGroupRef.current = model;
        setIsLoading(false);

        // Immediately apply active colorway texture atlas
        applyActiveColorway();
      },
      undefined,
      (err) => {
        console.error('Error loading 3D model:', err);
        setIsLoading(false);
      }
    );
  }, [activeProduct.id, isOpen]);

  // Helper to resolve the correct 2048x2048 dual-panel texture atlas
  const getTextureAtlasUrl = (model3dPath: string | undefined, swatchName: string) => {
    let modelKey = 'hero';
    if (model3dPath) {
      const match = model3dPath.match(/(?:hoodie|tee|kicks)_([a-z0-9]+)\.glb/i);
      if (match) {
        modelKey = match[1] === 'master' ? 'hero' : match[1];
      }
    }

    const lower = (swatchName || '').toLowerCase().trim();
    const validSlugs = [
      'asphalt', 'bone', 'white', 'royal', 'blue', 'red', 'crimson',
      'cocoa', 'charcoal', 'tan', 'ash', 'khaki', 'sand', 'rose',
      'sage', 'navy', 'black', 'onyx', 'jet', 'gold', 'carbon',
      'cement', 'obsidian', 'olive', 'indigo', 'maroon', 'ivory',
      'graphite', 'espresso', 'pine', 'slate', 'noir', 'grey',
      'choco', 'moss', 'sail', 'duck'
    ];

    let matchedSlug = '';
    for (const slug of validSlugs) {
      if (lower.includes(slug)) {
        matchedSlug = slug;
        break;
      }
    }
    if (matchedSlug === 'blue' && modelKey !== 'p1') matchedSlug = 'royal';
    if (!matchedSlug) {
      const defaults: Record<string, string> = {
        hero: 'asphalt',
        p1: 'black',
        p2: 'cocoa',
        p3: 'black',
        p4: 'sand',
        p5: 'white',
        p6: 'carbon',
        p7: 'sand',
        p8: 'indigo',
        p9: 'bone',
        p10: 'noir',
        p11: 'choco',
        p12: 'sail',
        p13: 'asphalt',
        p14: 'graphite',
        p15: 'espresso',
        p16: 'obsidian',
      };
      matchedSlug = defaults[modelKey] || 'black';
    }

    return {
      atlasUrl: `/assets/models/textures/tex_${modelKey}_${matchedSlug}.png`,
      fallbackUrl: `/assets/models/textures/tex_${modelKey}.png`,
    };
  };

  // Real-time Dynamic Direct UV Texture Mapping & Dynamic Kicks Material Tinting
  const applyActiveColorway = () => {
    const currentSwatch =
      activeProduct.swatches?.find((s) => s.name === activeColor) ||
      activeProduct.swatches?.[0];

    // DYNAMIC SNEAKER COLORWAY TINTING (Precision multi-material PBR recoloring)
    if (activeProduct.category === 'kicks' || (activeProduct.model3d || '').includes('kicks')) {
      if (!currentModelGroupRef.current) return;

      const KICKS_PALETTES: Record<string, Record<string, { sole: string; upper: string; suede: string; laces: string; silver: string }>> = {
        'wc-cat-9': {
          'Bone & Black Paisley': { sole: '#bd7a40', upper: '#e7e5e4', suede: '#140b06', laces: '#ffffff', silver: '#e8ecf4' },
          'Triple Obsidian': { sole: '#171717', upper: '#121214', suede: '#09090b', laces: '#1c1c1f', silver: '#52525b' },
          'Raw Cocoa & Gum': { sole: '#b86e32', upper: '#5c4033', suede: '#27160c', laces: '#f5f5f4', silver: '#d4af37' },
        },
        'wc-cat-10': {
          'Stealth Noir': { sole: '#1a1a1c', upper: '#121214', suede: '#0a0a0c', laces: '#1c1c1f', silver: '#71717a' },
          'Moonrock Grey': { sole: '#e4e4e7', upper: '#52525b', suede: '#27272a', laces: '#d4d4d8', silver: '#e4e4e7' },
          'Onyx & Bone': { sole: '#bd7a40', upper: '#e7e5e4', suede: '#18181b', laces: '#ffffff', silver: '#e8ecf4' },
        },
        'wc-cat-11': {
          'Chocolate Suede': { sole: '#b86e32', upper: '#52341f', suede: '#26160d', laces: '#f5f5dc', silver: '#e8ecf4' },
          'Jet Suede': { sole: '#1a1a1a', upper: '#1c1917', suede: '#0c0a09', laces: '#262626', silver: '#71717a' },
          'Moss Green Suede': { sole: '#b86e32', upper: '#3f4e42', suede: '#1c261e', laces: '#d1d5db', silver: '#e8ecf4' },
        },
        'wc-cat-12': {
          'Sail & Midnight Paisley': { sole: '#e0d5c1', upper: '#fafaf9', suede: '#1e293b', laces: '#ede8dc', silver: '#e8ecf4' },
          'Obsidian & Crimson': { sole: '#171717', upper: '#18181b', suede: '#881337', laces: '#e11d48', silver: '#e8ecf4' },
          'Khaki & Brown': { sole: '#bd7a40', upper: '#d6d3d1', suede: '#451a03', laces: '#e7e5e4', silver: '#e8ecf4' },
        },
        'wc-cat-16': {
          'Obsidian Canvas': { sole: '#b86e32', upper: '#18181b', suede: '#09090b', laces: '#ffffff', silver: '#e8ecf4' },
          'Off-White Raw Duck': { sole: '#b86e32', upper: '#f5f5f4', suede: '#d6d3d1', laces: '#fafaf9', silver: '#e8ecf4' },
          'Navy Blue Heavyweight': { sole: '#b86e32', upper: '#1e3a8a', suede: '#0f172a', laces: '#ffffff', silver: '#e8ecf4' },
        },
      };

      const prodPalettes = KICKS_PALETTES[activeProduct.id];
      const palette = (prodPalettes && currentSwatch?.name && prodPalettes[currentSwatch.name]) || {
        sole: '#bd7a40',
        upper: currentSwatch?.color || '#e7e5e4',
        suede: '#140b06',
        laces: '#ffffff',
        silver: '#e8ecf4',
      };

      currentModelGroupRef.current.traverse((child) => {
        if ((child as THREE.Mesh).isMesh) {
          const mesh = child as THREE.Mesh;
          const materials = Array.isArray(mesh.material) ? mesh.material : [mesh.material];
          materials.forEach((m) => {
            const stdMat = m as THREE.MeshStandardMaterial;
            if (!stdMat || !stdMat.name) return;
            const matName = stdMat.name;
            if (matName.includes('Sole')) {
              stdMat.color.set(palette.sole);
            } else if (matName.includes('Upper')) {
              stdMat.color.set(palette.upper);
            } else if (matName.includes('Suede')) {
              stdMat.color.set(palette.suede);
            } else if (matName.includes('Laces')) {
              stdMat.color.set(palette.laces);
            } else if (matName.includes('Chrome')) {
              stdMat.color.set(palette.silver);
            }
            stdMat.needsUpdate = true;
          });
        }
      });
      return;
    }

    if (!fabricMeshRef.current) return;

    const mat = fabricMeshRef.current.material as THREE.MeshStandardMaterial;
    if (!mat) return;

    const { atlasUrl, fallbackUrl } = getTextureAtlasUrl(
      activeProduct.model3d,
      currentSwatch?.name || activeColor
    );

    const textureLoader = new THREE.TextureLoader();
    textureLoader.load(
      atlasUrl,
      (tex) => {
        tex.colorSpace = THREE.SRGBColorSpace;
        tex.flipY = false;
        mat.map = tex;
        mat.color.set(0xffffff); // Keep true uncompressed texture colors
        mat.roughness = 0.90;
        mat.metalness = 0.04;
        mat.needsUpdate = true;
      },
      undefined,
      () => {
        // Fallback to base model texture atlas
        textureLoader.load(fallbackUrl, (tex) => {
          tex.colorSpace = THREE.SRGBColorSpace;
          tex.flipY = false;
          mat.map = tex;
          mat.color.set(0xffffff);
          mat.roughness = 0.90;
          mat.metalness = 0.04;
          mat.needsUpdate = true;
        });
      }
    );
  };

  // Re-apply whenever activeColor changes
  useEffect(() => {
    applyActiveColorway();
  }, [activeColor]);

  // Camera preset buttons
  const setCameraPreset = (view: 'front' | 'back' | 'angle' | 'close') => {
    if (!cameraRef.current || !controlsRef.current) return;
    setIsAutoRotate(false);
    const cam = cameraRef.current;
    const ctrl = controlsRef.current;
    const isKicks = activeProduct.category === 'kicks' || (activeProduct.model3d || '').includes('kicks');

    if (isKicks) {
      if (view === 'front') {
        cam.position.set(0, 0.22, 1.10);
        ctrl.target.set(0, 0.04, 0);
      } else if (view === 'back') {
        cam.position.set(0, 0.22, -1.10);
        ctrl.target.set(0, 0.04, 0);
      } else if (view === 'angle') {
        cam.position.set(0.85, 0.35, 0.85);
        ctrl.target.set(0, 0.04, 0);
      } else if (view === 'close') {
        cam.position.set(0, 0.15, 0.65);
        ctrl.target.set(0, 0.04, 0);
      }
    } else {
      if (view === 'front') {
        cam.position.set(0, 0.08, 2.2);
        ctrl.target.set(0, -0.05, 0);
      } else if (view === 'back') {
        cam.position.set(0, 0.08, -2.2);
        ctrl.target.set(0, -0.05, 0);
      } else if (view === 'angle') {
        cam.position.set(1.4, 0.30, 1.6);
        ctrl.target.set(0, -0.05, 0);
      } else if (view === 'close') {
        cam.position.set(0, 0.20, 1.20);
        ctrl.target.set(0, 0.14, 0);
      }
    }
    ctrl.update();
  };

  // 4K Snapshot Export (Hotkey P / Button)
  const take4KSnapshot = () => {
    if (!rendererRef.current || !sceneRef.current || !cameraRef.current) return;
    const renderer = rendererRef.current;
    const scene = sceneRef.current;
    const camera = cameraRef.current;

    const origWidth = renderer.domElement.width;
    const origHeight = renderer.domElement.height;
    renderer.setSize(3840, 2160, false);
    camera.aspect = 3840 / 2160;
    camera.updateProjectionMatrix();

    renderer.render(scene, camera);
    const dataURL = renderer.domElement.toDataURL('image/png');

    const link = document.createElement('a');
    link.download = `HOODOO_3D_${activeProduct.name.replace(/\s+/g, '_')}_${activeColor}.png`;
    link.href = dataURL;
    link.click();

    renderer.setSize(origWidth, origHeight, false);
    camera.aspect = origWidth / origHeight;
    camera.updateProjectionMatrix();

    setSnapshotTaken(true);
    setTimeout(() => setSnapshotTaken(false), 2500);
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/95 backdrop-blur-xl animate-fadeIn">
      {/* 3D WebGL Canvas Viewport */}
      <div ref={mountRef} className="absolute inset-0 w-full h-full cursor-grab active:cursor-grabbing select-none" />

      {/* Top Header Floating Dock */}
      <div className="absolute top-0 left-0 right-0 p-6 flex items-center justify-between pointer-events-none z-20">
        <div className="flex items-center gap-3">
          <div className={`w-9 h-9 rounded-xl ${currentPalette.studioAccentClass} flex items-center justify-center`}>
            <Move3d className="w-5 h-5" />
          </div>
          <div>
            <div className={`text-[10px] font-mono font-bold uppercase tracking-widest ${currentPalette.badgeText}`}>
              3D ATELIER VIEWPORT · 360° INSPECTION
            </div>
            <h2 className="text-sm sm:text-base font-extrabold tracking-tight text-white uppercase font-sans">
              {activeProduct.name}
            </h2>
          </div>
        </div>

        {/* Exit & Snapshot actions */}
        <div className="flex items-center gap-3 pointer-events-auto">
          <button
            onClick={take4KSnapshot}
            aria-label="Export 4K render frame"
            className="hidden sm:flex items-center gap-2 px-3.5 py-2 rounded-full bg-neutral-900/80 hover:bg-neutral-800 text-white text-xs font-mono font-bold tracking-wider border border-neutral-700/60 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400"
            title="Export Frame (Hotkey: P)"
          >
            <Camera className={`w-3.5 h-3.5 ${currentPalette.badgeText}`} />
            <span>EXPORT FRAME (P)</span>
          </button>

          <button
            onClick={onClose}
            aria-label="Close 3D View Space"
            className="p-2.5 rounded-full bg-neutral-900/90 hover:bg-neutral-800 text-white border border-neutral-700 transition-transform active:scale-95 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400"
          >
            <X className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* Left Dock: Switch Product Design */}
      <div className="absolute left-6 top-24 bottom-28 hidden md:flex flex-col justify-center gap-2 pointer-events-auto z-20 max-w-[220px]">
        <div className="flex items-center justify-between px-2 mb-1">
          <span className="text-[10px] font-mono font-bold text-neutral-400 uppercase tracking-widest">
            COLLECTION ARCHIVE
          </span>
        </div>

        {/* Category Filter Pills */}
        <div className="flex items-center gap-1 p-1 bg-neutral-950/80 border border-neutral-800 rounded-xl mb-1">
          {(['all', 'hoodie', 'tee', 'kicks'] as const).map((cat) => (
            <button
              key={cat}
              onClick={() => setActiveCategory(cat)}
              aria-label={`Filter by ${cat}`}
              className={`flex-1 py-1 text-[9px] font-mono font-bold uppercase rounded-lg transition-all focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-neutral-400 ${
                activeCategory === cat
                  ? `${currentPalette.buttonClass} text-white`
                  : 'text-neutral-400 hover:text-white'
              }`}
            >
              {cat === 'hoodie' ? 'hoodies' : cat === 'tee' ? 'tees' : cat}
            </button>
          ))}
        </div>

        <div className="space-y-1.5 overflow-y-auto pr-1 max-h-[55vh] scrollbar-none">
          {availableProducts
            .filter((p) => activeCategory === 'all' || p.category === activeCategory)
            .map((item) => {
              const isCur = activeProduct.id === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => {
                    setActiveProduct(item);
                    setActiveColor(item.swatches?.[0]?.name || 'Standard');
                  }}
                  aria-label={`View ${item.name}`}
                  className={`w-full text-left p-2.5 rounded-xl text-[11px] font-mono transition-all border focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400 ${
                    isCur
                      ? `bg-neutral-850 text-white ring-2 ${currentPalette.ringClass} border-transparent shadow-lg`
                      : 'bg-neutral-950/60 text-neutral-400 border-neutral-800 hover:text-white hover:border-neutral-700'
                  }`}
                >
                  <div className="font-bold truncate">{item.name}</div>
                  <div className="text-[9px] text-neutral-500 mt-0.5"><span className="tabular-nums">${item.price}</span> USD · <span className="uppercase">{item.category}</span></div>
                </button>
              );
            })}
        </div>
      </div>

      {/* Right Dock: Camera Presets & Auto-Rotate */}
      <div className="absolute right-6 top-24 flex flex-col gap-2 pointer-events-auto z-20">
        <button
          onClick={() => setIsAutoRotate((prev) => !prev)}
          aria-label="Toggle Auto-Rotate"
          className={`flex items-center gap-2 px-3 py-2 rounded-full text-xs font-mono font-bold tracking-wider border backdrop-blur-md transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400 ${
            isAutoRotate
              ? `${currentPalette.buttonClass} border-transparent`
              : 'bg-neutral-900/80 text-neutral-400 border-neutral-700 hover:text-white'
          }`}
          title="Toggle Auto-Rotate"
        >
          <RotateCw className={`w-3.5 h-3.5 ${isAutoRotate ? 'animate-spin' : ''}`} />
          <span>{isAutoRotate ? 'AUTOROTATE ON' : 'AUTOROTATE OFF'}</span>
        </button>

        <div className="flex flex-col gap-1 p-1 bg-neutral-950/80 border border-neutral-800 rounded-2xl backdrop-blur-md">
          {[
            { id: 'front', label: 'FRONT' },
            { id: 'angle', label: '45° ANGLE' },
            { id: 'back', label: 'BACK' },
            { id: 'close', label: 'CLOSE-UP' },
          ].map((preset) => (
            <button
              key={preset.id}
              onClick={() => setCameraPreset(preset.id as any)}
              aria-label={`Camera view ${preset.label}`}
              className="px-3 py-1.5 text-[10px] font-mono font-bold uppercase rounded-lg text-neutral-400 hover:text-white hover:bg-neutral-800 transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-neutral-400"
            >
              {preset.label}
            </button>
          ))}
        </div>
      </div>

      {/* Bottom Floating Control Dock: Real-Time Colorway Switching */}
      <div className="absolute bottom-6 left-1/2 -translate-x-1/2 flex flex-col items-center gap-3 pointer-events-auto z-20 max-w-lg w-full px-4">
        
        {/* Colorway Pill Selector: Real-Time 3D Color Change */}
        <div className="flex items-center gap-3 px-5 py-3 rounded-full bg-neutral-950/90 border border-neutral-800 shadow-2xl backdrop-blur-xl">
          <div className="text-[10px] font-mono font-bold text-neutral-400 uppercase tracking-widest flex items-center gap-1.5 mr-1">
            <Sparkles className={`w-3.5 h-3.5 ${currentPalette.badgeText}`} />
            <span>COLORWAY:</span>
          </div>

          <div className="flex items-center gap-2">
            {activeProduct.swatches?.map((swatch: Swatch) => {
              const isSelected = activeColor === swatch.name;
              return (
                <button
                  key={swatch.name}
                  onClick={() => setActiveColor(swatch.name)}
                  className={`group relative p-1 rounded-full transition-transform focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400 ${
                    isSelected ? `scale-125 ring-2 ${currentPalette.ringClass} shadow-lg` : 'opacity-70 hover:opacity-100 hover:scale-110'
                  }`}
                  title={`Apply ${swatch.name} in 3D`}
                  aria-label={`Select ${swatch.name}`}
                >
                  <div
                    className="w-6 h-6 rounded-full border border-neutral-600 shadow-inner"
                    style={{ backgroundColor: swatch.color }}
                  />
                  {isSelected && (
                    <span className="absolute -top-7 left-1/2 -translate-x-1/2 px-2 py-0.5 rounded bg-neutral-900 border border-neutral-700 text-white text-[9px] font-mono font-bold whitespace-nowrap shadow-md pointer-events-none">
                      {swatch.name}
                    </span>
                  )}
                </button>
              );
            })}
          </div>
        </div>

        {/* Orbit Hint */}
        <span className="text-[10px] font-mono text-neutral-500 uppercase tracking-widest">
          DRAG TO ORBIT 360° • SCROLL TO ZOOM • SHIFT+DRAG TO PAN
        </span>
      </div>

      {/* Loading Overlay */}
      {isLoading && (
        <div className="absolute inset-0 flex flex-col items-center justify-center bg-black/80 z-30">
          <div className="w-12 h-12 rounded-full border-2 border-neutral-400 border-t-transparent animate-spin mb-3" />
          <span className={`text-xs font-mono font-bold ${currentPalette.badgeText} uppercase tracking-widest`}>
            LOADING 3D ATELIER GARMENT...
          </span>
        </div>
      )}

      {/* Frame Snapshot Notification */}
      {snapshotTaken && (
        <div className={`absolute top-20 left-1/2 -translate-x-1/2 px-4 py-2 rounded-full ${currentPalette.buttonClass} text-xs font-mono font-bold uppercase tracking-widest shadow-2xl z-40 transition-opacity`}>
          FRAME SAVED TO DOWNLOADS
        </div>
      )}
    </div>
  );
};
