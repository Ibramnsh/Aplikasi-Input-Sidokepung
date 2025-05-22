document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("dataForm");
  const successAlert = document.getElementById("successAlert");
  const errorAlert = document.getElementById("errorAlert");
  const errorMessage = document.getElementById("errorMessage");
  const closeAlert = document.getElementById("closeAlert");
  const closeErrorAlert = document.getElementById("closeErrorAlert");
  const downloadLink = document.getElementById("downloadLink");
  const downloadExcel = document.getElementById("downloadExcel");

  // Check if Excel file exists and update download button
  fetch("/check-file")
    .then((response) => response.json())
    .then((data) => {
      if (data.exists) {
        downloadExcel.href = "/download/data.xlsx";
        downloadExcel.classList.remove("hidden");
      }
    })
    .catch((error) => console.error("Error checking file:", error));

  // Close success alert
  closeAlert.addEventListener("click", function () {
    successAlert.classList.add("hidden");
  });

  // Close error alert
  closeErrorAlert.addEventListener("click", function () {
    errorAlert.classList.add("hidden");
  });

  // Validasi input RT dan RW hanya angka
  document.getElementById("rt").addEventListener("input", function (e) {
    this.value = this.value.replace(/[^0-9]/g, "");
  });

  document.getElementById("rw").addEventListener("input", function (e) {
    this.value = this.value.replace(/[^0-9]/g, "");
  });

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    // Reset error messages
    document
      .querySelectorAll(".text-red-500")
      .forEach((el) => el.classList.add("hidden"));

    // Get form values
    const rt = document.getElementById("rt").value.trim();
    const rw = document.getElementById("rw").value.trim();
    const dusun = document.getElementById("dusun").value.trim();
    const namaKepala = document.getElementById("nama_kepala").value.trim();
    const alamat = document.getElementById("alamat").value.trim();

    // Validate form
    let isValid = true;

    if (!rt) {
      document.getElementById("rt_error").classList.remove("hidden");
      isValid = false;
    }

    if (!rw) {
      document.getElementById("rw_error").classList.remove("hidden");
      isValid = false;
    }

    if (!dusun) {
      document.getElementById("dusun_error").classList.remove("hidden");
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
      // Create form data
      const formData = new FormData();
      formData.append("rt", rt);
      formData.append("rw", rw);
      formData.append("dusun", dusun);
      formData.append("nama_kepala", namaKepala);
      formData.append("alamat", alamat);

      // Send data to server
      fetch("/submit", {
        method: "POST",
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            // Show success message
            successAlert.classList.remove("hidden");
            errorAlert.classList.add("hidden");

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
