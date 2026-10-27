document.addEventListener("DOMContentLoaded", () => {
  const imageInput = document.querySelector("#id_image");
  const previewContainer = document.querySelector(".field-image_preview .readonly");
  if (!imageInput || !previewContainer) return;

  const originalPreview = previewContainer.innerHTML;
  let previewUrl;
  imageInput.addEventListener("change", () => {
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    const selectedFile = imageInput.files[0];
    if (!selectedFile || !selectedFile.type.startsWith("image/")) {
      previewContainer.innerHTML = originalPreview;
      return;
    }
    previewUrl = URL.createObjectURL(selectedFile);
    const preview = document.createElement("img");
    preview.src = previewUrl;
    preview.alt = "Tanlangan yangilik rasmi";
    preview.className = "news-editor-image-preview";
    previewContainer.replaceChildren(preview);
  });
});
