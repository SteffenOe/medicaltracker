    document.addEventListener('DOMContentLoaded', function () {
        const select = document.getElementById('katSelect');
        const bdFields = document.getElementById('blutdruckFelder');
        const singleField = document.getElementById('einzelwertFeld');
        const label = document.getElementById('einzelwertLabel');
        const help = document.getElementById('einzelwertHelp');

        function updateFields() {
            if (select.value === 'Blutdruck') {
                bdFields.style.display = 'flex';
                singleField.style.display = 'none';
            } else if (select.value === 'Puls') {
                bdFields.style.display = 'none';
                singleField.style.display = 'block';
                label.innerText = 'Pulsfrequenz (bpm)';
                help.innerText = 'Gültiger Bereich: 30 bis 250 Schläge/Minute.';
            } else if (select.value === 'Gewicht') {
                bdFields.style.display = 'none';
                singleField.style.display = 'block';
                label.innerText = 'Körpergewicht (kg)';
                help.innerText = 'Gültiger Bereich: 2,0 bis 300,0 kg.';
            }
        }

        select.addEventListener('change', updateFields);
        updateFields();
    });