'use strict'

/***************************
 * Avatar uploading related functionality
 ***************************/
const dropArea = document.querySelector('.dropArea');
const avatarForm = document.querySelector('.dropArea form');
const fileField = document.getElementById('avatar--file');
const errorMsg = document.querySelector('.dropArea .error--msg');



//Preventing default behaviour
['dragover','dragenter','dragleave','drop'].forEach(event => {
    dropArea.addEventListener(event, e => {
        e.preventDefault();
    });
});


//changing the border color when a file is dragged over or dragged enter
['dragover','dragenter'].forEach(event => {
    dropArea.addEventListener(event, () => {
        avatarForm.classList.add('highlight');
    });
});


//setting border color of form back to default when dragged leave or drop occurs
['dragleave','drop'].forEach(event => {
    dropArea.addEventListener(event, () => {
        avatarForm.classList.remove('highlight');
    });
});




//function to upload avatar
const uploadAvatarFunc = (pics) => {
    
    const fileTypes = ['image/jpeg','image/jpg','image/png','image/gif'];
    if(pics.length === 1 && pics[0].size <= (16 * 1024 * 1024) && fileTypes.includes(pics[0].type)) {

        //1. Storing file in formData Object
        const formData = new FormData();
        formData.append('avatar',pics[0]);

        //2. Making http request using fetch api
        const httpReq = async () => {
            const init = {
                method : 'post',
                mode : 'same-origin',
                cache : 'no-cache',
                body : formData
            };
            const response = await fetch('/uploadAvatar',init);
            if(response.ok && response.status === 200) {
                return await response.json();
            }
            else {
                errorMsg.textContent = '☹ Sorry something went wrong';
            }
        };

        //3. Using the response received from server
        httpReq()
        .then(res => {
            if (avatarForm.lastElementChild.matches('img')) {
                avatarForm.removeChild(avatarForm.lastElementChild);
            }
            const img = document.createElement('img');
            img.src = `../static/user-images/${res['pic']}`;
            avatarForm.append(img);
            errorMsg.textContent = '';   
        })
        .catch(console.error);
    }

    else if(pics[0].size > 16 * 1024 * 1024) errorMsg.textContent = 'file size is greater than 16 MB';
    else if(!fileTypes.includes(pics[0].type)) errorMsg.textContent = 'file in jpg/png/gif format is only allowed';
    else errorMsg.textContent = 'Only one file is allowed to upload';
};





//event handler for drop Event
dropArea.addEventListener('drop', e => {
    const files = e.dataTransfer.files;
    const pics = [...files];
    uploadAvatarFunc(pics);
});





//event handler for file field
fileField.addEventListener('change', function() {
    uploadAvatarFunc([...this.files]);
});