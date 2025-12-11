document.addEventListener("DOMContentLoaded", function () {
	const inputFile =
		document.getElementById("template_file") ||
		document.querySelector('input[type="file"][name="template_file"]');
	const previewContainer = document.getElementById("preview-container");

	if (!inputFile) {
		console.error('No se encontró el input file "template_file"');
		return;
	}

	if (!previewContainer) {
		console.error('No se encontró el contenedor de preview con id "preview-container"');
		return;
	}

	inputFile.addEventListener("change", function (event) {
		const file = event.target.files[0];
		if (!file) {
			previewContainer.innerHTML = ""; // limpia preview si no hay archivo
			return;
		}

		// Vista previa
		const fileType = file.type;
		const reader = new FileReader();

		reader.onload = function (e) {
			if (fileType.startsWith("image/")) {
				previewContainer.innerHTML = `<img src="${e.target.result}" style="max-width:320px; max-height:120px; object-fit:cover;" />`;
			} else if (fileType === "video/mp4") {
				previewContainer.innerHTML = `<video width="320" height="120" controls style="object-fit:cover;">
					<source src="${e.target.result}" type="video/mp4">
					Tu navegador no soporta la reproducción de video.
				</video>`;
			} else {
				previewContainer.innerHTML = "Formato no soportado para vista previa.";
			}
		};

		reader.readAsDataURL(file);
	});
});
