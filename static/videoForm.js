
const initialVideoInput = document.querySelector("#initialvideo")
const secondVideoInput = document.querySelector("#secondvideo")
const initialVideoLabel = document.querySelector("label[for='initialvideo']")
const secondVideoLabel = document.querySelector("label[for='secondvideo']")

function changeLabel(event) {
  if (!event.target.files[0]) return
  
  if (event.target.id == "initialvideo") {
    initialVideoLabel.querySelector("img").src = "/static/video.svg"
    initialVideoLabel.querySelector("#info > div").innerText = event.target.files[0].name
  } else {
    secondVideoLabel.querySelector("img").src = "/static/video.svg"
    secondVideoLabel.querySelector("#info > div").innerText = event.target.files[0].name
  }
}

initialVideoInput.addEventListener("change", changeLabel)
secondVideoInput.addEventListener("change", changeLabel)