const URL = "./static/my_model/";
let model, maxPredictions;
const imagePreview = document.getElementById("image-preview");
const labelContainer = document.getElementById("label-container");

window.onload = async () => {
  const modelURL = URL + "model.json";
  const metadataURL = URL + "metadata.json";
  model = await tmImage.load(modelURL, metadataURL);
  maxPredictions = model.getTotalClasses();
};

function loadImage(event) {
  const file = event.target.files[0];
  const reader = new FileReader();
  reader.onload = function () {
    imagePreview.src = reader.result;
  };
  reader.readAsDataURL(file);
}

async function predict() {
  if (!imagePreview.src) {
    alert("Please upload an image first!");
    return;
  }

  const prediction = await model.predict(imagePreview, false);
  prediction.sort((a, b) => b.probability - a.probability);
  labelContainer.innerHTML = "";

  prediction.forEach(p => {
    const percent = (p.probability * 100).toFixed(1);

    // Create label text
    const label = document.createElement("div");
    label.innerText = `${p.className}: ${percent}%`;

    // Create progress bar container
    const progressBarContainer = document.createElement("div");
    progressBarContainer.classList.add("progress");

    // Create progress bar
    const bar = document.createElement("div");
    bar.classList.add("progress-bar");
    bar.style.width = `${percent}%`;
    bar.innerText = `${percent}%`;

    progressBarContainer.appendChild(bar);
    labelContainer.appendChild(label);
    labelContainer.appendChild(progressBarContainer);
  });

  // Send prediction to Flask backend
  await fetch("/log", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(prediction),
  });
}
 