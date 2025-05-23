document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("dataForm");
  const successAlert = document.getElementById("successAlert");
  const errorAlert = document.getElementById("errorAlert");
  const errorMessage = document.getElementById("errorMessage");
  const successMessage = document.getElementById("successMessage");
  const closeAlert = document.getElementById("closeAlert");
  const closeErrorAlert = document.getElementById("closeErrorAlert");
  const remainingElement = document.getElementById("remaining");
  const pertanyaan510 = document.getElementById("pertanyaan_5_10");
  const namaInput = document.getElementById("nama");
  const namaPlaceholders = document.querySelectorAll(".nama-placeholder");

  // Highlight radio items when selected
  const radioItems = document.querySelectorAll(".radio-item");
  radioItems.forEach((item) => {
    const radio = item.querySelector('input[type="radio"]');
    if (radio) {
      radio.addEventListener("change", function () {
        // Remove highlight from all items in the same group
        const name = this.name;
        document.querySelectorAll(`input[name="${name}"]`).forEach((r) => {
          const radioItem = r.closest(".radio-item");
          if (radioItem) {
            radioItem.classList.remove(
              "bg-primary-50",
              "border",
              "border-primary-200"
            );
          }
        });

        // Add highlight to selected item
        if (this.checked) {
          item.classList.add("bg-primary-50", "border", "border-primary-200");
        }
      });
    }
  });

  // Update nama placeholder saat nama diinput
  namaInput.addEventListener("input", function () {
    const nama = this.value.trim() || "NAMA";
    namaPlaceholders.forEach((placeholder) => {
      placeholder.textContent = nama;
    });
  });

  // Logika untuk menampilkan pertanyaan 5.10 jika semua jawaban 5.7, 5.8, 5.9 adalah "Tidak"
  const workStatusRadios = document.querySelectorAll(".work-status-radio");
  workStatusRadios.forEach((radio) => {
    radio.addEventListener("change", checkWorkStatus);
  });

  function checkWorkStatus() {
    const bekerjaUpah = document.querySelector(
      'input[name="bekerja_upah"]:checked'
    )?.value;
    const menjalankanUsaha = document.querySelector(
      'input[name="menjalankan_usaha"]:checked'
    )?.value;
    const membantuUsaha = document.querySelector(
      'input[name="membantu_usaha"]:checked'
    )?.value;

    // Jika semua pertanyaan sudah dijawab
    if (bekerjaUpah && menjalankanUsaha && membantuUsaha) {
      // Jika semua jawaban "Tidak", tampilkan pertanyaan 5.10
      if (
        bekerjaUpah === "Tidak" &&
        menjalankanUsaha === "Tidak" &&
        membantuUsaha === "Tidak"
      ) {
        pertanyaan510.classList.remove("hidden");
      } else {
        pertanyaan510.classList.add("hidden");
        // Reset jawaban pertanyaan 5.10
        const memilikiPekerjaanRadios = document.querySelectorAll(
          'input[name="memiliki_pekerjaan"]'
        );
        memilikiPekerjaanRadios.forEach((radio) => {
          radio.checked = false;
        });
      }
    }
  }

  // Close success alert
  closeAlert.addEventListener("click", function () {
    successAlert.classList.add("hidden");
  });

  // Close error alert
  closeErrorAlert.addEventListener("click", function () {
    errorAlert.classList.add("hidden");
  });

  // Input event listeners to hide error messages when typing
  document.getElementById("nama").addEventListener("input", () => {
    document.getElementById("nama_error").classList.add("hidden");
  });

  document.getElementById("umur").addEventListener("input", () => {
    document.getElementById("umur_error").classList.add("hidden");
  });

  // Radio button event listeners to hide error messages when selecting
  document.querySelectorAll('input[type="radio"]').forEach((radio) => {
    radio.addEventListener("change", function () {
      const errorId = `${this.name}_error`;
      const errorElement = document.getElementById(errorId);
      if (errorElement) {
        errorElement.classList.add("hidden");
      }
    });
  });

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    // Reset error messages
    document
      .querySelectorAll(".text-red-500")
      .forEach((el) => el.classList.add("hidden"));

    // Get form values
    const nama = document.getElementById("nama").value.trim();
    const umur = document.getElementById("umur").value.trim();
    const hubungan = document.querySelector(
      'input[name="hubungan"]:checked'
    )?.value;
    const jenisKelamin = document.querySelector(
      'input[name="jenis_kelamin"]:checked'
    )?.value;
    const statusPerkawinan = document.querySelector(
      'input[name="status_perkawinan"]:checked'
    )?.value;
    const pendidikan = document.querySelector(
      'input[name="pendidikan"]:checked'
    )?.value;
    const kegiatan = document.querySelector(
      'input[name="kegiatan"]:checked'
    )?.value;
    const bekerjaUpah = document.querySelector(
      'input[name="bekerja_upah"]:checked'
    )?.value;
    const menjalankanUsaha = document.querySelector(
      'input[name="menjalankan_usaha"]:checked'
    )?.value;
    const membantuUsaha = document.querySelector(
      'input[name="membantu_usaha"]:checked'
    )?.value;

    // Validate form
    let isValid = true;

    if (!nama) {
      document.getElementById("nama_error").classList.remove("hidden");
      isValid = false;

      // Add shake animation
      const input = document.getElementById("nama");
      input.classList.add("border-red-500");
      input.animate(
        [
          { transform: "translateX(0)" },
          { transform: "translateX(-5px)" },
          { transform: "translateX(5px)" },
          { transform: "translateX(-5px)" },
          { transform: "translateX(5px)" },
          { transform: "translateX(0)" },
        ],
        {
          duration: 500,
          easing: "ease-in-out",
        }
      );

      // Remove red border after 2 seconds
      setTimeout(() => {
        input.classList.remove("border-red-500");
      }, 2000);
    }

    if (!umur) {
      document.getElementById("umur_error").classList.remove("hidden");
      isValid = false;

      // Add shake animation
      const input = document.getElementById("umur");
      input.classList.add("border-red-500");
      input.animate(
        [
          { transform: "translateX(0)" },
          { transform: "translateX(-5px)" },
          { transform: "translateX(5px)" },
          { transform: "translateX(-5px)" },
          { transform: "translateX(5px)" },
          { transform: "translateX(0)" },
        ],
        {
          duration: 500,
          easing: "ease-in-out",
        }
      );

      // Remove red border after 2 seconds
      setTimeout(() => {
        input.classList.remove("border-red-500");
      }, 2000);
    } else if (parseInt(umur) < 15) {
      document.getElementById("umur_error").classList.remove("hidden");
      document.getElementById("umur_error").textContent =
        "Umur minimal 15 tahun";
      isValid = false;

      // Add shake animation
      const input = document.getElementById("umur");
      input.classList.add("border-red-500");
      input.animate(
        [
          { transform: "translateX(0)" },
          { transform: "translateX(-5px)" },
          { transform: "translateX(5px)" },
          { transform: "translateX(-5px)" },
          { transform: "translateX(5px)" },
          { transform: "translateX(0)" },
        ],
        {
          duration: 500,
          easing: "ease-in-out",
        }
      );

      // Remove red border after 2 seconds
      setTimeout(() => {
        input.classList.remove("border-red-500");
      }, 2000);
    }

    if (!hubungan) {
      document.getElementById("hubungan_error").classList.remove("hidden");
      isValid = false;
    }

    if (!jenisKelamin) {
      document.getElementById("jenis_kelamin_error").classList.remove("hidden");
      isValid = false;
    }

    if (!statusPerkawinan) {
      document
        .getElementById("status_perkawinan_error")
        .classList.remove("hidden");
      isValid = false;
    }

    if (!pendidikan) {
      document.getElementById("pendidikan_error").classList.remove("hidden");
      isValid = false;
    }

    if (!kegiatan) {
      document.getElementById("kegiatan_error").classList.remove("hidden");
      isValid = false;
    }

    if (!bekerjaUpah) {
      document.getElementById("bekerja_upah_error").classList.remove("hidden");
      isValid = false;
    }

    if (!menjalankanUsaha) {
      document
        .getElementById("menjalankan_usaha_error")
        .classList.remove("hidden");
      isValid = false;
    }

    if (!membantuUsaha) {
      document
        .getElementById("membantu_usaha_error")
        .classList.remove("hidden");
      isValid = false;
    }

    // Validasi pertanyaan 5.10 jika ditampilkan
    let memilikiPekerjaan = null;
    if (!pertanyaan510.classList.contains("hidden")) {
      memilikiPekerjaan = document.querySelector(
        'input[name="memiliki_pekerjaan"]:checked'
      )?.value;
      if (!memilikiPekerjaan) {
        document
          .getElementById("memiliki_pekerjaan_error")
          .classList.remove("hidden");
        isValid = false;
      }
    }

    if (isValid) {
      // Show loading state
      const submitButton = form.querySelector('button[type="submit"]');
      const originalButtonText = submitButton.innerHTML;
      submitButton.innerHTML = `
                <svg class="animate-spin -ml-1 mr-2 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Menyimpan...
            `;
      submitButton.disabled = true;

      // Create form data
      const formData = new FormData();
      formData.append("nama", nama);
      formData.append("umur", umur);
      formData.append("hubungan", hubungan);
      formData.append("jenis_kelamin", jenisKelamin);
      formData.append("status_perkawinan", statusPerkawinan);
      formData.append("pendidikan", pendidikan);
      formData.append("kegiatan", kegiatan);
      formData.append("bekerja_upah", bekerjaUpah);
      formData.append("menjalankan_usaha", menjalankanUsaha);
      formData.append("membantu_usaha", membantuUsaha);

      if (memilikiPekerjaan) {
        formData.append("memiliki_pekerjaan", memilikiPekerjaan);
      }

      // Send data to server
      fetch("/submit-individu", {
        method: "POST",
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          // Reset button state
          submitButton.innerHTML = originalButtonText;
          submitButton.disabled = false;

          if (data.success) {
            // Jika perlu redirect ke halaman pekerjaan
            if (data.redirect_to_pekerjaan) {
              window.location.href = data.redirect_url;
              return;
            }

            // Show success message
            successMessage.textContent =
              data.message || "Data berhasil disimpan";
            successAlert.classList.remove("hidden");
            errorAlert.classList.add("hidden");

            // Reset form
            form.reset();
            pertanyaan510.classList.add("hidden");
            namaPlaceholders.forEach((placeholder) => {
              placeholder.textContent = "NAMA";
            });

            // Reset radio item highlights
            radioItems.forEach((item) => {
              item.classList.remove(
                "bg-primary-50",
                "border",
                "border-primary-200"
              );
            });

            // Scroll to success message
            successAlert.scrollIntoView({ behavior: "smooth" });

            // Update remaining count
            if (data.remaining) {
              remainingElement.textContent = data.remaining;
            }

            // If all data has been submitted, redirect to home page
            if (data.complete) {
              setTimeout(() => {
                window.location.href = data.redirect_url;
              }, 2000);
            }

            // Hide success message after 5 seconds
            setTimeout(() => {
              successAlert.classList.add("hidden");
            }, 5000);
          } else {
            // Show error message
            errorMessage.textContent = data.message || "Terjadi kesalahan.";
            errorAlert.classList.remove("hidden");
            successAlert.classList.add("hidden");

            // Scroll to error message
            errorAlert.scrollIntoView({ behavior: "smooth" });
          }
        })
        .catch((error) => {
          // Reset button state
          submitButton.innerHTML = originalButtonText;
          submitButton.disabled = false;

          console.error("Error:", error);
          errorMessage.textContent = "Terjadi kesalahan pada server.";
          errorAlert.classList.remove("hidden");
          successAlert.classList.add("hidden");

          // Scroll to error message
          errorAlert.scrollIntoView({ behavior: "smooth" });
        });
    } else {
      // Show error message for validation errors
      errorMessage.textContent = "Mohon lengkapi semua field yang wajib diisi.";
      errorAlert.classList.remove("hidden");
      successAlert.classList.add("hidden");

      // Scroll to first error
      const firstError = document.querySelector(".text-red-500:not(.hidden)");
      if (firstError) {
        firstError.scrollIntoView({ behavior: "smooth", block: "center" });
      }
    }
  });
});
