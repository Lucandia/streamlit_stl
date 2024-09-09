class STLViewer extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    this.connected = true;

    const shadowRoot = this.attachShadow({ mode: 'open' });
    const container = document.createElement('div');
    container.style.width = '100%';
    container.style.height = '100%';

    shadowRoot.appendChild(container);

    if (!this.hasAttribute('model')) {
      throw new Error('model attribute is required');
    }

    const model = this.getAttribute('model');
    const color = parseInt(this.getAttribute('color').replace("#","0x"), 16);
    const auto_rotate = this.getAttribute('auto_rotate');
    let materialType = this.getAttribute('materialType');
    

    let camera = new THREE.PerspectiveCamera(50, container.clientWidth / container.clientHeight, 1, 1000);
    let renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    container.appendChild(renderer.domElement);

    window.addEventListener('resize', function () {
      renderer.setSize(container.clientWidth, container.clientHeight);
      camera.aspect = container.clientWidth / container.clientHeight;
      camera.updateProjectionMatrix();
    }, false);
    let controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableZoom = true;
    let scene = new THREE.Scene();
    scene.add(new THREE.HemisphereLight(0xffffff,0x222222,1.5));

    let dirLight = new THREE.DirectionalLight(0xffffff,1.5);
    dirLight.position.set(-1,0,-1);
    scene.add(dirLight);


    new THREE.STLLoader().load(model, (geometry) => {
      let material = new THREE.MeshPhongMaterial({
        color: color,
        specular: 100,
        shininess: 100,
      });

      let wireframe = new THREE.MeshBasicMaterial({
        color: color,
        wireframe: true, 
        wireframeLinewidth: 40 
      });

      if (materialType == 'material') {
        materialType = material;
      } else {
        materialType = wireframe;
      }
        
      let mesh = new THREE.Mesh(geometry, materialType);
      //mesh = THREE.SceneUtils.createMultiMaterialObject(geometry, [material, lines]);

      //rotation is represented in radians - this rotats 90 degrees.
      mesh.rotation.x = -1*(Math.PI / 2);
      scene.add(mesh);

      let middle = new THREE.Vector3();
      geometry.computeBoundingBox();
      geometry.boundingBox.getCenter(middle);
      mesh.geometry.applyMatrix4(new THREE.Matrix4().makeTranslation(-middle.x, -middle.y, -middle.z));
      let largestDimension = Math.max(geometry.boundingBox.max.x, geometry.boundingBox.max.y, geometry.boundingBox.max.z)
      camera.position.z = largestDimension * 1.5 ;
      camera.position.y = 120;
      camera.lookAt(new THREE.Vector3(0,0,0)); 
      //camera.position.x = 10;

      if (auto_rotate == 'true') {
        controls.autoRotate = true;
        controls.autoRotateSpeed = .5;
      }
      let animate = () => {
        controls.update();
        renderer.render(scene, camera);
        if (this.connected) {
          requestAnimationFrame(animate);
        }
      };
      animate();
    });
  }

  disconnectedCallback() {
    this.connected = false;
  }
}

customElements.define('stl-viewer', STLViewer);