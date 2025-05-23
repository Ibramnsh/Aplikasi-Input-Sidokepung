$(document).ready(function() {
    function resetDependentFields() {
        $('#pemasaran_usaha_group').hide();
        $('#penjualan_marketplace_group').hide();
        $('#status_pekerjaan_diinginkan_group').hide();
        $('#bidang_usaha_group').hide();
        $('#lebih_dari_satu_pekerjaan_group').hide();

        $('#pemasaran_usaha').val('');
        $('#penjualan_marketplace').val('');
        $('#status_pekerjaan_diinginkan').val('');
        $('#bidang_usaha').val('');
        $('#lebih_dari_satu_pekerjaan').val('');
    }

    $('#status_pekerjaan').change(function() {
        resetDependentFields();
        var status = $(this).val();

        // Show pemasaran usaha, penjualan marketplace, status pekerjaan diinginkan if "Berusaha Sendiri"
        if (status === 'Bekerja' || status === 'Berusaha Sendiri') {
            $('#pemasaran_usaha_group').show();
            $('#penjualan_marketplace_group').show();
            $('#status_pekerjaan_diinginkan_group').show();
        }

        // Show "Memiliki Lebih dari Satu Pekerjaan" for all statuses (always visible)
        if (status === 'Bekerja' || status === 'Berusaha Sendiri' || status === 'Buruh/Karyawan/Pegawai' || status === 'Pekerja Keluarga') {
            $('#lebih_dari_satu_pekerjaan_group').show();
        }
    });

    $('#pemasaran_usaha').change(function() {
        if ($(this).val() !== '') {
            $('#penjualan_marketplace_group').show();
        } else {
            $('#penjualan_marketplace_group').hide();
            $('#status_pekerjaan_diinginkan_group').hide();
            $('#bidang_usaha_group').hide();
            // 'Memiliki lebih dari satu pekerjaan' remains visible regardless
        }
    });

    $('#penjualan_marketplace').change(function() {
        if ($(this).val() !== '') {
            $('#status_pekerjaan_diinginkan_group').show();
        } else {
            $('#status_pekerjaan_diinginkan_group').hide();
            $('#bidang_usaha_group').hide();
            // 'Memiliki lebih dari satu pekerjaan' remains visible regardless
        }
    });

    $('#status_pekerjaan_diinginkan').change(function() {
        var val = $(this).val();
        if(val) {
            $('#bidang_usaha_group').show();
        } else {
            $('#bidang_usaha_group').hide();
        }
    });

    $('#bidang_usaha').on('input', function() {
        var val = $(this).val().trim();
        if(val.length > 0) {
            // Keep 'Memiliki lebih dari satu pekerjaan' visible
        } else {
            // Keep 'Memiliki lebih dari satu pekerjaan' visible regardless
        }
    });

    // Trigger change at page load to reflect initial state if any
    $('#status_pekerjaan').trigger('change');
});

