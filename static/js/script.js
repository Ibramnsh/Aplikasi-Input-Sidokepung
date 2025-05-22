document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("dataForm");
  const successAlert = document.getElementById("successAlert");
  const errorAlert = document.getElementById("errorAlert");
  const errorMessage = document.getElementById("errorMessage");
  const closeAlert = document.getElementById("closeAlert");
  const closeErrorAlert = document.getElementById("closeErrorAlert");
  const showFileLocationBtn = document.getElementById("showFileLocation");
  const fileLocationModal = document.getElementById("fileLocationModal");
  const fileLocationText = document.getElementById("fileLocationText");
  const closeModal = document.getElementById("closeModal");
  const fileLocationSuccess = document.getElementById("fileLocationSuccess");
  const downloadLink = document.getElementById("downloadLink");
  const downloadExcel = document.getElementById("downloadExcel");

  fetch("/file-location")
    .then((response) => response.json())
    .then((data) => {
      fetch("/download/data.xlsx", { method: "HEAD" })
        .then((response) => {
          if (response.ok) {
            downloadExcel.href = "/download/data.xlsx";
            downloadExcel.classList.remove("hidden");
          }
        })
        .catch((error) => console.error("Error checking file:", error));
    })
    .catch((error) => console.error("Error:", error));

  closeAlert.addEventListener("click", function () {
    successAlert.classList.add("hidden");
  });

  closeErrorAlert.addEventListener("click", function () {
    errorAlert.classList.add("hidden");
  });

  showFileLocationBtn.addEventListener("click", function () {
    fetch("/file-location")
      .then((response) => response.json())
      .then((data) => {
        fileLocationText.textContent = data.file_location;
        fileLocationModal.classList.remove("hidden");
      })
      .catch((error) => {
        console.error("Error:", error);
        errorMessage.textContent = "Gagal mendapatkan lokasi file.";
        errorAlert.classList.remove("hidden");
      });
  });

  closeModal.addEventListener("click", function () {
    fileLocationModal.classList.add("hidden");
  });

  window.addEventListener("click", function (event) {
    if (event.target === fileLocationModal) {
      fileLocationModal.classList.add("hidden");
    }
  });

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    document
      .querySelectorAll(".text-red-500")
      .forEach((el) => el.classList.add("hidden"));

    const rtRwDusun = document.getElementById("rt_rw_dusun").value.trim();
    const namaKepala = document.getElementById("nama_kepala").value.trim();
    const alamat = document.getElementById("alamat").value.trim();

    let isValid = true;

    if (!rtRwDusun) {
      document.getElementById("rt_rw_dusun_error").classList.remove("hidden");
      isValid = false;
    }

    if (!namaKepala) {
      document.getElementById("nama_kepala_error").classList.remove("hidden");
      isValid = false;
    }

    if (!alamat) {
      document.getElementById("alamat_error").classList.remove("hidden");
      isValid = false;
    }

    if (isValid) {
      const formData = new FormData();
      formData.append("rt_rw_dusun", rtRwDusun);
      formData.append("nama_kepala", namaKepala);
      formData.append("alamat", alamat);

      fetch("/submit", {
        method: "POST",
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            // Show pesan sukses
            successAlert.classList.remove("hidden");
            errorAlert.classList.add("hidden");

            // Show file location
            if (data.file_location) {
              fileLocationSuccess.textContent = data.file_location;
              fileLocationSuccess.classList.remove("hidden");
            }

            // Update download link
            if (data.download_url) {
              downloadLink.href = data.download_url;
              downloadExcel.href = data.download_url;
              downloadExcel.classList.remove("hidden");
            }

            // Reset form
            form.reset();

            // Hide success message after 10 seconds
            setTimeout(() => {
              successAlert.classList.add("hidden");
            }, 10000);
          } else {
            // Show error message
            errorMessage.textContent = data.message || "Terjadi kesalahan.";
            errorAlert.classList.remove("hidden");
            successAlert.classList.add("hidden");
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          errorMessage.textContent = "Terjadi kesalahan pada server.";
          errorAlert.classList.remove("hidden");
          successAlert.classList.add("hidden");
        });
    }
  });
});
