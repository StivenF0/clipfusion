
const initialVideoInput = document.querySelector("#initialvideo")
const secondVideoInput = document.querySelector("#secondvideo")
const initialVideoLabel = document.querySelector("label[for='initialvideo']")
const secondVideoLabel = document.querySelector("label[for='secondvideo']")

function checkVideo(type) {
  const mimetype = type.split("/")
  return mimetype[0] === "video"
}

function handleDragOver(event) {
  event.preventDefault()
}

function handleDragDrop(event) {
  console.log("Drop file")
  event.preventDefault()

  if (event.dataTransfer.items.length > 1) return

  for (const item of event.dataTransfer.items) {
    if (item.kind !== "file") return
    if (!checkVideo(item.type)) return

    if (event.target.getAttribute("for") === "initialvideo") {
      initialVideoInput.files = event.dataTransfer.files
      updateLabel(initialVideoInput)
    } else if (event.target.getAttribute("for") === "secondvideo") {
      secondVideoInput.files = event.dataTransfer.files
      updateLabel(secondVideoInput)
    }
  }
}

function changeLabel(event) {
  if (!event.target.files[0]) return
  
  if (event.target.id == "initialvideo") {
    updateLabel(initialVideoInput)
  } else {
    updateLabel(secondVideoInput)
  }
}

function updateLabel(inputElement) {
  if (inputElement.id == "initialvideo") {
    initialVideoLabel.querySelector("img").src = "/static/video.svg"
    initialVideoLabel.querySelector("#info > div").innerText = inputElement.files[0].name
  } else {
    secondVideoLabel.querySelector("img").src = "/static/video.svg"
    secondVideoLabel.querySelector("#info > div").innerText = inputElement.files[0].name
  }
}

initialVideoInput.addEventListener("change", changeLabel)
secondVideoInput.addEventListener("change", changeLabel)

initialVideoLabel.addEventListener("dragover", handleDragOver)
secondVideoLabel.addEventListener("dragover", handleDragOver)

initialVideoLabel.addEventListener("drop", handleDragDrop)
secondVideoLabel.addEventListener("drop", handleDragDrop)