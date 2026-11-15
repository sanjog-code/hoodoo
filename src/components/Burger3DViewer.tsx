import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { RotateCw, Layers, Sparkles, ZoomIn, Eye } from 'lucide-react';

interface Burger3DViewerProps {
  scrollProgress?: number; // 0.0 to 1.0 from parent scroll
  exploded?: boolean;
  onLayerHover?: (layerName: string | null) => void;
  className?: string;
}

export const Burger3DViewer: React.FC<Burger3DViewerProps> = ({
  scrollProgress = 0,
  exploded: externalExploded = false,
  onLayerHover,
  className = '',
}) => {
  const mountRef = useRef<HTMLDivElement>(null);
  const [internalExploded, setInternalExploded] = useState<boolean>(false);
  const [isRotating, setIsRotating] = useState<boolean>(true);
  const [activeLayerInfo, setActiveLayerInfo] = useState<string | null>(null);
  const [modelLoaded, setModelLoaded] = useState<boolean>(false);
  const [steamActive, setSteamActive] = useState<boolean>(true);

  // References for Three.js state
  const sceneRef = useRef<THREE.Scene | null>(null);
  const cameraRef = useRef<THREE.PerspectiveCamera | null>(null);
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);
  const burgerGroupRef = useRef<THREE.Group | null>(null);
  const layersMapRef = useRef<{ [key: string]: THREE.Object3D }>({});
  const particlesRef = useRef<THREE.Points | null>(null);

  const isExploded = externalExploded || internalExploded;

  useEffect(() => {
    const container = mountRef.current;
    if (!container) return;

    // 1. Scene Setup
    const scene = new THREE.Scene();
    sceneRef.current = scene;

    // 2. Camera Setup (50mm virtual lens, high focal sharpness)
    const initialWidth = container.clientWidth || 600;
    const initialHeight = container.clientHeight || 500;

    const camera = new THREE.PerspectiveCamera(
      36,
      initialWidth / initialHeight,
      0.1,
      100
    );
    camera.position.set(0, 0.4, 5.0);
    cameraRef.current = camera;

    // 3. 4K-Grade WebGL Renderer (with robust fallback for headless/CI)
    let renderer: THREE.WebGLRenderer;
    try {
      renderer = new THREE.WebGLRenderer({
        antialias: true,
        alpha: true,
        powerPreference: 'high-performance',
      });
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2.5));
      renderer.setSize(initialWidth, initialHeight);
      renderer.shadowMap.enabled = true;
      renderer.shadowMap.type = THREE.PCFSoftShadowMap;
      renderer.toneMapping = THREE.ACESFilmicToneMapping;
      renderer.toneMappingExposure = 1.25;
      container.appendChild(renderer.domElement);
      rendererRef.current = renderer;
    } catch (e) {
      console.warn('WebGL initialization failed, creating fallback canvas', e);
      const fallbackCanvas = document.createElement('canvas');
      fallbackCanvas.width = initialWidth;
      fallbackCanvas.height = initialHeight;
      container.appendChild(fallbackCanvas);
      return;
    }

    // 4. Studio Chiaroscuro Lighting (Warm Key + Cool Cyberpunk Rim)
    const ambientLight = new THREE.AmbientLight(0xfff7ed, 1.2);
    scene.add(ambientLight);

    // Key Light (Golden Griddle Glow)
    const keyLight = new THREE.DirectionalLight(0xffb84d, 3.2);
    keyLight.position.set(4, 5, 4);
    keyLight.castShadow = true;
    keyLight.shadow.mapSize.width = 2048;
    keyLight.shadow.mapSize.height = 2048;
    keyLight.shadow.bias = -0.0001;
    scene.add(keyLight);

    // Rim Light 1 (Electric Ultraviolet/Pink Edge Separation)
    const rimLightPink = new THREE.DirectionalLight(0xff007f, 2.4);
    rimLightPink.position.set(-4, 3, -4);
    scene.add(rimLightPink);

    // Rim Light 2 (Neon Lime Edge)
    const rimLightLime = new THREE.DirectionalLight(0xa3e635, 1.8);
    rimLightLime.position.set(3, -2, -3);
    scene.add(rimLightLime);

    // Top Soft Spotlight
    const spotLight = new THREE.SpotLight(0xffedd5, 2.0, 15, Math.PI / 4, 0.3);
    spotLight.position.set(0, 6, 2);
    scene.add(spotLight);

    // 5. Contact Shadow Plane
    const shadowGeo = new THREE.PlaneGeometry(6, 6);
    const shadowMat = new THREE.ShadowMaterial({ opacity: 0.45 });
    const shadowPlane = new THREE.Mesh(shadowGeo, shadowMat);
    shadowPlane.rotation.x = -Math.PI / 2;
    shadowPlane.position.y = -1.2;
    shadowPlane.receiveShadow = true;
    scene.add(shadowPlane);

    // 6. Master Burger Group
    const burgerGroup = new THREE.Group();
    burgerGroup.position.set(0, -0.1, 0);
    scene.add(burgerGroup);
    burgerGroupRef.current = burgerGroup;

    // 7. Sizzle Steam Particle System
    const particleCount = 60;
    const particleGeo = new THREE.BufferGeometry();
    const particlePositions = new Float32Array(particleCount * 3);
    const particleSpeeds = new Float32Array(particleCount);

    for (let i = 0; i < particleCount; i++) {
      particlePositions[i * 3] = (Math.random() - 0.5) * 1.4;
      particlePositions[i * 3 + 1] = (Math.random() - 0.5) * 0.3;
      particlePositions[i * 3 + 2] = (Math.random() - 0.5) * 1.4;
      particleSpeeds[i] = 0.005 + Math.random() * 0.01;
    }
    particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));

    const particleMat = new THREE.PointsMaterial({
      color: 0xffedd5,
      size: 0.06,
      transparent: true,
      opacity: 0.35,
      blending: THREE.AdditiveBlending,
    });
    const steamParticles = new THREE.Points(particleGeo, particleMat);
    burgerGroup.add(steamParticles);
    particlesRef.current = steamParticles;

    // 8. Load Blender 4K GLTF Model with Fallback Procedural Assembly
    const loader = new GLTFLoader();
    loader.load(
      '/assets/models/krunch_burger_4k.glb',
      (gltf) => {
        const loadedModel = gltf.scene;
        loadedModel.traverse((child) => {
          if ((child as THREE.Mesh).isMesh) {
            const mesh = child as THREE.Mesh;
            mesh.castShadow = true;
            mesh.receiveShadow = true;

            // Map layers for exploded view
            const name = mesh.name.toLowerCase();
            if (name.includes('topbun') || name.includes('sphere')) {
              layersMapRef.current['topBun'] = mesh;
            } else if (name.includes('cucumber')) {
              layersMapRef.current['cucumber'] = mesh;
            } else if (name.includes('tomato')) {
              layersMapRef.current['tomato'] = mesh;
            } else if (name.includes('cheese') || name.includes('plane')) {
              layersMapRef.current['cheese'] = mesh;
            } else if (name.includes('patty')) {
              layersMapRef.current['patty'] = mesh;
            } else if (name.includes('bottombun')) {
              layersMapRef.current['bottomBun'] = mesh;
            }
          }
        });

        // Center and scale model
        loadedModel.scale.set(1.2, 1.2, 1.2);
        burgerGroup.add(loadedModel);
        setModelLoaded(true);
      },
      undefined,
      (err) => {
        console.warn('GLB load error, using high-fidelity procedural burger', err);
        buildProceduralBurger(burgerGroup, layersMapRef.current);
        setModelLoaded(true);
      }
    );

    // 9. Procedural Burger Fallback Generator (Guarantees zero blank screen)
    function buildProceduralBurger(
      parent: THREE.Group,
      layerMap: { [key: string]: THREE.Object3D }
    ) {
      // Materials
      const bunMat = new THREE.MeshPhysicalMaterial({
        color: 0xd97706,
        roughness: 0.38,
        clearcoat: 0.35,
        clearcoatRoughness: 0.2,
      });

      const sesameMat = new THREE.MeshStandardMaterial({
        color: 0xfef3c7,
        roughness: 0.3,
      });

      const cucumberMat = new THREE.MeshPhysicalMaterial({
        color: 0x16a34a,
        roughness: 0.2,
        transmission: 0.4,
        transparent: true,
        opacity: 0.95,
      });

      const tomatoMat = new THREE.MeshPhysicalMaterial({
        color: 0xdc2626,
        roughness: 0.15,
        clearcoat: 0.6,
      });

      const cheeseMat = new THREE.MeshPhysicalMaterial({
        color: 0xf59e0b,
        roughness: 0.3,
        clearcoat: 0.25,
      });

      const pattyMat = new THREE.MeshStandardMaterial({
        color: 0x3f2214,
        roughness: 0.85,
        metalness: 0.1,
      });

      // Top Bun
      const topBunGeo = new THREE.SphereGeometry(1.2, 32, 24, 0, Math.PI * 2, 0, Math.PI / 2);
      const topBun = new THREE.Mesh(topBunGeo, bunMat);
      topBun.scale.set(1.15, 0.65, 1.15);
      topBun.position.y = 0.55;
      topBun.castShadow = true;
      parent.add(topBun);
      layerMap['topBun'] = topBun;

      // Sesame seeds instanced on top bun
      const seedGeo = new THREE.SphereGeometry(0.035, 8, 6);
      seedGeo.scale(0.8, 1.6, 0.4);
      const seedCount = 90;
      const seedMesh = new THREE.InstancedMesh(seedGeo, sesameMat, seedCount);
      const dummy = new THREE.Object3D();
      for (let i = 0; i < seedCount; i++) {
        const phi = Math.random() * 0.85 + 0.15;
        const theta = Math.random() * Math.PI * 2;
        const r = 1.25 * Math.sin(phi);
        dummy.position.set(r * Math.cos(theta), 0.55 + 0.78 * Math.cos(phi), r * Math.sin(theta));
        dummy.rotation.set(Math.random() * 0.4, theta, Math.random() * 0.4);
        dummy.updateMatrix();
        seedMesh.setMatrixAt(i, dummy.matrix);
      }
      seedMesh.instanceMatrix.needsUpdate = true;
      topBun.add(seedMesh);

      // Cucumber / Pickle Slices
      const cucGroup = new THREE.Group();
      cucGroup.position.y = 0.38;
      const cucPositions = [
        [-0.45, 0.25, 0.1],
        [0.45, 0.28, -0.1],
        [-0.15, -0.45, 0.15],
        [0.35, -0.38, -0.15],
      ];
      cucPositions.forEach(([x, z, rz]) => {
        const cGeo = new THREE.CylinderGeometry(0.42, 0.42, 0.05, 24);
        const cMesh = new THREE.Mesh(cGeo, cucumberMat);
        cMesh.position.set(x, 0, z);
        cMesh.rotation.set(0.05, 0, rz);
        cMesh.castShadow = true;
        cucGroup.add(cMesh);
      });
      parent.add(cucGroup);
      layerMap['cucumber'] = cucGroup;

      // Tomato Slices
      const tomGroup = new THREE.Group();
      tomGroup.position.y = 0.24;
      const tom1 = new THREE.Mesh(new THREE.CylinderGeometry(0.58, 0.58, 0.09, 32), tomatoMat);
      tom1.position.set(-0.35, 0, 0);
      tom1.rotation.set(0.04, 0, 0.05);
      tom1.castShadow = true;
      tomGroup.add(tom1);

      const tom2 = new THREE.Mesh(new THREE.CylinderGeometry(0.58, 0.58, 0.09, 32), tomatoMat);
      tom2.position.set(0.35, 0.02, 0);
      tom2.rotation.set(-0.04, 0, -0.05);
      tom2.castShadow = true;
      tomGroup.add(tom2);
      parent.add(tomGroup);
      layerMap['tomato'] = tomGroup;

      // Melted Cheddar
      const cheeseGeo = new THREE.BoxGeometry(1.6, 0.04, 1.6);
      const cheese = new THREE.Mesh(cheeseGeo, cheeseMat);
      cheese.position.y = 0.12;
      cheese.rotation.y = Math.PI / 4;
      cheese.castShadow = true;
      parent.add(cheese);
      layerMap['cheese'] = cheese;

      // Smash Beef Patty
      const pattyGeo = new THREE.CylinderGeometry(1.25, 1.25, 0.28, 36);
      const patty = new THREE.Mesh(pattyGeo, pattyMat);
      patty.position.y = -0.06;
      patty.castShadow = true;
      parent.add(patty);
      layerMap['patty'] = patty;

      // Bottom Bun
      const bottomBunGeo = new THREE.CylinderGeometry(1.2, 1.15, 0.34, 32);
      const bottomBun = new THREE.Mesh(bottomBunGeo, bunMat);
      bottomBun.position.y = -0.38;
      bottomBun.castShadow = true;
      parent.add(bottomBun);
      layerMap['bottomBun'] = bottomBun;
    }

    // 10. Mouse Interaction / Inertial Dragging
    let isDragging = false;
    let prevMouseX = 0;
    let prevMouseY = 0;
    let targetRotY = 0;
    let targetRotX = 0;

    const onMouseDown = (e: MouseEvent) => {
      isDragging = true;
      prevMouseX = e.clientX;
      prevMouseY = e.clientY;
      setIsRotating(false);
    };

    const onMouseMove = (e: MouseEvent) => {
      if (!isDragging) return;
      const deltaX = e.clientX - prevMouseX;
      const deltaY = e.clientY - prevMouseY;
      prevMouseX = e.clientX;
      prevMouseY = e.clientY;

      targetRotY += deltaX * 0.008;
      targetRotX = Math.max(-0.5, Math.min(0.5, targetRotX + deltaY * 0.005));
    };

    const onMouseUp = () => {
      isDragging = false;
    };

    const domElement = renderer.domElement;
    domElement.addEventListener('mousedown', onMouseDown);
    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);

    // 11. Animation Render Loop
    let animationFrameId: number;
    const clock = new THREE.Clock();

    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);
      const delta = clock.getDelta();
      const time = clock.getElapsedTime();

      // Smooth scroll rotation interpolation
      if (burgerGroupRef.current) {
        // Base auto-spin or scroll rotation
        const scrollRotation = scrollProgress * Math.PI * 4; // Multiple 360 spins down page
        const spinSpeed = isRotating ? 0.3 * delta : 0;
        targetRotY += spinSpeed;

        burgerGroupRef.current.rotation.y += (targetRotY + scrollRotation - burgerGroupRef.current.rotation.y) * 0.08;
        burgerGroupRef.current.rotation.x += (targetRotX - burgerGroupRef.current.rotation.x) * 0.08;
        
        // Gentle organic floating hover
        burgerGroupRef.current.position.y = -0.1 + Math.sin(time * 1.8) * 0.05;
      }

      // Sizzle Steam particle animation
      if (particlesRef.current && steamActive) {
        const positions = particlesRef.current.geometry.attributes.position.array as Float32Array;
        for (let i = 0; i < particleCount; i++) {
          positions[i * 3 + 1] += particleSpeeds[i];
          if (positions[i * 3 + 1] > 1.2) {
            positions[i * 3 + 1] = -0.1;
            positions[i * 3] = (Math.random() - 0.5) * 1.4;
            positions[i * 3 + 2] = (Math.random() - 0.5) * 1.4;
          }
        }
        particlesRef.current.geometry.attributes.position.needsUpdate = true;
      }

      // Exploded Layer Animation (Smooth lerp)
      const layers = layersMapRef.current;
      const targetOffsets = isExploded
        ? {
            topBun: 1.1,
            cucumber: 0.65,
            tomato: 0.3,
            cheese: 0.0,
            patty: -0.35,
            bottomBun: -0.85,
          }
        : {
            topBun: 0.55,
            cucumber: 0.38,
            tomato: 0.24,
            cheese: 0.12,
            patty: -0.06,
            bottomBun: -0.38,
          };

      Object.entries(targetOffsets).forEach(([key, targetY]) => {
        if (layers[key]) {
          layers[key].position.y += (targetY - layers[key].position.y) * 0.1;
        }
      });

      renderer.render(scene, camera);
    };

    animate();

    // 12. Responsive Resize
    const handleResize = () => {
      if (!container || !camera || !renderer) return;
      camera.aspect = container.clientWidth / container.clientHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(container.clientWidth, container.clientHeight);
    };

    window.addEventListener('resize', handleResize);

    // Cleanup
    return () => {
      cancelAnimationFrame(animationFrameId);
      domElement.removeEventListener('mousedown', onMouseDown);
      window.removeEventListener('mousemove', onMouseMove);
      window.removeEventListener('mouseup', onMouseUp);
      window.removeEventListener('resize', handleResize);
      renderer.dispose();
      if (container.contains(renderer.domElement)) {
        container.removeChild(renderer.domElement);
      }
    };
  }, [scrollProgress, isExploded, isRotating, steamActive]);

  return (
    <div className={`relative w-full h-full min-h-[480px] lg:min-h-[640px] flex items-center justify-center select-none ${className}`}>
      
      {/* Three.js Canvas Container */}
      <div
        ref={mountRef}
        className="w-full h-full cursor-grab active:cursor-grabbing relative"
      />

      {/* Floating 4K Telemetry Badge */}
      <div className="absolute top-4 left-4 z-20 flex flex-col gap-1 pointer-events-none">
        <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-neutral-950/80 backdrop-blur-md border border-amber-500/30 text-[11px] font-mono text-amber-300">
          <span className="w-2 h-2 rounded-full bg-amber-400 animate-ping" />
          <span>4K PBR RENDER // 120 FPS BUFFER</span>
        </div>
        <div className="text-[10px] font-mono text-neutral-400 pl-2">
          PATTIES: 44 FARMS TX • 475°F SEAR
        </div>
      </div>

      {/* Floating Interactive Controls */}
      <div className="absolute bottom-6 right-6 z-20 flex items-center gap-2 bg-neutral-950/90 backdrop-blur-md p-1.5 rounded-xl border border-neutral-800 shadow-2xl">
        {/* Toggle Exploded View */}
        <button
          onClick={() => {
            setInternalExploded(!internalExploded);
            setActiveLayerInfo(internalExploded ? null : 'Exploded View: Inspecting layers');
          }}
          className={`flex items-center gap-1.5 px-3 py-2 rounded-lg text-xs font-mono font-bold transition-all active:translate-y-[1px] ${
            isExploded
              ? 'bg-amber-500 text-neutral-950 shadow-md shadow-amber-500/20'
              : 'text-neutral-300 hover:text-white hover:bg-neutral-800'
          }`}
          title="Explode Burger Layers"
        >
          <Layers className="w-3.5 h-3.5" />
          <span>{isExploded ? 'ASSEMBLE' : 'EXPLODE'}</span>
        </button>

        {/* Toggle Auto Spin */}
        <button
          onClick={() => setIsRotating(!isRotating)}
          className={`p-2 rounded-lg text-xs font-mono transition-all active:translate-y-[1px] ${
            isRotating
              ? 'bg-neutral-800 text-amber-400'
              : 'text-neutral-400 hover:text-white hover:bg-neutral-800'
          }`}
          title="Toggle Auto Rotation"
        >
          <RotateCw className={`w-3.5 h-3.5 ${isRotating ? 'animate-spin' : ''}`} />
        </button>

        {/* Toggle Sizzle Steam */}
        <button
          onClick={() => setSteamActive(!steamActive)}
          className={`p-2 rounded-lg text-xs font-mono transition-all active:translate-y-[1px] ${
            steamActive
              ? 'bg-neutral-800 text-emerald-400'
              : 'text-neutral-400 hover:text-white hover:bg-neutral-800'
          }`}
          title="Toggle Griddle Sizzle Steam"
        >
          <Sparkles className="w-3.5 h-3.5" />
        </button>
      </div>

      {/* Exploded Layer Legend Pill */}
      {isExploded && (
        <div className="absolute top-6 right-6 z-20 hidden md:flex flex-col gap-1.5 bg-neutral-950/90 backdrop-blur-md p-3 rounded-lg border border-amber-500/30 text-xs font-mono text-neutral-300 shadow-xl pointer-events-none">
          <div className="text-[10px] uppercase font-bold text-amber-400 tracking-wider">
            ANATOMY OF THE BIG MOUTH:
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-amber-500" />
            <span>Top Brioche (Toasted Sesame Glaze)</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-500" />
            <span>Crispy Crinkle-Cut Cucumbers</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-red-500" />
            <span>Vine-Ripe Heirloom Tomato</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-yellow-400" />
            <span>Molten American Cheddar Droop</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-stone-700" />
            <span>44 Farms Smash Patty (Lacy Crust)</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-amber-600" />
            <span>Potato Roll Heel (Buttered Flat-Top)</span>
          </div>
        </div>
      )}

      {/* Subtle Drag Prompt */}
      <div className="absolute bottom-6 left-6 z-10 hidden sm:flex items-center gap-2 text-[11px] font-mono text-neutral-500 pointer-events-none">
        <Eye className="w-3.5 h-3.5 text-amber-500" />
        <span>CLICK & DRAG TO ORBIT 360° // SCROLL TO ROTATE</span>
      </div>

    </div>
  );
};
