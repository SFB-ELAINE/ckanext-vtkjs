import 'vtk.js/Sources/favicon';

import vtkActor from 'vtk.js/Sources/Rendering/Core/Actor';
import vtkFullScreenRenderWindow from 'vtk.js/Sources/Rendering/Misc/FullScreenRenderWindow';
import vtkMapper from 'vtk.js/Sources/Rendering/Core/Mapper';
import vtkSTLReader from 'vtk.js/Sources/IO/Geometry/STLReader';

// ----------------------------------------------------------------------------
// Example code
// ----------------------------------------------------------------------------

const reader = vtkSTLReader.newInstance();
const mapper = vtkMapper.newInstance({ scalarVisibility: false });
const actor = vtkActor.newInstance();

actor.setMapper(mapper);
mapper.setInputConnection(reader.getOutputPort());

// ----------------------------------------------------------------------------

function update() {
  const fullScreenRenderer = vtkFullScreenRenderWindow.newInstance();
  const renderer = fullScreenRenderer.getRenderer();
  const renderWindow = fullScreenRenderer.getRenderWindow();

  const resetCamera = renderer.resetCamera;
  const render = renderWindow.render;

  renderer.addActor(actor);
  resetCamera();
  render();
}

// ----------------------------------------------------------------------------
// Use a file reader to load a local file
// ----------------------------------------------------------------------------

// const myContainer = document.querySelector('body');
// const fileContainer = document.createElement('div');
// fileContainer.innerHTML = '<input type="file" class="file"/>';
// myContainer.appendChild(fileContainer);
//
// const fileInput = fileContainer.querySelector('input');
//
// function handleFile(event) {
//   event.preventDefault();
//   const dataTransfer = event.dataTransfer;
//   const files = event.target.files || dataTransfer.files;
//   if (files.length === 1) {
//     myContainer.removeChild(fileContainer);
//     const fileReader = new FileReader();
//     fileReader.onload = function onLoad(e) {
//       reader.parseAsArrayBuffer(fileReader.result);
//       update();
//     };
//     fileReader.readAsArrayBuffer(files[0]);
//   }
// }
//
// fileInput.addEventListener('change', handleFile);

// ----------------------------------------------------------------------------
// Use the reader to download a file
// ----------------------------------------------------------------------------


// reader.setUrl("http://172.17.0.2:5000/dataset/b5693066-5076-41fd-958d-8a52b29a0900/resource/3c3bcd7b-3a01-4341-9c3b-46a92be460c0/download/tooth_u2.stl", { binary: true }).then(update);

reader.setUrl(url, { binary: true }).then(update);
