
document.getElementById('id_profile_picture').addEventListener('change', function() {
    document.getElementById('uploadForm').submit();
});


function editPerson(){
    const editButton = document.getElementById("edit-info-btn");
    const saveButton = document.getElementById("save-info-btn");
    const cancelButton = document.getElementById("cancel-info-btn");
    const formInputs = document.querySelectorAll(".form-input, .form-select");
    const textElements = document.querySelectorAll("#first-name-text, #last-name-text, #year-of-study-text, #major-text");

    editButton.addEventListener("click", () => {
        formInputs.forEach(input => input.classList.remove("hidden"));
        textElements.forEach(text => text.classList.add("hidden"));
        editButton.classList.add("hidden");
        saveButton.classList.remove("hidden");
        cancelButton.classList.remove("hidden");
    });

    cancelButton.addEventListener("click", () => {
        formInputs.forEach(input => input.classList.add("hidden"));
        textElements.forEach(text => text.classList.remove("hidden"));
        saveButton.classList.add("hidden");
        cancelButton.classList.add("hidden");
        editButton.classList.remove("hidden");
    });
}

function editPassword(){
    const editPassBtn = document.getElementById('edit-pass-btn');
    const savePassBtn = document.getElementById('save-pass-btn');
    const cancelPassBtn = document.getElementById('cancel-pass-btn');
    const showPassSection = document.querySelector('.showpass');
    const editPassSection = document.querySelector('.editpass');

    // เมื่อคลิกปุ่ม "Change Password"
    editPassBtn.addEventListener('click', () => {
        showPassSection.classList.add('hidden');
        editPassSection.classList.remove('hidden');
        editPassBtn.classList.add('hidden');
        savePassBtn.classList.remove('hidden');
        cancelPassBtn.classList.remove('hidden');
    });

    // เมื่อคลิกปุ่ม "Cancel"
    cancelPassBtn.addEventListener('click', () => {
        showPassSection.classList.remove('hidden');
        editPassSection.classList.add('hidden');
        editPassBtn.classList.remove('hidden');
        savePassBtn.classList.add('hidden');
        cancelPassBtn.classList.add('hidden');
    });
}


document.addEventListener('DOMContentLoaded', function() {
    // Fade out message after 3 seconds
    setTimeout(function() {
        const messageBox = document.getElementById('message-box');
        if (messageBox) {
            messageBox.style.opacity = '0';  
            setTimeout(() => { 
                messageBox.style.display = 'none'; 
            }, 1000);  
        }
    }, 3000);  // Message visible for 3 seconds

    editPerson();
    editPassword();
});
