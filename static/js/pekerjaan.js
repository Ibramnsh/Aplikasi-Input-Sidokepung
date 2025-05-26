function toggleFields(index) {
    const statusPekerjaan = document.getElementById(`status_pekerjaan_${index}`).value;
    const additionalFields = document.getElementById(`additionalFields_${index}`);

    if (statusPekerjaan === 'Berusaha Sendiri') {
        additionalFields.style.display = 'block';
    } else {
        additionalFields.style.display = 'none';
    }
}

function toggleBidangUsaha(index) {
    const statusPekerjaanDiinginkan = document.getElementById(`status_pekerjaan_diinginkan_${index}`).value;
    const bidangUsahaField = document.getElementById(`bidang_usaha_container_${index}`);

    if (statusPekerjaanDiinginkan === 'Buruh/Karyawan/Pegawai') {
        bidangUsahaField.style.display = 'none';
    } else {
        bidangUsahaField.style.display = 'block';
    }
}

function addSideJobFields() {
    const sideJobFieldsContainer = document.getElementById('sideJobFieldsContainer');
    const sideJobCount = sideJobFieldsContainer.children.length;

    // Create two side job fields
    for (let i = 0; i < 2; i++) {
        const newSideJobFields = `
            <div class="side-job-fields mt-4 p-4 border border-gray-300 rounded-lg">
                <h2 class="text-lg font-semibold">Pekerjaan Sampingan ${sideJobCount + i + 1}</h2>
                <div>
                    <label for="status_pekerjaan_sampingan_${sideJobCount + i}" class="block text-sm font-medium text-gray-700">Status Pekerjaan</label>
                    <select id="status_pekerjaan_sampingan_${sideJobCount + i}" name="status_pekerjaan_sampingan_${sideJobCount + i}" class="form-input w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-300" required onchange="toggleFields('sampingan_${sideJobCount + i}')">
                        <option value="Berusaha Sendiri">Berusaha Sendiri</option>
                        <option value="Buruh/Karyawan/Pegawai">Buruh/Karyawan/Pegawai</option>
                        <option value="Pekerja Keluarga">Pekerja Keluarga</option>
                    </select>
                </div>

                <div id="additionalFields_sampingan_${sideJobCount + i}" style="display: none;">
                    <div>
                        <label for="pemasaran_usaha_sampingan_${sideJobCount + i}" class="block text-sm font-medium text-gray-700">Pemasaran Usaha</label>
                        <select id="pemasaran_usaha_sampingan_${sideJobCount + i}" name="pemasaran_usaha_sampingan_${sideJobCount + i}" class="form-input w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-300">
                            <option value="Online">Online</option>
                            <option value="Offline">Offline</option>
                        </select>
                    </div>

                    <div>
                        <label for="penjualan_marketplace_sampingan_${sideJobCount + i}" class="block text-sm font-medium text-gray-700">Penjualan Melalui Marketplace</label>
                        <select id="penjualan_marketplace_sampingan_${sideJobCount + i}" name="penjualan_marketplace_sampingan_${sideJobCount + i}" class="form-input w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-300">
                            <option value="Ya">Ya</option>
                            <option value="Tidak">Tidak</option>
                        </select>
                    </div>

                    <div>
                        <label for="status_pekerjaan_diinginkan_sampingan_${sideJobCount + i}" class="block text-sm font-medium text-gray-700">Status Pekerjaan yang Diinginkan</label>
                        <select id="status_pekerjaan_diinginkan_sampingan_${sideJobCount + i}" name="status_pekerjaan_diinginkan_sampingan_${sideJobCount + i}" class="form-input w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-300" required onchange="toggleBidangUsaha('sampingan_${sideJobCount + i}')">
                            <option value="Berusaha Sendiri">Berusaha Sendiri</option>
                            <option value="Buruh/Karyawan/Pegawai">Buruh/Karyawan/Pegawai</option>
                        </select>
                    </div>

                    <div id="bidang_usaha_container_sampingan_${sideJobCount + i}">
                        <label for="bidang_usaha_sampingan_${sideJobCount + i}" class="block text-sm font-medium text-gray-700">Usaha di Bidang Apa yang Anda Minati</label>
                        <input type="text" id="bidang_usaha_sampingan_${sideJobCount + i}" name="bidang_usaha_sampingan_${sideJobCount + i}" placeholder="Masukkan bidang usaha" class="form-input w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-300" />
                    </div>
                </div>
            </div>
        `;
        sideJobFieldsContainer.insertAdjacentHTML('beforeend', newSideJobFields);
    }
}
