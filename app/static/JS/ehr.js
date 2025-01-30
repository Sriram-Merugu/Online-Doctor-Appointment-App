// static/scripts.js
document.querySelectorAll('.add-field').forEach(function(button) {
    button.addEventListener('click', function() {
        const fieldType = this.dataset.field;
        const formGroup = document.createElement('div');
        formGroup.classList.add('form-group');

        const field = document.createElement('div');
        field.innerHTML = '{{ wtf.form_field(form[fieldType].entries.append_entry()) }}';

        formGroup.appendChild(field);
        this.parentNode.insertBefore(formGroup, this);
    });
});